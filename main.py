from bs4 import BeautifulSoup as bs
import requests
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_details import Client


client = Client()

date = input("Which year you want to travel to?? Type the date in this Format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/"
response = requests.get(URL+"2021-02-02")
soup = bs(response.text, "lxml")

# Scrapping Billboard top 100 songs
song_list = soup.find(name='ol', class_="chart-list__elements")
all_song_info = song_list.find_all(name="span", class_="chart-element__information")
song_names = []
for song_info in all_song_info:
    song = song_info.select(".chart-element__information__song")
    song_names.append(song[0].getText())

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client.get_client_id(),
        client_secret=client.get_client_secret(),
        redirect_uri="https://example.com/",
        show_dialog=True,
        scope="playlist-modify-private",
        cache_path="token.txt"
    ))

user_id = sp.current_user()["id"]
print(user_id)

year = date.split("-")[0]
song_uris = []
for song in song_names:
    data = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(data)
    try:
        uri = data["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)









