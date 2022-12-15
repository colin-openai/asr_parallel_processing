import os
from moviepy.editor import *
from pydub import AudioSegment

def convert_flac_to_mp3(flac_file, output_file):

    flac_audio = AudioSegment.from_file(flac_file, "flac")
    flac_audio.export(os.path.join(os.curdir,output_file + '.mp3'), format="mp3")

def convert_mp4_to_mp3(video_filepath):

    audio_filepath = video_filepath.replace('mp4','mp3')

    video = VideoFileClip(video_filepath)
    video.audio.write_audiofile(audio_filepath)

    return audio_filepath