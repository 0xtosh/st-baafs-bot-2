# st-baafs-bot-2
Clock bot as a tribute to the Sint-Baafs Cathedral in Ghent, Belgium

Original idea from the Kolner Dom Twitter account

# Prerequisites
* ```apt install python3 python3-pip ; pip3 install pytz tweepy```
* Get a developer account and Free API 2 keyset from Twitter and replace the four values in the script. Set the API access to READ+WRITE.
* Run the script from cron every hour e.g. 0 * * * * /usr/bin/python3 /home/bots/stbaafs-bot/stbaafsbot.py > /dev/null

By Tom Van de Wiele (2023) as a tribute to the city of Ghent, Belgium
