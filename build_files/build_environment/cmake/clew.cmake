# SPDX-License-Identifier: GPL-2.0-or-later

set(CLEW_EXTRA_ARGS)

ExternalProject_Add(external_clew
  URL file://${PACKAGE_DIR}/${CLEW_FILE}
  DOWNLOAD_DIR ${DOWNLOAD_DIR}
  URL_HASH ${CLEW_HASH_TYPE}=${CLEW_HASH}
  PREFIX ${BUILD_DIR}/clew
  CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${LIBDIR}/clew -Wno-dev ${DEFAULT_CMAKE_FLAGS} ${CLEW_EXTRA_ARGS}
  INSTALL_DIR ${LIBDIR}/clew
)