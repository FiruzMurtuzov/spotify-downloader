
import pafy
from pytube import YouTube
import os

import urllib.request
import re
import requests
from secret import *
import json
import base64
authUrl = 'https://accounts.spotify.com/api/token'
authHeader={}
authData={

}

def getAccessToken(clientID,clientSecret):

    message= f'{clientID}:{clientSecret}'
    message_bytes= message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message=base64_bytes.decode('ascii')

    authData['grant_type']= 'client_credentials'
    authHeader['Authorization'] = 'Basic '+base64_message

    res = requests.post(authUrl,headers=authHeader,data=authData)

    responseObject = res.json()
    #print(json.dumps(responseObject, indent=2))

    accesToken = responseObject['access_token']

    return accesToken
token = getAccessToken(clientID,clientSecret)
print(token)

def getPlaylistTracks(token,playlistID,limit):
    
    playlistEndPoint = f'https://api.spotify.com/v1/playlists/{playlistID}?limit={limit}'
    getHeader={
        'Authorization':"Bearer "+token
    }
    res = requests.get(playlistEndPoint,headers=getHeader)
    playlistObject = res.json()
    return playlistObject
playlistlol = input()
playlistID=playlistlol[34:]

tracklist = getPlaylistTracks(token,playlistID,200)

""" with open('blew.json','w') as f:
    json.dump(tracklist,f) """
alllist= []
for t in tracklist['tracks']['items']:
    ab= str(t['track']['artists'][0]['name'])
    
    ac= str(t['track']['name'])
    
    ac.replace(" ", "")
    ac.replace(" ", "")
    ac.replace("’", "")
    ac.replace("´", "")
    
    ab.replace("-", "")

    abc = ac+'+'+ab
   

    print(ac)
   
    abcd  = ''.join(abc.split())
    abcd = (''.join(abcd)).encode('utf-8')
    alllist.append(abcd)

   


video_urls= []
for url in alllist:
    youtube_search_page = urllib.request.urlopen('https://www.youtube.com/results?search_query='+url.decode("utf-8"))
    video_ids = re.findall(r"watch\?v=(\S{11})", youtube_search_page.read().decode())
    video_id = "https://www.youtube.com/watch?v="+video_ids[0]
    video_urls.append(video_id)
    yt = YouTube(video_id)

    video = yt.streams.filter(only_audio=True).first()
    print(video.title)

    out_file = video.download(output_path="./music")
    print(video_id)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
   

    
 
        
