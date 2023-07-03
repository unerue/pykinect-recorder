import ctypes


# K4A_DECLARE_HANDLE(k4a_device_t);
class _handle_k4a_device_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


# handling device open/close/start/capture
k4a_device_t = ctypes.POINTER(_handle_k4a_device_t)


# K4A_DECLARE_HANDLE(k4a_capture_t);
class _handle_k4a_capture_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


# after capturing image by device.open(), handling captured image
k4a_capture_t = ctypes.POINTER(_handle_k4a_capture_t)


# K4A_DECLARE_HANDLE(k4a_image_t);
class _handle_k4a_image_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


# handling image's metadata (exposure, h, w, size, timestamp, ...)
k4a_image_t = ctypes.POINTER(_handle_k4a_image_t)


# K4A_DECLARE_HANDLE(k4a_transformation_t);
class _handle_k4a_transformation_t(ctypes.Structure):
    _fields_ = [
        ("_rsvd", ctypes.c_size_t),
    ]


# format transformation like color_to_depth, depth_to_pts
k4a_transformation_t = ctypes.POINTER(_handle_k4a_transformation_t)

# class k4a_result_t(CtypeIntEnum):
k4a_result_t = ctypes.c_int
K4A_RESULT_SUCCEEDED = 0
K4A_RESULT_FAILED = 1

# class k4a_buffer_result_t(CtypeIntEnum):
k4a_buffer_result_t = ctypes.c_int
K4A_BUFFER_RESULT_SUCCEEDED = 0
K4A_BUFFER_RESULT_FAILED = 1
K4A_BUFFER_RESULT_TOO_SMALL = 2

# class k4a_wait_result_t(CtypeIntEnum):
k4a_wait_result_t = ctypes.c_int
K4A_WAIT_RESULT_SUCCEEDED = 0
K4A_WAIT_RESULT_FAILED = 1
K4A_WAIT_RESULT_TIMEOUT = 2

# Debug message level
# class k4a_log_level_t(CtypeIntEnum):
k4a_log_level_t = ctypes.c_int
K4A_LOG_LEVEL_CRITICAL = 0
K4A_LOG_LEVEL_ERROR = 1
K4A_LOG_LEVEL_WARNING = 2
K4A_LOG_LEVEL_INFO = 3
K4A_LOG_LEVEL_TRACE = 4
K4A_LOG_LEVEL_OFF = 5

# class k4a_depth_mode_t(CtypeIntEnum):
k4a_depth_mode_t = ctypes.c_int
K4A_DEPTH_MODE_OFF = 0
K4A_DEPTH_MODE_NFOV_2X2BINNED = 1
K4A_DEPTH_MODE_NFOV_UNBINNED = 2
K4A_DEPTH_MODE_WFOV_2X2BINNED = 3
K4A_DEPTH_MODE_WFOV_UNBINNED = 4
K4A_DEPTH_MODE_PASSIVE_IR = 5

# class k4a_color_resolution_t(CtypeIntEnum):
k4a_color_resolution_t = ctypes.c_int
K4A_COLOR_RESOLUTION_OFF = 0
K4A_COLOR_RESOLUTION_720P = 1
K4A_COLOR_RESOLUTION_1080P = 2
K4A_COLOR_RESOLUTION_1440P = 3
K4A_COLOR_RESOLUTION_1536P = 4
K4A_COLOR_RESOLUTION_2160P = 5
K4A_COLOR_RESOLUTION_3072P = 6

# class k4a_image_format_t(CtypeIntEnum):
k4a_image_format_t = ctypes.c_int
K4A_IMAGE_FORMAT_COLOR_MJPG = 0
K4A_IMAGE_FORMAT_COLOR_NV12 = 1
K4A_IMAGE_FORMAT_COLOR_YUY2 = 2
K4A_IMAGE_FORMAT_COLOR_BGRA32 = 3
K4A_IMAGE_FORMAT_DEPTH16 = 4
K4A_IMAGE_FORMAT_IR16 = 5
K4A_IMAGE_FORMAT_CUSTOM8 = 6
K4A_IMAGE_FORMAT_CUSTOM16 = 7
K4A_IMAGE_FORMAT_CUSTOM = 8

# depth_image to color interpolation
# class k4a_transformation_interpolation_type_t(CtypeIntEnum):
k4a_transformation_interpolation_type_t = ctypes.c_int
K4A_TRANSFORMATION_INTERPOLATION_TYPE_NEAREST = 0
K4A_TRANSFORMATION_INTERPOLATION_TYPE_LINEAR = 1

# class k4a_fps_t(CtypeIntEnum):
k4a_fps_t = ctypes.c_int
K4A_FRAMES_PER_SECOND_5 = 0
K4A_FRAMES_PER_SECOND_15 = 1
K4A_FRAMES_PER_SECOND_30 = 2

# class k4a_color_control_command_t(CtypeIntEnum):
k4a_color_control_command_t = ctypes.c_int
K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE = 0
K4A_COLOR_CONTROL_AUTO_EXPOSURE_PRIORITY = 1
K4A_COLOR_CONTROL_BRIGHTNESS = 2
K4A_COLOR_CONTROL_CONTRAST = 3
K4A_COLOR_CONTROL_SATURATION = 4
K4A_COLOR_CONTROL_SHARPNESS = 5
K4A_COLOR_CONTROL_WHITEBALANCE = 6
K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION = 7
K4A_COLOR_CONTROL_GAIN = 8
K4A_COLOR_CONTROL_POWERLINE_FREQUENCY = 9

# class k4a_color_control_mode_t(CtypeIntEnum):
k4a_color_control_mode_t = ctypes.c_int
K4A_COLOR_CONTROL_MODE_AUTO = 0
K4A_COLOR_CONTROL_MODE_MANUAL = 1

# Using When record with two or more devices
# class k4a_wired_sync_mode_t(CtypeIntEnum):
k4a_wired_sync_mode_t = ctypes.c_int
K4A_WIRED_SYNC_MODE_STANDALONE = 0
K4A_WIRED_SYNC_MODE_MASTER = 1
K4A_WIRED_SYNC_MODE_SUBORDINATE = 2

# class k4a_calibration_type_t(CtypeIntEnum):
k4a_calibration_type_t = ctypes.c_int
K4A_CALIBRATION_TYPE_UNKNOWN = -1
K4A_CALIBRATION_TYPE_DEPTH = 0
K4A_CALIBRATION_TYPE_COLOR = 1
K4A_CALIBRATION_TYPE_GYRO = 2
K4A_CALIBRATION_TYPE_ACCEL = 3
K4A_CALIBRATION_TYPE_NUM = 4

# class k4a_calibration_model_type_t(CtypeIntEnum):
k4a_calibration_model_type_t = ctypes.c_int
K4A_CALIBRATION_LENS_DISTORTION_MODEL_UNKNOWN = 0
K4A_CALIBRATION_LENS_DISTORTION_MODEL_THETA = 1
K4A_CALIBRATION_LENS_DISTORTION_MODEL_POLYNOMIAL_3K = 2
K4A_CALIBRATION_LENS_DISTORTION_MODEL_RATIONAL_6KT = 3
K4A_CALIBRATION_LENS_DISTORTION_MODEL_BROWN_CONRADY = 4

# class k4a_firmware_build_t(CtypeIntEnum):
k4a_firmware_build_t = ctypes.c_int
K4A_FIRMWARE_BUILD_RELEASE = 0
K4A_FIRMWARE_BUILD_DEBUG = 1

# class k4a_firmware_signature_t(CtypeIntEnum):
k4a_firmware_signature_t = ctypes.c_int
K4A_FIRMWARE_SIGNATURE_MSFT = 0
K4A_FIRMWARE_SIGNATURE_TEST = 1
K4A_FIRMWARE_SIGNATURE_UNSIGNED = 2


# define K4A_SUCCEEDED(_result_) (_result_ == K4A_RESULT_SUCCEEDED)
def K4A_SUCCEEDED(result):
    return result == K4A_RESULT_SUCCEEDED


# define K4A_FAILED(_result_) (!K4A_SUCCEEDED(_result_))
def K4A_FAILED(result):
    return not K4A_SUCCEEDED(result)


# Callback Function
"""
typedef void(k4a_logging_message_cb_t)(
    void *context,
    k4a_log_level_t level,
    const char *file,
    const int line,
    const char *message
);

typedef void(k4a_memory_destroy_cb_t)(void *buffer, void *context);

typedef uint8_t *(k4a_memory_allocate_cb_t)(int size, void **context);
"""


class _k4a_device_configuration_t(ctypes.Structure):
    """
    Configuration parameters for an Azure Kinect device.

    Used by `k4a_device_start_cameras()` to specify the configuration of the data capture.

    Attributes:
        color_format (c_int): Image format to capture with the color camera. The color camera
            does not natively produce BGRA32 images. Setting `K4A_IMAGE_FORMAT_COLOR_BGRA32` for
            color_format will result in higher CPU utilization.
        color_resolution (c_int): Image resolution to capture with the color camera.
        depth_mode (c_int): Capture mode for the depth camera.
        camera_fps (c_int): Desired frame rate for the color and depth camera.
        synchronized_images_only (c_bool): Only produce `k4a_capture_t` objects if they contain
            synchronized color and depth images. This setting controls the behavior in which
            images are dropped when images are produced faster than they can be read,
            or if there are errors in reading images from the device. If set to true,
            `k4a_capture_t` objects will only be produced with both color and depth images.
            If set to false, `k4a_capture_t` objects may be produced only a single image
            when the corresponding image is dropped. Setting this to false ensures that
            the caller receives all of the images received from the camera, regardless of
            whether the corresponding images expected in the capture are available.
            If either the color or depth camera are disabled, this setting has no effect.
        depth_delay_off_color_usec (c_int32): Desired delay between the capture of the color image
            and the capture of the depth image. A negative value indicates that the depth image
            should be captured before the color image. Any value between negative and
            positive one capture period is valid.
        wired_sync_mode (c_int): The external synchronization mode.
        subordinate_delay_off_master_usec (c_uint32): The external synchronization timing. If this
            camera is a subordinate, this sets the capture delay between the color camera capture and the
            external input pulse. A setting of zero indicates that the master and subordinate color images
            should be aligned. This setting does not effect the 'Sync out' connection. This value must be
            positive and range from zero to one capture period. If this is not a subordinate, then this
            value is ignored.
        disable_streaming_indicator (c_bool): Streaming indicator automatically turns on when the color or
            depth camera's are in use. This setting disables that behavior and keeps the LED in an off state.
    """

    _fields_ = [
        ("color_format", ctypes.c_int),
        ("color_resolution", ctypes.c_int),
        ("depth_mode", ctypes.c_int),
        ("camera_fps", ctypes.c_int),
        ("synchronized_images_only", ctypes.c_bool),
        ("depth_delay_off_color_usec", ctypes.c_int32),
        ("wired_sync_mode", ctypes.c_int),
        ("subordinate_delay_off_master_usec", ctypes.c_uint32),
        ("disable_streaming_indicator", ctypes.c_bool),
    ]


k4a_device_configuration_t = _k4a_device_configuration_t


class _k4a_calibration_extrinsics_t(ctypes.Structure):
    """
    Extrinsic calibration data.

    Extrinsic calibration defines the physical relationship between two separate devices.

    Attributes:
        rotation (c_float[9]): 3x3 Rotation matrix stored in row major orde
        translation (c_float[3]): Translation vector, x,y,z (in millimeters)
    """

    _fields_ = [
        ("rotation", ctypes.c_float * 9),
        ("translation", ctypes.c_float * 3),
    ]


# rotation => 3x3(9) rotation, translation => Vector(x, y, z)
k4a_calibration_extrinsics_t = _k4a_calibration_extrinsics_t


class _param(ctypes.Structure):
    """
    Individual parameter or array representation of intrinsic model.

    Attributes:
        cx (c_float): Principal point in image, x.
        cy (c_float): Principal point in image, y.
        fx (c_float): Focal length x.
        fy (c_float): Focal length y.
        k1 (c_float): k1 radial distortion coefficient
        k2 (c_float): k2 radial distortion coefficient
        k3 (c_float): k3 radial distortion coefficient
        k4 (c_float): k4 radial distortion coefficient
        k5 (c_float): k5 radial distortion coefficient
        k6 (c_float): k6 radial distortion coefficient
        codx (c_float): Center of distortion in Z=1 plane, x (only used for Rational6KT)
        cody (c_float): Center of distortion in Z=1 plane, y (only used for Rational6KT)
        p2 (c_float): Tangential distortion coefficient 2.
        c1 (c_float): Tangential distortion coefficient 1.
        metric_radius (c_float): Metric radius.
    """

    _fields_ = [
        ("cx", ctypes.c_float),
        ("cy", ctypes.c_float),
        ("fx", ctypes.c_float),
        ("fy", ctypes.c_float),
        ("k1", ctypes.c_float),
        ("k2", ctypes.c_float),
        ("k3", ctypes.c_float),
        ("k4", ctypes.c_float),
        ("k5", ctypes.c_float),
        ("k6", ctypes.c_float),
        ("codx", ctypes.c_float),
        ("cody", ctypes.c_float),
        ("p2", ctypes.c_float),
        ("p1", ctypes.c_float),
        ("metric_radius", ctypes.c_float),
    ]


class _k4a_calibration_intrinsic_parameters_t(ctypes.Union):
    """
    Camera intrinsic calibration data.

    Attributes:
        param (_param): Individual parameter representation of intrinsic model.
        v (c_float[15]): Array representation of intrinsic model parameters.
    """

    _fields_ = [
        ("param", _param),
        ("v", ctypes.c_float * 15),
    ]


k4a_calibration_intrinsic_parameters_t = _k4a_calibration_intrinsic_parameters_t


class _k4a_calibration_intrinsics_t(ctypes.Structure):
    """
    Camera sensor intrinsic calibration data.

    Intrinsic calibration represents the internal optical properties of the camera.

    Azure Kinect devices are calibrated with Brown Conrady which is compatible with OpenCV.

    Attributes:
        type (c_int): Type of calibration model used.
        parameter_count (c_uint): Number of valid entries in parameters.
        parameters (k4a_calibration_intrinsic_parameters_t): Calibration parameters.
    """

    _fields_ = [
        ("type", ctypes.c_int),
        ("parameter_count", ctypes.c_uint),
        ("parameters", k4a_calibration_intrinsic_parameters_t),
    ]


# v => Parameter counts (_params)
k4a_calibration_intrinsics_t = _k4a_calibration_intrinsics_t


class _k4a_calibration_camera_t(ctypes.Structure):
    """
    Camera calibration contains intrinsic and extrinsic calibration information for a camera.

    Attributes:
        extrinsics (k4a_calibration_extrinsics_t): Extrinsic calibration data.
        intrinsics (k4a_calibration_intrinsics_t): Intrinsic calibration data.
        resolution_width (c_int): Resolution width of the calibration sensor.
        resolution_height (c_int): Resolution height of the calibration sensor.
        metric_radius (c_float): Max FOV of the camera.
    """

    _fields_ = [
        ("extrinsics", k4a_calibration_extrinsics_t),
        ("intrinsics", k4a_calibration_intrinsics_t),
        ("resolution_width", ctypes.c_int),
        ("resolution_height", ctypes.c_int),
        ("metric_radius", ctypes.c_float),
    ]


k4a_calibration_camera_t = _k4a_calibration_camera_t


# k4a_calibration_extrinsics_t[4][4] => 3D 변환을 가능하게 해줌.
class _k4a_calibration_t(ctypes.Structure):
    """
    Calibration type representing device calibration.

    Attributes:
        depth_camera_calibration (k4a_calibration_camera_t): Depth camera calibration.
        color_camera_calibration (k4a_calibration_camera_t): Color camera calibration.
        extrinsics (k4a_calibration_extrinsics_t[K4A_CALIBRATION_TYPE_NUM][K4A_CALIBRATION_TYPE_NUM]):
            Extrinsic transformation parameters. The extrinsic parameters allow 3D coordinate conversions
            between depth camera, color camera, the IMU's gyroscope and accelerometer.
            To transform from a source to a target 3D coordinate system, use the parameters stored
            under extrinsics[source][target].
        depth_mode (c_int): Depth camera mode for which calibration was obtained.
        color_resolution (c_int): Color camera resolution for which calibration was obtained.
    """

    _fields_ = [
        ("depth_camera_calibration", k4a_calibration_camera_t),
        ("color_camera_calibration", k4a_calibration_camera_t),
        (
            "extrinsics",
            (k4a_calibration_extrinsics_t * K4A_CALIBRATION_TYPE_NUM) * K4A_CALIBRATION_TYPE_NUM,
        ),
        ("depth_mode", ctypes.c_int),
        ("color_resolution", ctypes.c_int),
    ]


k4a_calibration_t = _k4a_calibration_t


class _k4a_version_t(ctypes.Structure):
    """
    Version information.

    Attributes:
        major (c_uint32): Major version; represents a breaking change.
        minor (c_uint32): Minor version; represents additional features,
            no regression from lower versions with same major version.
        iteration (c_uint32): Reserved.
    """

    _fields_ = [
        ("major", ctypes.c_uint32),
        ("minor", ctypes.c_uint32),
        ("iteration", ctypes.c_uint32),
    ]


k4a_version_t = _k4a_version_t


class _k4a_hardware_version_t(ctypes.Structure):
    """
    Structure to define hardware version.

    Attributes:
        rgb (k4a_version_t): Color camera firmware version.
        depth (k4a_version_t): Depth camera firmware version.
        audio (k4a_version_t): Audio device firmware version.
        depth_sensor (k4a_version_t): Depth sensor firmware version.
        firmware_build (c_int): Build type reported by the firmware.
        firmware_signature (c_int): Signature type of the firmware.
    """

    _fields_ = [
        ("rgb", k4a_version_t),
        ("depth", k4a_version_t),
        ("audio", k4a_version_t),
        ("depth_sensor", k4a_version_t),
        ("firmware_build", ctypes.c_int),
        ("firmware_signature", ctypes.c_int),
    ]


k4a_hardware_version_t = _k4a_hardware_version_t


class _xy(ctypes.Structure):
    """
    XY or array representation of vector.

    Attributes:
        x (c_float): X component of a vector.
        y (c_float): Y component of a vector.
    """

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
    ]

    def __iter__(self):
        return {"x": self.x, "y": self.y}

    def __str__(self):
        return str(self.__iter__())


# Two dimensional floating point vector
class _k4a_float2_t(ctypes.Union):
    """
    Two dimensional floating point vector.

    Attributes:
        xy (_xy): X, Y representation of a vector.
        v (c_float[2]): Array representation of a vector.
    """

    _fields_ = [("xy", _xy), ("v", ctypes.c_float * 2)]

    def __init__(self, v=(0, 0)):
        super().__init__()
        self.xy = _xy(v[0], v[1])

    def __iter__(self):
        xy = self.xy.__iter__()
        xy.update({"v": [v for v in self.v]})
        return xy

    def __str__(self):
        return self.xy.__str__()


k4a_float2_t = _k4a_float2_t


class _xyz(ctypes.Structure):
    """
    XYZ or array representation of vector.

    Attributes:
        x (c_float): X component of a vector.
        y (c_float): Y component of a vector.
        z (c_float): Z component of a vector.
    """

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]

    def __iter__(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    def __str__(self):
        return str(self.__iter__())


# Three dimensional floating point vector
class _k4a_float3_t(ctypes.Union):
    """
    Three dimensional floating point vector.

    Attributes:
        xyz (_xyz): X, Y, Z representation of a vector.
        v (c_float[3]): Array representation of a vector.
    """

    _fields_ = [("xyz", _xyz), ("v", ctypes.c_float * 3)]

    def __init__(self, v=(0, 0, 0)):
        super().__init__()
        self.xyz = _xyz(v[0], v[1], v[2])

    def __iter__(self):
        xyz = self.xyz.__iter__()
        xyz.update({"v": [v for v in self.v]})
        return xyz

    def __str__(self):
        return self.xyz.__str__()


k4a_float3_t = _k4a_float3_t


class _k4a_imu_sample_t(ctypes.Structure):
    """
    IMU sample.

    Attributes:
        temperature (c_float): Temperature reading of this sample (Celsius).
        acc_sample (k4a_float3_t): Accelerometer sample in meters per second squared.
        acc_timestamp_usec (c_uint64): Timestamp of the accelerometer in microseconds.
        gyro_sample (k4a_float3_t): Gyro sample in radians per second.
        gyro_timestamp_usec (c_uint64): Timestamp of the gyroscope in microseconds.
    """

    _fields_ = [
        ("temperature", ctypes.c_float),
        ("acc_sample", k4a_float3_t),
        ("acc_timestamp_usec", ctypes.c_uint64),
        ("gyro_sample", k4a_float3_t),
        ("gyro_timestamp_usec", ctypes.c_uint64),
    ]


k4a_imu_sample_t = _k4a_imu_sample_t


IMU_SAMPLE_SIZE = ctypes.sizeof(k4a_imu_sample_t)


K4A_DEVICE_DEFAULT = 0
K4A_WAIT_INFINITE = -1

color_command_dict = {
    "K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE": 0,
    "K4A_COLOR_CONTROL_AUTO_EXPOSURE_PRIORITY": 1,
    "K4A_COLOR_CONTROL_BRIGHTNESS": 2,
    "K4A_COLOR_CONTROL_CONTRAST": 3,
    "K4A_COLOR_CONTROL_SATURATION": 4,
    "K4A_COLOR_CONTROL_SHARPNESS": 5,
    "K4A_COLOR_CONTROL_WHITEBALANCE": 6,
    "K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION": 7,
    "K4A_COLOR_CONTROL_GAIN": 8,
    "K4A_COLOR_CONTROL_POWERLINE_FREQUENCY": 9,
}
