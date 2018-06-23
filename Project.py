import argparse
import datetime
import imutils
import time
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

camera = cv2.VideoCapture('Walk1.mpg')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
print camera.grab()
firstFrame = None
while(camera.isOpened()):

    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    out.write(frame)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    _, contours, _= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.imshow("Main Video", frame)
    cv2.imshow("Threshed Image", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(35) & 0xFF
    if key == ord("q"):
        break
        

camera.release()
out.release()
cv2.destroyAllWindows()
