# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 22:44:14 2018

@author: Harsha Neel
"""

import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = os.getlogin()
scope = 'user-library-read user-read-private user-read-playback-state user-modify-playback-state'

# User ID: 1244825148

# Erase cache and prompt for user permission
try : 
    token = util.prompt_for_user_token(username, scope)
except: 
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)
    
    
# Create Spotify object with permissions
spotifyObj = spotipy.Spotify(auth=token)

user = spotifyObj.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']

trackNamesAndIDs = {}
trackObjects = []

# Loop
while True:
    # Main menu
    print()
    print(">>> Welcome to Spotify " + displayName + "!")
    print()
    print("Please enter the name of the playlist you'd like to fetch")
    print()
    choice = input("Your choice: ")
    trackNamesAndIDs = {}
    trackObjects = []
    
    # This is to provide the option of exitting the script
    # Since the input can be anything, the processing has been moved to the else block instead of the if block
    # The exit choice is specific, and hance it stays in the if block.
    if choice == "exit":
        break;
    
    # Since choice can have pretty much any value, the exi
    else:
        userID = user['id']
        print("User ID is: " + userID)
        allUserPlaylists = spotifyObj.user_playlists(userID)
        print("all playlists have been retrieved")

        
        # Loop through all user playslists in order to get the desired playlist.
        # There is a search method in the spotipy object, but it searches through all of spotify, instead of within the user's items. 
        # So this is unfortunately the only way to do retrieve my chosen playlist from my playlists 
        for item in allUserPlaylists['items']:
            if item['name'] == choice:
                playlistID = item['id']
                desiredPlaylist = spotifyObj.user_playlist(userID, playlistID)
                print("Playlist " + choice + " has been fetched. Playlist ID" + " = " + playlistID)
                trackInfo = desiredPlaylist['tracks']['items']
                                
                # Pulling out track ID and Name to store in dictionary
                for item in trackInfo:
                    trackID = item['track']['id']
                    trackName = item['track']['name']
                    trackNamesAndIDs[trackName] = trackID
                    print(trackName + ": " + trackID)
                    
                    
        # Counter variable for numbering items inside the for loop
        count = 1       
        
        # Get each track's audio features and track objects
        for name, ID in trackNamesAndIDs.items():
            trackFeats = spotifyObj.audio_features(ID)
            #print(json.dumps(trackFeats, sort_keys=True, indent=4))
            trackObj = spotifyObj.track(ID)
            print("\n" + str(count) + ". Obtained track object for track " + name)
            trackObjects.append(trackObj)
            print("   Popularity of " + trackObj['name'] + ": " + str(trackObj['popularity']))
            count += 1
        