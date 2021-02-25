"""Creating a playlist."""

import os
import requests
from bs4 import BeautifulSoup
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_ID = os.environ.get('Client_ID')
SPOTIFY_SECRET = os.environ.get('Client_Secret')
SPOTIFY_REDIRECT = os.environ.get('REDIRECT_URI')

print('Which music year do you want to create a playlist from?')

# Get the date
date = input('Type in this format YYYY-MM-DD: ')

# Get the list of music from that date from Billboard Hot 100
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"
BILLBOARD_ENDPOINT = f"{BILLBOARD_URL}/{date}"

response = requests.get(BILLBOARD_ENDPOINT)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")
song_list = soup.find_all(name="span", class_="chart-element__information__song")
songs = [song.getText() for song in song_list]

# Authenticate Spotify
sp = Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                       client_secret=SPOTIFY_SECRET,
                                       redirect_uri=SPOTIFY_REDIRECT,
                                       scope="playlist-modify-private",
                                       show_dialog=True,
                                       cache_path="token.txt"))

user_id = sp.current_user()["id"]

# Get the songs URI in spotify
spotify_song = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        spotify_song.append(uri)
    except IndexError:
        print(f"Skipping the song: {song}, it doesn't exist in Spotify.")

# Create a playlist on spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Throwback", public=False)

# Add the songs to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_song)
