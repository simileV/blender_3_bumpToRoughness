'''
*
# Copyright 2022 Aleksander Berg-Jones
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
*
'''


'''
#use example from console
python abjB2R_split.py "D:\projects_3d\b2r_blender\Bump2Roughness\blenderTest\splitEXR_test\couchNormalTest.jpg"

# Pre req
#PYTHON 27
download wheels for numpy-1.16.6+mkl and openexr
https://www.lfd.uci.edu/~gohlke/pythonlibs/
python -m pip install numpy-1.16.6+mkl-cp27-cp27m-win_amd64.whl
python -m pip install OpenEXR-1.3.2-cp27-cp27m-win_amd64.whl
'''

import Imath
import OpenEXR
import sys
import os

pathToMakeTx = r'C:\Users\aleks\source\repos\vcpkg\vcpkg\installed\x64-windows\tools\openimageio\maketx.exe'

#convert the image to 6 channel EXR with bumpslopes
def b2r_gen(filename):
    myIn = filename
    myOut = os.path.splitext(filename)[0] + '_b2r.exr'
    
    myConcatMakeTx = pathToMakeTx + ' -d float --bumpslopes ' + myIn + ' -o ' + myOut
    os.system(myConcatMakeTx)
    
    b2r_split_dual(myOut)
    
# split into 2 exrs for channels 0-2, 3-5 
def b2r_split_dual(filename):
    file = OpenEXR.InputFile(filename)
    
    dw = file.header()['dataWindow']
    sz = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    b0_h = file.channel('b0_h', FLOAT)
    b1_dhds = file.channel('b1_dhds', FLOAT)
    b2_dhdt = file.channel('b2_dhdt', FLOAT)

    b3_dhds2 = file.channel('b3_dhds2', FLOAT)
    b4_dhdt2 = file.channel('b4_dhdt2', FLOAT)
    b5_dh2dsdt = file.channel('b5_dh2dsdt', FLOAT)
    
    outSplit0 = os.path.splitext(filename)[0] + '_split0.exr'
    out0 = OpenEXR.OutputFile(outSplit0, OpenEXR.Header(sz[0], sz[1]))
    out0.writePixels({'R' : b0_h, 'G' : b1_dhds, 'B' : b2_dhdt })
    out0.close()

    outSplit1 = os.path.splitext(filename)[0] + '_split1.exr'
    out1 = OpenEXR.OutputFile(outSplit1, OpenEXR.Header(sz[0], sz[1]))
    out1.writePixels({'R' : b3_dhds2, 'G' : b4_dhdt2, 'B' : b5_dh2dsdt })
    out1.close()

# b2r_gen(r"D:\projects_3d\b2r_blender\Bump2Roughness\blenderTest\splitEXR_test\testB2N_NormalMap.png")
b2r_gen(sys.argv[1])