# -*- coding: utf-8 -*-

import telebot
from api import MyKaggleApi, Notifier
import time

# In[]: Proxies list is available here: http://spys.one/en/socks-proxy-list/
PROXY = False

if PROXY:
    IP = '96.113.176.101' # Proxy IP
    PORT = '1080' # Proxy Port
    telebot.apihelper.proxy = {'https': f'socks5h://{IP}:{PORT}'}

# In[]: Telegram bot stuff
TOKEN = '1234567890:ABCDEFGHIJ' # Your telegram bot token
CHAT_ID = 1234567890 # Your chat id with bot

tb = telebot.TeleBot(TOKEN)

# In[]:                      
kapi = MyKaggleApi()
notifier = Notifier(tb, CHAT_ID)

# In[]:
COMPETITION = 'landmark-recognition-2020' # Kaggle Competition Name
TIME_START_MONITOR_GAP = 30 # Timestep for refreshing your submissions list before new submission appears

# In[]:
try:
    
    pendings = {}
        
    while True:
    
        try:
            submissions = kapi.competition_submissions(competition=COMPETITION, num=10)
        except:
            notifier.api_error()
        
        if submissions:
            for submission in submissions:
                if submission.status == 'pending' and submission.id not in pendings:
                    tb_message = notifier.notify(submission.start_info())
                    pendings[submission.id] = tb_message
                    time.sleep(submission.update_period)
                
        time.sleep(TIME_START_MONITOR_GAP)
        
        try:
            submissions = kapi.competition_submissions(competition=COMPETITION, num=10)
        except:
            notifier.api_error()
        
        if submissions:
            for submission in submissions:
                if submission.status != 'pending' and submission.id in pendings:
                    notifier.notify(submission.finish_info(), pendings[submission.id])
                    del pendings[submission.id]
                                
        time.sleep(TIME_START_MONITOR_GAP)
        
except KeyboardInterrupt:
    
    notifier.shutdown()