import os
# from pathlib import Path

from googleapiclient.discovery import build
import dotenv

# env_file_path = Path(__file__).parent / ".env"

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

season = (1, 2, 3, "final")
episode = 1
search_query = f"attack on titan season {season} episode {episode} reaction"
max_result = 10

search_response = youtube.search().list(
    q=search_query,
    part="id,snippet",
    maxResults=max_result,
    type="video"
).execute()


print(search_response)
