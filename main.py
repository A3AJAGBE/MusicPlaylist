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
print(songs)

# Authenticate Spotify
sp = Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                       client_secret=SPOTIFY_SECRET,
                                       redirect_uri=SPOTIFY_REDIRECT,
                                       scope="playlist-modify-private",
                                       show_dialog=True,
                                       cache_path="token.txt"))

user_id = sp.current_user()["id"]