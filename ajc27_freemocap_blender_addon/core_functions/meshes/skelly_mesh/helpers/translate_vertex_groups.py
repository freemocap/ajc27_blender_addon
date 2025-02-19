import bpy
import bmesh
from mathutils import Vector


def translate_vertex_groups(target_mesh, vertex_groups, bone_info):

    for vertex_group, info in vertex_groups.items():

        # Get the vertex group index
        vertex_group_index = target_mesh.vertex_groups[vertex_group].index

        # Get the origin vertex group index
        origin_vertex_group_index = target_mesh.vertex_groups[vertex_group + '_origin'].index

        # Try to get the end vertex group index
        try:
            end_vertex_group_index = target_mesh.vertex_groups[vertex_group + '_end'].index
        except KeyError:
            # Handle the case where the vertex group does not exist
            print(f"The vertex group '{vertex_group}_end' does not exist.")
            end_vertex_group_index = None

        # Find the origin vertex
        origin_vertex = None
        for vert in target_mesh.data.vertices:
            for group in vert.groups:
                if group.group == origin_vertex_group_index:
                    origin_vertex = vert
                    break
            if origin_vertex:
                break

        # Calculate distance vector
        bone_position = bone_info[info['armature_bone']]['head_position']
        delta_vector = Vector((
            bone_position[0] - origin_vertex.co[0],
            bone_position[1] - origin_vertex.co[1],
            bone_position[2] - origin_vertex.co[2]
        ))

        # Get the bmesh representation
        bm = bmesh.from_edit_mesh(target_mesh.data)

        # Ensure we start with no selections
        bpy.ops.mesh.select_all(action='DESELECT')

        # Find and select vertices in the specified vertex group
        for vert in bm.verts:
            bpy_vert = target_mesh.data.vertices[vert.index]
            for group in bpy_vert.groups:
                if group.group in [
                        vertex_group_index,
                        origin_vertex_group_index,
                        end_vertex_group_index]:
                    vert.select = True
                    break

        # Move the selected vertices by delta_vector
        bmesh.ops.translate(
            bm,
            vec=delta_vector,
            verts=[vert for vert in bm.verts if vert.select]
        )

        # Deselect all vertices
        for vert in bm.verts:
            vert.select = False

        # Update the mesh vertices' positions
        bmesh.update_edit_mesh(target_mesh.data)

    return
