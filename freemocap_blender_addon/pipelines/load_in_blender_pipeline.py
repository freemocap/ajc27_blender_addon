from dataclasses import dataclass

from freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import \
    create_empties_from_trajectories
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from freemocap_blender_addon.pipelines.pure_python_pipeline import PurePythonPipeline
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class LoadInBlenderPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    print("Running all stages...")

    def run(self):
        # Pure python stuff
        print("Loading freemocap data....")
        freemocap_data = PurePythonPipeline(recording_path_str=self.recording_path_str).run()

        for stage, trajectories in freemocap_data.items():
            trajectories = {key: value.trajectory_data * .001 for key, value in trajectories.items()}
            create_empties_from_trajectories(trajectories=trajectories, name=stage)




if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()
    pipeline = LoadInBlenderPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
