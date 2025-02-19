
def parent_vertex_groups_to_armature(target_mesh, vertex_groups, armature):
    # Add the hook modifiers
    for vertex_group, info in vertex_groups.items():
        hook = target_mesh.modifiers.new(name='Hook_' + vertex_group, type='HOOK')
        hook.object = armature
        hook.subtarget = info['armature_bone']
        hook.vertex_group = vertex_group

    return
