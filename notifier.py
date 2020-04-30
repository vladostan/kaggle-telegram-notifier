# -*- coding: utf-8 -*-

import telebot
from api import MyKaggleApi
from kaggle.models.kaggle_models_extended import parse
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
TIME_START_MONITOR_GAP = 30 # Timestep for refreshing your submissions list before new submission appears
TIME_SUBMISSION_END_GAP = 5 # Timestep for refreshing your submissions list while your submission is being executed

while True:
    
    result = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
    
    while result['status'] != 'pending':
        result = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
        time.sleep(TIME_START_MONITOR_GAP)
        
    time_start = parse(result['date'])

    message = f"Submission name: {result['fileName']}\n" \
    f"Submission id: {result['ref']}\n" \
    f"Submission url: {result['url']}\n" \
    f"Submission start time: {time_start} UTC\n" \
    f"Submission status: {result['status']}\n"
    print(message)
    
    try:
        tb_message = tb.send_message(CHAT_ID, message)
    except Exception as e:
        print(e)
    
    while result['status'] == 'pending':
        result = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
        time.sleep(TIME_SUBMISSION_END_GAP)
        
    time_finish = datetime.now(timezone('UTC')).replace(microsecond=0).replace(tzinfo=None) - timedelta(seconds=TIME_SUBMISSION_END_GAP)
    
    message = f"Submission name: {result['fileName']}\n" \
    f"Submission id: {result['ref']}\n" \
    f"Submission url: {result['url']}\n" \
    f"Submission finish time: {time_finish} UTC\n" \
    f"Submission status: {result['status']}\n" \
    f"Submission public score: {result['publicScore']}\n" \
    f"Submission runtime: {int((time_finish-time_start).total_seconds())} seconds"
    print(message)
    
    try:
        if tb_message:
            tb.reply_to(tb_message, message)
        else:
            tb.send_message(CHAT_ID, message)
    except Exception as e:
        print(e)