## Overwatch AimBot Detection

This project is designed to detect enemies in Overwatch gameplay videos and calculate suspicion scores for potential AimBot usage. The system uses YOLOv5 for object detection and tracks aim movements to identify abnormal behaviors indicative of AimBot use.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Unrealized features](#unrealized-features)

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aimbot_detection.git
   cd overwatch-aimbot-detection

## Usage
1. Prepare your video

    Place your Overwatch gameplay video in the video directory.
    Update the video_path variable in main.py to point to your video file.

2. Run the detection
1. **run**
   ```bash
    python aim_check.py

The processed frames will be saved in the output_frames directory, and the video will be displayed with overlays showing detection results and suspicion scores.

## Unrealized features
Cheat detection for multiple games and different cheats
