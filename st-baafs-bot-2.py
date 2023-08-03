import tweepy
from tweepy import API
import time
from datetime import datetime
import pytz
#
# st-baafs-bot 2.0 using free twitter/x APIv2
#
# set cronjob for every hour:
# 0 * * * * /usr/bin/python3 /path/to/stbaafsbot.py > /dev/null
#
api_key             = "fill in"
api_secret          = "fill in"
access_token        = "fill in"
access_token_secret = "fill in"

cest = pytz.timezone('Europe/Paris')  # CEST timezone for Ghent, Belgium
current_time = datetime.now(cest)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client

print("Checking hour...")
if current_time.minute == 0:
   print("We are at the top of the hour!")
   hour_12 = int(current_time.strftime('%I'))
   tweet = "DONG " * hour_12
   print ("Making API connection...")
   client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
   print("Tweeting the hourly amount of DONGS: " + tweet)
   client_v2.create_tweet(text = tweet)
   print ("Done")
else:
   print("We are not at the top of the hour. Not doing anything, bye")

