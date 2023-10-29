from bs4 import BeautifulSoup
import requests
import spotipy
import config

SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
SPOTIFY_SECRET = config.SPOTIFY_SECRET
SPOTIFY_USER = config.SPOTIFY_USER
REDIRECT_URL = "https://open.spotify.com"
USERNAME = config.USERNAME

music_travel_to_date = input(
    "Which year do you want to travel to? Type the date in the format YYYY-MM-DD: "
)
searched_year = int(music_travel_to_date.split("-")[0])

base_url = "https://www.billboard.com/charts/hot-100/"

destination_url = f"{base_url}/{music_travel_to_date}"
response = requests.get(destination_url)
songs = response.text
soup = BeautifulSoup(songs, "html.parser")
titles = soup.select(
    ".o-chart-results-list-row-container .o-chart-results-list-row .o-chart-results-list__item .c-title"
)

list_titles = [title.getText().strip() for title in titles]


auth_manager = spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_SECRET,
    redirect_uri=REDIRECT_URL,
    username=USERNAME,
    cache_path="token.txt",
    scope="playlist-modify-private",
    show_dialog=True,
)
sp = spotipy.Spotify(auth_manager=auth_manager)
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

user_id = sp.current_user()["id"]


spotify_songs = []

for track in list_titles:
    try:
        result = (
            sp.search(q=f"track:{track} year:{searched_year}", type="track", limit=1)
        )["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{track} : Not found on Spotify.")
    else:
        spotify_songs.append(result)


playlist = sp.user_playlist_create(
    user=SPOTIFY_USER,
    name=f"{music_travel_to_date} Billboard 100",
    public=False,
)
playlist_id = playlist["id"]

add_songs_to_playlist = sp.playlist_add_items(
    playlist_id=playlist_id, items=spotify_songs
)

print("Songs added to your spotify playlist.")
