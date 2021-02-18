import cv2

# capture webcam
video = cv2.VideoCapture(0)

while True:
    # grab a frame
    check, frame = video.read()

    # use grayscale images to increase accuracy in face recognition
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show frame in a window
    cv2.imshow("Capturing", gray_frame)

    # wait for 1ms and break loop if user press 'q'
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# release camera and close windows at the end
video.release()
cv2.destroyAllWindows()
