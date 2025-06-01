import os
import time
from datetime import datetime, timedelta
from atproto import Client, models
import pytz
import argparse
import random

CREDENTIALS_FILE = 'credentials.txt' # should contain the bluesky handle on one line and app password on the second line
BLUESKY_HANDLE = None
BLUESKY_APP_PASSWORD = None
BELL_TOWER_TIMEZONE = pytz.timezone('Europe/Brussels')

EMOJIS = ["🔔", "🎶", "🎵"]

def log_message(message):
    timestamp = datetime.now(BELL_TOWER_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    print(f"[{timestamp}] {message}")

def load_credentials():
    global BLUESKY_HANDLE, BLUESKY_APP_PASSWORD
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                BLUESKY_HANDLE = lines[0].strip()
                BLUESKY_APP_PASSWORD = lines[1].strip()
                log_message(f"Credentials loaded from {CREDENTIALS_FILE}")
                return True
            else:
                log_message(f"Error: {CREDENTIALS_FILE} must contain at least two lines (handle and app password).")
                return False
    except FileNotFoundError:
        log_message(f"Error: {CREDENTIALS_FILE} not found. Please create it with your Bluesky handle and app password.")
        return False
    except Exception as e:
        log_message(f"Error loading credentials from {CREDENTIALS_FILE}: {e}")
        return False

client = Client()

def login_to_bluesky():
    if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
        log_message("Bluesky handle or app password not loaded. Cannot log in.")
        return False

    try:
        log_message(f"Attempting to log in as {BLUESKY_HANDLE}...")
        client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        log_message("Successfully logged in to Bluesky!")
        return True
    except Exception as e:
        log_message(f"Error logging in to Bluesky: {e}")
        return False

def post_bell_tower_chime(debug_mode=False, debug_hour=None):
    current_time = datetime.now(BELL_TOWER_TIMEZONE)
    log_message(f"Checking hour in {current_time.tzname()}: {current_time.strftime('%H:%M:%S')}")

    post_text = None
    hour_to_post = None

    if debug_mode:
        log_message("Debug mode active.")
        if debug_hour:
            hour_to_post = debug_hour
            log_message(f"Debug mode: Using specified hour: {hour_to_post}")
        else:
            hour_to_post = int(current_time.strftime('%I'))
            log_message(f"Debug mode: No specific hour provided, using current hour: {hour_to_post}")
    elif current_time.minute == 0:
        log_message("We are at the top of the hour!")
        hour_to_post = int(current_time.strftime('%I'))
    else:
        log_message("We are not at the top of the hour. Not doing anything, bye.")
        return

    if hour_to_post:
        random_emoji = random.choice(EMOJIS)

        post_text = random_emoji + " " + "DONG " * hour_to_post
        log_message(f"Generated post: '{post_text}' for hour {hour_to_post}.")

        log_message(f"Attempting to post: '{post_text}'")
        try:
            client.post(text=post_text)
            log_message("Post successful!")
        except Exception as e:
            log_message(f"Error posting to Bluesky: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bluesky Bell Tower Bot that posts hourly chimes.")
    parser.add_argument('--debug', action='store_true',
                        help="Enable debug mode. Posts will be attempted regardless of the minute.")
    parser.add_argument('--hour', type=int, choices=range(1, 13),
                        help="Specify the hour (1-12) for debug mode. If not provided in debug mode, "
                             "the current system hour will be used.")
    args = parser.parse_args()

    if not load_credentials():
        log_message("Bot failed to start due to credential loading error.")
        exit(1)

    if not login_to_bluesky():
        log_message("Bot failed to start due to login error. Please check your credentials.")
        exit(1)

    post_bell_tower_chime(debug_mode=args.debug, debug_hour=args.hour)
    log_message("Script finished execution.")
