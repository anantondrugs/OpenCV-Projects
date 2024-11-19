# from ExtractFrameAndDetect.extractstore import directory as sort
import cv2 
import numpy as np 
import os




# path1 = r'C:\ROBOCON\OpenCV\sort&detect\data\videos'
# path2 = r'C:\ROBOCON\OpenCV\sort&detect\data\images'
# sort(path1 , path2)



count = 0
count_dir1=0
count_dir2=0
while True:
    count = count+1
    
    # path = os.path.join(r'C:\ROBOCON\OpenCV\sort&detect\data\images',f"video{count}")
    path = os.path.join(r'C:\ROBOCON\OpenCV\sort&detect\data\videos',f"video{count}.mp4")
    dirdetected = os.path.join(r'C:\ROBOCON\OpenCV\sort&detect\data\detected images',f"video{count}")
    dirdiscarded = os.path.join(r'C:\ROBOCON\OpenCV\sort&detect\data\discarded images',f"video{count}")

    if not os.path.exists(path):
        break
    
    if not os.path.exists(dirdetected):
        os.makedirs(dirdetected)

    if not os.path.exists(dirdiscarded):
        os.makedirs(dirdiscarded)
    cap = cv2.VideoCapture(path)
    count1=0
    count_dir1=0
    count_dir2=0
    while True:
        # Read image. 
        # count1 = count1+1
        # finalpath = os.path.join(path,f"image{count1}.jpg")
        # if not os.path.exists(finalpath):
        #     break
        # frame = cv2.imread(finalpath)
        
        succ,frame = cap.read()
        if not succ: 
            break
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_bound = np.array([0, 100, 80])  # Lower bound for orange
        upper_bound = np.array([10, 180, 160])  
        mask = cv2.inRange(hsv , lower_bound , upper_bound)

        # Blur using 5 * 5 kernel. 
        blurred = cv2.blur(mask,(5,5)) 
         
        detected_circles = cv2.HoughCircles(blurred, 
                        cv2.HOUGH_GRADIENT, 1, 100, param1 = 100, 
                    param2 = 18, minRadius = 40, maxRadius = 100) 

        # Draw circles that are detected. 
        if detected_circles is not None: 

            # Convert the circle parameters a, b and r to integers. 
            detected_circles = np.uint16(np.around(detected_circles)) 

            for pt in detected_circles[0, :]: 
                a, b, r = pt[0], pt[1], pt[2] 

                # Draw the circumference of the circle. 
                cv2.circle(frame, (a, b), r, (0, 255, 0), 2) 

                # Draw a small circle (of radius 1) to show the center. 
                cv2.circle(frame, (a, b), 1, (0, 0, 255), 3) 
            count_dir1 = count_dir1+1
            os.chdir(dirdetected)
            cv2.imwrite(f"image{count_dir1}.jpg",frame)
        else:
            count_dir2=count_dir2+1
            os.chdir(dirdiscarded)
            cv2.imwrite(f"image{count_dir2}.jpg",frame)
        cv2.imshow("Detected Circle", frame)  
        cv2.imshow("Blurred",blurred)    
        if cv2.waitKey(10) == ord('q'):
            break
            

    cv2.destroyAllWindows()
    falsepositive = 0
    falsenegative = 30
    truepositive = 112
    truenegative= 185

accuracy = (truepositive+truenegative)/(falsenegative+falsepositive+truenegative+truepositive)
print("Accuracy: ",accuracy*100)
print("True Positive% : ",(truepositive/(truepositive+falsenegative))*100)
print("True Negative% : ",(truenegative/(truenegative+falsepositive))*100)
print("False Positive: ",(falsepositive/(truepositive+falsenegative))*100)
print("False Negative: ",(falsenegative/(truenegative+falsepositive))*100)