from . import material 
from . import math_utils
from math import radians
import json

import bpy
import math
from mathutils import Vector, Matrix
import numpy as np


def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    """
    Return the grease-pencil object with the given name. Initialize one if not already present.
    :param gpencil_obj_name: name/key of the grease pencil object in the scene
    """

    # If not present already, create grease pencil object
    if gpencil_obj_name not in bpy.context.scene.objects:
        # bpy.ops.object.gpencil_add(radius=1.0, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), type='EMPTY')
        # bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
        gp_data  = bpy.data.grease_pencils.new(gpencil_obj_name)
        gp_object = bpy.data.objects.new(gpencil_obj_name,gp_data)
        bpy.context.collection.objects.link(gp_object)
        # rename grease pencil
        # bpy.context.scene.objects[-1].name = gpencil_obj_name

    # Get grease pencil object
    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    return gpencil

def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil, gpencil_layer_name='GPencilLayer',
                            clear_layer=False) -> bpy.types.GPencilLayer:
    """
    Return the grease-pencil layer with the given name. Create one if not already present.
    :param gpencil: grease-pencil object for the layer data
    :param gpencil_layer_name: name/key of the grease pencil layer
    :param clear_layer: whether to clear all previous layer data
    """

    # Get grease pencil layer or create one if none exists
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)

    if clear_layer:
        gpencil_layer.clear()  # clear all previous layer data

    # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame

    return gpencil_layer

def draw_bezier_curve(
            gp_object=None,
            gp_obj_name="GPencil",
            gp_layer=None,
            gp_layer_name="GPencilLayer",
            clear_layer=False,
            gp_material_index=0,
            gp_material_name=None,
            gp_frame_index=1, 
            f=None,
            t=None,
            c1=None,
            c2=None,
            co="XZY",           
            use_cyclic=False,
            line_width=10,
            segments=90):
    if(f==None or t==None or c1==None or c2==None):
        raise Exception("cord is none")
    
    co_indexes = (ord(co[0])-88,ord(co[1])-88,ord(co[2])-88)
    points = math_utils.cubic_bezier_curve(f,c1,c2,t,segments)

    if(gp_object is None):
        gp_object  = get_grease_pencil(gp_obj_name)

    if(gp_layer is None):
        gp_layer = get_grease_pencil_layer(gpencil=gp_object,gpencil_layer_name=gp_layer_name,clear_layer=clear_layer)
    elif(clear_layer):
        gp_layer.clear() 

    gp_frame = gp_layer.frames.new(gp_frame_index)   

    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    gp_stroke.use_cyclic = use_cyclic        # closes the stroke
    gp_stroke.line_width = line_width
    if gp_material_name is not None:
        gp_material_index = material.index_of_material(gp_object=gp_object,material_name=gp_material_name)
        if gp_material_index <0:
            gp_material_index = 0

    gp_stroke.material_index = gp_material_index        
 
    gp_stroke.points.add(count=segments)
    co_indexes = (ord(co[0])-88,ord(co[1])-88,ord(co[2])-88)
    for i in range(segments):
        p=[0,0,0]
        p[co_indexes[0]] = points[i][0]
        p[co_indexes[1]] = points[i][1] 
        p[co_indexes[2]] = 0
        gp_stroke.points[i].co = tuple(p)

    return gp_stroke


def create_circle_points(center=(0,0,0,0),radius=0.5,segments=90,co="XZY"):
    points = [(0,0,0)]*segments
    angle = 2*math.pi/segments
    co_indexes = (ord(co[0])-88,ord(co[1])-88,ord(co[2])-88)
    for i in range(segments):
        current = angle*i 
        p=[0,0,0]
        p[co_indexes[0]] = center[co_indexes[0]] + radius*math.cos(current)
        p[co_indexes[1]] = center[co_indexes[1]] + radius*math.sin(current)    
        p[co_indexes[2]] = center[co_indexes[2]]
        points[i] = Vector((p[0],p[1],p[2]))
    return points

def draw_circle(
            gp_object=None,
            gp_obj_name="GPencil",
            gp_layer=None,
            gp_layer_name="GPencilLayer",
            clear_layer=False,
            gp_material_index=0,
            gp_material_name=None,
            gp_frame_index=1, 
            center=(0,0,0,0),
            angles=(0,360),
            co="XZY",
            radius= 0.5,
            line_width=10,
            segments=90):
    angle = 2*math.pi/segments
    angles = (angles[0]*math.pi/180,angles[1]*math.pi/180)
    if(gp_object is None):
        gp_object  = get_grease_pencil(gp_obj_name)

    if(gp_layer is None):
        gp_layer = get_grease_pencil_layer(gpencil=gp_object,gpencil_layer_name=gp_layer_name,clear_layer=clear_layer)
    elif(clear_layer):
        gp_layer.clear() 

    gp_frame = gp_layer.frames.new(gp_frame_index)
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    gp_stroke.use_cyclic = True        # closes the stroke
    gp_stroke.line_width = line_width
    if gp_material_name is None:
        gp_stroke.material_index = gp_material_index
    else:
        gp_stroke.material_index = material.index_of_material(gp_object=gp_object,material_name=gp_material_name)

    # Define stroke geometry
    gp_stroke.points.add(count=segments)
    co_indexes = (ord(co[0])-88,ord(co[1])-88,ord(co[2])-88)
        
    for i in range(segments):
        current = angle*i 
        if(current>=angles[0] and current<=angles[1]):
            p=[0,0,0]
            p[co_indexes[0]] = center[co_indexes[0]] + radius*math.cos(current)
            p[co_indexes[1]] = center[co_indexes[1]] + radius*math.sin(current)    
            p[co_indexes[2]] = center[co_indexes[2]]
            gp_stroke.points[i].co = tuple(p)

    return gp_stroke

def get_selected_strokes():
    gp_object = bpy.context.active_object.data
    strokes = []
    if(type(gp_object)==bpy.types.GreasePencil):
        gpl = gp_object.layers
        if bpy.context.mode == 'EDIT_GPENCIL':
            for l in gpl:
                if l.lock or l.hide or not l.active_frame:#or len(l.frames)
                    continue
                if gp_object.use_multiedit:
                    target_frames = [f for f in l.frames if f.select]
                else:
                    target_frames = [l.active_frame]
                
                for f in target_frames:
                    for s in f.strokes:
                        if s.select:
                            strokes.append((f,s))                       
        elif bpy.context.mode == 'OBJECT':#object mode -> all points
            for l in gpl:# if l.hide:continue# only visible ? (might break things)
                if not len(l.frames):
                    continue#skip frameless layer
                for s in l.active_frame.strokes:
                    strokes.append((l.active_frame,s))  
    return strokes

def get_points_means_center(points):
    a = np.array([ p.co for p in points ])
    c = np.mean(a,axis=0)
    return c



def rotate_keep_stroke(gp_stroke,gp_frame,ang,co="XZY"):
    axis = co[-1]
    mat_rot = Matrix.Rotation(radians(ang), 4,axis )
    p_n = len(gp_stroke.points)
    new_stroke = gp_frame.strokes.new()    
    new_stroke.points.add(count=p_n)
    new_stroke.display_mode =  gp_stroke.display_mode  
    new_stroke.use_cyclic = gp_stroke.use_cyclic
    new_stroke.line_width = gp_stroke.line_width
    new_stroke.material_index = gp_stroke.material_index
    # new_stroke.bound_box_max = gp_stroke.bound_box_max
    # new_stroke.bound_box_min = gp_stroke.bound_box_min
    start_co = get_points_means_center(gp_stroke.points)
    mat_loc = Vector((start_co[0],start_co[1], start_co[2]))
    mat_out =  mat_rot @ mat_loc
    new_start_co = (mat_out[0],mat_out[1],mat_out[2])   

    for i in range(p_n):
        old_co =  gp_stroke.points[i].co
        new_co = (old_co[0]-start_co[0]+new_start_co[0],
                  old_co[1]-start_co[1]+new_start_co[1],
                  old_co[2]-start_co[2]+new_start_co[2])
        new_stroke.points[i].co = new_co
        p = new_stroke.points[i]

 

    # for i in range(p_n):
    #     p = gp_stroke.points[i]
    #     mat_loc = Vector((p.co[0], p.co[1], p.co[2]))
    #     mat_out =  mat_rot @ mat_loc
    #     new_stroke.points[i].co = (mat_out[0],mat_out[1],mat_out[2])


def rotate_duplicate_stroke(gp_stroke,gp_frame,ang,co="XZY"):
    axis = co[-1]
    mat_rot = Matrix.Rotation(radians(ang), 4,axis )
    p_n = len(gp_stroke.points)
    new_stroke = gp_frame.strokes.new()    
    new_stroke.points.add(count=len(gp_stroke.points))
    new_stroke.display_mode =  gp_stroke.display_mode  
    new_stroke.use_cyclic = gp_stroke.use_cyclic
    new_stroke.line_width = gp_stroke.line_width
    new_stroke.material_index = gp_stroke.material_index
    for i in range(p_n):
        p = gp_stroke.points[i]
        mat_loc = Vector((p.co[0], p.co[1], p.co[2]))
        mat_out =  mat_rot @ mat_loc
        new_stroke.points[i].co = (mat_out[0],mat_out[1],mat_out[2])        

def test_frame(frame):
    if(type(frame) == int):
        print("this is frame")

def load_json():
    with open('c:/java/test.json') as f:
        data = json.load(f)
        return data