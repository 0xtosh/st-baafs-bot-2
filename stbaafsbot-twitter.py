import tweepy
import time
from datetime import datetime, timedelta
import pytz
import random
import argparse

api_key             = ""
api_secret          = ""
access_token        = ""
access_token_secret = ""

cest = pytz.timezone('Europe/Brussels') 

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client

def log_message(message):
    timestamp = datetime.now(cest).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    print(f"[{timestamp}] {message}")

parser = argparse.ArgumentParser(description="St. Baafs Bot: Tweets the hourly amount of 'DONGS'.")
parser.add_argument(
    '--debug',
    action='store_true', 
    help='Enable debug mode. Tweets will be attempted regardless of the minute. '
         'For testing, the actual tweet command is commented out by default.'
)
parser.add_argument(
    '--hour',
    type=int,
    choices=range(1, 13), 
    help='Specify the hour (1-12) for debug mode. If not provided in debug mode, '
         'the current system hour will be used.'
)

args = parser.parse_args() # Parses the arguments from the command line

current_time = datetime.now(cest)

log_message("Checking hour...")

should_tweet = False
hour_to_tweet = None

if args.debug:
    should_tweet = True
    log_message("Debug mode enabled.")
    if args.hour:
        hour_to_tweet = args.hour
        log_message(f"Debug mode: Tweeting for specified hour: {hour_to_tweet}")
    else:
        hour_to_tweet = int(current_time.strftime('%I'))
        log_message(f"Debug mode: No specific hour provided, using current hour: {hour_to_tweet}")
else:
    if current_time.minute == 0:
        should_tweet = True
        hour_to_tweet = int(current_time.strftime('%I'))
        log_message("We are at the top of the hour!")
        log_message(f"Current hour: {hour_to_tweet}")
    else:
        log_message("We are not at the top of the hour. Not doing anything, bye")

if should_tweet:
    emojis = ["🔔", "🎶", "🎵"]

    random_emoji = random.choice(emojis)

    tweet = random_emoji + " " + "DONG " * hour_to_tweet

    log_message("Making API connection...")
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
    log_message("Tweeting the hourly amount of DONGS: " + tweet)

    log_message("Done")
