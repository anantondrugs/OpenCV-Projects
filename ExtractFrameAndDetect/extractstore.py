import cv2 
import os

count = 0
count1 = 0

def directory(path1 , path2):
    while True:
        global count1
        count1 = count1 + 1

        finalpath = os.path.join(path1 , f"video{count1}.mp4")
        cap = cv2.VideoCapture(finalpath)

        if not os.path.exists(finalpath):
            break
        
        finaldir = os.path.join(path2 , f"video{count1}")
        os.makedirs(finaldir)
        count=0
        while True:
            succ , frame = cap.read()
            if not succ:
                break

            os.chdir(finaldir)
            cv2.imshow("Framed",frame)
            count = count+1
            cv2.imwrite(f"image{count}.jpg",frame)

            if cv2.waitKey(3) == ord("q"):
                break
    cv2.destroyAllWindows()
    cap.release()


