import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

# YouTube API Scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(port=8080, open_browser=True)
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_short(video_path, title, description, category_id="22", privacy_status="public"):
    youtube = get_authenticated_service()

    request_body = {
        "snippet": {
            "title": title + " #Shorts",  # Adding #Shorts to the title
            "description": description + " #Shorts",
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = googleapiclient.http.MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print(f"Short Uploaded! Video ID: {response['id']}")

# if __name__ == "__main__":
#     video_path = "your_video.mp4"  # Change to your video path
#     upload_short(video_path, "My YouTube Shorts Video", "This is a Shorts test upload.")
