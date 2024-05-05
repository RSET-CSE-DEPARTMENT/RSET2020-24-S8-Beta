import os
import eye_game
import os
import cv2
from os import listdir
mysp=__import__("my-voice-analysis")

def confidence():
    result=0
    count=0
    sc=0
    eyepos=""
    folder_dir = "data"
    try:
        for images in os.listdir(folder_dir):
        # check if the image ends with png
            if (images.endswith(".jpg")):
                count=count+1
                img = (folder_dir+"/"+images) 
                # print(folder_dir+"/"+images)
                # print(eye_game.get_gaze_direction(img))
                try:
                    eyepos=(eye_game.get_gaze_direction(img))
                    if(eyepos=="center" or eyepos =="down"):
                        result=result+1
                except AssertionError:
                    print('no face')
        print(result)
        sc1=result/count*100
        if sc1>80:
            sc=5
        elif sc1>60:
            sc=4
        elif sc1>40:
            sc=3
        elif sc1>20:
            sc=2
        else:
            sc=1
    except ZeroDivisionError:
        print("Zero division error")
    except AssertionError:
        print('no face')
    
    print("Eye contact Score: ",sc)
    c= r"C:/rajagiri/final_year_project/front_end_trial/data"
    wav_files = [file for file in os.listdir(c) if file.endswith(".wav")]
    print(wav_files)
    i=1
    score=0
    length=len(wav_files)
    for wav_file in wav_files:
            p=wav_file[0:-4]
            print(p)
            try:
                speaking=mysp.myspst(p,c)
                original=mysp.myspod(p,c)
                print("Speaking duration: ",speaking)
                print("Original duration: ",original)
                if(original/speaking>=2):
                    score+=1
                elif(original/speaking>=1.75):
                    score+=2
                elif(original/speaking>=1.5):
                    score+=3
                elif(original/speaking>=1.25):
                    score+=4
                elif(original/speaking>=1):
                    score+=5
                rate=mysp.myspatc(p,c)
                if rate<=2:
                    score+=1
                elif rate<3:
                    score+=2
                elif rate==3:
                    score+=3
                elif rate<=4:
                    score+=4
                else:
                    score+=5
            except ZeroDivisionError:
                print("Zero division error")
            i+=1
    vsc=round(score/(length*2))
    print("Voice confidence Score: ",vsc)
    print("Final Confidence Score: ",round(0.7*vsc+0.3*sc))
    return round(0.7*vsc+0.3*sc)
# print(confidence())