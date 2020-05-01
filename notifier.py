# -*- coding: utf-8 -*-

import telebot
from api import MyKaggleApi, Notifier
import time

# In[]: Proxies list is available here: http://spys.one/en/socks-proxy-list/
IP = '96.113.176.101' # Proxy IP
PORT = '1080' # Proxy Port
telebot.apihelper.proxy = {'https': f'socks5h://{IP}:{PORT}'}

# In[]: Telegram bot stuff
TOKEN = '1234567890:ABCDEFGHIJ' # Your telegram bot token
CHAT_ID = 1234567890 # Your chat id with bot

tb = telebot.TeleBot(TOKEN)
notifier = Notifier(tb, CHAT_ID)

# In[]: Kaggle API stuff                     
kapi = MyKaggleApi()
kapi.authenticate()

# In[]:
COMPETITION = 'abstraction-and-reasoning-challenge' # Kaggle Competition Name
TIME_START_MONITOR_GAP = 30 # Timestep for refreshing your submissions list before new submission appears

# In[]:
try:
    
    notifier.start()
    
    while True:
    
        submission = kapi.competition_submissions(competition=COMPETITION, num=1)[0]
        
        while submission.status != 'pending':
            submission = kapi.competition_submissions(competition=COMPETITION, num=1)[0]
            time.sleep(TIME_START_MONITOR_GAP)
            
        tb_message = notifier.notify(submission.start_info())
        
        while submission.status == 'pending':
            submission = kapi.competition_submissions(competition=COMPETITION, num=1)[0]
            time.sleep(submission.update_period)
            
        notifier.notify(submission.finish_info(), tb_message)
        
except KeyboardInterrupt:
    
    notifier.interrupted()