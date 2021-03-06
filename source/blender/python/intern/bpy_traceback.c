/* SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup pythonintern
 *
 * This file contains utility functions for getting data from a python stack
 * trace.
 */

#include <Python.h>
#include <frameobject.h>

#include "BLI_path_util.h"
#include "BLI_utildefines.h"
#ifdef WIN32
#  include "BLI_string.h" /* BLI_strcasecmp */
#endif

#include "bpy_traceback.h"

static const char *traceback_filepath(PyTracebackObject *tb, PyObject **coerce)
{
  *coerce = PyUnicode_EncodeFSDefault(tb->tb_frame->f_code->co_filename);
  return PyBytes_AS_STRING(*coerce);
}

/* copied from pythonrun.c, 3.4.0 */
_Py_static_string(PyId_string, "<string>");

static int parse_syntax_error(PyObject *err,
                              PyObject **message,
                              PyObject **filename,
                              int *lineno,
                              int *offset,
                              PyObject **text)
{
  long hold;
  PyObject *v;
  _Py_IDENTIFIER(msg);
  _Py_IDENTIFIER(filename);
  _Py_IDENTIFIER(lineno);
  _Py_IDENTIFIER(offset);
  _Py_IDENTIFIER(text);

  *message = NULL;
  *filename = NULL;

  /* new style errors.  `err' is an instance */
  *message = _PyObject_GetAttrId(err, &PyId_msg);
  if (!*message) {
    goto finally;
  }

  v = _PyObject_GetAttrId(err, &PyId_filename);
  if (!v) {
    goto finally;
  }
  if (v == Py_None) {
    Py_DECREF(v);
    *filename = _PyUnicode_FromId(&PyId_string);
    if (*filename == NULL) {
      goto finally;
    }
    Py_INCREF(*filename);
  }
  else {
    *filename = v;
  }

  v = _PyObject_GetAttrId(err, &PyId_lineno);
  if (!v) {
    goto finally;
  }
  hold = PyLong_AsLong(v);
  Py_DECREF(v);
  if (hold < 0 && PyErr_Occurred()) {
    goto finally;
  }
  *lineno = (int)hold;

  v = _PyObject_GetAttrId(err, &PyId_offset);
  if (!v) {
    goto finally;
  }
  if (v == Py_None) {
    *offset = -1;
    Py_DECREF(v);
  }
  else {
    hold = PyLong_AsLong(v);
    Py_DECREF(v);
    if (hold < 0 && PyErr_Occurred()) {
      goto finally;
    }
    *offset = (int)hold;
  }

  v = _PyObject_GetAttrId(err, &PyId_text);
  if (!v) {
    goto finally;
  }
  if (v == Py_None) {
    Py_DECREF(v);
    *text = NULL;
  }
  else {
    *text = v;
  }
  return 1;

finally:
  Py_XDECREF(*message);
  Py_XDECREF(*filename);
  return 0;
}
/* end copied function! */

void python_script_error_jump(const char *filepath, int *lineno, int *offset)
{
  PyObject *exception, *value;
  PyTracebackObject *tb;

  *lineno = -1;
  *offset = 0;

  PyErr_Fetch(&exception, &value, (PyObject **)&tb);

  if (exception && PyErr_GivenExceptionMatches(exception, PyExc_SyntaxError)) {
    /* no trace-back available when `SyntaxError`.
     * python has no API's to this. reference #parse_syntax_error() from pythonrun.c */
    PyErr_NormalizeException(&exception, &value, (PyObject **)&tb);

    if (value) { /* should always be true */
      PyObject *message;
      PyObject *filename_py, *text_py;

      if (parse_syntax_error(value, &message, &filename_py, lineno, offset, &text_py)) {
        const char *filename = PyUnicode_AsUTF8(filename_py);
        /* python adds a '/', prefix, so check for both */
        if ((BLI_path_cmp(filename, filepath) == 0) ||
            (ELEM(filename[0], '\\', '/') && BLI_path_cmp(filename + 1, filepath) == 0)) {
          /* good */
        }
        else {
          *lineno = -1;
        }
      }
      else {
        *lineno = -1;
      }
    }
    PyErr_Restore(exception, value, (PyObject *)tb); /* takes away reference! */
  }
  else {
    PyErr_NormalizeException(&exception, &value, (PyObject **)&tb);
    PyErr_Restore(exception, value, (PyObject *)tb); /* takes away reference! */
    PyErr_Print();

    for (tb = (PyTracebackObject *)PySys_GetObject("last_traceback");
         tb && (PyObject *)tb != Py_None;
         tb = tb->tb_next) {
      PyObject *coerce;
      const char *tb_filepath = traceback_filepath(tb, &coerce);
      const int match = ((BLI_path_cmp(tb_filepath, filepath) == 0) ||
                         (ELEM(tb_filepath[0], '\\', '/') &&
                          BLI_path_cmp(tb_filepath + 1, filepath) == 0));
      Py_DECREF(coerce);

      if (match) {
        *lineno = tb->tb_lineno;
        /* used to break here, but better find the inner most line */
      }
    }
  }
}
