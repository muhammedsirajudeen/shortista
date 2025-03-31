import openai 
import os
import subprocess
from moviepy import VideoFileClip
from datetime import datetime,timedelta
from load_keys import OPENAI_KEY,SHORT_DURATION
# OpenAI API Key (Replace with your key)
openai.api_key=OPENAI_KEY
def extract_audio(video_path, audio_path):
    """Extracts audio from the video."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec="libmp3lame")
    print(f"Audio extracted: {audio_path}")

def transcribe_audio(audio_path):
    """Sends audio to OpenAI Whisper API for transcription."""
    with open(audio_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    print(response)
    transcript = response.text
    print(f"Transcription:\n{transcript}")
    return transcript

def save_srt(transcript, srt_path, video_duration):
    """Saves the transcript as an SRT subtitle file with proper timing."""
    words = transcript.split()  # Split transcript into words
    num_words = len(words)
    words_per_caption = 10  # Number of words per caption
    captions = [words[i:i + words_per_caption] for i in range(0, num_words, words_per_caption)]

    # Calculate duration per caption
    caption_duration = video_duration / len(captions)

    with open(srt_path, "w") as srt_file:
        for i, caption in enumerate(captions):
            start_time = i * caption_duration
            end_time = start_time + caption_duration

            # Convert start and end times to SRT format
            start_time_str = str(timedelta(seconds=start_time)).split(".")[0] + ",000"
            end_time_str = str(timedelta(seconds=end_time)).split(".")[0] + ",000"

            # Write the caption to the SRT file
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start_time_str} --> {end_time_str}\n")
            srt_file.write(f"{' '.join(caption)}\n\n")

    print(f"Subtitles saved: {srt_path}")

def burn_subtitles(video_path, srt_path, output_path):
    """Burns subtitles onto the video using ffmpeg."""
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ensure the SRT file exists
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    # Construct and run the ffmpeg command
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_path
    ]
    print("Running command:", " ".join(command))  # Debugging
    subprocess.run(command, check=True)
    print(f"Video with subtitles saved: {output_path}")

def burn_subtitles(video_path, srt_path, output_path):
    """Burns subtitles onto the video using ffmpeg."""
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(command, check=True)
    print(f"Video with subtitles saved: {output_path}")
def save_ass(transcript, ass_path, video_duration):
    """Saves the transcript as an ASS subtitle file with custom styling."""
    words = transcript.split()  # Split transcript into words
    num_words = len(words)
    words_per_caption = 10  # Number of words per caption
    captions = [words[i:i + words_per_caption] for i in range(0, num_words, words_per_caption)]

    # Calculate duration per caption
    caption_duration = video_duration / len(captions)

    # Write the ASS file
    with open(ass_path, "w") as ass_file:
        # Write the ASS header with styling
        ass_file.write("[Script Info]\n")
        ass_file.write("Title: Custom Subtitles\n")
        ass_file.write("ScriptType: v4.00+\n")
        ass_file.write("Collisions: Normal\n")
        ass_file.write("PlayDepth: 0\n\n")

        ass_file.write("[V4+ Styles]\n")
        ass_file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                       "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
                       "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        ass_file.write("Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,2,10,10,10,1\n\n")

        ass_file.write("[Events]\n")
        ass_file.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        # Write each caption with timing
        for i, caption in enumerate(captions):
            start_time = i * caption_duration
            end_time = start_time + caption_duration

            # Convert start and end times to ASS format
            start_time_str = str(timedelta(seconds=start_time)).split(".")[0] + ".00"
            end_time_str = str(timedelta(seconds=end_time)).split(".")[0] + ".00"

            # Write the caption to the ASS file
            ass_file.write(f"Dialogue: 0,{start_time_str},{end_time_str},Default,,0,0,0,,{' '.join(caption)}\n")

    print(f"Subtitles saved: {ass_path}")
def caption_generator(video_path):
    output_video = "output_captioned/captioned_video.mp4"
    audio_path = "temp_audio.mp3"
    srt_path = "captions.srt"
    ass_path="captions.ass"

    # Extract audio and get transcription
    extract_audio(video_path, audio_path)
    transcript = transcribe_audio(audio_path)
    # Save captions as SRT file
    save_srt(transcript, srt_path,SHORT_DURATION)
    save_ass(transcript,ass_path,SHORT_DURATION)
    # Burn captions into the video
    burn_subtitles(video_path, ass_path, output_video)
    return output_video