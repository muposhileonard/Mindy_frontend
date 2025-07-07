import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path)
    return audio_path

def generate_transcript(video_path):
    audio_path = extract_audio(video_path)
    
    # TODO: Use a real speech-to-text service here
    # For now, just return dummy transcript
    return "[Transcript Placeholder: Real transcription coming soon.]"
