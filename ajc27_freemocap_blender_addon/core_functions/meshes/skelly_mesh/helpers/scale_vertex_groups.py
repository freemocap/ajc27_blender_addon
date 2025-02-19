import bpy
import bmesh
from mathutils import Vector, Matrix


def scale_vertex_groups(target_mesh, vertex_groups, bone_info):
    for vertex_group, info in vertex_groups.items():

        # Get the vertex group index
        vertex_group_index = target_mesh.vertex_groups[vertex_group].index

        # Set the origin and end vertex sufixes according to the group
        origin_sufix = '_left' if vertex_group == "FMC_pelvis" else '_origin'
        end_sufix = '_right' if vertex_group == "FMC_pelvis" else '_end'

        # Get the origin vertex group index
        origin_vertex_group_index = target_mesh.vertex_groups[vertex_group + origin_sufix].index

        # Try to get the end vertex group index
        try:
            end_vertex_group_index = target_mesh.vertex_groups[vertex_group + end_sufix].index
        except KeyError:
            # Handle the case where the vertex group does not exist
            # print(f"The vertex group '{vertex_group}_end' does not exist.")
            end_vertex_group_index = None

        # Find the origin and end vertices
        origin_vertex = None
        end_vertex = None
        for vert in target_mesh.data.vertices:
            for group in vert.groups:
                if group.group == origin_vertex_group_index:
                    origin_vertex = vert
                    break
                if group.group == end_vertex_group_index:
                    end_vertex = vert
                    break
            if origin_vertex and end_vertex:
                break

        if origin_vertex is not None and end_vertex is not None:
            # Calculate the distance between origin and end vertices
            origin_end_vector = origin_vertex.co - end_vertex.co
            origin_end_distance = origin_end_vector.length

            # Get the corresponding bone length
            if vertex_group == "FMC_pelvis":
                # TODO : make length as the sum of the elements of a armature_bone list to avoid this if
                bone_length = bone_info['pelvis.L']['length'] + bone_info['pelvis.R']['length']
            else:
                bone_length = bone_info[info['armature_bone']]['length']

            # Get the scale ratio using the bone length
            scale_ratio = bone_length / origin_end_distance

            # Get the bmesh representation
            bm = bmesh.from_edit_mesh(target_mesh.data)

            # Ensure we start with no selections
            bpy.ops.mesh.select_all(action='DESELECT')

            # Find and select vertices in the specified vertex group
            for vert in bm.verts:
                bpy_vert = target_mesh.data.vertices[vert.index]
                for group in bpy_vert.groups:
                    if group.group in [vertex_group_index, origin_vertex_group_index, end_vertex_group_index]:
                        vert.select = True
                        break

            # Scale the selected vertices
            bmesh.ops.scale(
                bm,
                vec=Vector((scale_ratio, scale_ratio, scale_ratio)),
                space=Matrix.Translation(-bone_info[info['armature_bone']]['head_position']),
                verts=[vert for vert in bm.verts if vert.select],
            )

            # Deselect all vertices
            for vert in bm.verts:
                vert.select = False

    return
