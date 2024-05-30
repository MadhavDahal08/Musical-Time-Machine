import requests
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()
time = input("Which year do you want to travel to? Type the date in this format YY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{time}/"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

redirect_uri = "http://example.com"

response = requests.get(URL)
data = response.text

soup = BeautifulSoup(data, "html.parser")
titles = soup.select(selector="li ul li h3")
list_of_titles = [title.getText().strip() for title in titles]

scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Madhav Dahal",
    )
)
user_id = sp.current_user()["id"]
# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_names =list_of_titles

song_uris = []
year = time.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
