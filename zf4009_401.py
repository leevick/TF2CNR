#!python3

import bpy
import bmesh
import sys
import os
import pathlib

dir = pathlib.Path(__file__).parent.as_posix()
if not dir in sys.path:
    sys.path.append(dir)

from utils import add_cube, moveOrigin

bpy.data.meshes.remove(bpy.data.meshes[0])
bpy.data.lights.remove(bpy.data.lights[0])
bpy.data.cameras.remove(bpy.data.cameras[0])


argv = sys.argv
argv = argv[argv.index("--") + 1:]

leftPole = add_cube((0.120, 0.150, 2.750), (0.910, 0, 2.750 / 2))
rightPole = add_cube((0.120, 0.150, 2.750), (-0.910, 0, 2.750 / 2))


bpy.ops.wm.save_mainfile(
    filepath=f"{os.getcwd()}/{argv[0]}.blend")
