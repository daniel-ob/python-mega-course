import time
from datetime import datetime

import cv2
import pandas

from plotting import plot


# configuration
CAM_STABILISATION_ENABLED = True
PLOTTING_ENABLED = True
LOG_FILENAME = "log.csv"
PLOT_FILENAME = "plot.html"

background = None
presence_hist = [0, 0]
log = []
log_df = pandas.DataFrame(columns=["Enter", "Exit"])

# capture webcam
video = cv2.VideoCapture(0)

if CAM_STABILISATION_ENABLED:
    # stabilize webcam image for 5s at startup
    for i in range(10):
        check, frame = video.read()
        time.sleep(0.5)

while True:
    presence = 0

    # grab a frame
    check, frame = video.read()

    # convert frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Gaussian Blurring of frame
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # store first frame as background image
    if background is None:
        background = gray
        continue

    # background subtraction
    delta = cv2.absdiff(background, gray)

    # apply a threshold
    ret, thresh = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)
    # smooth threshold: remove holes
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # filter out contours with area smaller than 10000 px
        if cv2.contourArea(contour) < 10000:
            continue
        # if a contour is found, there is presence on image
        presence = 1
        # calculate minimal up-right bounding rectangle for contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # draw a green rectangle around contour (frame, corner1, corner2, color, thickness)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # update presence history
    presence_hist.append(presence)

    # record time when objects enter and exit the frame
    if presence_hist[-1] != presence_hist[-2]:
        log.append(datetime.now())

    # show image in a window
    # cv2.imshow("Gray", gray)
    # cv2.imshow("Delta", delta)
    # cv2.imshow("Thresh", thresh)
    cv2.imshow("Color", frame)

    # wait for 1ms and break loop if user press 'q'
    key = cv2.waitKey(1)
    if key == ord("q"):
        # if an object is present, record exit time before closing
        if presence:
            log.append(datetime.now())
        break

# Save log in a CSV file using a pandas DataFrame
for i in range(0, len(log), 2):
    # add a row to DF
    log_df = log_df.append({"Enter": log[i], "Exit": log[i+1]}, ignore_index=True)
log_df.to_csv(LOG_FILENAME)

if PLOTTING_ENABLED:
    # Shows a plot of the log and saves it to a html file
    plot(log_df, PLOT_FILENAME)

# release camera and close windows at the end
video.release()
cv2.destroyAllWindows()
