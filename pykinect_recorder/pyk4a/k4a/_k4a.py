# -*- coding: utf-8 -*-

import ctypes
import sys
import traceback
from ._k4atypes import *

k4a_dll = None


def setup_library(module_k4a_path):
    global k4a_dll

    try:
        k4a_dll = ctypes.CDLL(module_k4a_path)

    except Exception as e:
        print("Failed to load library", e)
        sys.exit(1)


# ?
def k4a_device_get_installed_count() -> ctypes.c_uint32:
    """
    Gets the number of connected devices.

    This API counts the number of Azure Kinect devices connected to the host PC.

    Returns:
        c_uint32: Number of sensors connected to the PC.
    """
    return k4a_dll.k4a_device_get_installed_count()


def k4a_device_open(device_id: ctypes.c_uint32, device_handle: ctypes.POINTER(k4a_device_t)) -> ctypes.c_int:
    """
    Open an Azure Kinect device.

    If successful, `k4a_device_open()` will return a device handle in the device_handle parameter.
    This handle grants exclusive access to the device and may be used in the other Azure Kinect API calls.

    When done with the device, close the handle with `k4a_device_close()`.

    Args:
        device_id (c_uint32): The index of the device to open, starting with 0.
            Optionally pass in `K4A_DEVICE_DEFAULT`.
        device_handle (POINTER(k4a_device_t)): Output parameter which on success will return a handle to the device.

    Returns:
        c_int: `K4A_RESULT_SUCCEEDED` if the device was opened successfully.
    """
    _k4a_device_open = k4a_dll.k4a_device_open
    _k4a_device_open.restype = ctypes.c_int
    _k4a_device_open.argtypes = (ctypes.c_uint32, ctypes.POINTER(k4a_device_t))

    return _k4a_device_open(device_id, device_handle)


def k4a_device_close(device_handle: k4a_device_t) -> None:
    """
    Closes an Azure Kinect device.

    Once closed, the handle is no longer valid.

    Before closing the handle to the device, ensure that all `k4a_capture_t` captures have been
    released with `k4a_capture_release()`.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
    """
    _k4a_device_close = k4a_dll.k4a_device_close
    _k4a_device_close.restype = None
    _k4a_device_close.argtypes = (k4a_device_t,)
    _k4a_device_close(device_handle)


def k4a_device_get_capture(
    device_handle: k4a_device_t, capture_handle: ctypes.POINTER(k4a_capture_t), timeout: ctypes.c_int32
) -> ctypes.c_int:
    """
    Reads a sensor capture.

    Gets the next capture in the streamed sequence of captures from the camera. If a new capture
    is not currently available, this function will block until the timeout is reached. The SDK
    will buffer at least two captures worth of data before dropping the oldest capture. Callers
    needing to capture all data need to ensure they read the data as fast as the data is being
    produced on average.

    Upon successfully reading a capture this function will return success and populate capture.
    If a capture is not available in the configured `timeout_in_ms`, then the API will return
    `K4A_WAIT_RESULT_TIMEOUT`.

    If the call is successful and a capture is returned, callers must call `k4a_capture_release()`
    to return the allocated memory.

    This function needs to be called while the device is in a running state; after
    `k4a_device_start_cameras()` is called and before `k4a_device_stop_cameras()` is called.

    This function returns an error when an internal problem is encountered; such as loss of the
    USB connection, inability to allocate enough memory, and other unexpected issues. Any error
    returned by this function signals the end of streaming data, and caller should stop the stream
    using `k4a_device_stop_cameras()`.

    If this function is waiting for data (non-zero timeout) when `k4a_device_stop_cameras()` or
    `k4a_device_close()` is called on another thread, this function will return an error.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        capture_handle (POINTER(k4a_capture_t)): If successful this contains a handle to a capture object.
            Caller must call `k4a_capture_release()` when its done using this capture.
        timeout (c_int32): Specifies the time in milliseconds the function should block waiting
            for the capture. If set to 0, the function will return without blocking. Passing a
            value of `K4A_WAIT_INFINITE` will block indefinitely until data is available, the
            device is disconnected, or another error occurs.

    Returns:
        c_int: `K4A_WAIT_RESULT_SUCCEEDED` if a capture is returned. If a capture is not available
            before the timeout elapses, the function will return `K4A_WAIT_RESULT_TIMEOUT`. All other
            failures will return `K4A_WAIT_RESULT_FAILED`.
    """
    _k4a_device_get_capture = k4a_dll.k4a_device_get_capture
    _k4a_device_get_capture.restype = ctypes.c_int
    _k4a_device_get_capture.argtypes = (
        k4a_device_t,
        ctypes.POINTER(k4a_capture_t),
        ctypes.c_int32,
    )

    return _k4a_device_get_capture(device_handle, capture_handle, timeout)


def k4a_device_get_imu_sample(
    device_handle: k4a_device_t, imu_sample_handle: ctypes.POINTER(k4a_imu_sample_t), timeout: ctypes.c_int32
) -> ctypes.c_int:
    """
    Reads an IMU sample.

    Gets the next sample in the streamed sequence of IMU samples from the device. If a new sample
    is not currently available, this function will block until the timeout is reached. The API will
    buffer at least two camera capture intervals worth of samples before dropping the oldest sample.
    Callers needing to capture all data need to ensure they read the data as fast as the data is being
    produced on average.

    Upon successfully reading a sample this function will return success and populate `imu_sample`.
    If a sample is not available in the configured `timeout_in_ms`, then the API will return
    `K4A_WAIT_RESULT_TIMEOUT`.

    This function needs to be called while the device is in a running state; after `k4a_device_start_imu()`
    is called and before `k4a_device_stop_imu()` is called.

    This function returns an error when an internal problem is encountered; such as loss of the USB
    connection, inability to allocate enough memory, and other unexpected issues. Any error returned
    by this function signals the end of streaming data, and caller should stop the stream using
    `k4a_device_stop_imu()`.

    If this function is waiting for data (non-zero timeout) when `k4a_device_stop_imu()` or
    `k4a_device_close()` is called on another thread, this function will return an error.

    The memory the IMU sample is written to is allocated and owned by the caller, so there is no need
    to call an Azure Kinect API to free or release the sample.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        imu_sample_handle (POINTER(k4a_imu_sample_t)): Pointer to the location for the API to write the IMU sample.
        timeout (c_int32): Specifies the time in milliseconds the function should block waiting for
            the sample. If set to 0, the function will return without blocking. Passing a value of
            `K4A_WAIT_INFINITE` will block indefinitely until data is available, the device is
            disconnected, or another error occurs.

    Returns:
        c_int: `K4A_WAIT_RESULT_SUCCEEDED` if a sample is returned. If a sample is not available
            before the timeout elapses, the function will return `K4A_WAIT_RESULT_TIMEOUT`.
            All other failures will return `K4A_WAIT_RESULT_FAILED`.
    """
    _k4a_device_get_imu_sample = k4a_dll.k4a_device_get_imu_sample
    _k4a_device_get_imu_sample.restype = ctypes.c_int
    _k4a_device_get_imu_sample.argtypes = (
        k4a_device_t,
        ctypes.POINTER(k4a_imu_sample_t),
        ctypes.c_int32,
    )

    return _k4a_device_get_imu_sample(device_handle, imu_sample_handle, timeout)


def k4a_capture_create(capture_handle: ctypes.POINTER(k4a_capture_t)) -> k4a_result_t:
    """
    Create an empty capture object.

    Call this function to create a `k4a_capture_t` handle for a new capture.
    Release it with `k4a_capture_release()`.

    The new capture is created with a reference count of 1.

    Args:
        capture_handle (POINTER(k4a_capture_t)): Pointer to a location to store the handle.

    Returns:
        k4a_result_t: Returns `K4A_RESULT_SUCCEEDED` on success. Errors are indicated with
            `K4A_RESULT_FAILED` and error specific data can be found in the log.
    """
    _k4a_capture_create = k4a_dll.k4a_capture_create
    _k4a_capture_create.restype = k4a_result_t
    _k4a_capture_create.argtypes = (ctypes.POINTER(k4a_capture_t),)

    return _k4a_capture_create(capture_handle)


def k4a_capture_release(capture_handle: k4a_capture_t) -> None:
    """
    Release a capture.

    Call this function when finished using the capture.

    Args:
        capture_handle (k4a_capture_t): Capture to release.
    """
    _k4a_capture_release = k4a_dll.k4a_capture_release
    _k4a_capture_release.restype = None
    _k4a_capture_release.argtypes = (k4a_capture_t,)

    _k4a_capture_release(capture_handle)


def k4a_capture_reference(capture_handle: k4a_capture_t) -> None:
    """
    Add a reference to a capture.

    Call this function to add an additional reference to a capture.
    This reference must be removed with `k4a_capture_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture to add a reference to.
    """
    _k4a_capture_reference = k4a_dll.k4a_capture_reference
    _k4a_capture_reference.restype = None
    _k4a_capture_reference.argtypes = (k4a_capture_t,)

    _k4a_capture_reference(capture_handle)


def k4a_capture_get_color_image(capture_handle: k4a_capture_t) -> k4a_image_t:
    """
    Get the color image associated with the given capture.

    Call this function to access the color image part of this capture.
    Release the `k4a_image_t` with `k4a_image_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture handle containing the image.

    Returns:
        k4a_image_t
    """
    _k4a_capture_get_color_image = k4a_dll.k4a_capture_get_color_image
    _k4a_capture_get_color_image.restype = k4a_image_t
    _k4a_capture_get_color_image.argtypes = (k4a_capture_t,)

    return _k4a_capture_get_color_image(capture_handle)


def k4a_capture_get_depth_image(capture_handle: k4a_capture_t) -> k4a_image_t:
    """
    Get the depth image associated with the given capture.

    Call this function to access the depth image part of this capture.
    Release the `k4a_image_t` with `k4a_image_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture handle containing the image.

    Returns:
        k4a_image_t
    """
    _k4a_capture_get_depth_image = k4a_dll.k4a_capture_get_depth_image
    _k4a_capture_get_depth_image.restype = k4a_image_t
    _k4a_capture_get_depth_image.argtypes = (k4a_capture_t,)

    return _k4a_capture_get_depth_image(capture_handle)


def k4a_capture_get_ir_image(capture_handle: k4a_capture_t) -> k4a_image_t:
    """
    Get the IR image associated with the given capture.

    Call this function to access the IR image part of this capture.
    Release the `k4a_image_t` with `k4a_image_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture handle containing the image.

    Returns:
        k4a_image_t
    """
    _k4a_capture_get_ir_image = k4a_dll.k4a_capture_get_ir_image
    _k4a_capture_get_ir_image.restype = k4a_image_t
    _k4a_capture_get_ir_image.argtypes = (k4a_capture_t,)

    return _k4a_capture_get_ir_image(capture_handle)


def k4a_capture_set_color_image(capture_handle: k4a_capture_t, image_handle: k4a_image_t) -> None:
    """
    Set or add a color image to the associated capture.

    When a `k4a_image_t` is added to a `k4a_capture_t`, the `k4a_capture_t` will automatically add a
    reference to the `k4a_image_t`.

    If there is already a color image contained in the capture, the existing image will be
    dereferenced and replaced with the new image.

    To remove a color image to the capture without adding a new image, this function can be
    called with a NULL `image_handle`.

    Any `k4a_image_t` contained in this `k4a_capture_t` will automatically be dereferenced when
    all references to the `k4a_capture_t` are released with `k4a_capture_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture handle to hold the image.
        image_handle (k4a_image_t): Image handle containing the image.
    """
    _k4a_capture_set_color_image = k4a_dll.k4a_capture_set_color_image
    _k4a_capture_set_color_image.restype = None
    _k4a_capture_set_color_image.argtypes = (
        k4a_capture_t,
        k4a_image_t,
    )

    _k4a_capture_set_color_image(capture_handle, image_handle)


def k4a_capture_set_depth_image(capture_handle: k4a_capture_t, image_handle: k4a_image_t) -> None:
    """
    Set or add a depth image to the associated capture.

    When a `k4a_image_t` is added to a `k4a_capture_t`, the `k4a_capture_t` will automatically add a
    reference to the `k4a_image_t`.

    If there is already an image depth image contained in the capture, the existing image will
    be dereferenced and replaced with the new image.

    To remove a depth image to the capture without adding a new image, this function can be called
    with a NULL `image_handle`.

    Any `k4a_image_t` contained in this `k4a_capture_t` will automatically be dereferenced when all
    references to the `k4a_capture_t` are released with `k4a_capture_release()`.

    Args:
        capture_handle (k4a_capture_t): Capture handle to hold the image.
        image_handle (k4a_image_t): Image handle containing the image.
    """
    _k4a_capture_set_depth_image = k4a_dll.k4a_capture_set_depth_image
    _k4a_capture_set_depth_image.restype = None
    _k4a_capture_set_depth_image.argtypes = (
        k4a_capture_t,
        k4a_image_t,
    )

    _k4a_capture_set_depth_image(capture_handle, image_handle)


def k4a_capture_set_ir_image(capture_handle: k4a_capture_t, image_handle: k4a_image_t) -> None:
    """
    Set or add an IR image to the associated capture.

    When a `k4a_image_t` is added to a `k4a_capture_t`, the `k4a_capture_t` will automatically add a
    reference to the `k4a_image_t`.

    If there is already an IR image contained in the capture, the existing image will be dereferenced
    and replaced with the new image.

    To remove a IR image to the capture without adding a new image, this function can be called with
    a NULL `image_handle`.

    Any `k4a_image_t` contained in this `k4a_capture_t` will automatically be dereferenced when all
    references to the `k4a_capture_t` are released with k4a_capture_release().

    Args:
        capture_handle (k4a_capture_t): Capture handle to hold the image.
        image_handle (k4a_image_t): Image handle containing the image.
    """
    _k4a_capture_set_ir_image = k4a_dll.k4a_capture_set_ir_image
    _k4a_capture_set_ir_image.restype = None
    _k4a_capture_set_ir_image.argtypes = (
        k4a_capture_t,
        k4a_image_t,
    )

    _k4a_capture_set_ir_image(capture_handle, image_handle)


def k4a_capture_set_temperature_c(capture_handle: k4a_capture_t, temperature: ctypes.c_float) -> None:
    """
    Set the temperature associated with the capture.

    Args:
        capture_handle (k4a_capture_t): Capture handle to set the temperature on.
        temperature (c_float): Temperature in Celsius to store.
    """
    # K4A_EXPORT void k4a_capture_set_temperature_c(k4a_capture_t capture_handle, float temperature_c);

    _k4a_capture_set_temperature_c = k4a_dll.k4a_capture_set_temperature_c
    _k4a_capture_set_temperature_c.restype = None
    _k4a_capture_set_temperature_c.argtypes = (
        k4a_capture_t,
        ctypes.c_float,
    )

    _k4a_capture_set_temperature_c(capture_handle, temperature)


def k4a_capture_get_temperature_c(capture_handle: k4a_capture_t) -> ctypes.c_float:
    """
    Get the temperature associated with the capture.

    Args:
        capture_handle (k4a_capture_t): Capture handle to retrieve the temperature from.

    Returns:
        c_float: This function returns the temperature of the device at the time of the capture in
            Celsius. If the temperature is unavailable, the function will return NAN.
    """
    # K4A_EXPORT float k4a_capture_get_temperature_c(k4a_capture_t capture_handle);

    _k4a_capture_get_temperature_c = k4a_dll.k4a_capture_get_temperature_c
    _k4a_capture_get_temperature_c.restype = ctypes.c_float
    _k4a_capture_get_temperature_c.argtypes = (k4a_capture_t,)

    return _k4a_capture_get_temperature_c(capture_handle)


def k4a_image_create(
    image_format: k4a_image_format_t,
    width: ctypes.c_int,
    height: ctypes.c_int,
    stride: ctypes.c_int,
    image_handle: ctypes.POINTER(k4a_image_t),
) -> k4a_result_t:
    """
    Create an image.

    This function is used to create images of formats that have consistent stride. The function
    is not suitable for compressed formats that may not be represented by the same number of
    bytes per line.

    For most image formats, the function will allocate an image buffer of size `height_pixels` * `stride_bytes`.
    Buffers `K4A_IMAGE_FORMAT_COLOR_NV12` format will allocate an additional `height_pixels` / 2 set of lines
    (each of `stride_bytes`). This function cannot be used to allocate `K4A_IMAGE_FORMAT_COLOR_MJPG` buffers.

    To create an image object without the API allocating memory, or to represent an image that has a
    non-deterministic stride, use `k4a_image_create_from_buffer()`.

    The `k4a_image_t` is created with a reference count of 1.

    When finished using the created image, release it with `k4a_image_release`.

    Args:
        image_format (k4a_image_format_t): The format of the image that will be stored in this image container.
        width (c_int): Width in pixels.
        height (c_int): Height in pixels.
        stride (c_int): The number of bytes per horizontal line of the image. If set to 0, the stride
            will be set to the minimum size given the `format` and `width_pixels`.
        image_handle (POINTER(k4a_image_t)): Pointer to store image handle in.

    Returns:
        k4a_result_t: Returns `K4A_RESULT_SUCCEEDED` on success. Errors are indicated with `K4A_RESULT_FAILED`.
    """
    _k4a_image_create = k4a_dll.k4a_image_create
    _k4a_image_create.restype = k4a_result_t
    _k4a_image_create.argtypes = (
        k4a_image_format_t,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(k4a_image_t),
    )

    return _k4a_image_create(image_format, width, height, stride, image_handle)


def k4a_image_create_from_buffer(
    image_format: k4a_image_format_t,
    width: ctypes.c_int,
    height: ctypes.c_int,
    stride: ctypes.c_int,
    buffer: ctypes.POINTER(ctypes.c_uint8),
    buffer_size: ctypes.c_size_t,
    buffer_release_cb: ctypes.c_void_p,
    buffer_release_cb_context: ctypes.c_void_p,
    image_handle: ctypes.POINTER(k4a_image_t),
) -> k4a_result_t:
    """
    Create an image from a pre-allocated buffer.

    This function creates a `k4a_image_t` from a pre-allocated buffer. When all references to this
    object reach zero the provided `buffer_release_cb` callback function is called so that the memory
    can be released. If this function fails, the API will not use the memory provided in buffer,
    and the API will not call `buffer_release_cb`.

    The `k4a_image_t` is created with a reference count of 1.

    Release the reference on this function with `k4a_image_release()`.

    Args:
        image_format (k4a_image_format_t): The format of the image that will be stored in this image
            container.
        width (c_int): Width in pixels.
        height (c_int): Height in pixels.
        stride (c_int): The number of bytes per horizontal line of the image.
        buffer (POINTER(c_uint8)): Pointer to a pre-allocated image buffer.
        buffer_size (c_size_t): Size in bytes of the pre-allocated image buffer.
        buffer_release_cb (c_void_p): Callback to the buffer free function, called when all references
            to the buffer have been released. This parameter is optional.
        buffer_release_cb_context (c_void_p): Context for the buffer free function. This value will
            be called as a parameter to `buffer_release_cb` when the callback is invoked.
        image_handle (POINTER(k4a_image_t)): Pointer to store image handle in.

    Returns:
        k4a_result_t: Returns `K4A_RESULT_SUCCEEDED` on success. Errors are indicated with
            `K4A_RESULT_FAILED` and error specific data can be found in the log.
    """
    _k4a_image_create_from_buffer = k4a_dll.k4a_image_create_from_buffer
    _k4a_image_create_from_buffer.restype = k4a_result_t
    _k4a_image_create_from_buffer.argtypes = (
        k4a_image_format_t,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.c_size_t,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.POINTER(k4a_image_t),
    )

    return _k4a_image_create_from_buffer(
        image_format,
        width,
        height,
        stride,
        buffer,
        buffer_size,
        buffer_release_cb,
        buffer_release_cb_context,
        image_handle,
    )


def k4a_image_get_buffer(image_handle: k4a_image_t) -> ctypes.POINTER(ctypes.c_uint8):
    """
    Get the image buffer.

    Use this buffer to access the raw image data.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        POINTER(c_uint8): The function will return NULL if there is an error, and will normally return a pointer
            to the image buffer. Since all `k4a_image_t` instances are created with an image buffer, this
            function should only return NULL if the `image_handle` is invalid.
    """
    # K4A_EXPORT uint8_t *k4a_image_get_buffer(k4a_image_t image_handle);

    _k4a_image_get_buffer = k4a_dll.k4a_image_get_buffer
    _k4a_image_get_buffer.restype = ctypes.POINTER(ctypes.c_uint8)
    _k4a_image_get_buffer.argtypes = (k4a_image_t,)

    return _k4a_image_get_buffer(image_handle)


def k4a_image_get_size(image_handle: k4a_image_t) -> ctypes.c_size_t:
    """
    Get the image buffer size.

    Use this function to know what the size of the image buffer is returned by `k4a_image_get_buffer()`.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_size_t: The function will return 0 if there is an error, and will normally return the image size.
            Since all `k4a_image_t` instances are created with an image buffer, this function should only
            return 0 if the `image_handle` is invalid.
    """
    # K4A_EXPORT size_t k4a_image_get_size(k4a_image_t image_handle);

    _k4a_image_get_size = k4a_dll.k4a_image_get_size
    _k4a_image_get_size.restype = ctypes.c_size_t
    _k4a_image_get_size.argtypes = (k4a_image_t,)

    return _k4a_image_get_size(image_handle)


def k4a_image_get_format(image_handle: k4a_image_t) -> k4a_image_format_t:
    """
    Get the format of the image.

    Use this function to determine the format of the image buffer.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        k4a_image_format_t: This function is not expected to fail, all `k4a_image_t`'s are created
            with a known format. If the `image_handle` is invalid, the function will return
            `K4A_IMAGE_FORMAT_CUSTOM`.
    """
    # K4A_EXPORT k4a_image_format_t k4a_image_get_format(k4a_image_t image_handle);

    _k4a_image_get_format = k4a_dll.k4a_image_get_format
    _k4a_image_get_format.restype = k4a_image_format_t
    _k4a_image_get_format.argtypes = (k4a_image_t,)

    return _k4a_image_get_format(image_handle)


def k4a_image_get_width_pixels(image_handle: k4a_image_t) -> ctypes.c_int:
    """
    Get the image width in pixels.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_int: This function is not expected to fail, all `k4a_image_t`'s are created with a known width.
            If the `image_handle` is invalid, the function will return 0.
    """
    # K4A_EXPORT int k4a_image_get_width_pixels(k4a_image_t image_handle);

    _k4a_image_get_width_pixels = k4a_dll.k4a_image_get_width_pixels
    _k4a_image_get_width_pixels.restype = ctypes.c_int
    _k4a_image_get_width_pixels.argtypes = (k4a_image_t,)

    return _k4a_image_get_width_pixels(image_handle)


def k4a_image_get_height_pixels(image_handle: k4a_image_t) -> ctypes.c_int:
    """
    Get the image height in pixels.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_int: This function is not expected to fail, all `k4a_image_t`'s are created with a known height.
        If the `image_handle` is invalid, the function will return 0.
    """
    # K4A_EXPORT int k4a_image_get_height_pixels(k4a_image_t image_handle);

    _k4a_image_get_height_pixels = k4a_dll.k4a_image_get_height_pixels
    _k4a_image_get_height_pixels.restype = ctypes.c_int
    _k4a_image_get_height_pixels.argtypes = (k4a_image_t,)

    return _k4a_image_get_height_pixels(image_handle)


def k4a_image_get_stride_bytes(image_handle: k4a_image_t) -> ctypes.c_int:
    """
    Get the image stride in bytes.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_int: This function is not expected to fail, all `k4a_image_t`'s are created with a known stride.
        If the `image_handle` is invalid, or the image's format does not have a stride, the function
        will return 0.
    """
    # K4A_EXPORT int k4a_image_get_stride_bytes(k4a_image_t image_handle);

    _k4a_image_get_stride_bytes = k4a_dll.k4a_image_get_stride_bytes
    _k4a_image_get_stride_bytes.restype = ctypes.c_int
    _k4a_image_get_stride_bytes.argtypes = (k4a_image_t,)

    return _k4a_image_get_stride_bytes(image_handle)


def k4a_image_get_timestamp_usec(image_handle: k4a_image_t) -> ctypes.c_uint64:
    """
    Get the image's device timestamp in microseconds.

    Returns the device timestamp of the image. Timestamps are recorded by the device and represent
    the mid-point of exposure. They may be used for relative comparison, but their absolute value
    has no defined meaning.

    Note:
        Deprecated starting in 1.2.0. Please use `k4a_image_get_device_timestamp_usec()`.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint64: If the `image_handle` is invalid or if no timestamp was set for the image, this
            function will return 0. It is also possible for 0 to be a valid timestamp originating
            from the beginning of a recording or the start of streaming.
    """
    # K4A_DEPRECATED_EXPORT uint64_t k4a_image_get_timestamp_usec(k4a_image_t image_handle);

    _k4a_image_get_timestamp_usec = k4a_dll.k4a_image_get_timestamp_usec
    _k4a_image_get_timestamp_usec.restype = ctypes.c_uint64
    _k4a_image_get_timestamp_usec.argtypes = (k4a_image_t,)

    return _k4a_image_get_timestamp_usec(image_handle)


def k4a_image_get_device_timestamp_usec(image_handle: k4a_image_t) -> ctypes.c_uint64:
    """
    Get the image's device timestamp in microseconds.

    Returns the device timestamp of the image, as captured by the hardware. Timestamps are recorded
    by the device and represent the mid-point of exposure. They may be used for relative comparison,
    but their absolute value has no defined meaning.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint64: If the `image_handle` is invalid or if no timestamp was set for the image, this
            function will return 0. It is also possible for 0 to be a valid timestamp originating
            from the beginning of a recording or the start of streaming.
    """
    # K4A_EXPORT uint64_t k4a_image_get_device_timestamp_usec(k4a_image_t image_handle);

    _k4a_image_get_device_timestamp_usec = k4a_dll.k4a_image_get_device_timestamp_usec
    _k4a_image_get_device_timestamp_usec.restype = ctypes.c_uint64
    _k4a_image_get_device_timestamp_usec.argtypes = (k4a_image_t,)

    return _k4a_image_get_device_timestamp_usec(image_handle)


def k4a_image_get_system_timestamp_nsec(image_handle: k4a_image_t) -> ctypes.c_uint64:
    """
    Get the image's system timestamp in nanoseconds.

    Returns the system timestamp of the image. Timestamps are recorded by the host. They may be
    used for relative comparision, as they are relative to the corresponding system clock. The
    absolute value is a monotonic count from an arbitrary point in the past.

    The system timestamp is captured at the moment host PC finishes receiving the image.

    On Linux the system timestamp is read from clock_gettime(CLOCK_MONOTONIC), which measures
    realtime and is not impacted by adjustments to the system clock. It starts from an arbitrary
    point in the past. On Windows the system timestamp is read from QueryPerformanceCounter(),
    it also measures realtime and is not impacted by adjustments to the system clock. It also starts
    from an arbitrary point in the past.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint64: If the `image_handle` is invalid or if no timestamp was set for the image, this function
            will return 0. It is also possible for 0 to be a valid timestamp originating from the beginning
            of a recording or the start of streaming.
    """
    # K4A_EXPORT uint64_t k4a_image_get_system_timestamp_nsec(k4a_image_t image_handle);

    _k4a_image_get_system_timestamp_nsec = k4a_dll.k4a_image_get_system_timestamp_nsec
    _k4a_image_get_system_timestamp_nsec.restype = ctypes.c_uint64
    _k4a_image_get_system_timestamp_nsec.argtypes = (k4a_image_t,)

    return _k4a_image_get_system_timestamp_nsec(image_handle)


def k4a_image_get_exposure_usec(image_handle: k4a_image_t) -> ctypes.c_uint64:
    """
    Get the image exposure in microseconds.

    Returns an exposure time in microseconds. This is only supported on color image formats.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint64: If the `image_handle` is invalid, or no exposure was set on the image, the function will
            return 0. Otherwise, it will return the image exposure time in microseconds.
    """
    # K4A_EXPORT uint64_t k4a_image_get_exposure_usec(k4a_image_t image_handle);

    _k4a_image_get_exposure_usec = k4a_dll.k4a_image_get_exposure_usec
    _k4a_image_get_exposure_usec.restype = ctypes.c_uint64
    _k4a_image_get_exposure_usec.argtypes = (k4a_image_t,)

    return _k4a_image_get_exposure_usec(image_handle)


def k4a_image_get_white_balance(image_handle: k4a_image_t) -> ctypes.c_uint32:
    """
    Get the image white balance.

    Returns the image's white balance. This function is only valid for color captures, and not for depth
    or IR captures.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint32: Returns the image white balance in Kelvin. If `image_handle` is invalid, or the
        white balance was not set or not applicable to the image, the function will return 0.
    """
    # K4A_EXPORT uint32_t k4a_image_get_white_balance(k4a_image_t image_handle);

    _k4a_image_get_white_balance = k4a_dll.k4a_image_get_white_balance
    _k4a_image_get_white_balance.restype = ctypes.c_uint32
    _k4a_image_get_white_balance.argtypes = (k4a_image_t,)

    return _k4a_image_get_white_balance(image_handle)


def k4a_image_get_iso_speed(image_handle: k4a_image_t) -> ctypes.c_uint32:
    """
    Get the image white balance.

    Returns the image's white balance. This function is only valid for color captures, and not for
    depth or IR captures.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.

    Returns:
        c_uint32: Returns the image white balance in Kelvin. If `image_handle` is invalid, or the white
        balance was not set or not applicable to the image, the function will return 0.
    """
    # K4A_EXPORT uint32_t k4a_image_get_iso_speed(k4a_image_t image_handle);

    _k4a_image_get_iso_speed = k4a_dll.k4a_image_get_iso_speed
    _k4a_image_get_iso_speed.restype = ctypes.c_uint32
    _k4a_image_get_iso_speed.argtypes = (k4a_image_t,)

    return _k4a_image_get_iso_speed(image_handle)


def k4a_image_set_device_timestamp_usec(image_handle: k4a_image_t, timestamp_usec: ctypes.c_uint64) -> None:
    """
    Set the device time stamp, in microseconds, of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`.

    The device timestamp represents the mid-point of exposure of the image, as captured by the hardware.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the timestamp on.
        timestamp_usec (c_uint64): Device timestamp of the image in microseconds.
    """
    # K4A_EXPORT void k4a_image_set_device_timestamp_usec(k4a_image_t image_handle, uint64_t timestamp_usec);

    _k4a_image_set_device_timestamp_usec = k4a_dll.k4a_image_set_device_timestamp_usec
    _k4a_image_set_device_timestamp_usec.restype = None
    _k4a_image_set_device_timestamp_usec.argtypes = (
        k4a_image_t,
        ctypes.c_uint64,
    )

    _k4a_image_set_device_timestamp_usec(image_handle, timestamp_usec)


def k4a_image_set_timestamp_usec(image_handle: k4a_image_t, timestamp_usec: ctypes.c_uint64) -> None:
    """
    Set the device time stamp, in microseconds, of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`.

    The device timestamp represents the mid-point of exposure of the image, as captured by the hardware.

    Note:
        Deprecated starting in 1.2.0. Please use `k4a_image_set_device_timestamp_usec()`.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the timestamp on.
        timestamp_usec (c_uint64): Device timestamp of the image in microseconds.
    """
    # K4A_DEPRECATED_EXPORT void k4a_image_set_timestamp_usec(k4a_image_t image_handle, uint64_t timestamp_usec);

    _k4a_image_set_timestamp_usec = k4a_dll.k4a_image_set_timestamp_usec
    _k4a_image_set_timestamp_usec.restype = None
    _k4a_image_set_timestamp_usec.argtypes = (
        k4a_image_t,
        ctypes.c_uint64,
    )

    _k4a_image_set_timestamp_usec(image_handle, timestamp_usec)


def k4a_image_set_system_timestamp_nsec(image_handle: k4a_image_t, timestamp_nsec: ctypes.c_uint64) -> None:
    """
    Set the system time stamp, in nanoseconds, of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`.

    The system timestamp is a high performance and increasing clock (from boot). The timestamp
    represents the time immediately after the image buffer was read by the host PC.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the timestamp on.
        timestamp_nsec (c_uint64): Timestamp of the image in nanoseconds.
    """
    # K4A_EXPORT void k4a_image_set_system_timestamp_nsec(k4a_image_t image_handle, uint64_t timestamp_nsec);

    _k4a_image_set_system_timestamp_nsec = k4a_dll.k4a_image_set_system_timestamp_nsec
    _k4a_image_set_system_timestamp_nsec.restype = None
    _k4a_image_set_system_timestamp_nsec.argtypes = (
        k4a_image_t,
        ctypes.c_uint64,
    )

    _k4a_image_set_system_timestamp_nsec(image_handle, timestamp_nsec)


def k4a_image_set_exposure_usec(image_handle: k4a_image_t, exposure_usec: ctypes.c_uint64) -> None:
    """
    Set the exposure time, in microseconds, of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`. An exposure time of 0 is considered invalid. Only color image formats
    are expected to have a valid exposure time.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the exposure time on.
        exposure_usec (c_uint64): Exposure time of the image in microseconds.
    """
    # K4A_EXPORT void k4a_image_set_exposure_usec(k4a_image_t image_handle, uint64_t exposure_usec);

    _k4a_image_set_exposure_usec = k4a_dll.k4a_image_set_exposure_usec
    _k4a_image_set_exposure_usec.restype = None
    _k4a_image_set_exposure_usec.argtypes = (
        k4a_image_t,
        ctypes.c_uint64,
    )

    _k4a_image_set_exposure_usec(image_handle, exposure_usec)


def k4a_image_set_exposure_time_usec(image_handle: k4a_image_t, exposure_usec: ctypes.c_uint64) -> None:
    """
    Set the exposure time, in microseconds, of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`. An exposure time of 0 is considered invalid. Only color image formats are
    expected to have a valid exposure time.

    Note:
        Deprecated starting in 1.2.0. Please use `k4a_image_set_exposure_usec()`.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the exposure time on.
        exposure_usec (c_uint64): Exposure time of the image in microseconds.
    """
    # K4A_DEPRECATED_EXPORT void k4a_image_set_exposure_time_usec(k4a_image_t image_handle, uint64_t exposure_usec);

    _k4a_image_set_exposure_time_usec = k4a_dll.k4a_image_set_exposure_time_usec
    _k4a_image_set_exposure_time_usec.restype = None
    _k4a_image_set_exposure_time_usec.argtypes = (
        k4a_image_t,
        ctypes.c_uint64,
    )

    _k4a_image_set_exposure_time_usec(image_handle, exposure_usec)


def k4a_image_set_white_balance(image_handle: k4a_image_t, white_balance: ctypes.c_uint32) -> None:
    """
    Set the white balance of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`. A white balance of 0 is considered invalid. White balance is only meaningful
    for color images, and not expected on depth or IR images.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the white balance on.
        white_balance (c_uint32): White balance of the image in degrees Kelvin.
    """
    # K4A_EXPORT void k4a_image_set_white_balance(k4a_image_t image_handle, uint32_t white_balance);

    _k4a_image_set_white_balance = k4a_dll.k4a_image_set_white_balance
    _k4a_image_set_white_balance.restype = None
    _k4a_image_set_white_balance.argtypes = (
        k4a_image_t,
        ctypes.c_uint32,
    )

    _k4a_image_set_white_balance(image_handle, white_balance)


def k4a_image_set_iso_speed(image_handle: k4a_image_t, iso_speed: ctypes.c_uint32) -> None:
    """
    Set the ISO speed of the image.

    Use this function in conjunction with `k4a_image_create()` or `k4a_image_create_from_buffer()` to
    construct a `k4a_image_t`. An ISO speed of 0 is considered invalid. Only color images are expected
    to have a valid ISO speed.

    Args:
        image_handle (k4a_image_t): Handle of the image to set the ISO speed on.
        iso_speed (c_uint32): ISO speed of the image.
    """
    # K4A_EXPORT void k4a_image_set_iso_speed(k4a_image_t image_handle, uint32_t iso_speed);

    _k4a_image_set_iso_speed = k4a_dll.k4a_image_set_iso_speed
    _k4a_image_set_iso_speed.restype = None
    _k4a_image_set_iso_speed.argtypes = (
        k4a_image_t,
        ctypes.c_uint32,
    )

    _k4a_image_set_iso_speed(image_handle, iso_speed)


def k4a_image_reference(image_handle: k4a_image_t) -> None:
    """
    Add a reference to the `k4a_image_t`.

    References manage the lifetime of the object. When the references reach zero the object
    is destroyed. A caller must not access the object after its reference is released.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.
    """
    # K4A_EXPORT void k4a_image_reference(k4a_image_t image_handle);

    _k4a_image_reference = k4a_dll.k4a_image_reference
    _k4a_image_reference.restype = None
    _k4a_image_reference.argtypes = (k4a_image_t,)

    _k4a_image_reference(image_handle)


def k4a_image_release(image_handle: k4a_image_t) -> None:
    """
    Remove a reference from the `k4a_image_t`.

    References manage the lifetime of the object. When the references reach zero the object
    is destroyed. A caller must not access the object after its reference is released.

    Args:
        image_handle (k4a_image_t): Handle of the image for which the get operation is performed on.
    """
    # K4A_EXPORT void k4a_image_release(k4a_image_t image_handle);

    _k4a_image_release = k4a_dll.k4a_image_release
    _k4a_image_release.restype = None
    _k4a_image_release.argtypes = (k4a_image_t,)

    _k4a_image_release(image_handle)


def k4a_device_start_cameras(
    device_handle: k4a_device_t, config: ctypes.POINTER(k4a_device_configuration_t)
) -> k4a_result_t:
    """
    Starts color and depth camera capture.

    Individual sensors configured to run will now start to stream captured data.

    It is not valid to call `k4a_device_start_cameras()` a second time on the same `k4a_device_t`
    until `k4a_device_stop_cameras()` has been called.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        config (POINTER(k4a_device_configuration_t)): The configuration we want to run the device in.
            This can be initialized with `K4A_DEVICE_CONFIG_INIT_DISABLE_ALL`.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` is returned on success.
    """
    # K4A_EXPORT k4a_result_t k4a_device_start_cameras(k4a_device_t device_handle, const k4a_device_configuration_t *config);

    _k4a_device_start_cameras = k4a_dll.k4a_device_start_cameras
    _k4a_device_start_cameras.restype = k4a_result_t
    _k4a_device_start_cameras.argtypes = (
        k4a_device_t,
        ctypes.POINTER(k4a_device_configuration_t),
    )

    return _k4a_device_start_cameras(device_handle, config)


def k4a_device_stop_cameras(device_handle: k4a_device_t) -> None:
    """
    Stops the color and depth camera capture.

    The streaming of individual sensors stops as a result of this call. Once called,
    `k4a_device_start_cameras()` may be called again to resume sensor streaming.

    This function may be called while another thread is blocking in `k4a_device_get_capture()`.
    Calling this function while another thread is in that function will result in that function
    returning a failure.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
    """
    # K4A_EXPORT void k4a_device_stop_cameras(k4a_device_t device_handle);

    _k4a_device_stop_cameras = k4a_dll.k4a_device_stop_cameras
    _k4a_device_stop_cameras.restype = None
    _k4a_device_stop_cameras.argtypes = (k4a_device_t,)

    _k4a_device_stop_cameras(device_handle)


def k4a_device_start_imu(device_handle: k4a_device_t) -> k4a_result_t:
    """
    Starts the IMU sample stream.

    Call this API to start streaming IMU data. It is not valid to call this function a second time
    on the same `k4a_device_t` until `k4a_device_stop_imu()` has been called.

    This function is dependent on the state of the cameras. The color or depth camera must be started
    before the IMU. `K4A_RESULT_FAILED` will be returned if one of the cameras is not running.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` is returned on success. `K4A_RESULT_FAILED` if the sensor is
            already running or a failure is encountered
    """
    # K4A_EXPORT k4a_result_t k4a_device_start_imu(k4a_device_t device_handle);

    _k4a_device_start_imu = k4a_dll.k4a_device_start_imu
    _k4a_device_start_imu.restype = k4a_result_t
    _k4a_device_start_imu.argtypes = (k4a_device_t,)

    return _k4a_device_start_imu(device_handle)


def k4a_device_stop_imu(device_handle: k4a_device_t) -> None:
    """
    Stops the IMU capture.

    The streaming of the IMU stops as a result of this call. Once called, `k4a_device_start_imu()`
    may be called again to resume sensor streaming, so long as the cameras are running.

    This function may be called while another thread is blocking in `k4a_device_get_imu_sample()`.
    Calling this function while another thread is in that function will result in that function
    returning a failure.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
    """
    # K4A_EXPORT void k4a_device_stop_imu(k4a_device_t device_handle);

    _k4a_device_stop_imu = k4a_dll.k4a_device_stop_imu
    _k4a_device_stop_imu.restype = None
    _k4a_device_stop_imu.argtypes = (k4a_device_t,)

    _k4a_device_stop_imu(device_handle)


def k4a_device_get_serialnum(
    device_handle: k4a_device_t, serial_number: ctypes.c_char_p, serial_number_size: ctypes.POINTER(ctypes.c_size_t)
) -> k4a_buffer_result_t:
    """
    Get the Azure Kinect device serial number.

    Queries the device for its serial number. If the caller needs to know the size of the serial
    number to allocate memory, the function should be called once with a NULL `serial_number` to
    get the needed size in the `serial_number_size` output, and then again with the allocated buffer.

    Only a complete serial number will be returned. If the caller's buffer is too small,
    the function will return `K4A_BUFFER_RESULT_TOO_SMALL` without returning any data in `serial_number`.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        serial_number (c_char_p): Location to write the serial number to. If the function returns
            `K4A_BUFFER_RESULT_SUCCEEDED`, this will be a NULL terminated string of ASCII characters.
            If this input is NULL `serial_number_size` will still be updated to return the size of
            the buffer needed to store the string.
        serial_number_size (POINTER(c_size_t)): On input, the size of the `serial_number` buffer if
            that pointer is not NULL. On output, this value is set to the actual number of bytes
            in the serial number (including the null terminator).

    Returns:
        k4a_buffer_result_t: A return of `K4A_BUFFER_RESULT_SUCCEEDED` means that the `serial_number`
            has been filled in. If the buffer is too small the function returns `K4A_BUFFER_RESULT_TOO_SMALL`
            and the size of the serial number is returned in the `serial_number_size` parameter.
            All other failures return `K4A_BUFFER_RESULT_FAILED`.
    """

    _k4a_device_get_serialnum = k4a_dll.k4a_device_get_serialnum
    _k4a_device_get_serialnum.restype = k4a_buffer_result_t
    _k4a_device_get_serialnum.argtypes = (
        k4a_device_t,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_size_t),
    )

    return _k4a_device_get_serialnum(device_handle, serial_number, serial_number_size)


def k4a_device_get_version(
    device_handle: k4a_device_t, hardware_version: ctypes.POINTER(k4a_hardware_version_t)
) -> k4a_result_t:
    """
    Get the version numbers of the device's subsystems.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        hardware_version (POINTER(k4a_hardware_version_t)): Location to write the version info to.

    Returns:
        k4a_result_t: A return of `K4A_RESULT_SUCCEEDED` means that the version structure has been
            filled in. All other failures return `K4A_RESULT_FAILED`.
    """
    # K4A_EXPORT k4a_result_t k4a_device_get_version(k4a_device_t device_handle, k4a_hardware_version_t *version);

    _k4a_device_get_version = k4a_dll.k4a_device_get_version
    _k4a_device_get_version.restype = k4a_result_t
    _k4a_device_get_version.argtypes = (
        k4a_device_t,
        ctypes.POINTER(k4a_hardware_version_t),
    )

    return _k4a_device_get_version(device_handle, hardware_version)


def k4a_device_get_color_control_capabilities(
    device_handle: k4a_device_t,
    command: k4a_color_control_command_t,
    supports_auto: ctypes.POINTER(ctypes.c_bool),
    min_value: ctypes.POINTER(ctypes.c_int32),
    max_value: ctypes.POINTER(ctypes.c_int32),
    step_value: ctypes.POINTER(ctypes.c_int32),
    default_value: ctypes.POINTER(ctypes.c_int32),
    default_mode: ctypes.POINTER(k4a_color_control_mode_t),
) -> k4a_result_t:
    """
    Get the Azure Kinect color sensor control capabilities.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        command (k4a_color_control_command_t): Color sensor control command.
        supports_auto (POINTER(c_bool)): Location to store whether the color sensor's control
            support auto mode or not. true if it supports auto mode, otherwise false.
        min_value (POINTER(c_int32)): Location to store the color sensor's control minimum
            value of /p command.
        max_value (POINTER(c_int32)): Location to store the color sensor's control maximum
            value of /p command.
        step_value (POINTER(c_int32)): Location to store the color sensor's control step
            value of /p command.
        default_value (POINTER(c_int32)): Location to store the color sensor's control default
            value of /p command.
        default_mode (POINTER(k4a_color_control_mode_t)): Location to store the color sensor's control
            default mode of /p command.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if the value was successfully returned, `K4A_RESULT_FAILED`
            if an error occurred.
    """

    _k4a_device_get_color_control_capabilities = k4a_dll.k4a_device_get_color_control_capabilities
    _k4a_device_get_color_control_capabilities.restype = k4a_result_t
    _k4a_device_get_color_control_capabilities.argtypes = (
        k4a_device_t,
        k4a_color_control_command_t,
        ctypes.POINTER(ctypes.c_bool),
        ctypes.POINTER(ctypes.c_int32),
        ctypes.POINTER(ctypes.c_int32),
        ctypes.POINTER(ctypes.c_int32),
        ctypes.POINTER(ctypes.c_int32),
        ctypes.POINTER(k4a_color_control_mode_t),
    )

    return _k4a_device_get_color_control_capabilities(
        device_handle,
        command,
        supports_auto,
        min_value,
        max_value,
        step_value,
        default_value,
        default_mode,
    )


def k4a_device_get_color_control(
    device_handle: k4a_device_t,
    command: k4a_color_control_command_t,
    mode: ctypes.POINTER(k4a_color_control_mode_t),
    value: ctypes.POINTER(ctypes.c_int32),
) -> k4a_result_t:
    """
    Get the Azure Kinect color sensor control value.

    Each control command may be set to manual or automatic. See the definition of
    `k4a_color_control_command_t` on how to interpret the `value` for each command.

    Some control commands are only supported in manual mode. When a command is in automatic mode,
    the `value` for that command is not valid.

    Control values set on a device are reset only when the device is power cycled. The device will
    retain the settings even if the `k4a_device_t` is closed or the application is restarted.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        command (k4a_color_control_command_t): Color sensor control command.
        mode (POINTER(k4a_color_control_mode_t)): Location to store the color sensor's control mode.
            This mode represents whether the command is in automatic or manual mode.
        value (POINTER(c_int32)): Location to store the color sensor's control value. This value
            is always written, but is only valid when the `mode` returned is `K4A_COLOR_CONTROL_MODE_MANUAL`
            for the current `command`.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if the value was successfully returned, `K4A_RESULT_FAILED`
            if an error occurred.
    """

    _k4a_device_get_color_control = k4a_dll.k4a_device_get_color_control
    _k4a_device_get_color_control.restype = k4a_result_t
    _k4a_device_get_color_control.argtypes = (
        k4a_device_t,
        k4a_color_control_command_t,
        ctypes.POINTER(k4a_color_control_mode_t),
        ctypes.POINTER(ctypes.c_int32),
    )

    return _k4a_device_get_color_control(device_handle, command, mode, value)


def k4a_device_set_color_control(
    device_handle: k4a_device_t,
    command: k4a_color_control_command_t,
    mode: k4a_color_control_mode_t,
    value: ctypes.c_int32,
) -> k4a_result_t:
    """
    Set the Azure Kinect color sensor control value.

    Each control command may be set to manual or automatic. See the definition of
    `k4a_color_control_command_t` on how to interpret the `value` for each command.

    Some control commands are only supported in manual mode. When a command is in automatic mode,
    the `value` for that command is not valid.

    Control values set on a device are reset only when the device is power cycled. The device will
    retain the settings even if the `k4a_device_t` is closed or the application is restarted.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        command (k4a_color_control_command_t): 	Color sensor control command.
        mode (k4a_color_control_mode_t): Color sensor control mode to set. This mode represents whether
            the command is in automatic or manual mode.
        value (c_int32): Value to set the color sensor's control to. The value is only valid if `mode`
            is set to `K4A_COLOR_CONTROL_MODE_MANUAL`, and is otherwise ignored.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if the value was successfully set, `K4A_RESULT_FAILED`
            if an error occurred.
    """

    _k4a_device_set_color_control = k4a_dll.k4a_device_set_color_control
    _k4a_device_set_color_control.restype = k4a_result_t
    _k4a_device_set_color_control.argtypes = (
        k4a_device_t,
        k4a_color_control_command_t,
        k4a_color_control_mode_t,
        ctypes.c_int32,
    )

    return _k4a_device_set_color_control(device_handle, command, mode, value)


def k4a_device_get_raw_calibration(
    device_handle: k4a_device_t, data: ctypes.POINTER(ctypes.c_uint8), data_size: ctypes.POINTER(ctypes.c_size_t)
) -> k4a_buffer_result_t:
    """
    Get the raw calibration blob for the entire Azure Kinect device.

    `K4A_BUFFER_RESULT_SUCCEEDED` if data was successfully written. If `data_size` points to a buffer size
    that is too small to hold the output or data is NULL, `K4A_BUFFER_RESULT_TOO_SMALL` is returned and `data_size`
    is updated to contain the minimum buffer size needed to capture the calibration data.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        data (POINTER(c_uint8)): Location to write the calibration data to.
            This field may optionally be set to NULL for the caller to query for the needed data size.
        data_size (POINTER(c_size_t)): On passing `data_size` into the function this variable represents
            the available size of the `data` buffer. On return this variable is updated with the amount
            of data actually written to the buffer, or the size required to store the calibration buffer
            if `data` is NULL.

    Returns:
        k4a_buffer_result_t: `K4A_BUFFER_RESULT_SUCCEEDED` if `data` was successfully written.
            If `data_size` points to a buffer size that is too small to hold the output or `data` is NULL,
            `K4A_BUFFER_RESULT_TOO_SMALL` is returned and `data_size` is updated to contain the minimum
            buffer size needed to capture the calibration data.
    """

    _k4a_device_get_raw_calibration = k4a_dll.k4a_device_get_raw_calibration
    _k4a_device_get_raw_calibration.restype = k4a_buffer_result_t
    _k4a_device_get_raw_calibration.argtypes = (
        k4a_device_t,
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.POINTER(ctypes.c_size_t),
    )

    return _k4a_device_get_raw_calibration(device_handle, data, data_size)


def k4a_device_get_calibration(
    device_handle: k4a_device_t,
    depth_mode: k4a_depth_mode_t,
    color_resolution: k4a_color_resolution_t,
    calibration: ctypes.POINTER(k4a_calibration_t),
) -> k4a_result_t:
    """
    Get the camera calibration for the entire Azure Kinect device.

    The `calibration` represents the data needed to transform between the camera views and may be
    different for each operating `depth_mode` and `color_resolution` the device is configured to operate in.

    The `calibration` output is used as input to all calibration and transformation functions.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        depth_mode (k4a_depth_mode_t): Mode in which depth camera is operated.
        color_resolution (k4a_color_resolution_t): Resolution in which color camera is operated.
        calibration (POINTER(k4a_calibration_t)): Location to write the calibration.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `calibration` was successfully written.
            `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_device_get_calibration = k4a_dll.k4a_device_get_calibration
    _k4a_device_get_calibration.restype = k4a_result_t
    _k4a_device_get_calibration.argtypes = (
        k4a_device_t,
        k4a_depth_mode_t,
        k4a_color_resolution_t,
        ctypes.POINTER(k4a_calibration_t),
    )

    return _k4a_device_get_calibration(device_handle, depth_mode, color_resolution, calibration)


def k4a_device_get_sync_jack(
    device_handle: k4a_device_t,
    sync_in_jack_connected: ctypes.POINTER(ctypes.c_bool),
    sync_out_jack_connected: ctypes.POINTER(ctypes.c_bool),
) -> k4a_result_t:
    """
    Get the device jack status for the synchronization in and synchronization out connectors.

    If `sync_out_jack_connected` is true then `k4a_device_configuration_t` wired_sync_mode mode can be set to
    `K4A_WIRED_SYNC_MODE_STANDALONE` or `K4A_WIRED_SYNC_MODE_MASTER`. If `sync_in_jack_connected` is true then
    `k4a_device_configuration_t` wired_sync_mode mode can be set to `K4A_WIRED_SYNC_MODE_STANDALONE` or
    `K4A_WIRED_SYNC_MODE_SUBORDINATE`.

    Args:
        device_handle (k4a_device_t): Handle obtained by `k4a_device_open()`.
        sync_in_jack_connected (POINTER(c_bool)): Upon successful return this value will be set to true
            if a cable is connected to this sync in jack.
        sync_out_jack_connected (POINTER(c_bool)): Upon successful return this value will be set to true
            if a cable is connected to this sync out jack.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if the connector status was successfully read.
    """

    _k4a_device_get_sync_jack = k4a_dll.k4a_device_get_sync_jack
    _k4a_device_get_sync_jack.restype = k4a_result_t
    _k4a_device_get_sync_jack.argtypes = (
        k4a_device_t,
        ctypes.POINTER(ctypes.c_bool),
        ctypes.POINTER(ctypes.c_bool),
    )

    return _k4a_device_get_sync_jack(device_handle, sync_in_jack_connected, sync_out_jack_connected)


def k4a_calibration_get_from_raw(
    raw_calibration: ctypes.POINTER(ctypes.c_char),
    raw_calibration_size: ctypes.c_size_t,
    depth_mode: k4a_depth_mode_t,
    color_resolution: k4a_color_resolution_t,
    calibration: ctypes.POINTER(k4a_calibration_t),
) -> k4a_result_t:
    """
    Get the camera calibration for a device from a raw calibration blob.

    The `calibration` represents the data needed to transform between the camera views
    and is different for each operating `depth_mode` and `color_resolution` the device is
    configured to operate in.

    The `calibration` output is used as input to all transformation functions.

    Args:
        raw_calibration (POINTER(c_char)): Raw calibration blob obtained from a device or recording.
            The raw calibration must be NULL terminated.
        raw_calibration_size (c_size_t): The size, in bytes, of raw_calibration including
            the NULL termination.
        depth_mode (k4a_depth_mode_t): Mode in which depth camera is operated.
        color_resolution (k4a_color_resolution_t): Resolution in which color camera is operated.
        calibration (POINTER(k4a_calibration_t)): Location to write the calibration.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `calibration` was successfully written.
            `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_calibration_get_from_raw = k4a_dll.k4a_calibration_get_from_raw
    _k4a_calibration_get_from_raw.restype = k4a_result_t
    _k4a_calibration_get_from_raw.argtypes = (
        ctypes.POINTER(ctypes.c_char),
        ctypes.c_size_t,
        k4a_depth_mode_t,
        k4a_color_resolution_t,
        ctypes.POINTER(k4a_calibration_t),
    )

    return _k4a_calibration_get_from_raw(
        raw_calibration, raw_calibration_size, depth_mode, color_resolution, calibration
    )


def k4a_calibration_3d_to_3d(
    calibration: ctypes.POINTER(k4a_calibration_t),
    source_point3d_mm: ctypes.POINTER(k4a_float3_t),
    source_camera: k4a_calibration_type_t,
    target_camera: k4a_calibration_type_t,
    target_point3d_mm: ctypes.POINTER(k4a_float3_t),
) -> k4a_result_t:
    """
    Transform a 3D point of a source coordinate system into a 3D point of the target coordinate system.

    This function is used to transform 3D points between depth and color camera coordinate systems.
    The function uses the extrinsic camera calibration. It computes the output via multiplication with
    a precomputed matrix encoding a 3D rotation and a 3D translation. If `source_camera` and `target_camera`
    are the same, then `target_point3d_mm` will be identical to `source_point3d_mm`.

    Args:
        calibration (POINTER(k4a_calibration_t)): Location to read the camera calibration data.
        source_point3d_mm (POINTER(k4a_float3_t)): The 3D coordinates in millimeters representing a point
            in `source_camera`.
        source_camera (k4a_calibration_type_t): The current camera.
        target_camera (k4a_calibration_type_t): The target camera.
        target_point3d_mm (POINTER(k4a_float3_t)): Pointer to the output where the new 3D coordinates of
            the input point in the coordinate space of `target_camera` is stored in millimeters.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `target_point3d_mm` was successfully written.
            `K4A_RESULT_FAILED` if `calibration` contained invalid transformation parameters.
    """

    _k4a_calibration_3d_to_3d = k4a_dll.k4a_calibration_3d_to_3d
    _k4a_calibration_3d_to_3d.restype = k4a_result_t
    _k4a_calibration_3d_to_3d.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        ctypes.POINTER(k4a_float3_t),
        k4a_calibration_type_t,
        k4a_calibration_type_t,
        ctypes.POINTER(k4a_float3_t),
    )

    return _k4a_calibration_3d_to_3d(calibration, source_point3d_mm, source_camera, target_camera, target_point3d_mm)


def k4a_calibration_2d_to_3d(
    calibration: ctypes.POINTER(k4a_calibration_t),
    source_point2d: ctypes.POINTER(k4a_float2_t),
    source_depth_mm: ctypes.c_float,
    source_camera: k4a_calibration_type_t,
    target_camera: k4a_calibration_type_t,
    target_point3d_mm: ctypes.POINTER(k4a_float3_t),
    valid: ctypes.POINTER(ctypes.c_int),
) -> k4a_result_t:
    """
    Transform a 2D pixel coordinate with an associated depth value of the source camera into
    a 3D point of the target coordinate system.

    This function applies the intrinsic calibration of `source_camera` to compute the 3D ray
    from the focal point of the camera through pixel source_point2d. The 3D point on this ray
    is then found using `source_depth_mm`. If `target_camera` is different from `source_camera`,
    the 3D point is transformed to `target_camera` using `k4a_calibration_3d_to_3d()`.
    In practice, `source_camera` and `target_camera` will often be identical.
    In this case, no 3D to 3D transformation is applied.

    If `source_point2d` is not considered as valid pixel coordinate according to the intrinsic camera model,
    valid is set to 0. If it is valid, valid will be set to 1. The user should not use the value of
    `target_point3d_mm` if valid was set to 0.

    Args:
        calibration (POINTER(k4a_calibration_t)): Location to read the camera calibration obtained by
            k4a_device_get_calibration().
        source_point2d (POINTER(k4a_float2_t)): The 2D pixel in `source_camera` coordinates.
        source_depth_mm (c_float): The depth of `source_point2d` in millimeters. One way to derive the
            depth value in the color camera geometry is to use the function `k4a_transformation_depth_image_to_color_camera()`.
        source_camera (k4a_calibration_type_t): The current camera.
        target_camera (k4a_calibration_type_t): The target camera.
        target_point3d_mm (POINTER(k4a_float3_t)): Pointer to the output where the 3D coordinates of
            the input pixel in the coordinate system of `target_camera` is stored in millimeters.
        valid (POINTER(c_int)): The output parameter returns a value of 1 if the `source_point2d` is a
            valid coordinate, and will return 0 if the coordinate is not valid in the calibration model.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `target_point3d_mm` was successfully written. `K4A_RESULT_FAILED`
            if calibration contained invalid transformation parameters. If the function returns
            `K4A_RESULT_SUCCEEDED`, but valid is 0, the transformation was computed, but the results in
            `target_point3d_mm` are outside of the range of valid calibration and should be ignored.
    """

    _k4a_calibration_2d_to_3d = k4a_dll.k4a_calibration_2d_to_3d
    _k4a_calibration_2d_to_3d.restype = k4a_result_t
    _k4a_calibration_2d_to_3d.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        ctypes.POINTER(k4a_float2_t),
        ctypes.c_float,
        k4a_calibration_type_t,
        k4a_calibration_type_t,
        ctypes.POINTER(k4a_float3_t),
        ctypes.POINTER(ctypes.c_int),
    )

    return _k4a_calibration_2d_to_3d(
        calibration,
        source_point2d,
        source_depth_mm,
        source_camera,
        target_camera,
        target_point3d_mm,
        valid,
    )


def k4a_calibration_3d_to_2d(
    calibration: ctypes.POINTER(k4a_calibration_t),
    source_point3d_mm: ctypes.POINTER(k4a_float3_t),
    source_camera: k4a_calibration_type_t,
    target_camera: k4a_calibration_type_t,
    target_point2d: ctypes.POINTER(k4a_float2_t),
    valid: ctypes.POINTER(ctypes.c_int),
) -> k4a_result_t:
    """
    Transform a 3D point of a source coordinate system into a 2D pixel coordinate of the target camera.

    If `target_camera` is different from `source_camera`, `source_point3d_mm` is transformed to `target_camera`
    using `k4a_calibration_3d_to_3d()`. In practice, `source_camera` and `target_camera` will often be identical.
    In this case, no 3D to 3D transformation is applied. The 3D point in the coordinate system of
    `target_camera` is then projected onto the image plane using the intrinsic calibration of `target_camera`.

    If `source_point3d_mm` does not map to a valid 2D coordinate in the `target_camera` coordinate system,
    `valid` is set to 0. If it is valid, `valid` will be set to 1. The user should not use the value of
    `target_point2d` if `valid` was set to 0.

    Args:
        calibration (POINTER(k4a_calibration_t)): Location to read the camera calibration obtained
            by `k4a_device_get_calibration()`.
        source_point3d_mm (POINTER(k4a_float3_t)): The 3D coordinates in millimeters representing
            a point in source_camera
        source_camera (k4a_calibration_type_t): The current camera.
        target_camera (k4a_calibration_type_t): The target camera.
        target_point2d (POINTER(k4a_float2_t)): Pointer to the output where the 2D pixel in
            `target_camera` coordinates is stored.
        valid (POINTER(c_int)): The output parameter returns a value of 1 if the `source_point3d_mm` is
            a valid coordinate in the `target_camera` coordinate system, and will return 0 if the coordinate
            is not valid in the calibration model.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `target_point2d` was successfully written. `K4A_RESULT_FAILED`
            if `calibration` contained invalid transformation parameters. If the function returns `K4A_RESULT_SUCCEEDED`,
            but `valid` is 0, the transformation was computed, but the results in `target_point2d` are outside of the range
            of valid calibration and should be ignored.
    """

    _k4a_calibration_3d_to_2d = k4a_dll.k4a_calibration_3d_to_2d
    _k4a_calibration_3d_to_2d.restype = k4a_result_t
    _k4a_calibration_3d_to_2d.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        ctypes.POINTER(k4a_float3_t),
        k4a_calibration_type_t,
        k4a_calibration_type_t,
        ctypes.POINTER(k4a_float2_t),
        ctypes.POINTER(ctypes.c_int),
    )

    return _k4a_calibration_3d_to_2d(
        calibration,
        source_point3d_mm,
        source_camera,
        target_camera,
        target_point2d,
        valid,
    )


def k4a_calibration_2d_to_2d(
    calibration: ctypes.POINTER(k4a_calibration_t),
    source_point2d: ctypes.POINTER(k4a_float2_t),
    source_depth_mm: ctypes.c_float,
    source_camera: k4a_calibration_type_t,
    target_camera: k4a_calibration_type_t,
    target_point2d: ctypes.POINTER(k4a_float2_t),
    valid: ctypes.POINTER(ctypes.c_int),
) -> k4a_result_t:
    """
    Transform a 2D pixel coordinate with an associated depth value of the source camera into
    a 2D pixel coordinate of the target camera.

    This function maps a pixel between the coordinate systems of the depth and color cameras.
    It is equivalent to calling `k4a_calibration_2d_to_3d()` to compute the 3D point corresponding
    to `source_point2d` and then using `k4a_calibration_3d_to_2d()` to map the 3D point into
    the coordinate system of the `target_camera`.

    If `source_camera` and `target_camera` are identical, the function immediately sets `target_point2d`
    to `source_point2d` and returns without computing any transformations.

    If `source_point2d` does not map to a valid 2D coordinate in the `target_camera` coordinate system,
    `valid` is set to 0. If it is valid, `valid` will be set to 1. The user should not use the value
    of `target_point2d` if `valid` was set to 0.

    Args:
        calibration (POINTER(k4a_calibration_t)): Location to read the camera calibration obtained
            by `k4a_device_get_calibration()`.
        source_point2d (POINTER(k4a_float2_t)): The 2D pixel in `source_camera` coordinates.
        source_depth_mm (c_float): The depth of source_point2d in millimeters. One way to derive the depth
            value in the color camera geometry is to use the function `k4a_transformation_depth_image_to_color_camera()`.
        source_camera (k4a_calibration_type_t): The current camera.
        target_camera (k4a_calibration_type_t): The target camera.
        target_point2d (POINTER(k4a_float2_t)): The 2D pixel in `target_camera` coordinates.
        valid (POINTER(c_int)): The output parameter returns a value of 1 if the `source_point2d`
            is a valid coordinate in the `target_camera` coordinate system, and will return 0 if the
            coordinate is not valid in the calibration model.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `target_point2d` was successfully written.
            `K4A_RESULT_FAILED` if calibration contained invalid transformation parameters.
            If the function returns `K4A_RESULT_SUCCEEDED`, but `valid` is 0, the transformation
            was computed, but the results in `target_point2d` are outside of the range of valid calibration
            and should be ignored.
    """

    _k4a_calibration_2d_to_2d = k4a_dll.k4a_calibration_2d_to_2d
    _k4a_calibration_2d_to_2d.restype = k4a_result_t
    _k4a_calibration_2d_to_2d.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        ctypes.POINTER(k4a_float2_t),
        ctypes.c_float,
        k4a_calibration_type_t,
        k4a_calibration_type_t,
        ctypes.POINTER(k4a_float2_t),
        ctypes.POINTER(ctypes.c_int),
    )

    return _k4a_calibration_2d_to_2d(
        calibration,
        source_point2d,
        source_depth_mm,
        source_camera,
        target_camera,
        target_point2d,
        valid,
    )


def k4a_calibration_color_2d_to_depth_2d(
    calibration: ctypes.POINTER(k4a_calibration_t),
    source_point2d: ctypes.POINTER(k4a_float2_t),
    depth_image: k4a_image_t,
    target_point2d: ctypes.POINTER(k4a_float2_t),
    valid: ctypes.POINTER(ctypes.c_int),
) -> k4a_result_t:
    """
    Transform a 2D pixel coordinate from color camera into a 2D pixel coordinate of the depth camera.

    This function represents an alternative to `k4a_calibration_2d_to_2d()` if the number of pixels
    that need to be transformed is small. This function searches along an epipolar line in the depth
    image to find the corresponding depth pixel. If a larger number of pixels need to be transformed,
    it might be computationally cheaper to call `k4a_transformation_depth_image_to_color_camera()`
    to get correspondence depth values for these color pixels, then call the function
    `k4a_calibration_2d_to_2d()`.

    If `source_point2d` does not map to a valid 2D coordinate in the `target_camera` coordinate system,
    `valid` is set to 0. If it is valid, `valid` will be set to 1. The user should not use the value
    of `target_point2d` if `valid` was set to 0.

    Args:
        calibration (POINTER(k4a_calibration_t)): Location to read the camera calibration obtained
            by `k4a_device_get_calibration()`.
        source_point2d (POINTER(k4a_float2_t)): The 2D pixel in color camera coordinates.
        depth_image (k4a_image_t): 	Handle to input depth image.
        target_point2d (POINTER(k4a_float2_t)): The 2D pixel in depth camera coordinates.
        valid (POINTER(c_int)): The output parameter returns a value of 1 if the `source_point2d`
            is a valid coordinate in the `target_camera` coordinate system, and will return 0
            if the coordinate is not valid in the calibration model.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `target_point2d` was successfully written.
            `K4A_RESULT_FAILED` if `calibration` contained invalid transformation parameters.
            If the function returns `K4A_RESULT_SUCCEEDED`, but `valid` is 0, the transformation
            was computed, but the results in `target_point2d` are outside of the range of valid
            calibration and should be ignored.
    """

    _k4a_calibration_color_2d_to_depth_2d = k4a_dll.k4a_calibration_color_2d_to_depth_2d
    _k4a_calibration_color_2d_to_depth_2d.restype = k4a_result_t
    _k4a_calibration_color_2d_to_depth_2d.argtypes = (
        ctypes.POINTER(k4a_calibration_t),
        ctypes.POINTER(k4a_float2_t),
        k4a_image_t,
        ctypes.POINTER(k4a_float2_t),
        ctypes.POINTER(ctypes.c_int),
    )

    return _k4a_calibration_color_2d_to_depth_2d(calibration, source_point2d, depth_image, target_point2d, valid)


def k4a_transformation_create(calibration: ctypes.POINTER(k4a_calibration_t)) -> k4a_transformation_t:
    """
    Get handle to transformation handle.

    The transformation handle is used to transform images from the coordinate system of one camera into the other.
    Each transformation handle requires some pre-computed resources to be allocated, which are retained
    until the handle is destroyed.

    The transformation handle must be destroyed with `k4a_transformation_destroy()` when it is no longer to be used.

    Args:
        calibration (POINTER(k4a_calibration_t)): A calibration structure obtained by `k4a_device_get_calibration()`.

    Returns:
        k4a_transformation_t: A transformation handle. A NULL is returned if creation fails.
    """
    # K4A_EXPORT k4a_transformation_t k4a_transformation_create(const k4a_calibration_t *calibration);

    _k4a_transformation_create = k4a_dll.k4a_transformation_create
    _k4a_transformation_create.restype = k4a_transformation_t
    _k4a_transformation_create.argtypes = (ctypes.POINTER(k4a_calibration_t),)

    return _k4a_transformation_create(calibration)


def k4a_transformation_destroy(transformation_handle: k4a_transformation_t) -> None:
    """
    Destroy transformation handle.

    Args:
        transformation_handle (k4a_transformation_t): Transformation handle to destroy.
    """
    # K4A_EXPORT void k4a_transformation_destroy(k4a_transformation_t transformation_handle);

    _k4a_transformation_destroy = k4a_dll.k4a_transformation_destroy
    _k4a_transformation_destroy.restype = None
    _k4a_transformation_destroy.argtypes = (k4a_transformation_t,)

    _k4a_transformation_destroy(transformation_handle)


def k4a_transformation_depth_image_to_color_camera(
    transformation_handle: k4a_transformation_t, depth_image: k4a_image_t, transformed_depth_image: k4a_image_t
) -> k4a_result_t:
    """
    Transforms the depth map into the geometry of the color camera.

    This produces a depth image for which each pixel matches the corresponding pixel coordinates
    of the color camera.

    `depth_image` and `transformed_depth_image` must be of format `K4A_IMAGE_FORMAT_DEPTH16`.

    `transformed_depth_image` must have a width and height matching the width and height of the color
    camera in the mode specified by the `k4a_calibration_t` used to create the `transformation_handle`
    with `k4a_transformation_create()`.

    The contents `transformed_depth_image` will be filled with the depth values derived
    from `depth_image` in the color camera's coordinate space.

    `transformed_depth_image` should be created by the caller using `k4a_image_create()` or
    `k4a_image_create_from_buffer()`.

    Args:
        transformation_handle (k4a_transformation_t): Transformation handle.
        depth_image (k4a_image_t): Handle to input depth image.
        transformed_depth_image (k4a_image_t): Handle to output transformed depth image.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `transformed_depth_image` was successfully written
            and `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_transformation_depth_image_to_color_camera = k4a_dll.k4a_transformation_depth_image_to_color_camera
    _k4a_transformation_depth_image_to_color_camera.restype = k4a_result_t
    _k4a_transformation_depth_image_to_color_camera.argtypes = (
        k4a_transformation_t,
        k4a_image_t,
        k4a_image_t,
    )

    _k4a_transformation_depth_image_to_color_camera(transformation_handle, depth_image, transformed_depth_image)


def k4a_transformation_depth_image_to_color_camera_custom(
    transformation_handle: k4a_transformation_t,
    depth_image: k4a_image_t,
    custom_image: k4a_image_t,
    transformed_depth_image: k4a_image_t,
    transformed_custom_image: k4a_image_t,
    interpolation_type: k4a_transformation_interpolation_type_t,
    invalid_custom_value: ctypes.c_uint32,
) -> k4a_result_t:
    """
    Transforms depth map and a custom image into the geometry of the color camera.

    This produces a depth image and a corresponding custom image for which each pixel matches
    the corresponding pixel coordinates of the color camera.

    `depth_image` and `transformed_depth_image` must be of format `K4A_IMAGE_FORMAT_DEPTH16`.

    `custom_image` and `transformed_custom_image` must be of format `K4A_IMAGE_FORMAT_CUSTOM8`
    or `K4A_IMAGE_FORMAT_CUSTOM16`.

    `transformed_depth_image` and `transformed_custom_image` must have a width and height matching
    the width and height of the color camera in the mode specified by the `k4a_calibration_t` used
    to create the `transformation_handle` with `k4a_transformation_create()`.

    `custom_image` must have a width and height matching the width and height of `depth_image`.

    The contents `transformed_depth_image` will be filled with the depth values derived from `depth_image`
    in the color camera's coordinate space.

    The contents `transformed_custom_image` will be filled with the values derived from `custom_image`
    in the color camera's coordinate space.

    `transformed_depth_image` and `transformed_custom_image` should be created by the caller using
    `k4a_image_create()` or `k4a_image_create_from_buffer()`.

    Using `K4A_TRANSFORMATION_INTERPOLATION_TYPE_LINEAR` for `interpolation_type` could create
    new values to `transformed_custom_image` which do no exist in `custom_image`.
    Using `K4A_TRANSFORMATION_INTERPOLATION_TYPE_NEAREST` will prevent this from happenning
    but will result in a less smooth image.

    Args:
        transformation_handle (k4a_transformation_t): Transformation handle.
        depth_image (k4a_image_t): Handle to input depth image.
        custom_image (k4a_image_t): Handle to input custom image.
        transformed_depth_image (k4a_image_t): Handle to output transformed depth image.
        transformed_custom_image (k4a_image_t): Handle to output transformed custom image.
        interpolation_type (k4a_transformation_interpolation_type_t): Parameter that controls
            how pixels in `custom_image` should be interpolated when transformed to color camera space.
            K4A_TRANSFORMATION_INTERPOLATION_TYPE_LINEAR if linear interpolation should be used.
            K4A_TRANSFORMATION_INTERPOLATION_TYPE_NEAREST if nearest neighbor interpolation should be used.
        invalid_custom_value (c_uint32): Defines the custom image pixel value that should be written to
            `transformed_custom_image` in case the corresponding depth pixel can not be transformed
            into the color camera space.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `transformed_depth_image` and `transformed_custom_image`
            were successfully written and `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_transformation_depth_image_to_color_camera_custom = (
        k4a_dll.k4a_transformation_depth_image_to_color_camera_custom
    )
    _k4a_transformation_depth_image_to_color_camera_custom.restype = k4a_result_t
    _k4a_transformation_depth_image_to_color_camera_custom.argtypes = (
        k4a_transformation_t,
        k4a_image_t,
        k4a_image_t,
        k4a_image_t,
        k4a_image_t,
        k4a_transformation_interpolation_type_t,
        ctypes.c_uint32,
    )

    return _k4a_transformation_depth_image_to_color_camera_custom(
        transformation_handle,
        depth_image,
        custom_image,
        transformed_depth_image,
        transformed_custom_image,
        interpolation_type,
        invalid_custom_value,
    )


def k4a_transformation_color_image_to_depth_camera(
    transformation_handle: k4a_transformation_t,
    depth_image: k4a_image_t,
    color_image: k4a_image_t,
    transformed_color_image: k4a_image_t,
) -> k4a_result_t:
    """
    Transforms a color image into the geometry of the depth camera.

    This produces a color image for which each pixel matches the corresponding pixel coordinates
    of the depth camera.

    `depth_image` and `color_image` need to represent the same moment in time. The depth data will
    be applied to the color image to properly warp the color data to the perspective of the depth camera.

    `depth_image` must be of type `K4A_IMAGE_FORMAT_DEPTH16`. `color_image` must be of format
    `K4A_IMAGE_FORMAT_COLOR_BGRA32`.

    `transformed_color_image` image must be of format `K4A_IMAGE_FORMAT_COLOR_BGRA32`.
    `transformed_color_image` must have the width and height of the depth camera in the mode specified
    by the `k4a_calibration_t` used to create the `transformation_handle` with `k4a_transformation_create()`.

    `transformed_color_image` should be created by the caller using `k4a_image_create()` or
    `k4a_image_create_from_buffer()`.

    Args:
        transformation_handle (k4a_transformation_t): Transformation handle.
        depth_image (k4a_image_t): Handle to input depth image.
        color_image (k4a_image_t): Handle to input color image.
        transformed_color_image (k4a_image_t): Handle to output transformed color image.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `transformed_color_image` was successfully written
            and `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_transformation_color_image_to_depth_camera = k4a_dll.k4a_transformation_color_image_to_depth_camera
    _k4a_transformation_color_image_to_depth_camera.restype = k4a_result_t
    _k4a_transformation_color_image_to_depth_camera.argtypes = (
        k4a_transformation_t,
        k4a_image_t,
        k4a_image_t,
        k4a_image_t,
    )

    return _k4a_transformation_color_image_to_depth_camera(
        transformation_handle, depth_image, color_image, transformed_color_image
    )


def k4a_transformation_depth_image_to_point_cloud(
    transformation_handle: k4a_transformation_t,
    depth_image: k4a_image_t,
    camera: k4a_calibration_type_t,
    xyz_image: k4a_image_t,
) -> k4a_result_t:
    """
    Transforms the depth image into 3 planar images representing X, Y and Z-coordinates of
    corresponding 3D points.

    `depth_image` must be of format `K4A_IMAGE_FORMAT_DEPTH16`.

    The camera parameter tells the function what the perspective of the `depth_image` is.
    If the `depth_image` was captured directly from the depth camera, the value should be
    `K4A_CALIBRATION_TYPE_DEPTH`. If the `depth_image` is the result of a transformation
    into the color camera's coordinate space using `k4a_transformation_depth_image_to_color_camera()`,
    the value should be `K4A_CALIBRATION_TYPE_COLOR`.

    The format of `xyz_image` must be `K4A_IMAGE_FORMAT_CUSTOM`. The width and height of `xyz_image` must
    match the width and height of `depth_image`. `xyz_image` must have a stride in bytes of at least
    6 times its width in pixels.

    Each pixel of the `xyz_image` consists of three int16_t values, totaling 6 bytes. The three int16_t
    values are the X, Y, and Z values of the point.

    `xyz_image` should be created by the caller using `k4a_image_create()` or `k4a_image_create_from_buffer()`.

    Args:
        transformation_handle (k4a_transformation_t): Transformation handle.
        depth_image (k4a_image_t): Handle to input depth image.
        camera (k4a_calibration_type_t): Geometry in which depth map was computed.
        xyz_image (k4a_image_t): Handle to output xyz image.

    Returns:
        k4a_result_t: `K4A_RESULT_SUCCEEDED` if `xyz_image` was successfully written and
            `K4A_RESULT_FAILED` otherwise.
    """

    _k4a_transformation_depth_image_to_point_cloud = k4a_dll.k4a_transformation_depth_image_to_point_cloud
    _k4a_transformation_depth_image_to_point_cloud.restype = k4a_result_t
    _k4a_transformation_depth_image_to_point_cloud.argtypes = (
        k4a_transformation_t,
        k4a_image_t,
        k4a_calibration_type_t,
        k4a_image_t,
    )

    return _k4a_transformation_depth_image_to_point_cloud(transformation_handle, depth_image, camera, xyz_image)


def VERIFY(result, error):
    if result != K4A_RESULT_SUCCEEDED:
        print(error)
        # traceback.print_stack()
        sys.exit(1)
