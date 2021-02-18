import cv2
import time

background = None

# capture webcam
video = cv2.VideoCapture(0)

# stabilize webcam image for 5s at startup
for i in range(10):
    check, frame = video.read()
    time.sleep(0.5)

while True:
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
        # calculate minimal up-right bounding rectangle for contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # draw a green rectangle around contour (frame, corner1, corner2, color, thickness)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # show image in a window
    # cv2.imshow("Gray", gray)
    # cv2.imshow("Delta", delta)
    # cv2.imshow("Thresh", thresh)
    cv2.imshow("Color", frame)

    # wait for 1ms and break loop if user press 'q'
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# release camera and close windows at the end
video.release()
cv2.destroyAllWindows()
