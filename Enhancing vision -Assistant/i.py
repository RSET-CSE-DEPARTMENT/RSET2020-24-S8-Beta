import face_recognition
import os
import pickle
import cv2

def add_new_face(person_name):
  """
  Captures images of a person and saves them along with their extracted face encodings for training.
  """

  known_faces_dir = "known_faces"
  os.makedirs(known_faces_dir, exist_ok=True)  # Create directory if it doesn't exist

  person_dir = os.path.join(known_faces_dir, person_name)
  os.makedirs(person_dir, exist_ok=True)  # Create directory for the person

  num_images = 10

  # Load existing face encodings and names (if any)
  known_face_encodings = []
  known_face_names = []
  try:
    with open("known_faces.pkl", "rb") as f:
      known_face_encodings, known_face_names = pickle.load(f)
  except FileNotFoundError:
    pass  # No existing data, continue

  # Capture new images and encodings
  for i in range(num_images):
    print(f"Taking picture {i+1} of {person_name}")
    cap = cv2.VideoCapture(0)  # Use default webcam
    ret, frame = cap.read()

    # Ensure a face is detected before saving the image
    while True:
      faces = face_recognition.face_locations(frame)
      if len(faces) > 0:
        break
      ret, frame = cap.read()

    cv2.imwrite(os.path.join(person_dir, f"{person_name}_{i}.jpg"), frame)
    cap.release()
    cv2.destroyAllWindows()

    # Extract face encoding from the captured image
    face_encoding = face_recognition.face_encodings(frame)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(person_name)

  # Save face encodings and names to a file
  with open("known_faces.pkl", "wb") as f:
    pickle.dump((known_face_encodings, known_face_names), f)

  print(f"Training data collected and saved for {person_name}.")


def recognize_face():
  """
  Attempts to load known faces from a file and performs face recognition on a captured image.
  Returns the detected person's name (or a custom message if no face is found).
  """

  # Try loading face encodings from a file
  try:
    with open("known_faces.pkl", "rb") as f:
      known_face_encodings, known_face_names = pickle.load(f)

  except FileNotFoundError:
    print("No known faces file found. Please add faces using the 'add_new_face' function.")
    return "Unknown"

  # Capture a new image
  cap = cv2.VideoCapture(0)
  ret, frame = cap.read()

  # Check if a frame is captured successfully
  if not ret:
    print("Error: Failed to capture frame from webcam.")
    cap.release()
    cv2.destroyAllWindows()
    return "Error: Webcam capture failed."

  # Handle the scenario where no face is detected
  face_locations = face_recognition.face_locations(frame)
  if not face_locations:
    cap.release()
    cv2.destroyAllWindows()
    return "No face detected."  # Custom message for no face

  face_encodings = face_recognition.face_encodings(frame, face_locations)

  for face_encoding, face_location in zip(face_encodings, face_locations):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    # If a match is found, get the name of the person
    if True in matches:
      first_match_index = matches.index(True)
      name = known_face_names[first_match_index]

    # Close resources
    cap.release()
    cv2.destroyAllWindows()

    return name  # Return the detected person's name        

import speech_recognition as sr
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

def record_audio():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Record audio from the microphone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            print("Recognizing...")
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            text="Timeout. No speech detected."
            return text
        except sr.UnknownValueError:
            text="Sorry, I couldn't understand what you said."
            return text
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            return 0
    return None, None



import textwrap
import pickle
from IPython.display import display, Markdown
import os
import PIL.Image
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('.', '*')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY=Enter Api key Here
genai.configure(api_key=GOOGLE_API_KEY)

# Check if the model is already saved
model_path = 'vision_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        vision_model = pickle.load(f)
    print("Model loaded from", model_path)
else:
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    # Save the model
    with open(model_path, 'wb') as f:
        pickle.dump(vision_model, f)
    print("Model saved to", model_path)
from gtts import gTTS
import pygame
import io

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    
    # Create an in-memory file-like object
    audio_file = io.BytesIO()
    
    # Save audio to the in-memory file-like object
    tts.write_to_fp(audio_file)
    audio_file.seek(0)  # Move to the beginning of the file
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.quit()

# Example usage

import cv2

def capture_image():
    # Open the first webcam device
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the captured frame
  
    # Save the captured image
    cv2.imwrite('captured_image.jpg', frame)

    # Release the capture
    cap.release()

 
import pickle

# Define the path where the model is saved
model_path = 'vision_model.pkl'

# Load the model from the file
with open(model_path, 'rb') as f:
    vision_model = pickle.load(f)

# Now you can use vision_model as your loaded model
print("Model loaded successfully from", model_path)




while(1):
 audio_text = record_audio()
 if('add new face'==audio_text):
     text_to_speech("type the name of the person")
     name=input("person_name: ")
     text_to_speech("taking pictures of "+name)
     add_new_face(name)
     continue
 if(audio_text=='stop'):
    text_to_speech("thank you")
    break
 if(audio_text=="Sorry, I couldn't understand what you said."):
    print("Sorry, I couldn't understand what you said.")
    continue
 capture_image()
 name=recognize_face()
 img = PIL.Image.open(r"captured_image.jpg")

 if(name=='No face detected.'):
  response= vision_model.generate_content([audio_text,img],stream=True)
 else:
  response= vision_model.generate_content([audio_text+"name of the person in the image is "+name,img],stream=True)    
 response.resolve()

 print("Assistant:"+response.text)
 text = response.text
 text_to_speech(text)
 to_markdown(response.text)