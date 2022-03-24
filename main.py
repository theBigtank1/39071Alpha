# ELEC 3907 Group 1A
# API Interface Code
# Written by Tanner Krauter

# imports the spotipy library
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)  # Ignore warning for now
reader = SimpleMFRC522()
import time

# Define key variables
username = 'tawseefpatel'
clientID = '0e82adf631c444569cce986dea9e374c'
clientSecret = '3a757ec0b128429c85335863da705696'
redirectURI = 'https://www.google.ca/'
playback_state = False
loop_running = True
track_info = ""
current_volume = 100

# Create spotify object to interact with
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI,
                                               scope="user-modify-playback-state user-read-currently-playing user-read-playback-state", open_browser="False"))

# Opens spotify webpage on device
webbrowser.open("https://open.spotify.com/", new=1, autoraise=False)

time.sleep(20)

# Gets the device ID of the current device
devices = sp.devices()
device_id = devices['devices'][0]['id']
print(device_id)

# Makes the current device active for the software to interact with
sp.transfer_playback(device_id)
playback_state = True
sp.volume(100)
current_volume = 100
# Functions


# Adds media to the spotify queue
def add_to_queue(song_uri):
    sp.add_to_queue(song_uri)
    try:
        sp.start_playback(device_id)
    except:
        print("Song Playing")
    return True


# Gets info about the current media
def get_current_song_info():
    try:
        track = sp.current_user_playing_track()
        return (track['item']['name'] + " by " + track['item']['artists'][0]['name'])
    except:
        return 'none'


# Pauses or plays media depending on the current state
def play_pause_song(is_playing):
    if is_playing:
        sp.pause_playback(device_id)
        return False
    else:
        sp.start_playback('ab0bc3e6e491c36b242dc54eff8d7a61373ae60f')
        return True


# Skips to next media
def skip_song():
    sp.next_track(device_id)
    track = get_current_song_info()
    return track


# Returns to previous media
def return_to_song():
    sp.previous_track(device_id)
    track = get_current_song_info()
    return track


# Gets the most recent episode of a podcast
def get_most_recent_podcast(show_id):
    recent_episode = sp.show_episodes(show_id, '1')
    episode_id = recent_episode['items'][0]['id']
    full_id = 'spotify:episode:' + episode_id
    return full_id


# Turns volume up in increments of 10
def volume_up(volume):
    if volume > 90:
        sp.volume(100)
        return 100
    else:
        sp.volume(volume + 10)
        return volume + 10


# Turns volume down in increments of 10
def volume_down(volume):
    if volume < 10:
        sp.volume(0)
        return 0
    else:
        sp.volume(volume - 10)
        return volume - 10


GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# Return button - on Pin 9
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 9 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(8, GPIO.RISING, callback=return_to_song())  # Setup event on pin 9 rising edge
# Pause play button - on Pin10
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10, GPIO.RISING, callback=play_pause_song(playback_state))  # Setup event on pin 10 rising edge
# Skip button - on Pin11
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 11 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(11, GPIO.RISING, callback=skip_song())  # Setup event on pin 11 rising edge
# Volume up button - on Pin12
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 12 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(12, GPIO.RISING, calback=volume_up(current_volume))  # Setup event on pin 12 rising edge
# Volume down button - on Pin13
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 13 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(13, GPIO.RISING, calback=volume_down(current_volume))  # Setup event on pin 13 rising edge

# Main software loop
while loop_running:
    #nput_text = reader.read()
    playback_state = add_to_queue(input_text)
    track_info = get_current_song_info()

GPIO.cleanup()
