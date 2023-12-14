import math
import os
import time
from pathlib import Path


import bpy

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.add_render_background import \
    add_render_background

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_cameras import place_cameras
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_lights import place_lights
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.rearrange_background_videos import \
    rearrange_background_videos
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import render_parameters, export_profiles

def create_video(scene: bpy.types.Scene,
                 recording_folder: str,
                 export_profile: str = 'debug',
                 start_frame: int = 1,
                 end_frame: int = 250) -> None:

    # Set the output file name
    video_file_name = Path(recording_folder).name + '.mp4'
    # Set the output file
    video_render_path = str(Path(recording_folder) / video_file_name)
    bpy.context.scene.render.filepath = video_render_path
    print(f"Exporting video to: {video_render_path} ...")

    # Set the output format to MPEG4
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'

    # Set the codec
    bpy.context.scene.render.ffmpeg.codec = 'H264'

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Get start time
    start = time.time()

    # Place the required cameras
    cameras_positions = place_cameras(scene, export_profile)

    # Place the required lights
    place_lights(scene, cameras_positions)

    # Rearrange the background videos

    # Render the animation
    bpy.ops.render.render(animation=True)



    if  Path(video_render_path).exists():
        print(f"Video file successfully created at: {video_render_path}")
    else:
        print("ERROR - Video file was not created!! Nothing found at:  {video_render_path} ")
    