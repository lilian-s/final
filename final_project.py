## SI 206 2017
## Final Project

## Name: Lilian Sheu
## Discussion: Thursdays 3-4pm

import unittest
import itertools
import collections

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
from instagram.client import InstagramAPI

# instagram authentication for insta_info file
insta_client_id = insta_info.client_id
insta_client_secret = insta_info.client_secret
insta_access_token = insta_info.access_token
insta_api = InstagramAPI(client_secret=insta_client_secret, access_token=insta_access_token)
insta_usr = insta_api.user_search('starlili7s')
print(insta_usr)
#'https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN'