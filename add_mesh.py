"""Calculates the 3D bounding box and the diameter of 3D object models."""
from deps.bop_toolkit_cosypose.bop_toolkit_lib import inout
from deps.bop_toolkit_cosypose.bop_toolkit_lib import misc
import os
CURR_DIR = os.path.abspath("")

models_info = {}
# You only need to provide the path
model = inout.load_ply(CURR_DIR+r'/inputs/meshes/obj_000031.ply')

# Calculate 3D bounding box.
ref_pt = list(map(float, model["pts"].min(axis=0).flatten()))
size = list(map(float, (model["pts"].max(axis=0) - ref_pt).flatten()))

# Calculated diameter.
diameter = misc.calc_pts_diameter(model["pts"])
models_info['obj_000031'] = {
    "min_x": ref_pt[0],
    "min_y": ref_pt[1],
    "min_z": ref_pt[2],
    "size_x": size[0],
    "size_y": size[1],
    "size_z": size[2],
    "diameter": diameter,
}

# Save the calculated info about the object models.
inout.save_json(CURR_DIR+r'/inputs/meshes/obj_000031.json', models_info)