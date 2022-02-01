# ELEC 3907 Group 1A
# API Interface Code
# Written by Tanner Krauter

# TODO: Change device ID to Pi, setup main loop, get input info and create events


# imports the spotipy library
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import webbrowser

# Define key variables
username = 'tawseefpatel'
clientID = '0e82adf631c444569cce986dea9e374c'
clientSecret = '----'
redirectURI = 'https://www.google.ca/'
playback_state = False

# Creates OAuth object for Spotify
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI)

# Creates a spotify token
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']

# Create spotify object to interact with
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI,
                                               scope="user-modify-playback-state user-read-currently-playing user-read-playback-state"))


def add_to_queue(song_uri):
    sp.add_to_queue(song_uri)
    try:
        sp.start_playback('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
        get_current_song_info()
    except:
        print("Song Playing")
    return True


def get_current_song_info():
    track = sp.current_user_playing_track()
    return (track['item']['name'] + " by " + track['item']['artists'][0]['name'])


def play_pause_song(is_playing):
    if is_playing:
        sp.pause_playback('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
        return False
    else:
        sp.start_playback('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
        return True


def skip_song():
    sp.next_track('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
    get_current_song_info()


def return_to_song():
    sp.previous_track('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
    get_current_song_info()


def get_most_recent_podcast(show_id):
    recent_episode = sp.show_episodes(show_id, '1')
    id = recent_episode['items'][0]['id']
    id = 'spotify:episode:' + id
    return id
