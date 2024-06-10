from abc import ABC
from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class Keypoint(TypeSafeDataclass, ABC):
    """
    A Keypoint is a named "key" location on a skeleton, used to define the position of a rigid body or linkage.
    In marker-based motion capture, keypoints could correspond to markers placed on the body.
    In markerless motion capture, keypoints could correspond to a tracked point in the image.
    When a Keypoint is hydrated with data, it becomes a Trajectory.

    `definition` is a human-oriented description of the keypoint's location (e.g. an anatomical
    description of a landmark on a bone).
    """
    name: str
    definition: str

    def __post_init__(self):
        print(f"Keypoint: {self.name} instantiated with definition {self.definition}")

    def __str__(self):
        return f"Keypoint: {self.name}"

@dataclass
class KeypointTrajectory(Keypoint):
    """
    A KeypointTrajectory is a Keypoint that has been hydrated with data.
    """
    data: np.ndarray

    def __post_init__(self):
        if not len(self.data.shape) == 2:
            raise ValueError("Data shape should be (frame, xyz)")
        if not self.data.shape[1] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")

        print(f"Instantiated KeypointTrajectory: {self}")

    def __str__(self):
        out_str = super().__str__()
        out_str += f"\n\tTrajectory Data shape: {self.data.shape}\n"
        return out_str



