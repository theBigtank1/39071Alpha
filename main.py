# ELEC 3907 Group 1A
# API Interface Code
# Written by Tanner Krauter

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="0e82adf631c444569cce986dea9e374c",
                                                           client_secret="----"))

runCode = True
count = 0
while runCode:
    count = count + 1
    if count == 50:
        runCode = False
print(count)
