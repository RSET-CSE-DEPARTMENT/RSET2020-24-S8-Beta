import threading
import argparse
import sys
import time
import datetime
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils1
import pygame
import firebase_admin
from firebase_admin import credentials, db
from pynput import keyboard
import time
#modules for tracking
from pyfirmata import Arduino, SERVO
from signal import pause
from time import sleep

# Constants
centre_x = 640 // 2
centre_y = 480 // 2
DELAY_TIME = 20  # Delay time in seconds before storing detection again
currentpan=90
currenttilt=90
angle_adjustment_enabled = False  # Track whether angle adjustment is enabled
# Load the audio file for 'Elephant'
ELEPHANT_AUDIO_FILE = 'Beesound.mp3'  # Change this to your audio file
# Initialize pygame mixer000
pygame.mixer.init()

# Initialize Firebase
cred = credentials.Certificate('/home/pi/objectdetection1/credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://tranqiscan-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# Dictionary to keep track of last detection time for each animal
last_detection_times = {}


port='/dev/ttyACM0'
panpin=8
tiltpin=7
board=Arduino(port)
board.digital[panpin].mode=SERVO
board.digital[tiltpin].mode=SERVO
m_pressed = False  # Track whether 'm' key has been pressed
def on_press(key):
    global m_pressed,currentpan,currenttilt
    print(key,type(key),"in\n\n\n\n\n\n")
    if key == keyboard.Key.left and m_pressed:
        # Decrease angle from current value to 0 while left is held down
        print("1\n\n\n\n\n\n")
        if currentpan > 0:
            currentpan -= 1
            board.digital[panpin].write(currentpan)
    elif key == keyboard.Key.right and m_pressed:
        # Increase angle from current value to 180 while right is held down
        print("2\n\n\n\n\n\n")
        if currentpan < 180:
            currentpan += 1
            board.digital[panpin].write(currentpan)
    elif key == keyboard.Key.down and m_pressed:  
        # Decrease angle from current value to 0 while down is held down
        print("3\n\n\n\n\n\n")
        if currenttilt > 0:
            currenttilt -= 1
            board.digital[tiltpin].write(currenttilt)
    elif key == keyboard.Key.up and m_pressed:
        # Increase angle from current value to 180 while up is held down
        print("4\n\n\n\n\n\n")
        if currenttilt < 180:
            currenttilt += 1
            board.digital[tiltpin].write(currenttilt)
    if hasattr(key, 'char'):
        if key.char == 'm':
            print("1\n\n\n\n\n\n")
        # Toggle m_pressed when 'm' is pressed
            m_pressed = not m_pressed
            print("Starting angle adjustment..." if m_pressed else "Stopping angle adjustment...")
listener = keyboard.Listener(on_press=on_press)

def store_animal_detection(animal):
    # Reference to the Firebase Realtime Database
    ref = db.reference('/Animal_detections')

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Push the detection information to the database
    ref.push({
        'Breed': animal,
        'Timestamp': current_datetime
    })


def play_audio():
    print("Elephant detected! Playing audio...")
    pygame.mixer.music.load(ELEPHANT_AUDIO_FILE)
    pygame.mixer.music.play()
    time.sleep(15)  # Sleep for 15 seconds
    pygame.mixer.music.stop()  # Stop the audio after 15 seconds


def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool, elephant_audio: str) -> None:
    """Continuously run inference on images acquired from the camera."""

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Initialize the object detection model
    base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(max_results=1, score_threshold=0.65)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

        counter += 1

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)
        detections = detection_result.detections

        # Draw circle at the center of the screen
        cv2.circle(image, (centre_x, centre_y), 5, (0, 0, 0), -1)

        if True:
            for detection in detections:
                for category in detection.categories:
                    detected_animal = category.category_name  # Change this based on your use case

                # Check if it's the first detection or if 20 seconds have passed since the last detection of this animal
                    if detected_animal not in last_detection_times or time.time() - last_detection_times[detected_animal] >= DELAY_TIME:
                    # Store the detection
                        store_animal_detection(detected_animal)
                        last_detection_times[detected_animal] = time.time()

                        if detected_animal == 'Elephant':
                        # Play audio in a separate thread
                            print("Elephant detected! Playing audio...")
                            audio_thread = threading.Thread(target=play_audio)
                            audio_thread.start()
                bounding_box = detection.bounding_box
                boxcentre_x = int(bounding_box.origin_x + (bounding_box.width / 2))
                boxcentre_y = int(bounding_box.origin_y + (bounding_box.height / 2))
                # Draw circle at the center of the bounding box
                cv2.circle(image, (boxcentre_x, boxcentre_y), 5, (0, 255, 0), -1)
                if(not m_pressed):
                    if(centre_x - boxcentre_x>0):
                        currentpan=90+((centre_x-boxcentre_x)//3)
                        board.digital[panpin].write(currentpan)
                    elif(centre_x - boxcentre_x<0):
                        currentpan=90-((boxcentre_x-centre_x)//3)
                        board.digital[panpin].write(currentpan)
                    if(centre_y- boxcentre_y>0):
                        currenttilt=90+((centre_y-boxcentre_y)//2)
                        board.digital[tiltpin].write(currenttilt)
                    elif(centre_y - boxcentre_y<0):
                        currenttilt=90-((boxcentre_y-centre_y)//2)
                        board.digital[tiltpin].write(currenttilt)         
                # Print bounding box centre and how much its offset from cenwtre of screen
                    print("Pan Angle, Tilt Angle:", currentpan, "    ",currenttilt,"\n\n\n\n\n\n")
                    print("Offset coordinates (x, y):", centre_x - boxcentre_x, ",", centre_y - boxcentre_y)

        # Draw keypoints and edges on input image
        image = utils1.visualize(image, detection_result)

        # Show the FPS
        if counter % 10 == 0:  # Update FPS every 10 frames
            end_time = time.time()
            fps = 10 / (end_time - start_time)
            start_time = time.time()

        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (24, 20)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 0, 255), 1)

        # Display the image
        cv2.imshow('object_detector', image)
        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    listener.start()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='Path of the object detection model.', required=False, default='best.tflite')
    parser.add_argument('--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument('--frameWidth', help='Width of frame to capture from camera.', required=False, type=int,
                        default=640)
    parser.add_argument('--frameHeight', help='Height of frame to capture from camera.', required=False, type=int,
                        default=480)
    parser.add_argument('--numThreads', help='Number of CPU threads to run the model.', required=False, type=int,
                        default=4)
    parser.add_argument('--enableEdgeTPU', help='Whether to run the model on EdgeTPU.', action='store_true',
                        required=False, default=False)
    parser.add_argument('--elephantAudio', help='Path of the audio file to play when Elephant is detected.',
                        required=False, default='/home/pi/objectdetection1/Beesound.mp3')  # Change this to your audio file
    args = parser.parse_args()
    run(args.model, args.cameraId, args.frameWidth, args.frameHeight, args.numThreads, args.enableEdgeTPU,
        args.elephantAudio)
    
if __name__ == '__main__':
    main()

