import os
import random
from moviepy import VideoFileClip
import datetime
from moviepy.video.io.VideoFileClip import VideoFileClip
from load_keys import SHORT_DURATION
def get_video_duration(video_path):
    try:
        video = VideoFileClip(video_path)        
        duration = int(video.duration)
        video.close()
        return duration
    except Exception as e:
        print(f"An error occurred while getting video duration: {e}")
        return None
def get_video_files(directory):
    video_extensions = ['.mp4', '.mkv', '.webm', '.avi', '.mov']
    video_files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
    return video_files

def select_random_video(directory):
    video_files = get_video_files(directory)
    if video_files:
        return random.choice(video_files)
    else:
        raise ValueError("No video files found in the directory")

def cut_video(input_video_path, output_video_path, start_time=0, duration=45):
    output_width = 1080
    output_height = 1920
    # still not resizing check it later

    video = VideoFileClip(input_video_path).resized(width=output_width)
    video=video.cropped(y_center=video.h / 2,height=output_height)
    
    duration=get_video_duration(input_video_path)
    random_start_time=random.randint(0,duration-60)
    cut = video.subclipped(random_start_time, random_start_time + SHORT_DURATION )
    cut.write_videofile(output_video_path, codec="libx264")

def slicer_entry_point():
    downloads_dir = "downloads"  #
    output_dir = "output"  
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        selected_video = select_random_video(downloads_dir)
        
        input_video_path = os.path.join(downloads_dir, selected_video)

        output_video_path = os.path.join(output_dir, f"cut_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{selected_video}")

        cut_video(input_video_path, output_video_path)
        return output_video_path
    except Exception as e:
        print(f"An error occurred: {e}")


