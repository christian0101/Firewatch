# Main.py - Fire detection using OpenCV
# Cristian Sorescu 879091

import numpy as np
import cv2
from videocaptureasync import VideoCaptureAsync
import time
import copy
import sys

# trained fire clssifier
# source: https://electronicsforu.com/electronics-projects/prototypes/image-processing-fire-extinguisher-arduino
fire_cascade = cv2.CascadeClassifier('fire_classifier.xml')

cap = VideoCaptureAsync(0)
cap.start()
time.sleep(2.0)

isFireDetected = None

t4 = time.strftime("%Y%m%d-%H%M%S")
bbox = open("logData/blackbox_" + t4 + ".txt", "w+")

# log
def log(msg_lvl = "info", msg = ""):
    st = time.strftime('%Y-%m-%d %H:%M:%S')

    white_text = "\033[0;0;40m"
    green_text = "\033[1;32;40m"
    yellow_text = "\033[0;33;40m"
    red_text = "\033[1;31;40m"
    
    timestamp = "[{0}]".format(st)

    # format message based on type
    msg_type = ("{0}[Warning]{1}".format(yellow_text, red_text),
                "{0}[INFO]{1}".format(white_text, green_text))[msg_lvl == "info"]

    print("{0}{1} {2} {3}".format(white_text, timestamp, msg_type, msg))

    # write to blackbox
    _log = "{0} {1}\n".format(timestamp, msg)
    bbox.write(_log)

    # return formated message
    return _log

# operate on live feed
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # t0 record initial time
    t0 = time.clock()

    # analyse frame for fire
    fire = fire_cascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # t0 and t1 are used to calculate time taken to detect fire
    t1 = time.clock() - t0

    # no fire(s) detected
    if len(fire) <= 0:
        if isFireDetected or isFireDetected is None:
            '''
            t3 = time.strftime("%Y%m%d-%H%M%S")
            # save frame for documentation
            cv2.imwrite("logData/" + t3 + "_no_fire-frame.jpg", frame)

            nf = open("logData/" + t3 + "_log.txt", "w+")
            nf.write(log("info", "No Fire Detected"))
            '''

            log("info", "No Fire Detected")
            isFireDetected = False
    else:
        # Draw a rectangle around the fire
        for (x, y, w, h) in fire:
            before = copy.deepcopy(frame)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if not isFireDetected or isFireDetected is None:
                t3 = time.strftime("%Y%m%d-%H%M%S")
                # save frame for documentation
                cv2.imwrite("logData/" + t3 + "_before-frame.jpg", before)
                cv2.imwrite("logData/" + t3 + "_after-frame.jpg", frame)

                f = open("logData/" + t3 + "_log.txt", "w+")
                f.write(log("warning", "Fire Detected within {:.2f} seconds!".format(t1)))
                isFireDetected = True

    # do not show live feed if requested
    if len(sys.argv) > 1:
        if not sys.argv[1] == "--no-feed":
            # Display the resulting frame
            cv2.imshow('Live Feed', frame)
    else:
        # Display the resulting frame
        cv2.imshow('Live Feed', frame)

    # if "q" pressed terminate
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.stop()
cv2.destroyAllWindows()
