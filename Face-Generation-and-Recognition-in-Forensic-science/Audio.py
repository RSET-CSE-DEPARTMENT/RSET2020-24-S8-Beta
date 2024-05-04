import speech_recognition as sr

# Create a Recognizer instance
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something...")
    audio_data = r.listen(source,timeout=15) # Record audio for 15 seconds

# Recognize speech
try:
    text = r.recognize_google(audio_data)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))