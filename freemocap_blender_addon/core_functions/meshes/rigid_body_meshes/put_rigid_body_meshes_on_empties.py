from typing import Tuple

from freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import ParentedEmpties
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.make_rigid_body_mesh import \
    make_rigid_body_mesh
from freemocap_blender_addon.freemocap_data.data_paths.default_path_enums import RightLeft
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.bones.bone_constraint_types import ConstraintType
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name
from freemocap_blender_addon.utilities.color_generator import generate_color, ColorType

DEFAULT_APPENDICULAR_RIGID_BODY_MESH_SQUISH = (.8, 1, 1)

DEFAULT_AXIAL_RIGID_BODY_MESH_SQUISH = (1.0, 1.0, 1.0)

DEFAULT_LEFT_SIDE_COLOR = "#0033BB"

DEFAULT_RIGHT_SIDE_COLOR = "#BB0033"


def put_rigid_body_meshes_on_empties(parented_empties: ParentedEmpties,
                                     segment_definitions: RigidSegmentDefinitions,
                                     ):
    axial_color = generate_color(ColorType.JEWEL)
    right_color = DEFAULT_RIGHT_SIDE_COLOR
    left_color = DEFAULT_LEFT_SIDE_COLOR
    axial_squish = DEFAULT_AXIAL_RIGID_BODY_MESH_SQUISH
    appendicular_squish = DEFAULT_APPENDICULAR_RIGID_BODY_MESH_SQUISH

    def get_color_and_squish(segment_name: str) -> Tuple[str, Tuple[float, float, float]]:
        if ".R" in segment_name:
            mesh_color = right_color
            mesh_squish = appendicular_squish
        elif ".L" in segment_name:
            mesh_color = left_color
            mesh_squish = appendicular_squish
        else:
            mesh_color = axial_color
            mesh_squish = axial_squish
        return mesh_color, mesh_squish

    for segment_name, segment in segment_definitions.items():
        print(
            f"Creating rigid body mesh for segment: {segment_name} with length: {segment.length:.3f}m")
        color, squish = get_color_and_squish(segment_name)

        bone_mesh = make_rigid_body_mesh(
            name=f"{parented_empties.parent_name}_rigid_body_mesh_{segment_name}",
            length=segment.length,
            squish_scale=squish,
            joint_color=color,
            cone_color=color,
            axis_visible=False
        )
        location_constraint = bone_mesh.constraints.new(type=ConstraintType.COPY_LOCATION.value)
        location_constraint.target = parented_empties.empties[segment.parent]

        track_to_constraint = bone_mesh.constraints.new(type=ConstraintType.DAMPED_TRACK.value)
        track_to_constraint.target = parented_empties.empties[segment.child]
        track_to_constraint.track_axis = "TRACK_Z"
        bone_mesh.parent = parented_empties.parent_object
