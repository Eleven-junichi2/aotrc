import os
# from pathlib import Path

# from googleapiclient.discovery import build
import requests
import dotenv

# env_file_path = Path(__file__).parent / ".env"

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")

# service = build("")

result = requests.get(
    f"https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&q=attack+on+titan&key={API_KEY}")
print(result.text)
