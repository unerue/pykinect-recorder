import ctypes
import numpy as np

from pykinect_azure.k4a._k4atypes import k4a_float3_t, k4a_float2_t


# K4A_DECLARE_HANDLE(k4abt_tracker_t);
class _handle_k4abt_tracker_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


k4abt_tracker_t = ctypes.POINTER(_handle_k4abt_tracker_t)


# K4A_DECLARE_HANDLE(k4abt_frame_t);
class _handle_k4abt_frame_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


k4abt_frame_t = ctypes.POINTER(_handle_k4abt_frame_t)

k4abt_result_t = ctypes.c_int
K4ABT_RESULT_SUCCEEDED = 0
K4ABT_RESULT_FAILED = 1

# class k4abt_joint_id_t(CtypeIntEnum):
K4ABT_JOINT_PELVIS = 0
K4ABT_JOINT_SPINE_NAVEL = 1
K4ABT_JOINT_SPINE_CHEST = 2
K4ABT_JOINT_NECK = 3
K4ABT_JOINT_CLAVICLE_LEFT = 4
K4ABT_JOINT_SHOULDER_LEFT = 5
K4ABT_JOINT_ELBOW_LEFT = 6
K4ABT_JOINT_WRIST_LEFT = 7
K4ABT_JOINT_HAND_LEFT = 8
K4ABT_JOINT_HANDTIP_LEFT = 9
K4ABT_JOINT_THUMB_LEFT = 10
K4ABT_JOINT_CLAVICLE_RIGHT = 11
K4ABT_JOINT_SHOULDER_RIGHT = 12
K4ABT_JOINT_ELBOW_RIGHT = 13
K4ABT_JOINT_WRIST_RIGHT = 14
K4ABT_JOINT_HAND_RIGHT = 15
K4ABT_JOINT_HANDTIP_RIGHT = 16
K4ABT_JOINT_THUMB_RIGHT = 17
K4ABT_JOINT_HIP_LEFT = 18
K4ABT_JOINT_KNEE_LEFT = 19
K4ABT_JOINT_ANKLE_LEFT = 20
K4ABT_JOINT_FOOT_LEFT = 21
K4ABT_JOINT_HIP_RIGHT = 22
K4ABT_JOINT_KNEE_RIGHT = 23
K4ABT_JOINT_ANKLE_RIGHT = 24
K4ABT_JOINT_FOOT_RIGHT = 25
K4ABT_JOINT_HEAD = 26
K4ABT_JOINT_NOSE = 27
K4ABT_JOINT_EYE_LEFT = 28
K4ABT_JOINT_EAR_LEFT = 29
K4ABT_JOINT_EYE_RIGHT = 30
K4ABT_JOINT_EAR_RIGHT = 31
K4ABT_JOINT_COUNT = 32

K4ABT_JOINT_NAMES = [
    "pelvis",
    "spine - navel",
    "spine - chest",
    "neck",
    "left clavicle",
    "left shoulder",
    "left elbow",
    "left wrist",
    "left hand",
    " left handtip",
    "left thumb",
    "right clavicle",
    "right shoulder",
    "right elbow",
    "right wrist",
    "right hand",
    "right handtip",
    "right thumb",
    "left hip",
    "left knee",
    "left ankle",
    "left foot",
    "right hip",
    "right knee",
    "right ankle",
    "right foot",
    "head",
    "nose",
    "left eye",
    "left ear",
    "right eye",
    "right ear",
]

K4ABT_SEGMENT_PAIRS = [
    [1, 0],
    [2, 1],
    [3, 2],
    [4, 2],
    [5, 4],
    [6, 5],
    [7, 6],
    [8, 7],
    [9, 8],
    [10, 7],
    [11, 2],
    [12, 11],
    [13, 12],
    [14, 13],
    [15, 14],
    [16, 15],
    [17, 14],
    [18, 0],
    [19, 18],
    [20, 19],
    [21, 20],
    [22, 0],
    [23, 22],
    [24, 23],
    [25, 24],
    [26, 3],
    [27, 26],
    [28, 26],
    [29, 26],
    [30, 26],
    [31, 26],
]

# class k4abt_sensor_orientation_t(CtypeIntEnum):
K4ABT_SENSOR_ORIENTATION_DEFAULT = 0
K4ABT_SENSOR_ORIENTATION_CLOCKWISE90 = 1
K4ABT_SENSOR_ORIENTATION_COUNTERCLOCKWISE90 = 2
K4ABT_SENSOR_ORIENTATION_FLIP180 = 3

# class k4abt_tracker_processing_mode_t(CtypeIntEnum):
K4ABT_TRACKER_PROCESSING_MODE_GPU = 0
K4ABT_TRACKER_PROCESSING_MODE_CPU = 1
K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA = 2
K4ABT_TRACKER_PROCESSING_MODE_GPU_TENSORRT = 3
K4ABT_TRACKER_PROCESSING_MODE_GPU_DIRECTML = 4


class _k4abt_tracker_configuration_t(ctypes.Structure):
    """
    Configuration parameters for a k4abt body tracker.

    Used by k4abt_tracker_create() to specify the configuration of the k4abt tracker.

    Attributes:
        sensor_orientation (c_int): The sensor mounting orientation type. Setting the correct
            orientation can help the body tracker to achieve more accurate body tracking results.
        processing_mode (c_int): Specify whether to use CPU only mode or GPU mode to run the tracker.
            The CPU only mode doesn't require the machine to have a GPU to run this SDK. But it will
            be much slower than the GPU mode.
        gpu_device_id (c_int32): Specify the GPU device ID to run the tracker. The setting is not
            effective if the processing_mode setting is set to K4ABT_TRACKER_PROCESSING_MODE_CPU.
            For K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA and K4ABT_TRACKER_PROCESSING_MODE_GPU_TENSORRT
            modes, ID of the graphic card can be retrieved using the CUDA API. In case when
            processing_mode is K4ABT_TRACKER_PROCESSING_MODE_GPU_DIRECTML, the device ID corresponds
            to the enumeration order of hardware adapters as given by IDXGIFactory::EnumAdapters.
            A device_id of 0 always corresponds to the default adapter, which is typically the primary
            display GPU installed on the system. More information can be found in the ONNX Runtime
            Documentation.
        model_path (c_char_p): Specify the model file name and location used by the tracker. If specified,
            the tracker will use this model instead of the default one.
    """

    _fields_ = [
        ("sensor_orientation", ctypes.c_int),
        ("processing_mode", ctypes.c_int),
        ("gpu_device_id", ctypes.c_int32),
        ("model_path", ctypes.c_char_p),
    ]


k4abt_tracker_configuration_t = _k4abt_tracker_configuration_t


class _wxyz(ctypes.Structure):
    """
    WXYZ or array representation of quaternion.

    Attributes:
        w (c_float): W representation of a quaternion.
        x (c_float): X representation of a quaternion.
        y (c_float): Y representation of a quaternion.
        z (c_float): Z representation of a quaternion.
    """

    _fields_ = [
        ("w", ctypes.c_float),
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]

    def __iter__(self):
        return {"w": self.w, "x": self.x, "y": self.y, "z": self.z}

    def __str__(self):
        return f"w:{self.w} x:{self.x} y:{self.y} z:{self.z}"


class k4a_quaternion_t(ctypes.Union):
    """
    Attributes:
        wxyz (_wxyz): W, X, Y, Z representation of a quaternion.
        v (c_float[4]): Array representation of a quaternion.
    """

    _fields_ = [("wxyz", _wxyz), ("v", ctypes.c_float * 4)]

    def __init__(self, q=(0, 0, 0, 0)):
        super().__init__()
        self.wxyz = _wxyz(q[0], q[1], q[2], q[3])

    def __iter__(self):
        wxyz = self.wxyz.__iter__()
        wxyz.update({"v": [v for v in self.v]})
        return wxyz

    def __str__(self):
        return self.wxyz.__str__()


# class k4abt_joint_confidence_level_t(CtypeIntEnum):
K4ABT_JOINT_CONFIDENCE_NONE = 0
K4ABT_JOINT_CONFIDENCE_LOW = 1
K4ABT_JOINT_CONFIDENCE_MEDIUM = 2
K4ABT_JOINT_CONFIDENCE_HIGH = 3
K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT = 4


class _k4abt_joint_t(ctypes.Structure):
    """
    Structure to define a single joint.

    The position and orientation together defines the coordinate system for the given joint.
    They are defined relative to the sensor global coordinate system.

    Attributes:
        position (k4a_float3_t): The position of the joint specified in millimeters.
        orientation (k4a_quaternion_t): The orientation of the joint specified in normalized quaternion.
        confidence_level (c_int): The confidence level of the joint.
    """

    _fields_ = [
        ("position", k4a_float3_t),
        ("orientation", k4a_quaternion_t),
        ("confidence_level", ctypes.c_int),
    ]

    def __init__(self, position=(0, 0, 0), orientation=(0, 0, 0, 0), confidence_level=0):
        super().__init__()
        self.position = k4a_float3_t(position)
        self.orientation = k4a_quaternion_t(orientation)
        self.confidence_level = confidence_level

    def __iter__(self):
        return {
            "position": self.position.__iter__(),
            "orientation": self.orientation.__iter__(),
            "confidence_level": self.confidence_level,
        }


k4abt_joint_t = _k4abt_joint_t


class k4abt_skeleton_t(ctypes.Structure):
    """
    Structure to define joints for skeleton.

    Attributes:
        joints (_k4abt_joint_t[K4ABT_JOINT_COUNT]): The joints for the body.
    """

    _fields_ = [
        ("joints", _k4abt_joint_t * K4ABT_JOINT_COUNT),
    ]

    def __init__(self, joints=(_k4abt_joint_t() for i in range(K4ABT_JOINT_COUNT))):
        super().__init__()
        self.joints = (_k4abt_joint_t * K4ABT_JOINT_COUNT)(*joints)

    def __iter__(self):
        return {"joints": [joint.__iter__() for joint in self.joints]}


class k4abt_body_t(ctypes.Structure):
    """
    Structure to define body.

    Attributes:
        id (c_uint32): An id for the body that can be used for frame-to-frame correlation.
        skeleton (k4abt_skeleton_t): The skeleton information for the body.
    """

    _fields_ = [
        ("id", ctypes.c_uint32),
        ("skeleton", k4abt_skeleton_t),
    ]

    def __init__(self, id=0, skeleton=k4abt_skeleton_t()):
        super().__init__()
        self.id = id
        self.skeleton = skeleton

    def __iter__(self):
        return {"id": self.id, "skeleton": self.skeleton.__iter__()}


class _k4abt_joint2D_t(ctypes.Structure):
    # https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.1.x/struct_microsoft_1_1_azure_1_1_kinect_1_1_body_tracking_1_1_joint.html
    _fields_ = [
        ("position", k4a_float2_t),
        ("confidence_level", ctypes.c_int),
    ]

    def __init__(self, position=(0, 0), confidence_level=0):
        super().__init__()
        self.position = k4a_float2_t(position)
        self.confidence_level = confidence_level

    def __iter__(self):
        return {
            "position": self.position.__iter__(),
            "confidence_level": self.confidence_level,
        }


k4abt_joint2D_t = _k4abt_joint2D_t


class k4abt_skeleton2D_t(ctypes.Structure):
    # https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.1.x/struct_microsoft_1_1_azure_1_1_kinect_1_1_body_tracking_1_1_skeleton.html
    _fields_ = [
        ("joints2D", _k4abt_joint2D_t * K4ABT_JOINT_COUNT),
    ]

    def __init__(self, joints=(_k4abt_joint2D_t() for i in range(K4ABT_JOINT_COUNT))):
        super().__init__()
        self.joints2D = (_k4abt_joint2D_t * K4ABT_JOINT_COUNT)(*joints)

    def __iter__(self):
        return {"joints2D": [joint.__iter__() for joint in self.joints2D]}


class k4abt_body2D_t(ctypes.Structure):
    # https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.1.x/struct_microsoft_1_1_azure_1_1_kinect_1_1_body_tracking_1_1_body.html
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("skeleton", k4abt_skeleton2D_t),
    ]

    def __init__(self, id=0, skeleton=k4abt_skeleton2D_t()):
        super().__init__()
        self.id = id
        self.skeleton = skeleton

    def __iter__(self):
        return {"id": self.id, "skeleton": self.skeleton.__iter__()}


K4ABT_BODY_INDEX_MAP_BACKGROUND = 255
K4ABT_INVALID_BODY_ID = 0xFFFFFFFF
K4ABT_DEFAULT_TRACKER_SMOOTHING_FACTOR = 0.0

K4ABT_DEFAULT_MODEL = 0
K4ABT_LITE_MODEL = 1

k4abt_tracker_default_configuration = k4abt_tracker_configuration_t()
k4abt_tracker_default_configuration.sensor_orientation = K4ABT_SENSOR_ORIENTATION_DEFAULT
k4abt_tracker_default_configuration.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_GPU
k4abt_tracker_default_configuration.gpu_device_id = 0

body_colors = np.ones((256, 3), dtype=np.uint8) * K4ABT_BODY_INDEX_MAP_BACKGROUND
body_colors[:7, :] = np.array(
    [
        [202, 183, 42],
        [42, 61, 202],
        [42, 202, 183],
        [202, 42, 61],
        [183, 42, 202],
        [42, 202, 61],
        [141, 202, 42],
    ]
)
