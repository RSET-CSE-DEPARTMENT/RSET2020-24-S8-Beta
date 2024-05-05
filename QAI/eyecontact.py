import eye_game
import os
import cv2
from os import listdir
folder_dir = "data"
result=0
count=0
eyepos=""
for images in os.listdir(folder_dir):
    # check if the image ends with png
    if (images.endswith(".jpg")):
        count=count+1
        img = (folder_dir+"/"+images) 
        # print(folder_dir+"/"+images)
        # print(eye_game.get_gaze_direction(img))
        eyepos=(eye_game.get_gaze_direction(img))
        if(eyepos=="center" or eyepos =="down"):
          result=result+1
print(result)
print(result/count*100)




