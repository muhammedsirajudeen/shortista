import yt_dlp
from load_keys import API_KEY,MAX_RESULTS,MIN_DURATION
from helper import convert_duration_to_seconds
from googleapiclient.discovery import build
from slicer import slicer_entry_point
from caption_generator import caption_generator
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
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Save with video title as the filename
        'format': 'best',  # Download the best quality video
        'quiet': False,  # Set to True for less output
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_multiple_videos(video_urls):
    for idx, url in enumerate(video_urls, 1):
        print(f"Downloading video {idx}: {url}")
        download_video(url)
        
    print('----Finished Downloading 1 Video----')



def entrypoint(query):
    video_urls=get_data_urls(query)
    print(video_urls)
    download_multiple_videos(video_urls)
    cut_video=slicer_entry_point()
    captioned_video=caption_generator(cut_video)
    print(captioned_video)
    #upload to youtube thats the pending work
