import requests
import math
import random


clientID = ""
clientSecret = ""
spotifyURL = "https://accounts.spotify.com/authorize"
baseURL = 'https://true-spotify-shuffle.brendawg.repl.co'
tokenURL = "https://accounts.spotify.com/api/token"
playlistEndpoint = "https://api.spotify.com/v1/me/playlists?limit=50"
profileEndpoint = "https://api.spotify.com/v1/me"


# make refresh token more rigid so it passes things correctly
    
#base api calls

def callApi(url, headers, data, refreshToken):
  request = apiRequest(url, headers, data)
  response = handleApiCall(request, refreshToken, url, headers, data, )
  return response

def apiRequest(url, headers, data):
  apiRequest = requests.get(url, headers=headers, data=data)
  return apiRequest

def handleApiCall(request, refreshToken, url, headers, data, ):
  if request.status_code == 200:
    data = request.json()
    return data

  elif request.status_code == 401:
    newAccessToken = refreshAccessToken(refreshToken)
    headers['Authorization'] = 'Bearer '+ newAccessToken
    request = callApi(url, headers, data, refreshToken)
    data = request.json()
    return data
    
  else:
    print(f"request text is{request.text} and request status code is {request.status_code}")
    return None

def apiTokenPost(headers, data):

  apiRequest = requests.post(tokenURL, headers=headers, data=data)
  
  if apiRequest.status_code == 200:
    data = apiRequest.json()
    return data
  else:
    print(f"request text is{apiRequest.text} and request status code is {apiRequest.status_code}")
    return None
  

#access token refreshing

def refreshAccessToken(refreshToken):

  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {
    "client_id" : clientID,
    "client_secret": clientSecret,
    "grant_type": 'refresh_token',
    "refresh_token": refreshToken,
  }

  data = apiTokenPost(headers, data)
  if data == None: return None
  
  newAccessToken = data['access_token']
  return newAccessToken

#retrieving playlist tracks with chunked requests
#then shuffling them
#then making new playlist

def chunkedTrackLoad(plID, playlistLength, accessToken):
  trackUris = []

  offset = 0
  for x in range(math.ceil(int(playlistLength)/50)):
    
    headers = {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization": f"Bearer {accessToken}"
    }
    data = {
    }

    trackResponse = apiRequest(f"https://api.spotify.com/v1/playlists/{plID}/tracks?limit=50&offset={offset}", headers, data)

    for item in trackResponse.json()['items']:
      if item['is_local'] != True: 
        trackUris.append(item["track"]["uri"])

    offset += 50

  return trackUris

def makeNewPlaylist(shuffledTracks, playlistName, userID, plID, accessToken):

  #creating the playlist

  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {accessToken}"
  }

  data = {
    "name": f"Truly Shuffled {playlistName}",
    "description": f"A truly shuffled version of {playlistName}, made on True Spotify Shuffle."
  }

  createResponse = requests.post(f"https://api.spotify.com/v1/users/{userID}/playlists", headers=headers, json=data)
  

  try:
    data = createResponse.json()
  except:
    print(data)

    
  newID = data['id']
  

  #adding tracks to playlist

  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {accessToken}"
  }

  loopsNeeded = math.ceil(len(shuffledTracks)/100)
  loops = 0
  position = 0
  for x in range(loopsNeeded):

    loops += 1

    if loops == loopsNeeded:
      trackChunk = shuffledTracks[position:]

    else: trackChunk = shuffledTracks[position:position+100]

    data = {
      "uris": trackChunk,
      "position": position
    }

    addResponse = requests.post(f"https://api.spotify.com/v1/playlists/{newID}/tracks", headers=headers, json=data)

    position += 100
  
  return "Truly Shuffled " + playlistName, newID

def SHUFFLE(plID, playlistLength, playlistName, userID, accessToken, refreshToken):

  trackList = chunkedTrackLoad(plID, playlistLength, accessToken)
  random.shuffle(trackList)
  accessToken = refreshAccessToken(refreshToken)
  shuffledPlName, newID = makeNewPlaylist(trackList, playlistName, userID, plID, accessToken)
  return shuffledPlName, newID


#getting the profile details

def getProfile(accessToken, refreshToken):

  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {accessToken}"
  }

  data = {}

  return callApi(profileEndpoint, headers, data, refreshToken)

#getting the playlists

def getPlaylist(accessToken, refreshToken):
  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {accessToken}"
  }
  data = {}

  return callApi(playlistEndpoint, headers, data, refreshToken)

#getting access token and refresh token

def callAuthApi(code):

  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
  }
  
  data = {
    "client_id" : clientID,
    "client_secret": clientSecret,
    "grant_type": 'authorization_code',
    "code": code,
    "redirect_uri": baseURL + "/select"
  }
  
  data = apiTokenPost(headers, data)
  if data == None: return None
  
  accessToken = data['access_token']
  refreshToken = data['refresh_token']
  
  return accessToken, refreshToken
