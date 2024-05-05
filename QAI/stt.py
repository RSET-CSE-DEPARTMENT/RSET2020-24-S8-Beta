# !pip install speechrecognition
# !pip install pyaudio
# !pip install pyttsx3
# !pip install pydub
# pip install fastpunct
# importing libraries
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
# from fastpunct import FastPunct

import shutil
import subprocess 
  

# create a speech recognition object
def speact_to_text():
    r = sr.Recognizer()
    # fastpunct = FastPunct()


    
    # convert mp3 to wav file 
    # subprocess.call(['ffmpeg', '-i', 'transcribe.mp3', 'transcribe.wav'])
    # path = "transcribe3.wav"

    # a function to recognize speech in the audio file
    # so that we don't repeat ourselves in in other functions
    def transcribe_audio(path):
        # use the audio file as the audio source
        with sr.AudioFile(path) as source:
            audio_listened = r.record(source)
            # try converting it to text
            text = r.recognize_google(audio_listened)

            # fastpunct.punct([text])

        return text

    # a function that splits the audio file into chunks on silence
    # and applies speech recognition
    def get_large_audio_transcription_on_silence(path):
        """Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks"""
        # open the audio file using pydub
        sound = AudioSegment.from_file(path)
        # split audio sound where silence is 500 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            try:
                text = transcribe_audio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
            try:
            #  shutil.rmtree(path)
                os.remove(chunk_filename)
            #  print("Directory removed successfully")
            except OSError as o:
                print(f"Error, {o.strerror}: {chunk_filename}")
        os.rmdir("audio-chunks")
        # return the text for all chunks detected
        return whole_text
    data_folder = "data"
    wav_files = [file for file in os.listdir(data_folder) if file.endswith(".wav")]
    i=1
    for wav_file in wav_files:
        file_path = os.path.join(data_folder, wav_file)
        # sound = AudioSegment.from_mp3(file_path)
        # sound.export(file_path, format="wav")
        out=get_large_audio_transcription_on_silence(file_path)
        print(file_path)
        print(out)
        out_file = os.path.join(data_folder, f"{i}.txt")
        with open(out_file, 'w') as file:
            file.write(out)
        i+=1
# speact_to_text()