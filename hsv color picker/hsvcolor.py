import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("COLOR PICKER")
cv2.createTrackbar("LH","COLOR PICKER",0,179,nothing)
cv2.createTrackbar("LS","COLOR PICKER",0,255,nothing)
cv2.createTrackbar("LV","COLOR PICKER",0,255,nothing)
cv2.createTrackbar("UH","COLOR PICKER",0,179,nothing)
cv2.createTrackbar("US","COLOR PICKER",0,255,nothing)
cv2.createTrackbar("UV","COLOR PICKER",0,255,nothing)


cap = cv2.VideoCapture(0)

while True:
    succ,frame = cap.read()
    if not succ:
        break

    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    lh = cv2.getTrackbarPos("LH","COLOR PICKER")
    ls = cv2.getTrackbarPos("LS","COLOR PICKER")
    lv = cv2.getTrackbarPos("LV","COLOR PICKER")
    uh = cv2.getTrackbarPos("UH","COLOR PICKER")
    us = cv2.getTrackbarPos("US","COLOR PICKER")
    uv = cv2.getTrackbarPos("UV","COLOR PICKER")

    lower = np.array([lh,ls,lv])
    upper = np.array([uh,us,uv])

    mask = cv2.inRange(hsv,lower,upper)
    objected = cv2.bitwise_and(frame,frame,mask=mask)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord("s"):
        arrayhsv = [(lh,ls,lv),(uh,us,uv)]
        print(arrayhsv)
    cv2.imshow("Feed",frame)
    cv2.imshow("Mask",mask)
    cv2.imshow("Objected",objected)

cap.release()
cv2.destroyAllWindows()