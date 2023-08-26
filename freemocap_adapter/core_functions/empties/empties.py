import math as m

import bpy

EMPTY_VELOCITIES = {}
EMPTY_POSITIONS = {}


def update_empty_positions():

    print('Updating Empty Positions Dictionary...')

    # Get the scene context
    scene = bpy.context.scene

    # Change to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Reset the empty positions dictionary with empty arrays for each empty
    for object in bpy.data.objects:
        if object.type == 'EMPTY' and object.name != 'freemocap_origin_axes' and object.name != 'world_origin' and object.name != '_full_body_center_of_mass':
            EMPTY_POSITIONS[object.name] = {'x': [], 'y': [], 'z': []}

    # Iterate through each scene frame and save the coordinates of each empty in the dictionary. Frame is displaced by -1 to match animation curves.
    for frame in range (scene.frame_start - 1, scene.frame_end):
        # Set scene frame
        scene.frame_set(frame)
        # Iterate through each object
        for object in bpy.data.objects:
            if object.type == 'EMPTY' and object.name != 'freemocap_origin_axes' and object.name != 'world_origin' and object.name != '_full_body_center_of_mass':
                # Save the x, y, z position of the empty
                EMPTY_POSITIONS[object.name]['x'].append(bpy.data.objects[object.name].location[0])
                EMPTY_POSITIONS[object.name]['y'].append(bpy.data.objects[object.name].location[1])
                EMPTY_POSITIONS[object.name]['z'].append(bpy.data.objects[object.name].location[2])

    # Reset the scene frame to the start
    scene.frame_set(scene.frame_start)

    print('Empty Positions Dictionary update completed.')


def update_empty_velocities(recording_fps):

    print('Updating Empty Speeds Dictionary...')

    # Get the scene context
    scene = bpy.context.scene

    # Change to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Reset the empty speeds dictionary with an array with one element of value zero for each empty marker
    for object in bpy.data.objects:
        if object.type == 'EMPTY' and object.name != 'freemocap_origin_axes' and object.name != 'world_origin' and object.name != '_full_body_center_of_mass':
            EMPTY_VELOCITIES[object.name] = {'speed': [0]}

    # Iterate through each scene frame starting from frame start + 1 and save the speed of each empty in the dictionary
    for frame in range (scene.frame_start + 1, scene.frame_end + 1):
        # Set scene frame
        scene.frame_set(frame)
        # Iterate through each object
        for object in bpy.data.objects:
            if object.type == 'EMPTY' and object.name != 'freemocap_origin_axes' and object.name != 'world_origin' and object.name != '_full_body_center_of_mass':
                # Save the speed of the empty based on the recording fps and the distance to the position of the empty in the previous frame
                # print('length:' + str(len(empty_positions[object.name]['x'])))
                # print('frame:'+str(frame))
                current_frame_position  = \
                (EMPTY_POSITIONS[object.name]['x'][frame - 1], EMPTY_POSITIONS[object.name]['y'][frame - 1],
                EMPTY_POSITIONS[object.name]['z'][frame - 1])
                previous_frame_position = (
                EMPTY_POSITIONS[object.name]['x'][frame - 2], EMPTY_POSITIONS[object.name]['y'][frame - 2],
                EMPTY_POSITIONS[object.name]['z'][frame - 2])
                seconds_per_frame = 1 / recording_fps
                EMPTY_VELOCITIES[object.name]['speed'].append(
                    m.dist(current_frame_position, previous_frame_position) / seconds_per_frame)

    # Reset the scene frame to the start
    scene.frame_set(scene.frame_start)

    print('Empty Speeds Dictionary update completed.')