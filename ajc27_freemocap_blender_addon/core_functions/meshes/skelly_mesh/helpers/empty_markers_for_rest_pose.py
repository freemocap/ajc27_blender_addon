# TODO: merge with a main empty information dictionary
_EMPTY_MARKERS = {
    'hips_center': {
        "bone": 'pelvis',
        "at_head": True,
    },
    'trunk_center': {
        "bone": 'spine.001',
        "at_head": True,
    },
    'neck_center': {
        "bone": 'neck',
        "at_head": True,
    },
    'head_center': {
        "bone": 'face',
        "at_head": True,
    },
    'nose': {
        "bone": 'face',
        "at_head": False,
    },
    'right_shoulder': {
        "bone": 'upper_arm.R',
        "at_head": True,
    },
    'left_shoulder': {
        "bone": 'upper_arm.L',
        "at_head": True,
    },
    'right_elbow': {
        "bone": 'forearm.R',
        "at_head": True,
    },
    'left_elbow': {
        "bone": 'forearm.L',
        "at_head": True,
    },
    'right_wrist': {
        "bone": 'hand.R',
        "at_head": True,
    },
    'left_wrist': {
        "bone": 'hand.L',
        "at_head": True,
    },
    'right_hand_wrist': {
        "bone": 'hand.R',
        "at_head": True,
    },
    'left_hand_wrist': {
        "bone": 'hand.L',
        "at_head": True,
    },
    'right_hand_thumb_cmc': {
        "bone": 'thumb.01.R',
        "at_head": True,
    },
    'left_hand_thumb_cmc': {
        "bone": 'thumb.01.L',
        "at_head": True,
    },
    'right_hand_index_finger_mcp': {
        "bone": 'f_index.01.R',
        "at_head": True,
    },
    'left_hand_index_finger_mcp': {
        "bone": 'f_index.01.L',
        "at_head": True,
    },
    'right_hand_middle_finger_mcp': {
        "bone": 'f_middle.01.R',
        "at_head": True,
    },
    'left_hand_middle_finger_mcp': {
        "bone": 'f_middle.01.L',
        "at_head": True,
    },
    'right_hand_ring_finger_mcp': {
        "bone": 'f_ring.01.R',
        "at_head": True,
    },
    'left_hand_ring_finger_mcp': {
        "bone": 'f_ring.01.L',
        "at_head": True,
    },
    'right_hand_pinky_mcp': {
        "bone": 'f_pinky.01.R',
        "at_head": True,
    },
    'left_hand_pinky_mcp': {
        "bone": 'f_pinky.01.L',
        "at_head": True,
    },
    'right_hand_thumb_mcp': {
        "bone": 'thumb.02.R',
        "at_head": True,
    },
    'left_hand_thumb_mcp': {
        "bone": 'thumb.02.L',
        "at_head": True,
    },
    'right_hand_index_finger_pip': {
        "bone": 'f_index.02.R',
        "at_head": True,
    },
    'left_hand_index_finger_pip': {
        "bone": 'f_index.02.L',
        "at_head": True,
    },
    'right_hand_middle_finger_pip': {
        "bone": 'f_middle.02.R',
        "at_head": True,
    },
    'left_hand_middle_finger_pip': {
        "bone": 'f_middle.02.L',
        "at_head": True,
    },
    'right_hand_ring_finger_pip': {
        "bone": 'f_ring.02.R',
        "at_head": True,
    },
    'left_hand_ring_finger_pip': {
        "bone": 'f_ring.02.L',
        "at_head": True,
    },
    'right_hand_pinky_pip': {
        "bone": 'f_pinky.02.R',
        "at_head": True,
    },
    'left_hand_pinky_pip': {
        "bone": 'f_pinky.02.L',
        "at_head": True,
    },
    'right_hand_thumb_ip': {
        "bone": 'thumb.03.R',
        "at_head": True,
    },
    'left_hand_thumb_ip': {
        "bone": 'thumb.03.L',
        "at_head": True,
    },
    'right_hand_index_finger_dip': {
        "bone": 'f_index.03.R',
        "at_head": True,
    },
    'left_hand_index_finger_dip': {
        "bone": 'f_index.03.L',
        "at_head": True,
    },
    'right_hand_middle_finger_dip': {
        "bone": 'f_middle.03.R',
        "at_head": True,
    },
    'left_hand_middle_finger_dip': {
        "bone": 'f_middle.03.L',
        "at_head": True,
    },
    'right_hand_ring_finger_dip': {
        "bone": 'f_ring.03.R',
        "at_head": True,
    },
    'left_hand_ring_finger_dip': {
        "bone": 'f_ring.03.L',
        "at_head": True,
    },
    'right_hand_pinky_dip': {
        "bone": 'f_pinky.03.R',
        "at_head": True,
    },
    'left_hand_pinky_dip': {
        "bone": 'f_pinky.03.L',
        "at_head": True,
    },
    'right_hand_thumb_tip': {
        "bone": 'thumb.03.R',
        "at_head": False,
    },
    'left_hand_thumb_tip': {
        "bone": 'thumb.03.L',
        "at_head": False,
    },
    'right_hand_index_finger_tip': {
        "bone": 'f_index.03.R',
        "at_head": False,
    },
    'left_hand_index_finger_tip': {
        "bone": 'f_index.03.L',
        "at_head": False,
    },
    'right_hand_middle_finger_tip': {
        "bone": 'f_middle.03.R',
        "at_head": False,
    },
    'left_hand_middle_finger_tip': {
        "bone": 'f_middle.03.L',
        "at_head": False,
    },
    'right_hand_ring_finger_tip': {
        "bone": 'f_ring.03.R',
        "at_head": False,
    },
    'left_hand_ring_finger_tip': {
        "bone": 'f_ring.03.L',
        "at_head": False,
    },
    'right_hand_pinky_tip': {
        "bone": 'f_pinky.03.R',
        "at_head": False,
    },
    'left_hand_pinky_tip': {
        "bone": 'f_pinky.03.L',
        "at_head": False,
    },
    'right_hip': {
        "bone": 'thigh.R',
        "at_head": True,
    },
    'left_hip': {
        "bone": 'thigh.L',
        "at_head": True,
    },
    'right_knee': {
        "bone": 'shin.R',
        "at_head": True,
    },
    'left_knee': {
        "bone": 'shin.L',
        "at_head": True,
    },
    'right_ankle': {
        "bone": 'foot.R',
        "at_head": True,
    },
    'left_ankle': {
        "bone": 'foot.L',
        "at_head": True,
    },
    'right_foot_index': {
        "bone": 'foot.R',
        "at_head": False,
    },
    'left_foot_index': {
        "bone": 'foot.L',
        "at_head": False,
    },
    'right_heel': {
        "bone": 'heel.02.R',
        "at_head": False,
    },
    'left_heel': {
        "bone": 'heel.02.L',
        "at_head": False,
    }
}
