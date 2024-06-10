from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC


class CervicalSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.NECK_BASE_C7
    child = SkullKeypoints.SKULL_CENTER_ATLAS_C1


class ThoracicSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T12
    child = AxialSkeletonKeypoints.NECK_BASE_C7


class LumbarSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = AxialSkeletonKeypoints.CHEST_CENTER_T12


class AxialSegments(Enum):
    CERVICAL: SimpleSegmentABC = CervicalSegment
    THORACIC: SimpleSegmentABC = ThoracicSegment
    LUMBAR: SimpleSegmentABC = LumbarSegment

if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in list(AxialSegments)]))
