Bump to Roughness in Cycles on CPU/GPU/OSL with a change to the principled shader to support it. I have added a Specular Normal input, a specular roughness input, and a diffuse roughness input. You must use the abjB2R_split script to generate and split the bump/normal texture with OIIO txmake with bumpslopes and then connect them to the b2r node with separateRGB. See https://bergjones.artstation.com/projects/xYNql4 for details and video comparison. The OSL shaders are at https://github.com/simileV/abj_osl_b2r. The project now runs on GPU. In this repo I have only enabled the gpu kernel for my gpu so make sure to enable the ones you need in cmakelists. I have also automatically set up the project to copy ACES into colormanagement instead of filmic. 

.. figure:: https://cdna.artstation.com/p/assets/images/images/047/176/298/large/similev-compb2r-2.jpg?1646936571
   :scale: 100 %
   :align: center

.. figure:: https://cdna.artstation.com/p/assets/images/images/047/895/378/large/similev-b2r-nodes.jpg?1648701126
   :scale: 100 %
   :align: center


.. Keep this document short & concise,
   linking to external resources instead of including content in-line.
   See 'release/text/readme.html' for the end user read-me.


Blender
=======

Blender is the free and open source 3D creation suite.
It supports the entirety of the 3D pipeline-modeling, rigging, animation, simulation, rendering, compositing,
motion tracking and video editing.

.. figure:: https://code.blender.org/wp-content/uploads/2018/12/springrg.jpg
   :scale: 50 %
   :align: center


Project Pages
-------------

- `Main Website <http://www.blender.org>`__
- `Reference Manual <https://docs.blender.org/manual/en/latest/index.html>`__
- `User Community <https://www.blender.org/community/>`__

Development
-----------

- `Build Instructions <https://wiki.blender.org/wiki/Building_Blender>`__
- `Code Review & Bug Tracker <https://developer.blender.org>`__
- `Developer Forum <https://devtalk.blender.org>`__
- `Developer Documentation <https://wiki.blender.org>`__


License
-------

Blender as a whole is licensed under the GNU General Public License, Version 3.
Individual files may have a different, but compatible license.

See `blender.org/about/license <https://www.blender.org/about/license>`__ for details.
