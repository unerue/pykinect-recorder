import ctypes
import platform
import sys
import traceback

from pykinect_azure.k4abt._k4abtTypes import *
from pykinect_azure.k4a._k4atypes import k4a_calibration_t, k4a_capture_t, k4a_image_t

k4abt_dll = None


def setup_library(module_k4abt_path):
    global k4abt_dll

    try:
        k4abt_dll = ctypes.CDLL(module_k4abt_path)

    except Exception as e:
        print("Failed to load body tracker library", e)
        sys.exit(1)
    setup_onnx_provider()


def setup_onnx_provider():
    if platform.system() == "Windows":
        setup_onnx_provider_windows()
    elif platform.system() == "Linux":
        setup_onnx_provider_linux()


def setup_onnx_provider_linux():
    k4abt_tracker_default_configuration.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA
    try:
        ctypes.cdll.LoadLibrary("libonnxruntime_providers_cuda.so")
    except Exception as e:
        ctypes.cdll.LoadLibrary("libonnxruntime.so.1.10.0")


def setup_onnx_provider_windows():
    try:
        ctypes.cdll.LoadLibrary("C:/Program Files/Azure Kinect Body Tracking SDK/tools/directml.dll")
    except Exception as e:
        try:
            ctypes.cdll.LoadLibrary(
                "C:/Program Files/Azure Kinect Body Tracking SDK/sdk/windows-desktop/amd64/release/bin/onnxruntime_providers_cuda.dll"
            )
            k4abt_tracker_default_configuration.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_GPU_CUDA
        except Exception as e:
            k4abt_tracker_default_configuration.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_CPU


def k4abt_tracker_create(sensor_calibration, config, tracker_handle):
    """
    Create a body tracker handle.

    If successful, k4abt_tracker_create() will return a body tracker handle in the tracker parameter.
    This handle grants access to the body tracker and may be used in the other k4abt API calls.

    When done with body tracking, close the handle with k4abt_tracker_destroy().

    Only one tracker is allowed to exist at the same time in each process. If you call this API without
    destroying the previous tracker you created, the API call will fail.

    Args:
        sensor_calibration (POINTER(k4a_calibration_t)): The sensor calibration that will be used for capture processing.
        config (k4abt_tracker_configuration_t): The configuration we want to run the tracker in. This can be initialized
            with K4ABT_TRACKER_CONFIG_DEFAULT.
        tracker_handle (POINTER(k4abt_tracker_t)): Output parameter which on success will return a handle to the body tracker.

    Returns:
        c_int: K4A_RESULT_SUCCEEDED if the body tracker handle was created successfully.
    """
    _k4abt_tracker_create = k4abt_dll.k4abt_tracker_create
    _k4abt_tracker_create.restype = ctypes.c_int
    _k4abt_tracker_create.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        k4abt_tracker_configuration_t,
        ctypes.POINTER(k4abt_tracker_t),
    )

    return _k4abt_tracker_create(sensor_calibration, config, tracker_handle)


def k4abt_tracker_destroy(tracker_handle):
    """
    Releases a body tracker handle.

    Once released, the tracker_handle is no longer valid.

    Args:
        tracker_handle (k4abt_tracker_t): Handle obtained by k4abt_tracker_create().
    """
    # K4ABT_EXPORT void k4abt_tracker_destroy(k4abt_tracker_t tracker_handle);

    _k4abt_tracker_destroy = k4abt_dll.k4abt_tracker_destroy
    _k4abt_tracker_destroy.argtypes = (k4abt_tracker_t,)

    _k4abt_tracker_destroy(tracker_handle)


def k4abt_tracker_set_temporal_smoothing(tracker_handle, smoothing_factor):
    """
    Control the temporal smoothing across frames.

    The default smoothness value is defined as K4ABT_DEFAULT_TRACKER_SMOOTHING_FACTOR.

    Args:
        tracker_handle (k4abt_tracker_t): Handle obtained by k4abt_tracker_create().
        smoothing_factor (c_float): Set between 0 for no smoothing and 1 for full smoothing.
            Less smoothing will increase the responsiveness of the detected skeletons but will
            cause more positional and orientational jitters.
    """
    # K4ABT_EXPORT void k4abt_tracker_set_temporal_smoothing(k4abt_tracker_t tracker_handle, float smoothing_factor);

    _k4abt_tracker_set_temporal_smoothing = k4abt_dll.k4abt_tracker_set_temporal_smoothing
    _k4abt_tracker_set_temporal_smoothing.argtypes = (k4abt_tracker_t, ctypes.c_float)

    _k4abt_tracker_set_temporal_smoothing(tracker_handle, smoothing_factor)


def k4abt_tracker_enqueue_capture(tracker_handle, sensor_capture_handle, timeout_in_ms):
    """
    Add a k4a sensor capture to the tracker input queue to generate its body tracking result
    asynchronously.

    Add a k4a capture to the tracker input queue so that it can be processed asynchronously
    to generate the body tracking result. The processed results will be added to an output
    queue maintained by k4abt_tracker_t instance. Call k4abt_tracker_pop_result to get the
    result and pop it from the output queue. If the input queue or output queue is full,
    this function will block up until the timeout is reached. Once body_frame data is read,
    the user must call k4abt_frame_release() to return the allocated memory to the SDK.

    Upon successfully insert a sensor capture to the input queue this function will return success.

    This function returns K4A_WAIT_RESULT_FAILED when either the tracker is shut down by
    k4abt_tracker_shutdown() API, or an internal problem is encountered before adding to
    the input queue: such as low memory condition, sensor_capture_handle not containing
    the depth data, or other unexpected issues.

    Args:
        tracker_handle (k4abt_tracker_t): Handle obtained by k4abt_tracker_create().
        sensor_capture_handle (k4a_capture_t): Handle to a sensor capture returned by k4a_device_get_capture()
            from k4a SDK. It should contain the depth data for this function to work. Otherwise the function
            will return failure.
        timeout_in_ms (c_int32): Specifies the time in milliseconds the function should block waiting to add
            the sensor capture to the tracker process queue. 0 is a check of the status without blocking.
            Passing a value of K4A_WAIT_INFINITE will block indefinitely until the capture is added to the
            process queue.

    Returns:
        c_int: K4A_WAIT_RESULT_SUCCEEDED if a sensor capture is successfully added to the processing queue.
        If the queue is still full before the timeout elapses, the function will return K4A_WAIT_RESULT_TIMEOUT.
        All other failures will return K4A_WAIT_RESULT_FAILED.
    """

    _k4abt_tracker_enqueue_capture = k4abt_dll.k4abt_tracker_enqueue_capture
    _k4abt_tracker_enqueue_capture.restype = ctypes.c_int
    _k4abt_tracker_enqueue_capture.argtypes = (
        k4abt_tracker_t,
        k4a_capture_t,
        ctypes.c_int32,
    )

    return _k4abt_tracker_enqueue_capture(tracker_handle, sensor_capture_handle, timeout_in_ms)


def k4abt_tracker_pop_result(tracker_handle, body_frame_handle, timeout_in_ms):
    """
    Gets the next available body frame.

    Retrieves the next available body frame result and pop it from the output queue in the k4abt_tracker_t.
    If a new body frame is not currently available, this function will block up until the timeout is reached.
    The SDK will buffer at least three body frames worth of data before stopping new capture being queued
    by k4abt_tracker_enqueue_capture. Once body_frame data is read, the user must call k4abt_frame_release()
    to return the allocated memory to the SDK.

    Upon successfully reads a body frame this function will return success.

    This function returns K4A_WAIT_RESULT_FAILED when either the tracker is shut down by
    k4abt_tracker_shutdown() API and the remaining tracker queue is empty, or an internal problem is
    encountered: such as low memory condition, or other unexpected issues.

    Args:
        tracker_handle (k4abt_tracker_t): Handle obtained by k4abt_tracker_create().
        body_frame_handle (POINTER(k4abt_frame_t)): If successful this contains a handle to a body frame object.
            Caller must call k4abt_release_frame() when its done using this frame.
        timeout_in_ms (c_int32): Specifies the time in milliseconds the function should block waiting
            for the body frame. 0 is a check of the queue without blocking. Passing a value of
            K4A_WAIT_INFINITE will blocking indefinitely.

    Returns:
        c_int: K4A_WAIT_RESULT_SUCCEEDED if a body frame is returned. If a body frame is not available
            before the timeout elapses, the function will return K4A_WAIT_RESULT_TIMEOUT. All other
            failures will return K4A_WAIT_RESULT_FAILED.
    """

    _k4abt_tracker_pop_result = k4abt_dll.k4abt_tracker_pop_result
    _k4abt_tracker_pop_result.restype = ctypes.c_int
    _k4abt_tracker_pop_result.argtypes = (
        k4abt_tracker_t,
        ctypes.POINTER(k4abt_frame_t),
        ctypes.c_int32,
    )

    return _k4abt_tracker_pop_result(tracker_handle, body_frame_handle, timeout_in_ms)


def k4abt_tracker_shutdown(tracker_handle):
    """
    Shutdown the tracker so that no further capture can be added to the input queue.

    Once the tracker is shutdown, k4abt_tracker_enqueue_capture() API will always immediately return
    failure.

    If there are remaining catpures in the tracker queue after the tracker is shutdown,
    k4abt_tracker_pop_result() can still return successfully. Once the tracker queue is empty,
    the k4abt_tracker_pop_result() call will always immediately return failure.

    This function may be called while another thread is blocking in k4abt_tracker_enqueue_capture()
    or k4abt_tracker_pop_result(). Calling this function while another thread is in that function will
    result in that function returning a failure.

    Args:
        tracker_handle (k4abt_tracker_t): Handle obtained by k4abt_tracker_create().
    """
    # K4ABT_EXPORT void k4abt_tracker_shutdown(k4abt_tracker_t tracker_handle);

    _k4abt_tracker_shutdown = k4abt_dll.k4abt_tracker_shutdown
    _k4abt_tracker_shutdown.argtypes = (k4abt_tracker_t,)

    _k4abt_tracker_shutdown(tracker_handle)


def k4abt_frame_release(body_frame_handle):
    """
    Release a body frame back to the SDK.

    Called when the user is finished using the body frame.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object to return to SDK.
    """
    # K4ABT_EXPORT void k4abt_frame_release(k4abt_frame_t body_frame_handle);

    _k4abt_frame_release = k4abt_dll.k4abt_frame_release
    _k4abt_frame_release.argtypes = (k4abt_frame_t,)

    _k4abt_frame_release(body_frame_handle)


def k4abt_frame_reference(body_frame_handle):
    """
    Add a reference to a body frame.

    Call this function to add an additional reference to a body frame.
    This reference must be removed with k4abt_frame_release().

    This function is not thread-safe.

    Args:
        body_frame_handle (k4abt_frame_t): Body frame to add a reference to.
    """
    # K4ABT_EXPORT void k4abt_frame_reference(k4abt_frame_t body_frame_handle);

    _k4abt_frame_reference = k4abt_dll.k4abt_frame_reference
    _k4abt_frame_reference.argtypes = (k4abt_frame_t,)

    _k4abt_frame_reference(body_frame_handle)


def k4abt_frame_get_num_bodies(body_frame_handle):
    """
    Get the number of people from the k4abt_frame_t.

    Called when the user has received a body frame handle and wants to access the data contained in it.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
            k4abt_tracker_pop_result function.

    Returns:
        c_uint32: Returns the number of detected bodies. 0 if the function fails.
    """
    # K4ABT_EXPORT uint32_t k4abt_frame_get_num_bodies(k4abt_frame_t body_frame_handle);

    _k4abt_frame_get_num_bodies = k4abt_dll.k4abt_frame_get_num_bodies
    _k4abt_frame_get_num_bodies.restype = ctypes.c_uint32
    _k4abt_frame_get_num_bodies.argtypes = (k4abt_frame_t,)

    return _k4abt_frame_get_num_bodies(body_frame_handle)


def k4abt_frame_get_body_skeleton(body_frame_handle, index, skeleton):
    """
    Get the joint information for a particular person index from the k4abt_frame_t.

    Called when the user has received a body frame handle and wants to access the data contained in it.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
            k4abt_tracker_pop_result function.
        index (c_uint32): The index of the body of which the joint information is queried.
        skeleton (POINTER(k4abt_skeleton_t)): If successful this contains the body skeleton information.

    Returns:
        c_int: K4A_RESULT_SUCCEEDED if a valid body skeleton is returned. All failures will
            return K4A_RESULT_FAILED.
    """
    # K4ABT_EXPORT k4a_result_t k4abt_frame_get_body_skeleton(k4abt_frame_t body_frame_handle, uint32_t index, k4abt_skeleton_t* skeleton);

    _k4abt_frame_get_body_skeleton = k4abt_dll.k4abt_frame_get_body_skeleton
    _k4abt_frame_get_body_skeleton.restype = ctypes.c_int
    _k4abt_frame_get_body_skeleton.argtypes = (
        k4abt_frame_t,
        ctypes.c_uint32,
        ctypes.POINTER(k4abt_skeleton_t),
    )

    return _k4abt_frame_get_body_skeleton(body_frame_handle, index, skeleton)


def k4abt_frame_get_body_id(body_frame_handle, index):
    """
        Get the body id for a particular person index from the k4abt_frame_t.

        Called when the user has received a body frame handle and wants to access the id of the body
        given a particular index.

        Args:
            body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
                k4abt_tracker_pop_result function.
            index (c_uint32): The index of the body of which the body id information is queried.
    Returns

        Returns:
            c_uint32: Returns the body id. All failures will return K4ABT_INVALID_BODY_ID.
    """
    # K4ABT_EXPORT uint32_t k4abt_frame_get_body_id(k4abt_frame_t body_frame_handle, uint32_t index);

    _k4abt_frame_get_body_id = k4abt_dll.k4abt_frame_get_body_id
    _k4abt_frame_get_body_id.restype = ctypes.c_uint32
    _k4abt_frame_get_body_id.argtypes = (k4abt_frame_t, ctypes.c_uint32)

    return _k4abt_frame_get_body_id(body_frame_handle, index)


def k4abt_frame_get_device_timestamp_usec(body_frame_handle):
    """
    Get the body frame's device timestamp in microseconds.

    Called when the user has received a body frame handle and wants to access the data contained in it.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
            k4abt_tracker_pop_result function.

    Returns:
        c_uint64: Returns the device timestamp of the body frame. If the body_frame_handle is invalid
            this function will return 0. It is also possible for 0 to be a valid timestamp originating
            from the beginning of a recording or the start of streaming.
    """
    # K4ABT_EXPORT uint64_t k4abt_frame_get_device_timestamp_usec(k4abt_frame_t body_frame_handle);

    _k4abt_frame_get_device_timestamp_usec = k4abt_dll.k4abt_frame_get_device_timestamp_usec
    _k4abt_frame_get_device_timestamp_usec.restype = ctypes.c_uint64
    _k4abt_frame_get_device_timestamp_usec.argtypes = (k4abt_frame_t,)

    return _k4abt_frame_get_device_timestamp_usec(body_frame_handle)


def k4abt_frame_get_body_index_map(body_frame_handle):
    """
    Get the body index map from k4abt_frame_t.

    Called when the user has received a body frame handle and wants to access the data contained in it.

    Body Index map is the body instance segmentation map. Each pixel maps to the corresponding pixel
    in the depth image or the ir image. The value for each pixel represents which body the pixel belongs
    to. It can be either background (value K4ABT_BODY_INDEX_MAP_BACKGROUND) or the index of a detected
    k4abt_body_t.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
            k4abt_tracker_pop_result function.

    Returns:
        k4a_image_t: Call this function to access the body index map image. Release the image with
            k4a_image_release().
    """
    # K4ABT_EXPORT k4a_image_t k4abt_frame_get_body_index_map(k4abt_frame_t body_frame_handle);

    _k4abt_frame_get_body_index_map = k4abt_dll.k4abt_frame_get_body_index_map
    _k4abt_frame_get_body_index_map.restype = k4a_image_t
    _k4abt_frame_get_body_index_map.argtypes = (k4abt_frame_t,)

    return _k4abt_frame_get_body_index_map(body_frame_handle)


def k4abt_frame_get_capture(body_frame_handle):
    """
    Get the original capture that is used to calculate the k4abt_frame_t.

    Called when the user has received a body frame handle and wants to access the data contained in it.

    Args:
        body_frame_handle (k4abt_frame_t): Handle to a body frame object returned by
            k4abt_tracker_pop_result function.

    Returns:
        k4a_capture_t: Call this function to access the original k4a_capture_t. Release this capture with
            k4a_capture_release().
    """
    # K4ABT_EXPORT k4a_capture_t k4abt_frame_get_capture(k4abt_frame_t body_frame_handle);

    _k4abt_frame_get_capture = k4abt_dll.k4abt_frame_get_capture
    _k4abt_frame_get_capture.restype = k4a_capture_t
    _k4abt_frame_get_capture.argtypes = (k4abt_frame_t,)

    return _k4abt_frame_get_capture(body_frame_handle)


def VERIFY(result, error):
    if result != K4ABT_RESULT_SUCCEEDED:
        print(error)
        traceback.print_stack()
        sys.exit(1)
