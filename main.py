from flask import Flask, render_template, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import accessSpotify as acSp
import urllib.parse
import json

clientID = ""
clientSecret = ""
spotifyURL = "https://accounts.spotify.com/authorize"
baseURL = 'https://true-spotify-shuffle.brendawg.repl.co'

def getAuthUrl():
  url = spotifyURL
  url += "?client_id=" + clientID
  url += "&response_type=code"
  url += f"&redirect_uri={baseURL}/select" 
  url += "&show_dialog=true"
  url += "&scope=user-read-private user-library-read user-library-modify playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"
  return url



app = Flask("True Spotify Shuffle")
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('landingPage.html', url=baseURL)

@app.route('/authorize')
def auth():
  
    url = getAuthUrl()
    return redirect(url)

@app.route('/select')
def select():

  code = request.args.get('code')
  if code == None: return redirect(baseURL)
  try:
    accessToken, refreshToken = acSp.callAuthApi(code)
  except:
    return redirect(baseURL)
  playlists = acSp.getPlaylist(accessToken, refreshToken)
  playlists = json.dumps(playlists)
  profileData = acSp.getProfile(accessToken, refreshToken)
  username = profileData['id']

  return render_template('selectPlaylist.html', url=baseURL, playlists=playlists, username=username, refreshToken=refreshToken)

@app.route('/finished')
def finished():

  playlistId = request.args.get('plID')
  playlistLength = request.args.get('plLength')
  playlistName = request.args.get('plName')
  refreshToken = request.args.get('refreshToken')

  accessToken = acSp.refreshAccessToken(refreshToken)

  profileData = acSp.getProfile(accessToken, refreshToken)
  username = profileData['id']
  
  newPlaylistName, newPlID = acSp.SHUFFLE(playlistId, playlistLength, playlistName, username, accessToken, refreshToken)

  return render_template('finished.html', url=baseURL, newPlaylistName=newPlaylistName, playlistName=playlistName, playlistID=newPlID)

app.run(host='0.0.0.0', port=81, debug=True)
