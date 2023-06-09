import bpy
import bmesh


def add_cube(dimension=(1, 1, 1), location=(0, 0, 0)) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location)
    bpy.ops.object.editmode_toggle()
    x, y, z = bpy.context.active_object.dimensions
    bpy.ops.transform.resize(
        value=(dimension[0] / 2.0, dimension[1] / 2.0, dimension[2] / 2.0))
    bpy.ops.object.editmode_toggle()
    return bpy.context.active_object


def add_plane(dimension=(1, 1), location=(0, 0, 0)) -> bpy.types.Object:
    bpy.ops.mesh.primitive_plane_add(location=location)
    bpy.ops.object.editmode_toggle()
    x, y, z = bpy.context.active_object.dimensions
    bpy.ops.transform.resize(
        value=(dimension[0] / 2.0, dimension[1] / 2.0, z))
    bpy.ops.object.editmode_toggle()
    return bpy.context.active_object


def moveOrigin(org):
    saved_location = bpy.context.scene.cursor.location.xyz
    bpy.context.scene.cursor.location = org
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location.xyz = saved_location


def bevel(obj: bpy.types.Object, width: float, segments: int = 1) -> None:
    bpy.context.view_layer.objects.active = obj
    bevel: bpy.types.BevelModifier = obj.modifiers.new(
        type="BEVEL", name="bevel")
    bevel.affect = "VERTICES"
    bevel.offset_type = "OFFSET"
    bevel.width = width
    bevel.segments = segments
    bpy.ops.object.modifier_apply(modifier="bevel")


def extrudeFace(obj: bpy.types.Object, depth=10e-3) -> None:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')

    bm = bmesh.new()
    bm = bmesh.from_edit_mesh(obj.data)

    for f in bm.faces:
        face = f.normal
    r = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
    TranslateDirection = face * depth  # Extrude Strength/Length
    bmesh.ops.translate(bm, vec=TranslateDirection, verts=verts)

    bmesh.update_edit_mesh(obj.data)
    bm.free()

    bpy.ops.object.editmode_toggle()
    pass


def digHoleObj(obj: bpy.types.Object, obj2: bpy.types.Object) -> None:
    # Create cut object
    cut = obj2

    # Apply boolean
    bpy.context.view_layer.objects.active = obj
    boolean = obj.modifiers.new(type="BOOLEAN", name="cut_ops")
    boolean.object = cut
    boolean.solver = "FAST"
    boolean.operation = "DIFFERENCE"
    cut.hide_set(True)
    bpy.ops.object.modifier_apply(modifier="cut_ops")
    bpy.data.objects.remove(cut)
    return


def union(obj: bpy.types.Object, obj2: bpy.types.Object) -> None:
    # Create cut object
    cut = obj2

    # Apply boolean
    bpy.context.view_layer.objects.active = obj
    boolean = obj.modifiers.new(type="BOOLEAN", name="union_ops")
    boolean.object = cut
    boolean.solver = "EXACT"
    boolean.operation = "UNION"
    cut.hide_set(True)
    bpy.ops.object.modifier_apply(modifier="union_ops")
    bpy.data.objects.remove(cut)
    return


def bevelWeight(obj: bpy.types.Object, width: float, segs: int = 6) -> bpy.types.Object:
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    bv: bpy.types.BevelModifier = obj.modifiers.new(
        type="BEVEL", name="bevel")
    bv.affect = "EDGES"
    bv.offset_type = "OFFSET"
    bv.limit_method = "WEIGHT"
    bv.width = width
    bv.segments = segs
    bpy.ops.object.modifier_apply(modifier="bevel")
    return obj


def createPolyLine(coords, name: str) -> bpy.types.Object:
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '2D'
    curveData.fill_mode = 'BOTH'
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords) - 1)

    for i, coord in enumerate(coords):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    # curveOB = bpy.data.objects.new('myCurve', curveData)

    # attach to scene and validate context
    view_layer = bpy.context.view_layer
    curveOB = bpy.data.objects.new(name, curveData)
    view_layer.active_layer_collection.collection.objects.link(curveOB)
    curveOB.select_set(True)
    bpy.context.view_layer.objects.active = curveOB

    return curveOB


def createPolygon(verts):
    bpy.ops.object.select_all(action="DESELECT")
    bm = bmesh.new()
    for v in verts:
        bm.verts.new((v[0], v[1], v[2]))
    bm.faces.new(bm.verts)

    bm.normal_update()

    me = bpy.data.meshes.new("")
    bm.to_mesh(me)

    ob = bpy.data.objects.new("", me)

    view_layer = bpy.context.view_layer
    view_layer.active_layer_collection.collection.objects.link(ob)

    ob.select_set(True)

    return ob
