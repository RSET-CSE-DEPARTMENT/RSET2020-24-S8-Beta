from moviepy.editor import VideoFileClip, AudioFileClip

def combine_video_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
video_path = "C:/Users/HP/Downloads/Learning_to_Dance/media/step_generated_0sdKZHV.mp4"
audio_path = "C:/Users/HP/Downloads/Learning_to_Dance/test.wav"
output_path = "output_combined.mp4"

combine_video_audio(video_path, audio_path, output_path)
