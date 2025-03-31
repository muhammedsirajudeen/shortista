# Shortista

## Overview
Shortista is a Python Flask-based application that allows users to generate and upload YouTube Shorts effortlessly. Users can enter a name, and the application will create a short video with a caption, ensuring the correct aspect ratio (9:16), and upload it to their YouTube channel.

## Features
- **Automated Short Video Generation**: Converts text input into a short-form video.
- **Correct Aspect Ratio (9:16)**: Ensures the video meets YouTube Shorts requirements.
- **YouTube API Integration**: Uploads directly to the user's YouTube channel.
- **OAuth Authentication**: Allows users to authenticate and upload videos to their own accounts.
- **Flask Web Interface**: Simple UI to enter the name and upload the generated video.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Pip
- Virtualenv (optional but recommended)

### Clone the Repository
```sh
git clone https://github.com/yourusername/shortista.git
cd shortista
```

### Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Configuration
### YouTube API Setup
1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the **YouTube Data API v3**.
   - Create **OAuth 2.0 credentials**.
   - Download the `client_secret.json` file and place it in the project directory.

2. **Set Up Environment Variables**:
```sh
export FLASK_APP=app.py
export CLIENT_SECRETS_FILE=client_secret.json
```

## Running the Application
```sh
flask run
```
This will start a local Flask server, typically at `http://127.0.0.1:5000/`.

## Usage
1. Open the web interface in your browser.
2. Enter a name or text prompt.
3. The system generates a video and uploads it to the authenticated user's YouTube channel.
4. The uploaded video appears in the user's YouTube Shorts section.

## Deployment
For production deployment, you can use:
- **Gunicorn** (for running Flask in production)
- **Docker** (to containerize the application)
- **Cloud Hosting** (e.g., AWS, Heroku, DigitalOcean)

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For issues or inquiries, please open an issue on GitHub or contact [your email].

