from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="Path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf", help="OpenCV object tracker type")
args = vars(ap.parse_args())

# Initialize tracker based on OpenCV version
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}

# Check if the tracker type is valid
if args["tracker"] not in OPENCV_OBJECT_TRACKERS:
    raise ValueError(f"Tracker '{args['tracker']}' is not supported.")

tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# Initialize the bounding box coordinates
initBB = None

# Start video stream or read video file
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    is_videostream = True
else:
    vs = cv2.VideoCapture(args["video"])
    is_videostream = False

fps = None
success_frames = 0
total_frames = 0

while True:
    # Grab the current frame
    frame = vs.read()
    frame = frame[1] if not is_videostream else frame

    if frame is None:
        break

    # Resize and get dimensions
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    # If tracking started, update and draw box
    if initBB is not None:
        total_frames += 1
        success, box = tracker.update(frame)
        if success:
            success_frames += 1
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        fps.update()
        fps.stop()

        accuracy = (success_frames / total_frames) * 100 if total_frames > 0 else 0

        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
            ("Accuracy", f"{accuracy:.2f}%")
        ]

        for (i, (k, v)) in enumerate(info):
            text = f"{k}: {v}"
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # Press 's' to select object
    if key == ord("s"):
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()  # reinitialize tracker
        tracker.init(frame, initBB)
        fps = FPS().start()
        # Reset counters when tracking restarts
        success_frames = 0
        total_frames = 0

    # Quit on 'q'
    elif key == ord("q"):
        break

# Final cleanup
if fps is not None:
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
if is_videostream:
    vs.stop()
else:
    vs.release()
