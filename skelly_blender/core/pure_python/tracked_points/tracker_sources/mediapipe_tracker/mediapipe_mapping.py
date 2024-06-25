from skelly_blender.core.pure_python.custom_types.base_enums import KeypointMappingsEnum
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints as bk
from skelly_blender.core.pure_python.tracked_points.tracker_sources.mediapipe_tracker.mediapipe_point_names import \
    MediapipeBodyPoints as mbp
_MEDIAPIPE_BODY_MAPPING = {
    bk.NOSE_TIP.name: [mbp.NOSE.lower()],
    bk.RIGHT_EYE_INNER.name: [mbp.RIGHT_EYE_INNER.lower()],
    bk.RIGHT_EYE_CENTER.name: [mbp.RIGHT_EYE.lower()],
    bk.RIGHT_EYE_OUTER.name: [mbp.RIGHT_EYE_OUTER.lower()],
    bk.RIGHT_ACOUSTIC_MEATUS.name: [mbp.RIGHT_EAR.lower()],
    bk.RIGHT_CANINE_TOOTH_TIP.name: [mbp.MOUTH_RIGHT.lower()],
    bk.LEFT_EYE_INNER.name: [mbp.LEFT_EYE_INNER.lower()],
    bk.LEFT_EYE_CENTER.name: [mbp.LEFT_EYE.lower()],
    bk.LEFT_EYE_OUTER.name: [mbp.LEFT_EYE_OUTER.lower()],
    bk.LEFT_ACOUSTIC_MEATUS.name: [mbp.LEFT_EAR.lower()],
    bk.LEFT_CANINE_TOOTH_TIP.name: [mbp.MOUTH_LEFT.lower()],
    bk.SKULL_ORIGIN_FORAMEN_MAGNUM.name: [mbp.LEFT_EAR.lower(),
                                          mbp.RIGHT_EAR.lower()],
    bk.SPINE_CERVICAL_TOP_C1_AXIS.name: {mbp.LEFT_EAR.lower(): .45,
                                         mbp.RIGHT_EAR.lower(): .45,
                                         mbp.LEFT_SHOULDER.lower(): .05,
                                         mbp.RIGHT_SHOULDER.lower(): .05},
    bk.SPINE_CERVICAL_ORIGIN_C7.name: {mbp.LEFT_EAR.lower(): .4,
                                       mbp.RIGHT_EAR.lower(): .4,
                                       mbp.LEFT_SHOULDER.lower(): .1,
                                       mbp.RIGHT_SHOULDER.lower(): .1},
    bk.SPINE_THORACIC_TOP_T1.name: [mbp.LEFT_SHOULDER.lower(),
                                    mbp.RIGHT_SHOULDER.lower()],
    bk.RIGHT_STERNOCLAVICLAR.name: {mbp.RIGHT_SHOULDER.lower(): .55,
                                    mbp.LEFT_SHOULDER.lower(): .45},
    bk.LEFT_STERNOCLAVICLAR.name: {mbp.RIGHT_SHOULDER.lower(): .45,
                                   mbp.LEFT_SHOULDER.lower(): .55},

    bk.SPINE_THORACIC_ORIGIN_T12.name: [mbp.LEFT_HIP.lower(),
                                        mbp.RIGHT_HIP.lower(),
                                        mbp.LEFT_SHOULDER.lower(),
                                        mbp.RIGHT_SHOULDER.lower()],
    bk.SPINE_LUMBAR_L1.name: {mbp.LEFT_HIP.lower(): .24,
                              mbp.RIGHT_HIP.lower(): .24,
                              mbp.LEFT_SHOULDER.lower(): .26,
                              mbp.RIGHT_SHOULDER.lower(): .26},
    bk.PELVIS_SPINE_SACRUM_ORIGIN.name: [mbp.LEFT_HIP.lower(),
                                         mbp.RIGHT_HIP.lower()],

    bk.RIGHT_SHOULDER.name: [mbp.RIGHT_SHOULDER.lower()],
    bk.RIGHT_ELBOW.name: [mbp.RIGHT_ELBOW.lower()],
    bk.RIGHT_WRIST.name: [mbp.RIGHT_WRIST.lower()],
    bk.RIGHT_INDEX_KNUCKLE.name: [mbp.RIGHT_INDEX.lower()],
    bk.RIGHT_PINKY_KNUCKLE.name: [mbp.RIGHT_PINKY.lower()],
    bk.RIGHT_THUMB_KNUCKLE.name: [mbp.RIGHT_THUMB.lower()],
    bk.PELVIS_RIGHT_HIP_ACETABULUM.name: [mbp.RIGHT_HIP.lower()],
    bk.RIGHT_KNEE.name: [mbp.RIGHT_KNEE.lower()],
    bk.RIGHT_ANKLE.name: [mbp.RIGHT_ANKLE.lower()],
    bk.RIGHT_HEEL.name: [mbp.RIGHT_HEEL.lower()],
    bk.RIGHT_HALLUX_TIP.name: [mbp.RIGHT_FOOT_INDEX.lower()],

    bk.LEFT_SHOULDER.name: [mbp.LEFT_SHOULDER.lower()],
    bk.LEFT_ELBOW.name: [mbp.LEFT_ELBOW.lower()],
    bk.LEFT_WRIST.name: [mbp.LEFT_WRIST.lower()],
    bk.LEFT_INDEX_KNUCKLE.name: [mbp.LEFT_INDEX.lower()],
    bk.LEFT_PINKY_KNUCKLE.name: [mbp.LEFT_PINKY.lower()],
    bk.LEFT_THUMB_KNUCKLE.name: [mbp.LEFT_THUMB.lower()],
    bk.PELVIS_LEFT_HIP_ACETABULUM.name: [mbp.LEFT_HIP.lower()],
    bk.LEFT_KNEE.name: [mbp.LEFT_KNEE.lower()],
    bk.LEFT_ANKLE.name: [mbp.LEFT_ANKLE.lower()],
    bk.LEFT_HEEL.name: [mbp.LEFT_HEEL.lower()],
    bk.LEFT_HALLUX_TIP.name: [mbp.LEFT_FOOT_INDEX.lower()],
}

MediapipeBodyMapping = KeypointMappingsEnum('MediapipeBodyMapping', _MEDIAPIPE_BODY_MAPPING)

if __name__ == "__main__":
    print(f"MediapipeBodyMapping enum created successfully with {len(MediapipeBodyMapping.__members__)} keys\n")
    print("\n".join([f"{key}: {value.value}" for key, value in MediapipeBodyMapping.__members__.items()]))
