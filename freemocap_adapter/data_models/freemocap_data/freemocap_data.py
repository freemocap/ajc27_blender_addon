import logging
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

from freemocap_adapter.data_models.freemocap_data.freemocap_data_stats import FreemocapDataStats

logger = logging.getLogger(__name__)


@dataclass
class DataPaths:
    body_npy: Path
    right_hand_npy: Path
    left_hand_npy: Path
    face_npy: Path

    @classmethod
    def from_recording_folder(cls, path: str):
        recording_path = Path(path)
        output_data_path = recording_path / "output_data"
        return cls(
            body_npy=output_data_path / "mediapipe_body_3d_xyz.npy",
            right_hand_npy=output_data_path / "mediapipe_right_hand_3d_xyz.npy",
            left_hand_npy=output_data_path / "mediapipe_left_hand_3d_xyz.npy",
            face_npy=output_data_path / "mediapipe_face_3d_xyz.npy"
        )


# TODO - need to break this up into a simple data class and a class that handles the operations.
@dataclass
class FreemocapData:
    body_fr_mar_xyz: np.ndarray
    right_hand_fr_mar_xyz: np.ndarray
    left_hand_fr_mar_xyz: np.ndarray
    face_fr_mar_xyz: np.ndarray

    data_source: str
    body_names: List[str]
    right_hand_names: List[str]
    left_hand_names: List[str]
    face_names: List[str]

    _intermediate_stages = None

    @property
    def number_of_frames(self):
        return self.body_fr_mar_xyz.shape[0]

    @property
    def number_of_body_markers(self):
        return self.body_fr_mar_xyz.shape[1]

    @property
    def number_of_right_hand_markers(self):
        return self.right_hand_fr_mar_xyz.shape[1]

    @property
    def number_of_left_hand_markers(self):
        return self.left_hand_fr_mar_xyz.shape[1]

    @property
    def number_of_face_markers(self):
        return self.face_fr_mar_xyz.shape[1]

    @property
    def number_of_hand_markers(self):
        if not self.number_of_right_hand_markers == self.number_of_left_hand_markers:
            logger.warning(f"Number of right hand markers ({self.number_of_right_hand_markers}) "
                           f"does not match number of left hand markers ({self.number_of_left_hand_markers}).")
        return self.number_of_right_hand_markers + self.number_of_left_hand_markers

    @property
    def number_of_markers(self):
        return (self.number_of_body_markers +
                self.number_of_right_hand_markers +
                self.number_of_left_hand_markers +
                self.number_of_face_markers)



    @classmethod
    def from_data(cls,
                  body_fr_mar_xyz: np.ndarray,
                  right_hand_fr_mar_xyz: np.ndarray,
                  left_hand_fr_mar_xyz: np.ndarray,
                  face_fr_mar_xyz: np.ndarray,
                  data_source: str = "mediapipe",
                  processing_stage: str = "original_from_file",
                  **kwargs) -> "FreemocapData":

        (body_names,
         face_names,
         left_hand_names,
         right_hand_names) = cls._create_trajecory_name_lists(body_fr_mar_xyz,
                                                              data_source,
                                                              face_fr_mar_xyz,
                                                              left_hand_fr_mar_xyz,
                                                              right_hand_fr_mar_xyz)

        instance = cls(
            body_fr_mar_xyz=body_fr_mar_xyz,
            right_hand_fr_mar_xyz=right_hand_fr_mar_xyz,
            left_hand_fr_mar_xyz=left_hand_fr_mar_xyz,
            face_fr_mar_xyz=face_fr_mar_xyz,
            data_source=data_source,
            body_names=body_names,
            right_hand_names=right_hand_names,
            left_hand_names=left_hand_names,
            face_names=face_names,
        )
        instance.mark_processing_stage(processing_stage)
        return instance

    @classmethod
    def _create_trajecory_name_lists(cls, body_fr_mar_xyz, data_source, face_fr_mar_xyz, left_hand_fr_mar_xyz,
                                     right_hand_fr_mar_xyz):
        if data_source == "mediapipe":
            from freemocap_adapter.data_models.mediapipe_names.trajectory_names import MEDIAPIPE_TRAJECTORY_NAMES
            body_names = MEDIAPIPE_TRAJECTORY_NAMES["body"]
            right_hand_names = [f"right_hand_{name}" for name in MEDIAPIPE_TRAJECTORY_NAMES["hand"]]
            left_hand_names = [f"left_hand_{name}" for name in MEDIAPIPE_TRAJECTORY_NAMES["hand"]]
            face_names = []
            for index in range(face_fr_mar_xyz.shape[1]):
                if index < len(MEDIAPIPE_TRAJECTORY_NAMES["face"]):
                    face_names.append(f"face_{MEDIAPIPE_TRAJECTORY_NAMES['face'][index]}")
                else:
                    face_names.append(f"face_{index}")
        else:
            logger.error(f"Data source {data_source} not recognized.")
            body_names = [f"body_{index}" for index in range(body_fr_mar_xyz.shape[1])]
            right_hand_names = [f"right_hand_{index}" for index in range(right_hand_fr_mar_xyz.shape[1])]
            left_hand_names = [f"left_hand_{index}" for index in range(left_hand_fr_mar_xyz.shape[1])]
            face_names = [f"face_{index}" for index in range(face_fr_mar_xyz.shape[1])]
            pass
        return body_names, face_names, left_hand_names, right_hand_names

    @classmethod
    def from_data_paths(cls,
                        data_paths: DataPaths,
                        scale: float = 1000,
                        **kwargs):
        return cls.from_data(
            body_fr_mar_xyz=np.load(str(data_paths.body_npy)) / scale,
            right_hand_fr_mar_xyz=np.load(str(data_paths.right_hand_npy)) / scale,
            left_hand_fr_mar_xyz=np.load(str(data_paths.left_hand_npy)) / scale,
            face_fr_mar_xyz=np.load(str(data_paths.face_npy)) / scale,
            **kwargs
        )

    @classmethod
    def from_recording_path(cls,
                            recording_path: str,
                            **kwargs):
        data_paths = DataPaths.from_recording_folder(recording_path)
        logger.info(f"Loading data from paths {data_paths}")
        return cls.from_data_paths(data_paths=data_paths, **kwargs)

    def mark_processing_stage(self, name: str, overwrite: bool = True):
        """
        Mark the current state of the data as a processing stage (e.g. "raw", "reoriented", etc.)
        """
        if self._intermediate_stages is None:
            self._intermediate_stages = {}
        if name in self._intermediate_stages.keys() and not overwrite:
            raise ValueError(f"Processing stage {name} already exists. Set overwrite=True to overwrite.")
        self._intermediate_stages[name] = deepcopy(self.__dict__)

    def get_processing_stage(self, name: str) -> "FreemocapData":
        """
        Get the data from a processing stage (e.g. "raw", "reoriented", etc.)
        """
        if self._intermediate_stages is None:
            raise ValueError("No processing stages have been marked yet.")

        return FreemocapData.from_data(**self._intermediate_stages[name])

    def __str__(self):
        return_strings = []
        for key in self._intermediate_stages.keys():
            label = f"Processing stage: {key}\n"
            label += f"{str(FreemocapDataStats.from_freemocap_data(self.get_processing_stage(name=key)))}"
            return_strings.append(label)

        return "\n".join(return_strings)

    def __add__(self, other: float):
        self.body_fr_mar_xyz += other
        self.right_hand_fr_mar_xyz += other
        self.left_hand_fr_mar_xyz += other
        self.face_fr_mar_xyz += other
        return self

    def __sub__(self, other: float):
        self.body_fr_mar_xyz -= other
        self.right_hand_fr_mar_xyz -= other
        self.left_hand_fr_mar_xyz -= other
        self.face_fr_mar_xyz -= other
        return self

    def __mul__(self, other: float):
        self.body_fr_mar_xyz *= other
        self.right_hand_fr_mar_xyz *= other
        self.left_hand_fr_mar_xyz *= other
        self.face_fr_mar_xyz *= other
        return self

    def __truediv__(self, number: float):
        # Check if the number is not zero (to avoid division by zero)
        if number != 0:
            # Perform division
            body_fr_mar_xyz = self.body_fr_mar_xyz / number
            right_hand_fr_mar_xyz = self.right_hand_fr_mar_xyz / number
            left_hand_fr_mar_xyz = self.left_hand_fr_mar_xyz / number
            face_fr_mar_xyz = self.face_fr_mar_xyz / number

            # Create a new FreemocapData instance with the divided matrices and return
            return FreemocapData(body_fr_mar_xyz=body_fr_mar_xyz,
                                 right_hand_fr_mar_xyz=right_hand_fr_mar_xyz,
                                 left_hand_fr_mar_xyz=left_hand_fr_mar_xyz,
                                 face_fr_mar_xyz=face_fr_mar_xyz,
                                 data_source=self.data_source,
                                 body_names=self.body_names,
                                 right_hand_names=self.right_hand_names,
                                 left_hand_names=self.left_hand_names,
                                 face_names=self.face_names,
                                 )

        else:
            print("Error: Division by zero.")
            return self  # Just return the current instance as is

    def _rotate_data(self, data, rotation_matrix):
        return np.dot(data, rotation_matrix.T)

    def apply_rotation(self, rotation_matrix):
        self.body_fr_mar_xyz = self._rotate_data(self.body_fr_mar_xyz, rotation_matrix)
        self.right_hand_fr_mar_xyz = self._rotate_data(self.right_hand_fr_mar_xyz, rotation_matrix)
        self.left_hand_fr_mar_xyz = self._rotate_data(self.left_hand_fr_mar_xyz, rotation_matrix)
        self.face_fr_mar_xyz = self._rotate_data(self.face_fr_mar_xyz, rotation_matrix)

    def apply_transform(self, transform):
        # Separate rotation matrix and translation vector
        rotation_matrix = transform[:3, :3]
        translation_vector = transform[:3, 3]

        # Apply rotation
        self.apply_rotation(rotation_matrix)

        # Apply translation
        self += translation_vector


if __name__ == "__main__":
    from freemocap_adapter.core_functions.load_data.get_path_to_sample_data import get_path_to_sample_data

    recording_path = get_path_to_sample_data()
    freemocap_data = FreemocapData.from_recording_path(recording_path=recording_path,
                                                       type="original")
    freemocap_data *= 2
    freemocap_data.mark_processing_stage("doubled")

    freemocap_data += 1e9
    freemocap_data.mark_processing_stage("added 1e9")

    freemocap_data -= 1e9
    freemocap_data.mark_processing_stage("subtracted 1e9")

    freemocap_data /= 2
    freemocap_data.mark_processing_stage("halved")

    freemocap_data.apply_rotation(np.eye(3).T)
    freemocap_data.mark_processing_stage("rotated")

    freemocap_data.apply_transform(np.eye(4).T)
    freemocap_data.mark_processing_stage("transformed")

    print(str(freemocap_data))