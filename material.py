import bpy

def create_gpencil_material(gpencil_obj_name=None,material_name=None,fill_color=(1,1,1,1),stroke_color=(0,0,0,1)):

    if gpencil_obj_name not in bpy.context.scene.objects:
        raise Exception("no gpencil object named of "+gpencil_obj_name)

    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    if material_name  in bpy.data.materials.keys():
        gp_mat = bpy.data.materials[material_name]
    else:
        gp_mat = bpy.data.materials.new(material_name)
 
    if not gp_mat.is_grease_pencil:
        bpy.data.materials.create_gpencil_data(gp_mat)

    gp_mat.grease_pencil.fill_color = fill_color
    gp_mat.grease_pencil.color = stroke_color
    gpencil.data.materials.append(gp_mat)        
    return gp_mat

def index_of_material(gpencil_obj_name=None,material_name=None):
    if gpencil_obj_name not in bpy.context.scene.objects:
        raise Exception("no gpencil object named of "+gpencil_obj_name)

    gpencil = bpy.context.scene.objects[gpencil_obj_name]
    return gpencil.data.materials.find(material_name)


def get_material(material_name=None):
    if material_name  in bpy.data.materials.keys():
        return   bpy.data.materials[material_name]
    else:
        raise Exception("no material_name object named of "+material_name)



#0.837 0.862 0.227
#0.042 0.002 0.041