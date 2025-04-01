import yt_dlp
from load_keys import API_KEY,MAX_RESULTS,MIN_DURATION
from helper import convert_duration_to_seconds
from googleapiclient.discovery import build
from slicer import slicer_entry_point
from caption_generator import caption_generator
from upload_youtube import upload_short
from title_description import generate_title_from_ass
import os
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_data_urls(query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=MAX_RESULTS,
        order="viewCount"  
    )
    response = request.execute()

    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']

        video_details = youtube.videos().list(
            part="contentDetails",
            id=video_id
        ).execute()

        duration = video_details['items'][0]['contentDetails']['duration']

        duration_seconds = convert_duration_to_seconds(duration)

        if duration_seconds >= MIN_DURATION:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_urls.append(video_url)
    return video_urls


def download_video(video_url, output_dir='downloads'):
    # TODO: if this fails we have to ensure that the remaining buffer is cleaned up
    video_filename=None
    try:
        ydl_opts = {
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Save with video title as the filename
            'format': 'best',  # Download the best quality video
            'quiet': False,  # Set to True for less output
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # Extract info without downloading
            video_title = info_dict.get('title', 'unknown_title')
            video_ext = info_dict.get('ext', 'mp4')  # Default to mp4 if extension is not found
            video_filename = f"{output_dir}/{video_title}.{video_ext}"
            ydl.download([video_url])
    except Exception as e:
        # Perform cleanup operations here
        print(f"Error in downloading video: {e}")
        print(f"Expected video file: {video_filename}")
def download_multiple_videos(video_urls):
    for idx, url in enumerate(video_urls, 1):
        print(f"Downloading video {idx}: {url}")
        download_video(url)
        
    print('----Finished Downloading 1 Video----')



def entrypoint(query):
    video_urls=get_data_urls(query)
    print(video_urls)
    download_multiple_videos(video_urls)
    # cut_video=slicer_entry_point()
    # captioned_video=caption_generator(cut_video)
    # print(captioned_video)
    # #upload to youtube thats the pending work
    # title=generate_title_from_ass()
    # upload_short(captioned_video, title,title)

def upload_short_helper():
    cut_video=slicer_entry_point()
    captioned_video=caption_generator(cut_video)
    print(captioned_video)
    #upload to youtube thats the pending work
    title=generate_title_from_ass()
    upload_short(captioned_video, title,title)
    # Remove the captioned video file after uploading
    if os.path.exists(captioned_video):
        os.remove(captioned_video)
        print(f"Removed captioned video: {captioned_video}")
    else:
        print(f"Captioned video not found: {captioned_video}")


# still there are some unprecendented errors that needs to be taken care of
# also access token and refresh token should be stored along with scope in the future
        #  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/vava/Programming/Projects/shortista/index.py", line 21, in upload_shorts
#     upload_short_helper()
#   File "/home/vava/Programming/Projects/shortista/pipeline/pipeline.py", line 87, in upload_short_helper
#     upload_short(captioned_video, title,title)
#   File "/home/vava/Programming/Projects/shortista/upload_youtube.py", line 57, in upload_short
#     request = youtube.videos().insert(
#               ^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute 'videos'
# try to fix this error as well
# fix aspect ratio issue as well and then scale hard