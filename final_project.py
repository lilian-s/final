## SI 206 2017
## Final Project

## Name: Lilian Sheu
## Discussion: Thursdays 3-4pm

import unittest
import itertools
import collections
import requests

# import API's
import insta_info
# import tweepy
# import twitter_info

import json
import sqlite3
import re
import sys
import datetime
from time import sleep
from instagram import client, oauth2, InstagramAPIError
from instagram.client import InstagramAPI

# instagram authentication for insta_info file
insta_client_id = insta_info.client_id
insta_client_secret = insta_info.client_secret
insta_access_token = insta_info.access_token
insta_api = InstagramAPI(client_id=insta_client_id, client_secret=insta_client_secret, 
	access_token=insta_access_token)
liked_media, url = insta_api.user_liked_media()
insta_cache_fname = 'insta_cache.json'

import hmac
from hashlib import sha256

def generate_sig(endpoint, params, secret):
    sig = endpoint
    for key in sorted(params.keys()):
        sig += '|%s=%s' % (key, params[key])
    return hmac.new(secret, sig, sha256).hexdigest()

endpoint = '/media/p/BcdKbapj-uO/'
params = {
    'access_token': insta_access_token,
    'count': 20,
}
insta_client_secret = '6dc1787668c64c939929c17683d7cb74'

sig = generate_sig(endpoint, params, insta_client_secret)
print(sig)

#api = InstagramAPI.API(auth, parser=InstagramAPI.parsers.JSONParser())
#'https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN'

# for media in liked_media:
# 	print(media)

try:
    cache_file = open(insta_cache_fname,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    INSTA_CACHE_DICTION = json.loads(cache_contents)
except:
    INSTA_CACHE_DICTION = {}

def get_user_insta():
	if 'x' in INSTA_CACHE_DICTION:
		print('Using Cached Data')
		insta_results = INSTA_CACHE_DICTION['x']
	else:
		print('Getting Data From Instagram')
		insta_results = liked_media
		INSTA_CACHE_DICTION['x'] = insta_results
		f = open(insta_cache_fname, 'w')
		f.write(json.dumps(INSTA_CACHE_DICTION, indent=2)) #indent to make cache more readable
		f.close()
	return insta_results

# Using my own Instagram username
#insta_test = get_user_insta()

table = sqlite3.connect('FinalProject.sqlite')
cur = table.cursor()
cur.execute('DROP TABLE IF EXISTS Instagram')
#cur.execute('DROP TABLE IF EXISTS Users')
#cur.execute("""CREATE TABLE Tweets (tweet_id TEXT PRIMARY KEY, "text" TEXT, user_posted TEXT, 
#	time_posted DATETIME, retweets INTEGER, FOREIGN KEY(user_posted) REFERENCES Users(user_id))""""")
#cur.execute("""CREATE TABLE Users (user_id TEXT PRIMARY KEY, 
#	screen_name TEXT, num_favs INTEGER, description TEXT)""")