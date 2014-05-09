from datetime import datetime
from django.shortcuts import render
import web
from web import form
import sys
import time
sys.path.insert(0, '/home/LISTPLAY1/LISTPLAY')
from listplay import list_play,create_playlist,year,file_txt,auth
from django import forms
from django.shortcuts import render_to_response
from django.template.context import RequestContext
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
import threading

DEVELOPER_KEY = "AIzaSyDRGb6TjiIJAdV3VHLjkt7WZJHlu-lF5Sc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class ContactForm(forms.Form):
    songsText=file_txt('/home/LISTPLAY1/LISTPLAY/songsText.txt')
    title = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'round','id':'title','placeholder': 'My PlayList','size':'17'}))
    artist = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'round','id':'artist','placeholder': 'Various Artists','size':'17'}))
    songs = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={'class':'round','id':'songs','rows':10, 'cols':50,'placeholder': songsText}))
    reverse = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'type':'checkbox', 'value':'None','name':'check','id':'slideTwo'}))

class MContactForm(forms.Form):
    songsText=file_txt('/home/LISTPLAY1/LISTPLAY/MsongsText.txt')
    title = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'round','id':'title','placeholder': 'My PlayList','size':'17'}))
    artist = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'round','id':'artist','placeholder': 'Various Artists','size':'17'}))
    songs = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={'class':'round','id':'songs','rows':10, 'cols':50,'placeholder': songsText}))
    reverse = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'type':'checkbox', 'value':'None','name':'check','id':'slideTwo'}))


from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            global SONGS
            SONGS = form.cleaned_data['songs']
            global ERR
            ERR=form.errors
            global TITLE
            TITLE = form.cleaned_data['title']
            global REVERSE
            REVERSE = form.cleaned_data['reverse']
            global ARTIST
            ARTIST = form.cleaned_data['artist']
            return HttpResponseRedirect('/thanks/')
        else:
            global YEAR
            YEAR=year()
            global Pid
            form = ContactForm()
            return render(request, 'index.html', {'form': form,'YEAR':YEAR},context_instance=RequestContext(request))
    else:
        global YEAR
        YEAR=year()
        global Pid
        form = ContactForm()
        return render(request, 'index.html', {'form': form,'YEAR':YEAR},context_instance=RequestContext(request))

def mobile(request):
    if request.method == 'POST':
        form = MContactForm(request.POST)
        if form.is_valid():
            global SONGS
            SONGS = form.cleaned_data['songs']
            global ERR
            ERR=form.errors
            global TITLE
            TITLE = form.cleaned_data['title']
            global REVERSE
            REVERSE = form.cleaned_data['reverse']
            global ARTIST
            ARTIST = form.cleaned_data['artist']
            return HttpResponseRedirect('/mobileT/')
        else:
            global YEAR
            YEAR=year()
            global Pid
            form = MContactForm()
            return render(request, 'mobile.html', {'form': form,'YEAR':YEAR},context_instance=RequestContext(request))
    else:
        global YEAR
        YEAR=year()
        global Pid
        form = MContactForm()
        return render(request, 'mobile.html', {'form': form,'YEAR':YEAR},context_instance=RequestContext(request))

def thanks(request):
    return output(request,False)

def mobileT(request):
    return output(request,True)

def output(request,m):
    output=""
    try:
        TITLE
    except NameError:
        TITLE=""
    else:
        {}
    TITLE=TITLE+" Made with ListPlay "
    Pid=create_playlist(YT="",title=TITLE)
    (s,E)=list_play(Pid,text=SONGS,artist=ARTIST,rev=REVERSE)
    if s==0:
        output=str('<a class="button-link" href="https://www.youtube.com/playlist?list=')+str(Pid)+str('"target="_blank" >Go to PlayList</a>')
    elif s==1:
        output=str('<span id="error"> No songs were found. <br /> Please try again using the official <br /> title and full performer&#39s name.</span>')
    elif s==2:
        output=str('<span id="error">The maximum playlist length is 200 songs. <br />  Please split your playlist appropriately.</span>')
    elif s==3:
        output=str('<span id="error">No songs were received. Please try again.</span>')
    elif s==4:
        output=str('<a class="button-link" href="https://www.youtube.com/playlist?list=')+str(Pid)+str('"target="_blank" >Go to PlayList</a><br />  <span id="error">Some songs could not be found. <br /> Please try again using the official <br /> title and full performer&#39s name.</span> ')
    if m:
        return render(request, 'Mthanks.html', {'output':output,'YEAR':YEAR})
    else:
        return render(request, 'thanks.html', {'output':output,'YEAR':YEAR})
