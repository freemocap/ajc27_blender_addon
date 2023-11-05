import traceback
from pathlib import Path
from typing import List

from .meshes.center_of_mass.com_mesh import create_center_of_mass_mesh
from .meshes.center_of_mass.com_trails import create_center_of_mass_trails
from .meshes.skelly_mesh.attach_skelly_mesh import attach_skelly_mesh_to_rig
from .rig.save_bone_and_joint_angles_from_rig import save_bone_and_joint_angles_from_rig
from ..core_functions.bones.enforce_rigid_bones import enforce_rigid_bones
from ..core_functions.empties.creation.create_freemocap_empties import (
    create_freemocap_empties,
)
from ..core_functions.freemocap_data_handler.helpers.get_or_create_freemocap_data_handler import (
    get_or_create_freemocap_data_handler,
)
from ..core_functions.freemocap_data_handler.helpers.saver import FreemocapDataSaver
from ..core_functions.freemocap_data_handler.operations.fix_hand_data import (
    fix_hand_data,
)
from ..core_functions.freemocap_data_handler.operations.put_skeleton_on_ground import (
    put_skeleton_on_ground,
)
from ..core_functions.load_data.load_freemocap_data import load_freemocap_data
from ..core_functions.load_data.load_videos import load_videos
from ..core_functions.meshes.attach_mesh_to_rig import attach_mesh_to_rig
from ..core_functions.rig.add_rig import add_rig
from ..core_functions.setup_scene.make_parent_empties import (
    create_parent_empty,
)
from ..core_functions.setup_scene.set_start_end_frame import set_start_end_frame
from ..data_models.parameter_models.parameter_models import Config


class MainController:
    """
    This class is used to run the program as a main script.
    """

    def __init__(self, recording_path: str, save_path: str, config: Config):
        self.rig = None
        self.empties = None
        self._data_parent_object = None
        self._empty_parent_object = None
        self._rigid_body_meshes_parent_object = None
        self._video_parent_object = None

        self.config = config

        self.recording_path = recording_path
        self.save_path = save_path
        self.recording_name = Path(self.recording_path).stem
        self.origin_name = f"{self.recording_name}_origin"
        self.rig_name = f"{self.recording_name}_rig"
        self._create_parent_empties()
        self.freemocap_data_handler = get_or_create_freemocap_data_handler(
            recording_path=self.recording_path
        )
        self.empties = None

    @property
    def data_parent_object(self):
        return self._data_parent_object

    @property
    def empty_names(self) -> List[str]:
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        empty_names = []

        def get_empty_names_from_dict(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    get_empty_names_from_dict(value) #recursion, baby!
                else:
                    empty_names.append(key)

        get_empty_names_from_dict(self.empties)

        return empty_names
    
    @property
    def center_of_mass_empty(self):
        if self.empties is None:
            raise ValueError("Empties have not been created yet!")
        return list(self.empties["other"]["center_of_mass"].values())[0]

    def _create_parent_empties(self):
        self._data_parent_object = create_parent_empty(name=self.origin_name,
                                                       display_scale=1.0,
                                                       type="ARROWS")
        self._empty_parent_object = create_parent_empty(
            name=f"empties",
            parent_object=self._data_parent_object,
            type="PLAIN_AXES",
            display_scale=0.3,
        )
        self._rigid_body_meshes_parent_object = create_parent_empty(
            name=f"rigid_body_meshes",
            parent_object=self._data_parent_object,
            type="CUBE",
            display_scale=0.2,
        )
        self._video_parent_object = create_parent_empty(
            name=f"videos",
            parent_object=self._data_parent_object,
            type="SPHERE",
            display_scale=0.1,
        )

    def load_freemocap_data(self):
        try:
            print("Loading freemocap data....")
            self.freemocap_data_handler = load_freemocap_data(
                recording_path=self.recording_path
            )
            self.freemocap_data_handler.mark_processing_stage("original_from_file")
            set_start_end_frame(
                number_of_frames=self.freemocap_data_handler.number_of_frames
            )
        except Exception as e:
            print(f"Failed to load freemocap data: {e}")
            raise e

    def calculate_virtual_trajectories(self):
        try:
            print("Calculating virtual trajectories....")
            self.freemocap_data_handler.calculate_virtual_trajectories()
            self.freemocap_data_handler.mark_processing_stage(
                "add_virtual_trajectories"
            )
        except Exception as e:
            print(f"Failed to calculate virtual trajectories: {e}")
            print(e)
            raise e

    def put_data_in_inertial_reference_frame(self):
        try:
            print("Putting freemocap data in inertial reference frame....")
            put_skeleton_on_ground(handler=self.freemocap_data_handler)
        except Exception as e:
            print(
                f"Failed when trying to put freemocap data in inertial reference frame: {e}"
            )
            print(traceback.format_exc())
            raise e

    def enforce_rigid_bones(self):
        print("Enforcing rigid bones...")
        try:
            self.freemocap_data_handler = enforce_rigid_bones(
                handler=self.freemocap_data_handler
            )

        except Exception as e:
            print(f"Failed during `enforce rigid bones`, error: `{e}`")
            print(e)
            raise e

    def fix_hand_data(self):
        try:
            print("Fixing hand data...")
            self.freemocap_data_handler = fix_hand_data(
                handler=self.freemocap_data_handler
            )
        except Exception as e:
            print(f"Failed during `fix hand data`, error: `{e}`")
            print(e)
            raise e

    def save_data_to_disk(self):
        try:
            print("Saving data to disk...")
            FreemocapDataSaver(handler=self.freemocap_data_handler).save(
                recording_path=self.recording_path
            )
        except Exception as e:
            print(f"Failed to save data to disk: {e}")
            print(e)
            raise e

    def create_empties(self):
        try:
            print("Creating keyframed empties....")

            self.empties = create_freemocap_empties(
                handler=self.freemocap_data_handler,
                parent_object=self._empty_parent_object,
            )
            print(f"Finished creating keyframed empties: {self.empties.keys()}")
        except Exception as e:
            print(f"Failed to create keyframed empties: {e}")

    def add_rig(self):
        try:
            print("Adding rig...")
            self.rig = add_rig(
                empty_names=self.empty_names,
                bone_data=self.freemocap_data_handler.metadata["bone_data"],
                rig_name=self.rig_name,
                parent_object=self._data_parent_object,
                keep_symmetry=self.config.add_rig.keep_symmetry,
                add_fingers_constraints=self.config.add_rig.add_fingers_constraints,
                use_limit_rotation=self.config.add_rig.use_limit_rotation,
            )
        except Exception as e:
            print(f"Failed to add rig: {e}")
            print(e)
            raise e

    def save_bone_and_joint_data_from_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Saving joint angles...")
            csv_file_path = str(
                Path(self.save_path).parent / "saved_data" / f"{self.recording_name}_bone_and_joint_data.csv")
            save_bone_and_joint_angles_from_rig(
                rig=self.rig,
                csv_save_path=csv_file_path,
                start_frame=0,
                end_frame=self.freemocap_data_handler.number_of_frames,
            )
        except Exception as e:
            print(f"Failed to save joint angles: {e}")
            print(e)
            raise e

    def attach_rigid_body_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")

        try:
            print("Adding rigid_body_bone_meshes...")
            attach_mesh_to_rig(
                body_mesh_mode=self.config.add_body_mesh.body_mesh_mode,
                rig=self.rig,
                empties=self.empties,
                parent_object=self._rigid_body_meshes_parent_object,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def attach_skelly_mesh_to_rig(self):
        if self.rig is None:
            raise ValueError("Rig is None!")
        try:
            print("Adding Skelly mesh!!! :D")
            body_dimensions = self.freemocap_data_handler.get_body_dimensions()
            attach_skelly_mesh_to_rig(
                rig=self.rig,
                body_dimensions=body_dimensions,
                empties=self.empties
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_mesh(self):

        try:
            print("Adding Center of Mass Mesh")
            create_center_of_mass_mesh(
                parent_object=self._rigid_body_meshes_parent_object,
                center_of_mass_empty=self.center_of_mass_empty,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def create_center_of_mass_trails(self):
        return
        try:
            print("Adding Center of Mass trail meshes")
            create_center_of_mass_trails(
                center_of_mass_xyz = self.freemocap_data_handler.center_of_mass_trajectory,
                center_of_mass_empty = self.freemocap_data_handler.center_of_mass_empty,
            )
        except Exception as e:
            print(f"Failed to attach mesh to rig: {e}")
            print(e)
            raise e

    def add_videos(self):
        try:
            print("Loading videos as planes...")
            load_videos(
                recording_path=self.recording_path,
                parent_object=self._video_parent_object,
            )
        except Exception as e:
            print(e)
            print(e)
            raise e

    def setup_scene(self):
        import bpy

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:  # iterate through areas in current screen
                if area.type == "VIEW_3D":
                    for (
                            space
                    ) in area.spaces:  # iterate through spaces in current VIEW_3D area
                        if space.type == "VIEW_3D":  # check if space is a 3D view
                            space.shading.type = "MATERIAL"

        # self.data_parent_object.hide_set(True)
        self._empty_parent_object.hide_set(True)
        self._rigid_body_meshes_parent_object.hide_set(True)
        self._video_parent_object.hide_set(True)


    def save_blender_file(self):
        print("Saving blender file...")
        import bpy

        bpy.ops.wm.save_as_mainfile(filepath=str(self.save_path))
        print(f"Saved .blend file to: {self.save_path}")

    def run_all(self):
        print("Running all stages...")

        #Pure python stuff
        self.load_freemocap_data()
        self.calculate_virtual_trajectories()
        self.put_data_in_inertial_reference_frame()
        self.enforce_rigid_bones()
        self.fix_hand_data()
        self.save_data_to_disk()

        #Blender stuff
        self.create_empties()
        self.add_rig()
        self.save_bone_and_joint_data_from_rig()
        self.attach_rigid_body_mesh_to_rig()
        self.attach_skelly_mesh_to_rig()
        self.create_center_of_mass_mesh()
        self.create_center_of_mass_trails()
        self.add_videos()
        self.setup_scene()
        self.save_blender_file()
        # export_fbx(recording_path=recording_path, )