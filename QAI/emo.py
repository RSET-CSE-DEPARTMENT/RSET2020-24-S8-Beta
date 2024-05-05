# import the required modules 
import cv2 
import matplotlib.pyplot as plt 
from deepface import DeepFace 
import os
from os import listdir
import numpy as np
import PIL
def emotion():
    x=0
    # get the path/directory
    folder_dir = "data"
    result=0
    ls=[]
    for images in os.listdir(folder_dir):
    
        # check if the image ends with png
        if (images.endswith(".jpg")):
            # pil_image = PIL.Image.open(folder_dir+"/"+images).convert('RGB')
            # open_cv_image = np.array(pil_image)
            # # Convert RGB to BGR
            # images = open_cv_image.copy()
    # read image 
            img = cv2.imread(folder_dir+"/"+images) 
            print(folder_dir+"/"+images)
    # call imshow() using plt object 
    # plt.imshow(img[:,:,::-1]) 

    # # display that image 
    # plt.show() 

    # storing the result 
            try:
                result = DeepFace.analyze(img,actions=['emotion']) 
                x+=1
                ls+=[result[0]]
            except ValueError:
                print('no face')

    # print result 
            print(result) 
    emotion_counts = {}
    for entry in ls:
        # Extract the 'dominant_emotion' value
        dominant_emotion = entry.get('dominant_emotion')
        
        # Increment the count for the dominant_emotion in emotion_counts
        emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1

    # Print the results
    print("Emotion counts:")
    total=0
    out={}
    for emotion, count in emotion_counts.items():
        total+=count
        # print(f"{emotion}: {count}")
    for emotion, count in emotion_counts.items():
        print(f"{emotion}: {(count/total)*100}%")
        out[emotion]=count/total*100
    return out
        