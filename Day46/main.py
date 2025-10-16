import requests
from bs4 import BeautifulSoup
from spotify_auth import SPOTIFY
from pprint import pprint
date_to_travel = input("Which year do you want to travel ? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
url = f"https://www.billboard.com/charts/hot-100/{date_to_travel}/"

user_spotify = SPOTIFY()
response = requests.get(url=url, headers=header)
response.raise_for_status()
web_page = response.text

web = BeautifulSoup(web_page, "html.parser")
title_in_web = web.find_all(name="h3", id="title-of-a-story")
list_of_titles = []
for title in title_in_web:
    list_of_titles.append(title.getText().strip())

new_query = []
for x in list_of_titles:
    q = f"track: {x} year:{date_to_travel.split("-")[0]}"
    new_query.append(q)
spotify_uris = []
for query in new_query:
    save_json_spotify = user_spotify.sp.search(q=query, type="track")
    try:
        uri_for_tracks = save_json_spotify["tracks"]["items"][0]["uri"]
        spotify_uris.append(uri_for_tracks)
    except IndexError:
        pass



playlist = user_spotify.sp.user_playlist_create(user=user_spotify.user, name=f"{date_to_travel} Billboard 100", public=False)

user_spotify.sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_uris)