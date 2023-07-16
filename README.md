<h1 align="center"> pykinect-recorder </h1>

<div align="center">
  <a href="https://pypi.python.org/pypi/pykinect-recorder"><img src="https://img.shields.io/pypi/v/pykinect-recorder.svg"></a>
  <a href="https://pypi.org/project/pykinect-recorder"><img src="https://img.shields.io/pypi/pyversions/pykinect-recorder.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</div>

<!-- <br>
<div>

</div> -->

<br>

<div display="flex;">
<img src="https://github.com/unerue/pykinect-recorder/assets/78347296/bb88a4a2-1ed6-490d-9e4e-83353c423401">
</div>

<br>


## Description
The pykinect-recorder is an educational/industrial library that provides sensor recording (including audio), playback, and computer vision soultions through a python wrapper of the Azure Kinect Sensor SDK.

Recording and playback example below.

<img src="https://github.com/unerue/pykinect-recorder/assets/78347296/e6afa357-52b6-4e52-83b0-b95dfe8a0d2e" width="50%" /><img src="https://github.com/unerue/pykinect-recorder/assets/78347296/c9695ccc-b991-4103-bced-34b49bb0f4fd" width="50%" />


## Documentation

You can find the API documentation on our website: https://pykinect-recorder.readthedocs.io/en/latest/index.html.

For details about API for Azure Kinect SDK please see Azure Kinect Sensor SDK github: https://github.com/microsoft/Azure-Kinect-Sensor-SDK.


##  Features

- [x] See RGB, IR, Depth, IMU and Audio data when recoding.
- [x] Control recording option (FPS, brightness, ...).
- [x] Change layout with drag and drop.
- [x] Playback recorded video.
- [ ] 3D reconstruction viewer with streaming/recorded video.
- [ ] Sync devices
- [ ] screen zoom in-out
- [ ] imu, microphone panel redesign
- [ ] Recording audio.
- [ ] Deep learning inference (mediapipe and native) with streaming/recorded video.
- [ ] Intel RealSense 
- [ ] Zenmuse SDK for Python


## Prerequisites

### Environment
- Windows 10 (Recommended).
- Windows 11.

### Install Azure Kinect SDK 
- Make sure you download Azure Kinect SDK before using this repo. 
- SDK version '1.4.1' supported in release 1.0.0.
- You can download Azure Kinect SDK [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md).
    

## Installation
 
### Using pip
```bash
pip install pykinect-recorder
pykinect-recorder
```
