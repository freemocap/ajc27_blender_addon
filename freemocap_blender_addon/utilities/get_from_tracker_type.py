from typing import List

from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, ComponentType
from freemocap_blender_addon.models.mediapipe_stuff.mediapipe_mapping import MediapipeBodyMapping
from freemocap_blender_addon.models.mediapipe_stuff.mediapipe_trajectory_names import MEDIAPIPE_BODY_NAMES, \
    MEDIAPIPE_FACE_NAMES, MEDIAPIPE_HAND_NAMES


def get_keypoint_names(component_type: ComponentType,
                       tracker_source: TrackerSourceType) -> List[str]:
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == ComponentType.BODY:
            return MEDIAPIPE_BODY_NAMES
        elif component_type == ComponentType.FACE:
            return MEDIAPIPE_FACE_NAMES
        elif component_type == ComponentType.RIGHT_HAND:
            return [f"right_hand_{name}" for name in MEDIAPIPE_HAND_NAMES]
        elif component_type == ComponentType.LEFT_HAND:
            return [f"left_hand_{name}" for name in MEDIAPIPE_HAND_NAMES]
        else:
            raise ValueError("Component type not recognized")


def get_mapping(component_type: ComponentType,
                tracker_source: TrackerSourceType): #TODO- figure out how to give this a generic `mapping` return type
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == ComponentType.BODY:
            return MediapipeBodyMapping

        else:
            raise ValueError("Component type not recognized")
    else:
        raise ValueError("Data source not recognized")
