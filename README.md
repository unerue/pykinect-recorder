<h1 align="center"> pykinect-recorder </h1>

<div align="center">
  <a href="https://pypi.python.org/pypi/pykinect-recorder"><img src="https://img.shields.io/pypi/v/pykinect-recorder.svg"></a>
  <a href="https://pypi.org/project/pykinect-recorder"><img src="https://img.shields.io/pypi/pyversions/pykinect-recorder.svg"></a>
</div>

<br>
<div>
The pykinect-recorder is an educational/industrial library that provides sensor recording (including audio), playback, and computer vision soultions through a python wrapper of the Azure Kinect Sensor SDK.
</div>

<br>

<div display="flex;">
<img src="https://github.com/unerue/pykinect-recorder/assets/78347296/6d97602a-7438-4829-8ed2-d46e63919975">
</div>

<br>

## Documentation


You can find the API documentation on our website: https://pykinect-recorder.readthedocs.io/en/latest/index.html

For details about API for Azure Kinect SDK please see Azure Kinect Sensor SDK website: https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html



##  Features

- [x] See RGB, IR, Depth, IMU and Audio data when recoding.
- [x] Control Recording option (FPS, brightness, ...).
- [x] Change layout with drag and drop.
- [x] Playback Recorded video.
- [ ] Recording Audio.
- [ ] 3D Viewer with streaming/recorded video.
- [ ] Deep Learning Inference with streaming/recorded video.
- [ ] Sync multi camera.

<br>

## Prerequisites

### Azure kinect SDK 

- Make sure you download Azure Kinect SDK before using this repo. 
- SDK version '1.4.1' supported in release 1.0.0.
- You can download Azure Kinect SDK [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md).
    
### Anaconda
- Make sure you download Anaconda before using this repo.
- You can download Miniconda [here](https://docs.conda.io/en/latest/miniconda.html).

<br>

## Installation
 
### Anaconda
```bash
conda create -n azure python=3.10 -y
conda activate azure
pip install pykinect-recorder

pykinect
```

<br>

## Features

ML Solutions: native, mediapipe, torchvision
