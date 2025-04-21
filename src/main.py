import json
import sys
from datetime import datetime

import httpx
from decouple import config

try:
    response = httpx.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials",
            "client_id": config("SPOTIFY_CLIENT_ID"),
            "client_secret": config("SPOTIFY_CLIENT_SECRET"),
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    access_token = response.json()["access_token"]
except Exception as exception:
    raise exception


url = f"https://api.spotify.com/v1/playlists/{sys.argv[1]}/tracks"
results = []

while url:
    try:
        response = httpx.get(url, headers={"Authorization": f"Bearer {access_token}"})
        response.raise_for_status()
        response = response.json()
        url = response["next"]

        for obj in response["items"]:
            results.append(
                {
                    "artists": ", ".join([x["name"] for x in obj["track"]["artists"]]),
                    "name": obj["track"]["name"],
                    "album": obj["track"]["album"]["name"],
                }
            )
    except Exception as exception:
        raise exception

timestamp = datetime.now().isoformat()
with open(f"{timestamp}.json", "w") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)
