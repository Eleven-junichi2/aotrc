import requests
import json

result = requests.get(
    "https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&q=attack+on+titan&key=AIzaSyB4V4mgc_hX7Ud66Dh1uDMMZmrx3_X5eKI")
print(result.text)
