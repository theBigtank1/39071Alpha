# ELEC 3907 Group 1A
# API Interface Code
# Written by Tanner Krauter

#imports the spotipy library
import spotipy
import json
import webbrowser


#Define key variables
username = 'tawseefpatel'
clientID = '0e82adf631c444569cce986dea9e374c'
clientSecret = '----'
redirectURI = 'https://www.google.ca/'


#Creates OAuth object for Spotify
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI)

#Creates a spotify token
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']

#Create spotify object to interact with
sp = spotipy.Spotify(auth=token)

user = sp.current_user()

print(sp.artist('spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'))
