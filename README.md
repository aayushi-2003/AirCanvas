# Air Canvas using OpenCV and MediaPipe
This project implements an Air Canvas using OpenCV and MediaPipe libraries in Python. It allows users to interact with a virtual canvas interface to draw using several colors and pen size.

## Features

1. Hand Tracking: Utilizes the MediaPipe library to detect and track the user's hand movements in real-time.
3. Draw in the Air: Utilizes the index finger as a virtual pen to create artwork in the air.
4. Customization: Choose from a variety of colors and pen sizes to customize the drawing.

## Modules
1. HandTracking.py
This module contains the implementation of hand tracking functionality using the MediaPipe library. It provides methods to detect and track the user's hand landmarks in real-time video streams from a webcam.

2. AirCanvas.py
The AirCanvas.py module implements the Air Canvas interface using OpenCV. It utilizes the hand tracking module to enable users to interact with the canvas using hand gestures.boxe

3. RectBoxes.py
Contains class to create boxes for the AirCanvas module using OpenCV.

## Requirements
1. Python 3.8
2. OpenCV 4.9.0.80
3. MediaPipe 0.10.9
4. autopy 4.0.0

## Installation
Install the required dependencies:
```sh
pip install -r requirements.txt
```

## Usage
1. Run the AirCanvas.py script:
``` sh
python virtualkeyboard.py
```
2. Ensure your webcam is connected and properly configured.
3. You can use your index finger to toggle buttons and draw on the canvas (board). Use middle and index fingers together over the board to pause drawing and move around.
