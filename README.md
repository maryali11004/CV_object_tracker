# Real time object tracker 
Using OpenCV Ready  object tracking Implementations , this program allows the user to select the object to be tracked using either the camera or a video and tracking results , accuracy and fps will be shown in real time.

## Implementation Details

- The project uses OpenCV’s built-in tracking algorithms. The default tracker is KCF, but others like CSRT or MOSSE can be selected via command-line arguments.
- The user selects an object in the first frame using a mouse-drawn bounding box (via `cv2.selectROI`).
- Once the object is selected, the tracker is initialized and continuously updated on each video frame using `tracker.update()`.
- Real-time video capture is handled with `imutils.video.VideoStream`, and performance is measured using `imutils.video.FPS`.
- The tracker displays a bounding box around the object and shows FPS on the screen during live tracking.
- The script supports both webcam input and video file input via command-line arguments.

##  Usage
- Run with webcam:
```bash
python object_tracker.py --tracker kcf
```
- Run with video File:
```
python object_tracker.py --video path/to/video.mp4 --tracker csrt
```
- After running the command in your terminal:
  - **Press s** To stop the video.
  - Select the object using the bounding box
  - **Press space** to apply it
  -**Press q** to quit the program
## Rrquirements:
Before running the program , make sure you have the following requiremets -->
- `OpenCV`
- `imutils`
- Python3.6+
