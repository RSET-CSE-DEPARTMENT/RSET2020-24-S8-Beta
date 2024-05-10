# app1.py

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
import mediapipe as mp

app = Flask(__name__)

@app.route('/')
def home1():
    return render_template('home1.html')

@app.route('/signin.html')
def signin():
    return render_template('signin.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/vid1.html')
def vid1():
    return render_template('vid1.html')

# Video processing and pose estimation endpoint
@app.route('/process_poses', methods=['POST'])
def process_poses():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file uploaded'})

        video_file = request.files['video']

        # Read the video file
        cap = cv2.VideoCapture(video_file)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # List to store pose graphs
        pose_graphs = []

        # Initialize MediaPipe Pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

        for _ in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            # You can use a human detection algorithm here
            # For example, using OpenCV's pre-trained Haar cascades
            # Replace this with your preferred method for human detection

            # Convert frame to grayscale for Haar cascades
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Load the pre-trained Haar cascade for human detection
            haarcascade_path = 'haarcascade_fullbody.xml'  # Update this path
            cascade = cv2.CascadeClassifier(haarcascade_path)

            # Detect humans in the frame
            humans = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(humans) > 0:
                # Process the frame with MediaPipe Pose model
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                # Extract pose landmarks from the results
                if results.pose_landmarks:
                    landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in results.pose_landmarks.landmark]
                    pose_graphs.append({'frame': frame, 'landmarks': landmarks})

        pose.close()
        cap.release()

        # Return the pose graphs
        return jsonify({'pose_graphs': pose_graphs})

    except Exception as e:
        print(f"Error processing poses: {e}")


if __name__ == '__main__':
    app.run(debug=True)
