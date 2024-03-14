"""Calculates the 3D bounding box and the diameter of 3D object models."""
from deps.bop_toolkit_cosypose.bop_toolkit_lib import inout
from deps.bop_toolkit_cosypose.bop_toolkit_lib import misc
import shutil
import os

CURR_DIR = os.path.abspath("")

# Kinda complex to set arbitrary name, will fix later. Let's use the ycbv convention for now.
# It's a pain to use weights from a certain dataset and import model not from that one. (We have to train anyway)
name = 'obj_000031'
MESH_DIR = CURR_DIR+r'/inputs/meshes/'+name+r'/'
URDF_DIR = CURR_DIR+r'/local_data/urdfs/ycbv/'+name+r'/'



models_info = {}
# You only need to provide the path
model = inout.load_ply(MESH_DIR+name+'.ply')

# Calculate 3D bounding box.
ref_pt = list(map(float, model["pts"].min(axis=0).flatten()))
size = list(map(float, (model["pts"].max(axis=0) - ref_pt).flatten()))

# Calculated diameter.
diameter = misc.calc_pts_diameter(model["pts"])
models_info[name] = {
    "min_x": ref_pt[0],
    "min_y": ref_pt[1],
    "min_z": ref_pt[2],
    "size_x": size[0],
    "size_y": size[1],
    "size_z": size[2],
    "diameter": diameter,
}

# Save the calculated info about the object models.
inout.save_json(MESH_DIR+name+'.json', models_info)

if not os.path.exists(MESH_DIR+name+'.mtl') and not os.path.exists(MESH_DIR+name+'.obj') and not os.path.exists(MESH_DIR+name+'.urdf'):
    print("Please add .mtl or .obj or .urdf")

if not os.path.exists(URDF_DIR):
    os.mkdir(URDF_DIR)
    shutil.copy(MESH_DIR+name+'.mtl', URDF_DIR)
    shutil.copy(MESH_DIR+name+'.obj', URDF_DIR)
    shutil.copy(MESH_DIR+name+'.urdf', URDF_DIR)
    
