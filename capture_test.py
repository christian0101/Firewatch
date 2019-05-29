# Video capture async test
# Compare default, single threaded, video capture to async, multi threaded, video capture
#
# Cristian Sorescu 879091

import cv2
from videocaptureasync import VideoCaptureAsync
import time
import os
from imutils.video import FPS

fire_cascade = cv2.CascadeClassifier('fire_classifier.xml')

# regular cv2 video capture, no threading
video = cv2.VideoCapture(0)
print("[INFO] Sampling frames from `cv.VideoCapture` module, no threading...")
time.sleep(2.0)

isFireDetected = None
fps = FPS().start()
frames = 0

# capture 30 frames
while(frames < 30):
    # Capture frame-by-frame
    ret, frame = video.read()

    # Our operations on the frame come here
    # gray image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # analyse frame for fire
    fire = fire_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(fire) <= 0:
        if isFireDetected or isFireDetected is None:
            print ("\033[1;32;40m No Fire Detected")
            isFireDetected = False
    else:
        # Draw a rectangle around the fire
        for (x, y, w, h) in fire:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if not isFireDetected or isFireDetected is None:
                print("\033[1;31;40m Fire Detected!")
                isFireDetected = True

    frames = frames + 1

video.release()
fps.stop()

os.system('tput init')
print("[INFO] Time elapsed for 30 frames: {:.2f}".format(fps.elapsed()))

# threaded video capture
video = VideoCaptureAsync(0)
video.start()
print("[INFO] Sampling threaded frames from `VideoCaptureAsync` module...")
time.sleep(2.0)

isFireDetected = None
fps = FPS().start()
frames = 0

# capture 30 frames
while(frames < 30):
    # Capture frame-by-frame
    ret, frame = video.read()

    # Our operations on the frame come here
    # gray image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # analyse frame for fire
    fire = fire_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(fire) <= 0:
        if isFireDetected or isFireDetected is None:
            print ("\033[1;32;40m No Fire Detected")
            isFireDetected = False
    else:
        # Draw a rectangle around the fire
        for (x, y, w, h) in fire:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if not isFireDetected or isFireDetected is None:
                print("\033[1;31;40m Fire Detected!")
                isFireDetected = True
                
    frames = frames + 1

video.stop()
fps.stop()

os.system('tput init')
print("[INFO] Time elapsed for 30 frames: {:.2f}".format(fps.elapsed()))
