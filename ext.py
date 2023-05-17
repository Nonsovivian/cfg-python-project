import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def search_spotify(song_name):
    # Authenticate and create a Spotipy client object
    client_credentials_manager = SpotifyClientCredentials(client_id='50e1220d38634b83ad07938b17db50c4',
                                                          client_secret='7f796ff87e564d96ae1436f8f610e415')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.search(q=song_name, type='track')

    #  search results
    song_details = []
    for track in results['tracks']['items']:
        song_name = track['name']
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        release_date = track['album']['release_date']
        popularity = track['popularity']
        song_details.append([song_name, artist_names, album_name, release_date, popularity])

    # Export  to CSV file
    with open('Album_details.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Song Name', 'Artist(s)', 'Album Name', 'Release Date', 'Popularity'])
        writer.writerows(song_details)

    print(f"{len(song_details)} results found.")

search_spotify('who is your guy?')
