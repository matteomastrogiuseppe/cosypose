"""Calculates the 3D bounding box and the diameter of 3D object models."""
from deps.bop_toolkit_cosypose.bop_toolkit_lib import inout
from deps.bop_toolkit_cosypose.bop_toolkit_lib import misc
import shutil
import os

CURR_DIR = os.path.abspath("")
DS_id = "camozzi"

# Kinda complex to set arbitrary id, will fix later. Let's use the ycbv convention for now.
# It's a pain to use weights from a certain dataset and import model not from that one. (We have to train anyway)
id = '3'

MESH_DIR = CURR_DIR+r'/inputs/meshes/'+id+r'/'
URDF_DIR = CURR_DIR+r'/local_data/urdfs/'+DS_id+'/'+id+r'/'
print(MESH_DIR)
# You only need to provide the path of .ply
model = inout.load_ply(MESH_DIR+id+'.ply')
shutil.copy(MESH_DIR+id+'.ply', CURR_DIR+'/local_data/bop_datasets/'+DS_id+'/models/')

# Calculate 3D bounding box.
ref_pt = list(map(float, model["pts"].min(axis=0).flatten()))
size = list(map(float, (model["pts"].max(axis=0) - ref_pt).flatten()))

# Calculated diameter.
diameter = misc.calc_pts_diameter(model["pts"])

models_info = {}
models_info[id] = {
    "min_x": ref_pt[0],
    "min_y": ref_pt[1],
    "min_z": ref_pt[2],
    "size_x": size[0],
    "size_y": size[1],
    "size_z": size[2],
    "diameter": diameter,
}

js = inout.load_json(CURR_DIR+r'/local_data/bop_datasets/'+DS_id+'/models/models_info.json')

if id not in js.keys():
    js[id] = {
    "min_x": ref_pt[0],
    "min_y": ref_pt[1],
    "min_z": ref_pt[2],
    "size_x": size[0],
    "size_y": size[1],
    "size_z": size[2],
    "diameter": diameter,
}

inout.save_json(CURR_DIR+r'/local_data/bop_datasets/'+DS_id+'/models/models_info.json', js)
inout.save_json(MESH_DIR+id+'.json', models_info)

if not os.path.exists(MESH_DIR+id+'.mtl') and not os.path.exists(MESH_DIR+id+'.obj') and not os.path.exists(MESH_DIR+id+'.urdf'):
    print("Please add .mtl or .obj or .urdf")

if not os.path.exists(URDF_DIR):
    os.mkdir(URDF_DIR)
    shutil.copy(MESH_DIR+id+'.mtl', URDF_DIR)
    shutil.copy(MESH_DIR+id+'.obj', URDF_DIR)
    shutil.copy(MESH_DIR+id+'.urdf', URDF_DIR)
