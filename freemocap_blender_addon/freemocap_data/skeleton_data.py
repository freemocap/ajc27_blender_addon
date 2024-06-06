from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from freemocap_blender_addon.freemocap_data.freemocap_data_component import FaceTrackedPoints, HandsData, \
    BodyTrackedPoints
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, DEFAULT_TRACKER_TYPE
from freemocap_blender_addon.utilities.get_path_to_test_data import get_path_to_test_data
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class SkeletonData(TypeSafeDataclass):
    body: BodyTrackedPoints
    hands: HandsData
    face: FaceTrackedPoints

    @classmethod
    def load_from_recording_path(cls,
                                 recording_path: str,
                                 tracker_type: TrackerSourceType) -> 'SkeletonData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            tracker_type=tracker_type)

        body = BodyTrackedPoints.create(data=np.load(data_paths.skeleton.body),
                                        data_source=tracker_type)

        face = FaceTrackedPoints.create(data=np.load(data_paths.skeleton.face),
                                        data_source=tracker_type)

        hands = HandsData.create(npy_paths=data_paths.skeleton.hands,
                                 data_source=tracker_type)

        return cls(body=body, hands=hands, face=face)

    def __str__(self):
        return f"SkeletonData: body={self.body}, hands={self.hands}, face={self.face}"


if __name__ == "__main__":
    recording_path_in = get_path_to_test_data()
    skeleton_data = SkeletonData.load_from_recording_path(recording_path=recording_path_in,
                                                          tracker_type=DEFAULT_TRACKER_TYPE)
    print(str(skeleton_data))
