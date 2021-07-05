import os

from requests_oauthlib import OAuth1Session

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

twitter = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_TOKEN_SECRET)

res = twitter.get('http://api.twitter.com/1.1/statuses/home_timeline.json')

for status in res.json():
    print('@' + status['user']['screen_name'], status['text'])