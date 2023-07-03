import ctypes

from . import _k4a


class Calibration:
    """
    Wrapper for `k4a_calibration_t`.

    Provides member functions for `k4a_calibration_t`.
    """

    def __init__(self, calibration_handle: _k4a.k4a_calibration_t):
        self._handle = calibration_handle
        self.color_params = self._handle.color_camera_calibration.intrinsics.parameters.param
        self.depth_params = self._handle.depth_camera_calibration.intrinsics.parameters.param

    def __del__(self):
        self.reset()

    def __str__(self):
        message = (
            "Rgb Intrinsic parameters: \n"
            f"\tcx: {self.color_params.cx}\n"
            f"\tcy: {self.color_params.cy}\n"
            f"\tfx: {self.color_params.fx}\n"
            f"\tfy: {self.color_params.fy}\n"
            f"\tk1: {self.color_params.k1}\n"
            f"\tk2: {self.color_params.k2}\n"
            f"\tk3: {self.color_params.k3}\n"
            f"\tk4: {self.color_params.k4}\n"
            f"\tk5: {self.color_params.k5}\n"
            f"\tk6: {self.color_params.k6}\n"
            f"\tcodx: {self.color_params.codx}\n"
            f"\tcody: {self.color_params.cody}\n"
            f"\tp2: {self.color_params.p2}\n"
            f"\tp1: {self.color_params.p1}\n"
            f"\tmetric_radius: {self.color_params.metric_radius}\n"
        )
        return message

    def get_matrix(self, camera: _k4a.k4a_calibration_type_t):
        if camera == _k4a.K4A_CALIBRATION_TYPE_COLOR:
            return [
                [self.color_params.fx, 0, self.color_params.cx],
                [0, self.color_params.fy, self.color_params.cy],
                [0, 0, 1],
            ]
        elif camera == _k4a.K4A_CALIBRATION_TYPE_DEPTH:
            return [
                [self.depth_params.fx, 0, self.depth_params.cx],
                [0, self.depth_params.fy, self.depth_params.cy],
                [0, 0, 1],
            ]

    def is_valid(self):
        return self._handle

    def handle(self):
        return self._handle

    def reset(self):
        if self.is_valid():
            self._handle = None

    # 3D point of source_camera to 3D point of target_camera
    def convert_3d_to_3d(
        self,
        source_point3d: _k4a.k4a_float3_t,
        source_camera: _k4a.k4a_calibration_type_t,
        target_camera: _k4a.k4a_calibration_type_t,
    ) -> _k4a.k4a_float3_t:
        """
        Transform a 3d point of a source coordinate system into a 3d point of the target coordinate system.

        Throws error on failure.

        Note:
            See also `k4a_calibration_3d_to_3d()`.

        Args:
            source_point3d (k4a_float3_t): The 3D coordinates in millimeters representing a point
                in `source_camera`.
            source_camera (k4a_calibration_type_t): The current camera.
            target_camera (k4a_calibration_type_t): The target camera.

        Returns:
            k4a_float3_t: Three dimensional floating point vector.
        """
        target_point3d = _k4a.k4a_float3_t()

        _k4a.VERIFY(
            _k4a.k4a_calibration_3d_to_3d(
                self._handle,
                source_point3d,
                source_camera,
                target_camera,
                target_point3d,
            ),
            "Failed to convert from 3D to 3D",
        )

        return target_point3d

    # 2D depth of source_camera to 3D point of target_camera
    def convert_2d_to_3d(
        self,
        source_point2d: _k4a.k4a_float2_t,
        source_depth: float,
        source_camera: _k4a.k4a_calibration_type_t,
        target_camera: _k4a.k4a_calibration_type_t,
    ) -> _k4a.k4a_float3_t:
        """
        Transform a 2d pixel coordinate with an associated depth value of the source camera
        into a 3d point of the target coordinate system.

        Returns false if the point is invalid in the target coordinate system
        (and therefore target_point3d should not be used) Throws error if calibration contains
        invalid data.

        Args:
            source_point2d (_k4a.k4a_float2_t): The 2D pixel in `source_camera` coordinates.
            source_depth (float): The depth of `source_point2d` in millimeters. One way to derive the
                depth value in the color camera geometry is to use the function `k4a_transformation_depth_image_to_color_camera()`.
            source_camera (_k4a.k4a_calibration_type_t): The current camera.
            target_camera (_k4a.k4a_calibration_type_t): The target camera.

        Returns:
            _k4a.k4a_float3_t: Three dimensional floating point vector.
        """
        target_point3d = _k4a.k4a_float3_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_2d_to_3d(
                self._handle,
                source_point2d,
                source_depth,
                source_camera,
                target_camera,
                target_point3d,
                valid,
            ),
            "Failed to convert from 2D to 3D",
        )

        return target_point3d

    # 3D point of source_camera to 2D pixel of target_camera
    def convert_3d_to_2d(
        self,
        source_point3d: _k4a.k4a_float3_t,
        source_camera: _k4a.k4a_calibration_type_t,
        target_camera: _k4a.k4a_calibration_type_t,
    ) -> _k4a.k4a_float2_t:
        """
        Transform a 3d point of a source coordinate system into a 2d pixel coordinate of the target
        camera.

        Returns false if the point is invalid in the target coordinate system
        (and therefore target_point2d should not be used) Throws error if calibration contains invalid data.

        Args:
            source_point3d (_k4a.k4a_float3_t): The 3D coordinates in millimeters representing
                a point in source_camera.
            source_camera (_k4a.k4a_calibration_type_t): _description_
            target_camera (_k4a.k4a_calibration_type_t): _description_

        Returns:
            _k4a.k4a_float2_t: _description_
        """
        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_3d_to_2d(
                self._handle,
                source_point3d,
                source_camera,
                target_camera,
                target_point2d,
                valid,
            ),
            "Failed to convert from 3D to 2D",
        )

        return target_point2d

    # 2D depth of source_camera to 2D pixel of target_camera
    def convert_2d_to_2d(
        self,
        source_point2d: _k4a.k4a_float2_t,
        source_depth: float,
        source_camera: _k4a.k4a_calibration_type_t,
        target_camera: _k4a.k4a_calibration_type_t,
    ) -> _k4a.k4a_float2_t:
        """


        Args:
            source_point2d (_k4a.k4a_float2_t): _description_
            source_depth (float): _description_
            source_camera (_k4a.k4a_calibration_type_t): _description_
            target_camera (_k4a.k4a_calibration_type_t): _description_

        Returns:
            _k4a.k4a_float2_t: _description_
        """
        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_2d_to_2d(
                self._handle,
                source_point2d,
                source_depth,
                source_camera,
                target_camera,
                target_point2d,
                valid,
            ),
            "Failed to convert from 2D to 2D",
        )

        return target_point2d

    # 2D pixel of color_camera to 2D pixel of depth camera
    def convert_color_2d_to_depth_2d(
        self, source_point2d: _k4a.k4a_float2_t, depth_image: _k4a.k4a_image_t
    ) -> _k4a.k4a_float2_t:
        target_point2d = _k4a.k4a_float2_t()
        valid = ctypes.c_int()

        _k4a.VERIFY(
            _k4a.k4a_calibration_color_2d_to_depth_2d(self._handle, source_point2d, depth_image, target_point2d, valid),
            "Failed to convert from Color 2D to Depth 2D",
        )

        return target_point2d
