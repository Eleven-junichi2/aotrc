import os
import io
import webbrowser
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image
import dotenv
import PySimpleGUI as sg
import requests
import emoji

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")


def remove_emoji(str_):
    return "".join(char for char in str_ if char not in emoji.UNICODE_EMOJI)


def search_reaction_videos(season: int, episode: int, max_result: int):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    search_query = \
        f"attack on titan season {season} episode {episode} reaction"
    try:
        search_response = youtube.search().list(
            q=search_query,
            part="id,snippet",
            maxResults=max_result,
            type="video"
        ).execute()
        return search_response
    except HttpError as error:
        print("HttpError: It causes probably exceeded access limit.")
        print("Sorry but you cannot use this app until tomorrow.")
        input()
        sys.exit(error)


def main():
    while True:
        try:
            season = int(input("which season (by number):"))
            episode = int(input("which episode (by number):"))
            max_result = int(input("how many result:"))
            break
        except ValueError:
            print("Please input by number.")
    search_response = search_reaction_videos(
        season=season, episode=episode, max_result=max_result)
    layout_scroll = []
    for item in search_response["items"]:
        thumb_img_response = requests.get(
            item["snippet"]["thumbnails"]["default"]["url"]).content
        thumb_img_bin = io.BytesIO(thumb_img_response)
        thumb_img = Image.open(thumb_img_bin)
        img_tmp_buffer = io.BytesIO()
        thumb_img.save(img_tmp_buffer, "PNG")
        frame = sg.Frame(
            title="",
            layout=[
                [sg.Text(remove_emoji(item["snippet"]["title"]),
                         enable_events=True,
                         key=("text", "video_id",
                              item["id"]["videoId"]))],
                [sg.Image(data=img_tmp_buffer.getvalue(),
                          enable_events=True,
                          key=("image",
                               item["id"]["videoId"]))],
                [sg.Text(f"Channel: {item['snippet']['channelTitle']}",
                         enable_events=True,
                         key=("text", "channel_id",
                              item["snippet"]["channelId"]))]])
        layout_scroll.append([frame, ])
    layout_column = sg.Column(
        layout_scroll,
        scrollable=True,
        size=(425, 525),
        expand_y=True,
        expand_x=True,)
    layout_root = [[layout_column, ]]
    window = sg.Window("aotrc", layout_root)
    url = ""
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        print(values, event)
        if isinstance(event, tuple):
            if event[1] == "video_id":
                url = f"https://www.youtube.com/watch?v={event[2]}"
            elif event[1] == "channel_id":
                url = f"https://www.youtube.com/channel/{event[2]}"
        if url:
            webbrowser.open_new_tab(url)


if __name__ == "__main__":
    main()
    input()
