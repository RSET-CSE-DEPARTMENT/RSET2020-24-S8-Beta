import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO
from yolov5 import detect
#cap = cv2.VideoCapture('0')
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='D:/Studies/project/FInal_year/yolov5/data/new_best.pt') #'D:/Studies/project/FInal_year/yolov5/data/new_best.pt'
detect.run('D:/Studies/project/FInal_year/yolov5/data/new_best.pt','0') #https://youtu.be/ydn2x5ima8o?si=aOypNWTTxL4NhPlEq
   # Display frame
# while True:
#     ret,frame = cap.read()
#     print(ret)
#     if ret is True:
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = model(frame)
#         print(results)
#         for image in results.render():
#             fig, ax = plt.subplots(figsize=(16, 12))
#             ax.imshow(image)
#             plt.show()
#             cv2.imshow("frame",frame)
#
#         #
#         #     #Press Q on keyboard to  exit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break
#     #     #When everything done, release the video capture object
# cap.release()
#     #
#     # #Closes all the frames
# cv2.destroyAllWindows()
