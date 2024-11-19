#################################################################################################
# This program is made to detect an orange basketball from a set of videos stored in a directory

# The videos are to be stored in the format "video1.mp4" , "video2.mp4" and so on

# The program extracts the frames from the videos and creates directories for each video  
# at the path specified where the detected and discared images are to be stored 

#------------------IMPORTANT NOTE-------------------------
# Define the paths of the directories before using in line 22 , 23 , 24
##################################################################################################
import cv2 
import numpy as np 
import os

count = 0
count_dir1=0
count_dir2=0
while True:
    count = count+1
    
    path = os.path.join(r'XX Insert the path of the folder with the videos XX',f"video{count}.mp4") #Insert path
    dirdetected = os.path.join(r'XX Inset the path where the detected frames are to be stored XX',f"video{count}")  #Insert path
    dirdiscarded = os.path.join(r'XX Inset the path where the discarded frames are to be stored XX',f"video{count}") #Insert path

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
        
        succ,frame = cap.read()
        if not succ: 
            break
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_bound = np.array([0, 100, 80])  
        upper_bound = np.array([10, 180, 160])  
        mask = cv2.inRange(hsv , lower_bound , upper_bound)

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
            
    cap.release()
    cv2.destroyAllWindows()
    

#Test data for texting the accuracy of the algorithm
#Can change the values for re-evaluation

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