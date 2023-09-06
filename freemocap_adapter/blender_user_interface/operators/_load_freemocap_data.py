import logging
import bpy

from freemocap_adapter.core_functions.empties.create.create_freemocap_empties import create_freemocap_empties
from freemocap_adapter.core_functions.load_data.load_freemocap_data import load_freemocap_data, \
    create_freemocap_origin_axes, set_start_end_frame

logger = logging.getLogger(__name__)


class FMC_ADAPTER_load_freemocap_data(bpy.types.Operator):  # , bpy_extras.io_utils.ImportHelper):
    bl_idname = 'fmc_adapter.load_freemocap_data'
    bl_label = "Load FreeMoCap Data"

    def execute(self, context):

        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_tool

        freemocap_origin_axes = create_freemocap_origin_axes()

        # if fmc_adapter_tool.recording_path == "":
        #     load_freemocap_data(recording_path=self.filepath)
        # else:
        try:
            logger.info("Loading freemocap data....")
            freemocap_data = load_freemocap_data(recording_path=fmc_adapter_tool.recording_path)
            set_start_end_frame(number_of_frames=freemocap_data.number_of_frames)
        except Exception as e:
            logger.error(e)
            return {'CANCELLED'}

        try:
            logger.info("Creating keyframed empties....")
            logger.info("Create keyframed empties...")
            freemocap_empties = create_freemocap_empties(freemocap_data=freemocap_data,
                                                         parent_object=freemocap_origin_axes, )
            logger.success(f"Finished creating keyframed empties: {freemocap_empties.keys()}")
        except Exception as e:
            logger.error(e)
            return {'CANCELLED'}





        return {'FINISHED'}