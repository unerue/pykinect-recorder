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
<img src="https://github.com/unerue/pykinect-recorder/assets/78347296/d875ad2c-03e3-4762-a0a1-80df63ea49fc">
</div>

<br>

##  Features

- [x] See RGB, IR, Depth, IMU and Audio data when recoding.
- [x] Control Recording option (FPS, brightness, ...).
- [x] Change layout with drag and drop.
- [x] Playback Recorded video.
- [ ] Recording Audio.
- [ ] 3D Viewer with streaming/recording.
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

## Installation<hr>
 
### Anaconda
```bash
conda create -n azure python=3.8 -y
conda activate azure
pip install pykinect-recorder

pykinect
```

<br>

## Features

ML Solutions: native, mediapipe, torchvision
