import cv2
import sounddevice as sd
import soundfile as sf
import threading
import time
import os
import numpy as np
from datetime import datetime

class Recorder:
    def __init__(self):
        self.video_output_folder = 'F:/video'  # Specify the default output folder for video
        self.audio_output_folder = 'F:/audio'  # Specify the default output folder for audio
        self.video_base_filename = os.path.join(self.video_output_folder, 'video')
        self.audio_base_filename = os.path.join(self.audio_output_folder, 'audio')
        self.video_recording = False
        self.audio_recording = False
        self.video_frames = []
        self.audio_frames = []
    def start_video_recording(self):
        self.video_recording = True
        self.video_thread = threading.Thread(target=self._record_video)
        self.video_thread.start()

    def stop_video_recording(self):
        self.video_recording = False
        self.video_thread.join()

    def _record_video(self):
        cap = cv2.VideoCapture(0)
        while self.video_recording:
            ret, frame = cap.read()
            if ret:
                self.video_frames.append(frame)
            else:
                break
            if len(self.video_frames) == 1200:  # 1200 frames at 20 fps = 1 minute
                self.save_video_frames()
        cap.release()

    def save_video_frames(self):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        video_filename = f"{self.video_base_filename}_{timestamp}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
        for frame in self.video_frames:
            out.write(frame)
        out.release()
        self.video_frames.clear()

    def start_audio_recording(self):
        self.audio_recording = True
        self.audio_thread = threading.Thread(target=self._record_audio)
        self.audio_thread.start()

    def stop_audio_recording(self):
        self.audio_recording = False
        self.audio_thread.join()

    def _record_audio(self):
        while self.audio_recording:
            duration = 60  # Record audio for 1 minute
            fs = 44100
            channels = 1
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
            sd.wait()
            self.audio_frames.append((recording, fs))
            if len(self.audio_frames) == 60:  # 60 seconds = 1 minute
                self.save_audio_frames()
        if self.audio_frames:
            self.save_audio_frames()

    def save_audio_frames(self):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        audio_filename = os.path.join(self.audio_output_folder, f"audio_{timestamp}.wav")
        recording, fs = zip(*self.audio_frames)
        recording = np.concatenate(recording)
        sf.write(audio_filename, recording, fs[0])
        self.audio_frames.clear()


if __name__ == "__main__":
    recorder = Recorder()

    # Ensure output folders exist
    for folder in [recorder.video_output_folder, recorder.audio_output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Start recording
    recorder.start_video_recording()
    recorder.start_audio_recording()

    try:
        # Record indefinitely
        while True:
            time.sleep(1)  # Sleep for 1 second
    except KeyboardInterrupt:
        # Stop recording if the process is interrupted (e.g., Ctrl+C)
        recorder.stop_video_recording()
        recorder.stop_audio_recording()
        # Save remaining frames
        if recorder.video_frames:
            recorder.save_video_frames()
        if recorder.audio_frames:
            recorder.save_audio_frames()
