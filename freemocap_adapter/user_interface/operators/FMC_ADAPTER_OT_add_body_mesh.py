import math as m
import time

import bpy
from bpy.types import Operator

from freemocap_adapter.core_functions.empties.adjust_empties import adjust_empties
from freemocap_adapter.core_functions.rig.add_rig import add_rig
from freemocap_adapter.core_functions.rig.attach_mesh import add_mesh_to_rig

ADJUST_EMPTIES_EXECUTED = True


class FMC_ADAPTER_OT_add_body_mesh(Operator):
    bl_idname = 'fmc_adapter.add_body_mesh'
    bl_label = 'Freemocap Adapter - Add Body Mesh'
    bl_description = 'Add a body mesh to the rig. The mesh can be a file or a custom mesh made with basic shapes. This method first executes Add Empties and Add Rig(if no rig available)'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_tool

        # Get start time
        start = time.time()

        # Reset the scene frame to the start
        scene.frame_set(scene.frame_start)

        if not ADJUST_EMPTIES_EXECUTED:
            print('Executing First Adjust Empties...')

            # Execute Adjust Empties first
            adjust_empties(z_align_ref_empty=fmc_adapter_tool.vertical_align_reference,
                           z_align_angle_offset=fmc_adapter_tool.vertical_align_angle_offset,
                           ground_ref_empty=fmc_adapter_tool.ground_align_reference,
                           z_translation_offset=fmc_adapter_tool.vertical_align_position_offset
                           )

        # Execute Add Rig if there is no rig in the scene
        try:
            root = bpy.data.objects['root']
        except:
            print('Executing Add Rig to have a rig for the mesh...')
            add_rig(use_limit_rotation=fmc_adapter_tool.use_limit_rotation)

        print('Executing Add Body Mesh...')
        add_mesh_to_rig(body_mesh_mode=fmc_adapter_tool.body_mesh_mode)

        # Get end time and print execution time
        end = time.time()
        print('Finished. Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))

        return {'FINISHED'}