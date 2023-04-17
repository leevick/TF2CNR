#!python3

import bpy
import bmesh
import sys
import os
import pathlib

dir = pathlib.Path(__file__).parent.as_posix()
if not dir in sys.path:
    sys.path.append(dir)

from utils import add_cube, moveOrigin, extrudeFace, createPolygon, createPolyLine, union


bpy.data.meshes.remove(bpy.data.meshes[0])
bpy.data.lights.remove(bpy.data.lights[0])
bpy.data.cameras.remove(bpy.data.cameras[0])


argv = sys.argv
argv = argv[argv.index("--") + 1:]

# Poles

leftPole = add_cube((0.120, 0.150, 2.750), (0.910, 0, 2.750 / 2))
rightPole = add_cube((0.120, 0.150, 2.750), (-0.910, 0, 2.750 / 2))

# Borad

verts = ((-0.9, 0, 0),
         (0.9, 0, 0),
         (0.9, 0, 0.775),
         (0, 0, 0.875),
         (-0.9, 0, 0.775))

board = createPolygon(verts)
board.location = (0, -0.025, 2.085)
extrudeFace(board, 0.05)


# Frames

verts = [
    (0, 0.055, 0),
    (0, 0.055, 0.07),
    (0, 0.025, 0.085),
    (0, -0.025, 0.085),
    (0, -0.055, 0.07),
    (0, -0.055, 0)]


frontFrame = createPolygon(verts)
extrudeFace(frontFrame, 1.7)
frontFrame.location = (0.85, 0, 2.0)


union(board, frontFrame)
# Board

for obj in bpy.data.objects:
    obj.select_set(False)
bpy.ops.object.select_all(action='DESELECT')


verts = ((0, -0.055, 0),
         (0, 0.055, 0),
         (0, 0.055, -0.025),
         (0, 0.025, -0.040),
         (0, -0.025, -0.040),
         (0, -0.055, -0.025), (0, -0.055, 0))

topFrame = createPolyLine(verts, "topFrame")
topFrame.location = (-0.9, 0, 2.9)
bpy.ops.object.convert(target="MESH")

topFrame2 = createPolyLine(verts, "topFrame")
topFrame2.location = (0, 0, 3.0)
bpy.ops.object.convert(target="MESH")


topFrame3 = createPolyLine(verts, "topFrame")
topFrame3.location = (0.9, 0, 2.9)
bpy.ops.object.convert(target='MESH')

topFrame = bpy.ops.object.join()

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='EDGE')
bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.bridge_edge_loops()
bpy.ops.mesh.fill()

bpy.ops.object.editmode_toggle()

topFrame = bpy.context.active_object

union(topFrame, board)

bpy.ops.wm.save_mainfile(
    filepath=f"{os.getcwd()}/{argv[0]}.blend")
