import subprocess
import os
import time
# Install necessary packages
subprocess.run(['pip', 'install', '--upgrade', 'opencv-python'])
subprocess.run(['pip', 'install', 'keyboard'])

# Change working directory to the YOLOv5 repository
os.chdir('yolov7-custom')

# Install YOLOv5 requirements
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Print current working directory
print(os.getcwd())

        
 # Start YOLOv5 detection in a separate process
process = subprocess.Popen(['python', 'detect.py', '--weights', 'yolov7-custom.pt', '--conf', '0.5', '--img-size', '640', '--source', 'knife.mp4', '--view-img'])

