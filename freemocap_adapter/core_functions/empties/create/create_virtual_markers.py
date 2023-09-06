from copy import copy
from typing import List, Dict

import numpy as np

from freemocap_adapter.core_functions.empties.create.create_empy_from_trajectory import \
    create_keyframed_empty_from_3d_trajectory_data
from freemocap_adapter.core_functions.load_data.load_freemocap_data import logger
from freemocap_adapter.data_models.freemocap_data.freemocap_data import FreemocapData
from freemocap_adapter.data_models.mediapipe_names.virtual_markers import MEDIAPIPE_VIRTUAL_MARKER_DEFINITIONS

import bpy

def test_virtual_marker_definitions(virtual_marker_definitions: dict):
    """
    Validate the virtual marker definitions dictionary to ensure that there are the same number of marker names and weights, and that the weights sum to 1
    """

    for (virtual_marker_name, virtual_marker_definition,) in virtual_marker_definitions.items():
        assert len(virtual_marker_definition["marker_names"]) == len(
            virtual_marker_definition["marker_weights"]
        ), f"marker_names and marker_weights must be the same length for virtual marker {virtual_marker_name}"
        assert (
                sum(virtual_marker_definition["marker_weights"]) == 1
        ), f"marker_weights must sum to 1 for virtual marker {virtual_marker_name}"


def calculate_virtual_marker_trajectory(
        trajectory_3d_frame_marker_xyz: np.ndarray,
        all_trajectory_names: list,
        component_trajectory_names: List,
        trajectory_weights: List,
) -> np.ndarray:
    """
    Create a virtual marker from a set of component markers. A 'Virtual Marker' is a 'fake' marker created by combining the data from 'real' (measured) marker/trajectory data
    `trajectory_3d_frame_marker_xyz`: all trajectory data in a numpy array with shape [frame, marker, xyz]
    `all_trajectory_names`: list of all trajectory names
    `component_trajectory_names`: the trajectories we'll use to make this virtual marker
    `trajectory_weights`: the weights we'll use to combine the compoenent trajectories into the virtual maker
    """

    # double check that the weights scale to one, otherwise this function will return screwy results
    assert np.sum(trajectory_weights) == 1, "Error - Trajectory_weights must sum to 1!"
    assert len(component_trajectory_names) == len(
        trajectory_weights
    ), "Error - component_trajectory_names and trajectory_weights must be the same length!"
    virtual_marker_xyz = np.zeros((trajectory_3d_frame_marker_xyz.shape[0], 3))

    for trajectory_name, weight in zip(component_trajectory_names, trajectory_weights):
        # pull out the trajectory data for this component trajectory and scale by it's `weight`
        component_trajectory_xyz = copy(
            trajectory_3d_frame_marker_xyz[:, all_trajectory_names.index(trajectory_name), :] * weight
        )

        # add it to the virtual marker
        virtual_marker_xyz += component_trajectory_xyz

    return virtual_marker_xyz


#TODO - disentagle "calculate" from "create empty" responsibilities
def calculate_virtual_trajectories(body_empty_scale: float,
                                   freemocap_data: FreemocapData,
                                    parent_object: bpy.types.Object,
                                   )->None:
    #######################################################################
    # %% create virtual markers
    logger.info("_________________________\n" 
                "Creating virtual markers...\n"
                "-------------------------\n")


    test_virtual_marker_definitions(MEDIAPIPE_VIRTUAL_MARKER_DEFINITIONS)

    virtual_marker_names = list(MEDIAPIPE_VIRTUAL_MARKER_DEFINITIONS.keys())
    virtual_markers = {}
    for virtual_marker_name in virtual_marker_names:
        component_trajectory_names = MEDIAPIPE_VIRTUAL_MARKER_DEFINITIONS[virtual_marker_name]["marker_names"]
        trajectory_weights = MEDIAPIPE_VIRTUAL_MARKER_DEFINITIONS[virtual_marker_name]["marker_weights"]

        logger.info(
            f"Calculating virtual marker trajectory: {virtual_marker_name} \n"
            f"Component trajectories: {component_trajectory_names} \n"
            f" weights: {trajectory_weights}\n"
        )

        virtual_marker_xyz = calculate_virtual_marker_trajectory(
            trajectory_3d_frame_marker_xyz=freemocap_data.body_fr_mar_xyz,
            all_trajectory_names=freemocap_data.body_names,
            component_trajectory_names=component_trajectory_names,
            trajectory_weights=trajectory_weights,
        )
        create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=virtual_marker_xyz,
            trajectory_name=virtual_marker_name,
            parent_origin=parent_object,
            empty_scale=body_empty_scale * 3,
            empty_type="PLAIN_AXES",
        )


