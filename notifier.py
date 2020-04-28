# -*- coding: utf-8 -*-

import telebot
from api import MyKaggleApi
import time
from datetime import datetime, timedelta
from pytz import timezone

# In[]: Proxies list is available here: http://spys.one/en/socks-proxy-list/
IP = '96.113.176.101' # Proxy IP
PORT = '1080' # Proxy Port
telebot.apihelper.proxy = {'https': f'socks5h://{IP}:{PORT}'}

# In[]: Telegram bot stuff
TOKEN = '1234567890:ABCDEFGHIJ' # Your telegram bot token
CHAT_ID = 1234567890 # Your chat id with bot

tb = telebot.TeleBot(TOKEN)

# In[]: Kaggle API stuff                     
api = MyKaggleApi()
api.authenticate()

# In[]:
COMPETITION = 'abstraction-and-reasoning-challenge' # Kaggle Competition Name
TIME_START_MONITOR_GAP = 15 # Timestep for refreshing your submissions list before new submission appears
TIME_SUBMISSION_END_GAP = 5 # Timestep for refreshing your submissions list while your submission is being executed

while True:
    result = api.competition_submissions_cli(competition=COMPETITION, last_only=True)
    
    while result['status'] == 'complete':
        result = api.competition_submissions_cli(competition=COMPETITION, last_only=True)
        time.sleep(TIME_START_MONITOR_GAP)

    message = f"Kernel: {result['fileName']}\n" \
    f"Submission time: {result['date']} UTC\n" \
    f"Status: {result['status']}\n" \
    f"Public score: {result['publicScore']}\n"
    print(message)
    
    try:
        tb.send_message(CHAT_ID, message)
    except Exception as e:
        print(e)
    
    while result['status'] == 'pending':
        result = api.competition_submissions_cli(competition=COMPETITION, last_only=True)
        time.sleep(TIME_SUBMISSION_END_GAP)
    
    message = f"Kernel: {result['fileName']}\n" \
    f"Submission time: {datetime.now(timezone('UTC')).replace(microsecond=0).replace(tzinfo=None) - timedelta(seconds=TIME_SUBMISSION_END_GAP)} UTC\n" \
    f"Status: {result['status']}\n" \
    f"Public score: {result['publicScore']}\n"
    print(message)
    
    try:
        tb.send_message(CHAT_ID, message)
    except Exception as e:
        print(e)