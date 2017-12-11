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

import json
import sqlite3
import re
import sys
import datetime
import instagram
from instagram.client import InstagramAPI

### 
### INSTAGRAM API BELOW
###
# instagram authentication for insta_info file
insta_client_id = insta_info.client_id
insta_client_secret = insta_info.client_secret
insta_access_token = insta_info.access_token
insta_api = InstagramAPI(client_id=insta_client_id, client_secret=insta_client_secret)
insta_url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='+insta_access_token
insta_data = {'key1':'value1', 'key2':'value2'}
recent_media = requests.get(url=insta_url, params=insta_data)

# for the Instagram cache
insta_cache_fname = 'insta_cache.json'
try:
    cache_file = open(insta_cache_fname,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    INSTA_CACHE_DICTION = json.loads(cache_contents)
except:
    INSTA_CACHE_DICTION = {}

def get_user_insta():
	if 'insta_data' in INSTA_CACHE_DICTION:
		print('Using Cached Data')
		insta_results = INSTA_CACHE_DICTION['insta_data']
	else:
		print('Getting Data From Instagram')
		# use json.loads to indent/make cache more readable
		insta_results = json.loads(recent_media.text)
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
cur.execute('DROP TABLE IF EXISTS Instagram')
cur.execute("""CREATE TABLE Instagram (post_id TEXT, author TEXT, 
	time_posted DATETIME, latitude TEXT, longitude TEXT)""")
cur.execute('DROP TABLE IF EXISTS "Instagram Tags"')
cur.execute("""CREATE TABLE "Instagram Tags" (hashtags TEXT)""")


# only using data from 'data' key for basic Instagram table
for x in insta_test['data']:
	if x['location'] != None:
		tup = x['id'], x['user']['username'], datetime.datetime.fromtimestamp(int(x['created_time'])), x['location']['latitude'], x['location']['longitude']
		cur.execute('INSERT INTO Instagram (post_id, author, time_posted, latitude, longitude) VALUES(?, ?, ?, ?, ?)',tup)
	else:
		tup = x['id'], x['user']['username'], datetime.datetime.fromtimestamp(int(x['created_time']))
		cur.execute('INSERT INTO Instagram (post_id, author, time_posted) VALUES(?, ?, ?)',tup)
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
# for Facebook API

# import webbrowser
# from requests_oauthlib import OAuth2Session
# from requests_oauthlib.compliance_fixes import facebook_compliance_fix

# APP_ID     = '269135383534303'
# APP_SECRET = '8b5130fddcf755cef3381e1cca4a4472'
# facebook_session = False

# # Reference: https://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
# def makeFacebookRequest(baseURL, params = {}):
#     global facebook_session
#     if not facebook_session:
#         # OAuth endpoints given in the Facebook API documentation
#         authorization_base_url = 'https://www.facebook.com/dialog/oauth'
#         token_url = 'https://graph.facebook.com/oauth/access_token'
#         redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

#         scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
#         facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
#         facebook_session = facebook_compliance_fix(facebook)

#         authorization_url, state = facebook_session.authorization_url(authorization_base_url)
#         print('Opening browser to {} for authorization'.format(authorization_url))
#         webbrowser.open(authorization_url)

#         redirect_response = raw_input('Paste the full redirect URL here: ')
#         facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

#     return facebook_session.get(baseURL, params=params)

# response = makeFacebookRequest('https://graph.facebook.com/me')
# current_user = json.loads(response.text)

# pos_ws = []
# f = open('positive-words.txt', 'r')

# for l in f.readlines()[35:]:
#     pos_ws.append(unicode(l.strip()))
# f.close()

# neg_ws = []
# f = open('negative-words.txt', 'r')
# for l in f.readlines()[35:]:
#     neg_ws.append(unicode(l.strip()))

# class Post():
#     """object representing status update"""
#     def __init__(self, post_dict={}):
#         if 'message' in post_dict:
#             self.message = post_dict['message']
#         else:
#             self.message = ""
#         if 'comments' in post_dict:
#             self.comments = post_dict['comments']['data']
#         else:
#             self.comments = []
#         # [PROBLEM 2B] Now, similarly, if the post has any likes, set self.likes to the value of the list of likes dictionaries. Otherwise, if there are no 'likes', set self.likes to an empty list.
#         if 'likes' in post_dict:
#             self.likes = len(post_dict['likes']['data'])
#         else:
#             self.likes = []

#     def positive(self):
#         return len(pos_ws)

#     def negative(self):
#         return len(neg_ws)

#     def emo_score(self):
#         emo_diff = len(pos_ws) - len(neg_ws)
#         return emo_diff

# # PROBLEM 4: Add comments for these lines of code explaining what is happening in them.
# sample = open('samplepost.json').read()
# sample_post_dict = json.loads(sample)
# p = Post(sample_post_dict)

# # Use the next lines of code if you're having trouble getting the tests to pass. They will help you understand what a post_dict contains, and what your code has actually extracted from it and assigned to the comments and likes instance variables.
# #print(json.dumps(sample_post_dict, indent=4))
# #print(json.dumps(p.comments, indent=4))
# #print(json.dumps(p.likes, indent=4))


# # Now, get a json-formatted version of your last 100 posts on Facebook.
# # (Don't worry if you don't have any feed posts; still write the code to make a request to get your feed.)
# baseurl = 'https://graph.facebook.com/me/feed'


# # PROBLEM 6:
# # Write code to compute the top 3 likers and the top 3 commenters on your posts overall, and save them in lists called top_likers and top_commenters. So top_likers should contain 3 names of people who made the most likes on all your Facebook posts, and top_commenters should contain 3 names of people who made the most comments on all your Facebook posts.
# # HINT: creating dictionaries and sorting may both be useful here!

# ### Code to help test whether problem 6 is working correctly
# try:
#     print ("Top commenters:", top_commenters)
#     for i in range(len(top_commenters)):
#         print(i, top_commenters[i])

#     print("Top likers:", top_likers)
#     for i in range(len(top_likers)):
#         print(i, top_likers[i])
# except:
#     print ("Problem 6 not correct.\ntop_commenters and/or top_likers has not been defined or is not the correct type, or you have another error.")
