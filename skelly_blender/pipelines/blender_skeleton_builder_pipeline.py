from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from skelly_blender.core.blender_stuff.armature_rig.armatures.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedTrajectories
from skelly_blender.core.blender_stuff.keyframed_empties.create_keyframed_empties import create_keyframed_empties
from skelly_blender.core.blender_stuff.rigid_body_meshes.put_rigid_body_meshes_on_empties import \
    put_rigid_body_meshes_on_empties
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skelly_blender.pipelines.blender_pipeline_config import PipelineConfig
from skelly_blender.pipelines.pure_python_pipeline import PurePythonPipeline
from skelly_blender.core.pure_python.freemocap_data.freemocap_trajectory_data import FreemocapTrajectoryData
from skelly_blender.tests.download_test_data import get_test_data_path


@dataclass
class BlenderSkeletonBuilderPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    pipeline_config: PipelineConfig = field(default_factory=PipelineConfig)

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, show_stages: bool = False, scale=.001):
        # Pure python stuff
        print("Loading freemocap data....")
        freemocap_data = PurePythonPipeline(recording_path_str=self.recording_path_str).run(scale=scale)

        trajectories_to_show = self._get_trajectories_to_show(freemocap_data=freemocap_data,
                                                              show_stages=show_stages)

        for stage, trajectories in trajectories_to_show.items():
            parented_empties = create_keyframed_empties(trajectories=trajectories,
                                                        parent_name=stage)
            # put_spheres_on_parented_empties(parented_empties=parented_empties)

            segment_definitions = freemocap_data.get_blenderized_segment_definitions()
            put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                             segment_definitions=segment_definitions
                                             )

            print("Generating armature from segment lengths and rest pose definitions...")
            armature_definition = ArmatureDefinition.create(
                armature_name=f"{self.recording_name}_armature",
                segment_definitions=blenderized_segment_definitions,
                pose_definition=self.pipeline_config.add_rig.rest_pose_definition,
                bone_constraints=self.pipeline_config.add_rig.bone_constraints,
            )
            armature = generate_armature(armature_definition=armature_definition)

            # attach_skelly_bone_meshes(
            #     armature=armature,
            #     armature_definition=armature_definition,
            # )

            rig = generate_rig(
                armature=armature,
                config=self.pipeline_config.add_rig,
            )

        print(f"Finished building blender skeleton for recording: {self.recording_name}")

    def _get_trajectories_to_show(self,
                                  freemocap_data: FreemocapTrajectoryData,
                                  show_stages: bool) -> Dict[str, BlenderizedTrajectories]:
        if show_stages:
            og_trajectories_to_show = freemocap_data.get_trajectories_by_stage(blenderize_names=True)
            trajectories_to_show = {}
            for key, trajectories in og_trajectories_to_show.items():
                trajectories_to_show[f"{self.recording_name}_{key}"] = {self.recording_name: trajectories}
        else:
            trajectories_to_show = {
                self.recording_name: freemocap_data.get_keypoint_trajectories(blenderize_names=True)}
        return trajectories_to_show


if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()
    pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
