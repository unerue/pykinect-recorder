import sys
import pytest
from pykinect_recorder.pyk4a._pyk4a import pykinect
from pykinect_recorder.pyk4a._pyk4a.k4a import _k4a
from pykinect_recorder.pyk4a._pyk4a.k4a import _k4atypes


def test_setup_library():
    """
    Check Azure Kinect SDK installed in execution environment.

    Azure kinect SDK can be installed in 'Linux', 'Windows'.

    The function operates automatically according to the execution environment.
    """
    assert pykinect.initialize_libraries() == True


def test_device_open():
    """
    Check the connection between desktop and Azure Kinect Camera.
    """
    device_handle = _k4atypes.k4a_device_t
    assert _k4a.k4a_device_open(0, device_handle) == _k4atypes.K4A_RESULT_SUCCEEDED


if __name__ == "__main__":
    test_setup_library()
    test_device_open()
