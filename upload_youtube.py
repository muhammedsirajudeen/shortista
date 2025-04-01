import psutil
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import socket
# YouTube API Scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"


def kill_process_on_port(port):
    """Kills the process running on the specified port."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    print(f"Killing process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                    proc.terminate()
                    proc.wait()  # Wait for the process to terminate
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print(f"No process found running on port {port}")
    return False

def is_port_in_use(port):
    """Checks if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_authenticated_service():
    port = 8080  # Move this to an environment variable if needed

    # Check if the port is in use and kill the process if necessary
    if is_port_in_use(port):
        print(f"Port {port} is in use. Attempting to free it...")
        if not kill_process_on_port(port):
            raise RuntimeError(f"Failed to free port {port}. Please check manually.")

    try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES
        )
        credentials = flow.run_local_server(port=port, open_browser=True)
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"Error in authenticating with Google: {e}")
        return None

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

