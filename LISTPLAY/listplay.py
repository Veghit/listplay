import Queue
import time
import json
import argparse
import httplib2
import httplib
import os
import sys
from apiclient import discovery
from oauth2client import file
from oauth2client.client import AccessTokenCredentials
from oauth2client import client
from oauth2client import tools
from apiclient.discovery import build
from oauth2client.tools import argparser
from itertools import groupby as g
import thread
from threading import Thread
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import requests
import urllib
from datetime import date
import httplib2
import os
import sys
from apiclient.errors import HttpError
import urllib2
from urllib2 import urlopen, HTTPError
import threading

Q=Queue.Queue()
DEVELOPER_KEY = "AIzaSyDRGb6TjiIJAdV3VHLjkt7WZJHlu-lF5Sc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE=""

def list_play(Pid,text="",artist="",rev=False):
    E=[];
    global YOUTUBE
    if YOUTUBE=="":
        YOUTUBE=auth()
    if text!="":
        lines=text.split("\n")
        s=song_list(lines)
        if len(s)>200:
          return (2,E)
        (L,E)=get_list_safe(s,artist)
        if len(L)<=len(E):
          return (1,E)
        if rev:
          L=reversed(L)
        add_to_playlist(L,Pid)
        if len(E)>0:
            s=4
        else:
            s=0
        return (s,E)
    else:
        return (3,E)

def file_txt(filename="text.txt"):
  with open(filename, "rb") as read_file:
    contents = read_file.read()
    return contents

def song_list(lines,artist=""):
  songs=list()
  for line in lines :
    song=strip(line)
    if (song!="" and (artist!="" or not (is_number(song)))):
      songs.append([song,""])
  for song in songs:
    song[0]=strip(song[0])
  songs=denumerize(songs)
  for song in songs:
    song[0]=strip(song[0])
  return songs

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def denumerize(songs):
  L=len(songs)
  if L==0:
    return songs
  D=[]
  S=[]
  den=False
  for i in range(L):
    j=0
    L2=len(songs[i][0])
    while(j<L2 and songs[i][0][j].isdigit() ):
      j+=1
    if j==0:
      num=0
    else:
      num=int(songs[i][0][:j])
    D.append(i-num)
    S.append(i+num)
  if (D.count(common(D))/float(L)>0.66 or S.count(common(S))/L>0.66):
    den=True
  if(den):
    for song in songs:
      j=0
      char=song[0][j]
      while(char.isdigit() or char==" " or char =="." or char == "  " ):
        j+=1
        char=song[0][j]
      song[0]=song[0][j:]
  return songs

def common(L):
  if L==[]:
    return None
  else:
    return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

def strip(t):
  L0=len(t)
  L=0
  while (L<L0):
    L0=len(t)
    question=t.find('?')
    space=t.find(' ')
    tab=t.find('\t')
    while(question==0 or space==0 or tab==0): # remove prefixes
      t=t[1:]
      question=t.find('?')
      space=t.find(' ')
      tab=t.find('\t')
    if(t[:2]=='. '):
       t=t[2:]
    space=t.rfind(' ')
    tab=t.rfind('\t')
    if (len(t)==0):
      break;
    while(space==len(t)-1 or tab==len(t)-1): # remove suffixes
      t=t[:-1]
      space=t.rfind(' ')
      tab=t.rfind('\t')
    cleaned = ""
    if(t.rfind('  ') !=-1):
      t=t[:t.rfind('  ')]+t[t.rfind('  ')+1:]
    if(t.rfind(' MB') == len(t)-3 or t.rfind(' KB') == len(t)-3):
      if (len(t) >= 7 and t[len(t)-4].isdigit() and t[len(t)-5].isdigit() and t[len(t)-6]=='.' and t[len(t)-7].isdigit()):
        t=t[:-7]
      elif (len(t) >= 6 and t[len(t)-4].isdigit() and t[len(t)-5]=='.' and t[len(t)-6].isdigit()):
        t=t[:-6]
    if(t.rfind('.m4a') == len(t)-4 or t.rfind('.txt') == len(t)-4 or t.rfind('.mp3') == len(t)-4 ):
        t=t[:-4]
    if (len(t) >=4 and t[len(t)-1].isdigit() and t[len(t)-2].isdigit() and t[len(t)-3]==':' and t[len(t)-4].isdigit()): # remove time of song eg. 5:42
      t=t[:-4]
    for letter in t: # clean characters
      O=ord(letter)
      if O==146:
          letter="'"
      if O==243:
          letter="o"
      if O==9:
          letter=" "
      if O<=255 and O!=13 and O!=34 and O!=147 and O!=148 and O!=150:
        cleaned += letter
    t=cleaned
    L=len(t)
  return t

def get_list_safe(songs,artist=""):
  errors=list()
  threads = []
  j=0
  for song in songs:
    q=get_address_safe(song[0],j,artist)
    if q[0]=="":
      errors.append(q[1])
    songs[q[1]][1]=q[0]
    j=j+1
  return (songs,sorted(errors))

def get_address(text,j,artist=""):
  address=""
  text=strip(text);
  text=artist+" "+text
  option=query(text,50)
  vid=youtube_search(option)
  if (len(vid)>0):
    i=0
    check=unicode.lower(vid[i])
    while((check.find("full album")!=-1 or check.find("PARODY")!=-1 or (check.find("live")!=-1 and check.find("performance")!=-1) or check.find("film")!=-1 or (check.find("1080p")!=-1)) and i+1<len(vid)):
      i+=1
      check=unicode.lower(vid[i])
    S=vid[i]
    address=S[S.rfind('(')+1:len(S)-1]
  Q.put([address,j])

def get_address_safe(text,j,artist=""):
  address=""
  text=strip(text);
  text=artist+" "+text
  option=query(text,50)
  vid=youtube_search(option)
  i=0
  address=vid[i][vid[i].rfind('(')+1:len(vid[i])-1]
  if (len(vid)>0):
    check=unicode.lower(vid[i])
    while(blocked(address,'IL') or (check.find("full album")!=-1 or check.find("PARODY")!=-1
           or (check.find("live")!=-1 and check.find("performance")!=-1)
           or check.find("film")!=-1 or (check.find("1080p")!=-1))
          and i+1<len(vid) ):
      i+=1
      address=vid[i][vid[i].rfind('(')+1:len(vid[i])-1]
      check=unicode.lower(vid[i])
  return[address,j]

class query:
    def __init__(self,*args):
        self.q=args[0]
        self.max_results=args[1];

def youtube_search(options):
  while True:
    try:
        search_response = YOUTUBE.search().list(q=options.q,part="id,snippet",maxResults=options.max_results,type='video',regionCode='IL').execute()
        videos = []
        for search_result in search_response.get("items", []):
          if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
          return (videos)
    except (httplib.ResponseNotReady):
        {}

def blocked (ID,country):
  L=YOUTUBE.videos().list(id=ID,part="snippet,contentDetails").execute().get('items')[0].get('contentDetails').get('regionRestriction')
  if L is None:
    return False
  else:
    L=L.get('blocked')
  return (L!=None and country in L)

def threadCheck():
    t=Thread(target=year,args=())
    t.start()


def auth():
    s='/home/LISTPLAY1/LISTPLAY/token.txt'
    client_id='567194806765-l67sshs1orf87ev33736prgrvo5nd1iq.apps.googleusercontent.com'
    client_secret='53r-jI-deYGLR2TtMv6DP9xk'
    text=file_txt(s)
    line=text.find("\n")
    token=text[:line]
    TokenTime=float(text[line+1:])
    now=time.time()
    if (now>TokenTime-300):
      h={'Host':'accounts.google.com','Content-Type':'application/x-www-form-urlencoded'}
      content={'client_id':client_id,'client_secret':client_secret,'refresh_token':'1/LHXhJe83OnuQtiyiLJ2lQzi-FkqYlicr10EczHRv22Q','grant_type':'refresh_token'}
      p=urllib.urlencode(content)
      r = requests.post('https://accounts.google.com/o/oauth2/token', data=p,headers=h)
      TokenTime=r.json().values()[2]+time.time()
      token=r.json().values()[0]
      f = open(s, 'w')
      f.write(token+ '\n' +str(TokenTime))
      f.close()
    credentials = AccessTokenCredentials(token,'my-user-agent/1.0')
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,http=credentials.authorize(httplib2.Http()))



def create_playlist(YT,title):
  if YT=="":
    YT=auth()
  playlists_insert_response = YT.playlists().insert(part="snippet,status",
  body=dict(snippet=dict(title=title,description="This playlist was created with LISTPLAY. Create one at listplay1.pythonanywhere.com"),status=dict(privacyStatus="unlisted"))).execute()
  Pid=playlists_insert_response["id"]
  return Pid

def add_to_playlist(L,Pid):
  for vid in L:
    if vid[1]!="":
      add_video_request=YOUTUBE.playlistItems().insert(
        part="snippet",body={'snippet': {'playlistId': Pid,'resourceId':{'kind': 'youtube#video','videoId': vid[1]}}}).execute()

def elapsed (expression, number =1):
  t1= time.clock ()
  for i in range (number):
    eval (expression)
    print i
  t2= time . clock()
  return ((t2 -t1)/number)

def year():
  return date.today().year