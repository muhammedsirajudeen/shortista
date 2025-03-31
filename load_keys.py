import os
from dotenv import load_dotenv
API_KEY=os.getenv('YOUTUBE_API_KEY')
OPENAI_KEY=os.getenv('OPENAI_API_KEY')
MAX_RESULTS=100
MIN_DURATION=600
SHORT_DURATION=45
#raise exception to exit gracefully
if API_KEY is None or OPENAI_KEY is None:
    raise Exception('Youtube api key not supplied')