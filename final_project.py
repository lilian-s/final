## SI 206 2017
## Final Project

## Name: Lilian Sheu
## Discussion: Thursdays 3-4pm

import unittest
import itertools
import collections
import requests
import json
import sqlite3
import re
import sys
import datetime

# to separate days of week for 28 datapoints total on bar graph
def day_of_week(time):
	day = time.weekday()
	if day == 0:
		dw = 'Mon'
	elif day == 1:
		dw = 'Tues'
	elif day == 2:
		dw = 'Wed'
	elif day == 3:
		dw = 'Thurs'
	elif day == 4:
		dw = 'Fri'
	elif day == 5:
		dw = 'Sat'
	else:
		dw = 'Sun'
	return dw

# to separate times of day for 28 datapoints total on bar graph
def time_of_day(time):
	separate = str(time).split()
	separate2 = separate[1].split(':')
	if int(separate2[0]) < 6:
		td = 'Dawn'
	elif int(separate2[0]) < 12:
		td = 'Morning'
	elif int(separate2[0]) < 18:
		td = 'Afternoon'
	else:
		td = 'Evening'
	return td

### 
### INSTAGRAM API BELOW
###
import insta_info
import instagram
from instagram.client import InstagramAPI
# instagram authentication for insta_info file
insta_client_id = insta_info.client_id
insta_client_secret = insta_info.client_secret
insta_access_token = insta_info.access_token
insta_api = InstagramAPI(client_id=insta_client_id, client_secret=insta_client_secret)
insta_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='+insta_access_token
insta_data = {'key1':'value1', 'key2':'value2'}
insta_recent_media = requests.get(url=insta_url, params=insta_data)

# for the Instagram cache
insta_cache_fname = 'insta_cache.json'
try:
    insta_cache_file = open(insta_cache_fname,'r')
    insta_cache_contents = insta_cache_file.read()
    insta_cache_file.close()
    INSTA_CACHE_DICTION = json.loads(insta_cache_contents)
except:
    INSTA_CACHE_DICTION = {}

def get_user_insta():
	if 'insta_data' in INSTA_CACHE_DICTION:
		print('Using Instagram Cached Data')
		insta_results = INSTA_CACHE_DICTION['insta_data']
	else:
		print('Getting Data From Instagram')
		# use json.loads to indent/make cache more readable
		insta_results = json.loads(insta_recent_media.text)
		INSTA_CACHE_DICTION['insta_data'] = insta_results
		f = open(insta_cache_fname, 'w')
		f.write(json.dumps(INSTA_CACHE_DICTION, indent=4))
		f.close()
	return insta_results
#calling the insta function to collect data for recent 20 posts
insta_test = get_user_insta()

# implementing the Final Project Table
table = sqlite3.connect('FinalProject.sqlite')
cur = table.cursor()
# starting the tables for Instagram data
cur.execute('DROP TABLE IF EXISTS Instagram')
cur.execute("""CREATE TABLE Instagram (post_id TEXT, author TEXT, 
	time_posted DATETIME, day_of_week TEXT, time_of_day TEXT, latitude TEXT, longitude TEXT)""")
cur.execute('DROP TABLE IF EXISTS "Instagram Tags"')
cur.execute("""CREATE TABLE "Instagram Tags" (hashtags TEXT)""")
# only using data from 'data' key for basic Instagram table
for x in insta_test['data']:
	INSTA_DT = datetime.datetime.fromtimestamp(int(x['created_time']))
	if x['location'] != None:
		tup = x['id'], x['user']['username'], INSTA_DT, day_of_week(INSTA_DT), time_of_day(INSTA_DT), x['location']['latitude'], x['location']['longitude']
		cur.execute("""INSERT INTO Instagram (post_id, author, 
			time_posted, day_of_week, time_of_day,
			latitude, longitude) VALUES(?, ?, ?, ?, ?, ?, ?)""",tup)
	else:
		tup = x['id'], x['user']['username'], INSTA_DT, day_of_week(INSTA_DT), time_of_day(INSTA_DT)
		cur.execute("""INSERT INTO Instagram (post_id, author, 
			time_posted, day_of_week, time_of_day) VALUES(?, ?, ?, ?, ?)""",tup)
# for Instagram Hashtags Table
for x in insta_test['data']:
	for y in x['tags']:
		cur.execute('INSERT INTO "Instagram Tags" (hashtags) VALUES(?)',[y])
table.commit()
###
### END OF INSTAGRAM API
###


###
### MOVING ONTO FACEBOOK API
###
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import fb_info
fb_client_id = fb_info.client_id
fb_client_secret = fb_info.client_secret
fb_redirect_uri = fb_info.redirect_uri
fb_access_token = fb_info.access_token
facebook = OAuth2Session(fb_client_id, redirect_uri=fb_redirect_uri)
facebook = facebook_compliance_fix(facebook)

fb_auth_base_url = 'https://www.facebook.com/dialog/oauth'
fb_token_url = 'https://graph.facebook.com/oauth/access_token'

# # Redirect user to Fa
# fb_auth_url, state = facebook.authorization_url(fb_auth_base_url)
# print ('Please go here and authorize,', fb_auth_url)

# # to redirect the user to get the redirect URL needed
# import webbrowser
# webbrowser.open(fb_auth_url)
# # Get the authorization verifier code from the callback url
# redirect_response = input('Paste the full redirect URL here:')

# # Fetch the access token
# facebook.fetch_token(fb_token_url, client_secret=fb_client_secret, authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
# limit to 20 to compare it to Instagram with its limit of 20 posts
# change in date format to match Instagram's
fb_request = facebook.get('https://graph.facebook.com/me/feed?limit=20&date_format=U')

# for the Facebook cache
fb_cache_fname = 'fb_cache.json'
try:
    fb_cache_file = open(fb_cache_fname,'r')
    fb_cache_contents = fb_cache_file.read()
    fb_cache_file.close()
    FB_CACHE_DICTION = json.loads(fb_cache_contents)
except:
    FB_CACHE_DICTION = {}

def get_user_fb():
	if 'fb_data' in FB_CACHE_DICTION:
		print('Using Facebook Cached Data')
		fb_results = FB_CACHE_DICTION['fb_data']
	else:
		print('Getting Data From Facebook')
		# use json.loads to indent/make cache more readable
		fb_results = json.loads(fb_request.text)
		FB_CACHE_DICTION['fb_data'] = fb_results
		f = open(fb_cache_fname, 'w')
		f.write(json.dumps(FB_CACHE_DICTION, indent=4))
		f.close()
	return fb_results
#calling the insta function to collect data for recent 20 posts
fb_test = get_user_fb()

# time to create table Facebook
cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute("""CREATE TABLE Facebook (feed_id TEXT, time_created DATETIME, day_of_week TEXT, time_of_day TEXT)""")

for x in fb_test['data']:
	FB_DT = datetime.datetime.fromtimestamp(x['created_time'])
	fb = x['id'], FB_DT, day_of_week(FB_DT), time_of_day(FB_DT)
	cur.execute('INSERT INTO Facebook (feed_id, time_created, day_of_week, time_of_day) VALUES(?, ?, ?, ?)',fb)
table.commit()
###
### END OF FACEBOOK API
###


###
### MOVING ONTO YOUTUBE API
###
import argparse
import os
import re
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.contrib import gce
import googleapiclient.discovery
from oauth2client.tools import argparser


YT_CLIENT_SECRETS_FILE = "client_secret.json"
YT_SCOPES = ['https://www.googleapis.com/auth/youtube/readonly']
YT_API_SERVICE_NAME = 'youtube'
YT_API_VERSION = 'v3'
YT_DEVELOPER_KEY = 'AIzaSyCOGtw9MsWkOfrG9YZ2c284r3RnMMO9d6s'
yt_channel_id = 'UCy2SY-NCZ-oTXY40H0HlqYQ'


def youtube_list(args):
	youtube = build(YT_API_SERVICE_NAME, YT_API_VERSION,
		developerKey=YT_DEVELOPER_KEY)
#	yt_response = youtube.activities().list(part="snippet,contentDetails", channelId=args.channel_id, maxResults=args.max_results).execute()
	yt_response = youtube.activities().list(part="snippet,contentDetails", channelId=args.channel_id, maxResults=args.max_results).execute()
	return yt_response

if __name__ == "__main__":
	argparser.add_argument("--channel_id", help="Channel ID", default=yt_channel_id)
	argparser.add_argument("--max_results", help="Max results", default=20)
	args = argparser.parse_args()
	yt_response = youtube_list(args)

# for the YouTube cache
yt_cache_fname = 'yt_cache.json'
try:
    yt_cache_file = open(yt_cache_fname,'r')
    yt_cache_contents = yt_cache_file.read()
    yt_cache_file.close()
    YT_CACHE_DICTION = json.loads(yt_cache_contents)
except:
    YT_CACHE_DICTION = {}

def get_user_yt():
	if 'yt_data' in YT_CACHE_DICTION:
		print('Using YouTube Cached Data')
		yt_results = YT_CACHE_DICTION['yt_data']
	else:
		print('Getting Data From YouTube')
		# use json.loads to indent/make cache more readable
		yt_results = yt_response
		YT_CACHE_DICTION['yt_data'] = yt_results
		f = open(yt_cache_fname, 'w')
		f.write(json.dumps(YT_CACHE_DICTION, indent=4))
		f.close()
	return yt_results
#calling the yt function to collect data for recent 20 posts
yt_test = get_user_yt()

# time to create table YouTube
cur.execute('DROP TABLE IF EXISTS YouTube')
cur.execute("""CREATE TABLE YouTube (feed_id TEXT, time_created DATETIME, day_of_week TEXT, time_of_day TEXT)""")

from dateutil import parser
for x in yt_test['items']:
	#converting UTC timestamp to fit the datetime format
	t = x['snippet']['publishedAt']
	YT_DT = datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%S.000Z')
	yt = x['id'], YT_DT, day_of_week(YT_DT), time_of_day(YT_DT)
	cur.execute('INSERT INTO YouTube (feed_id, time_created, day_of_week, time_of_day) VALUES(?, ?, ?, ?)',yt)
table.commit()

