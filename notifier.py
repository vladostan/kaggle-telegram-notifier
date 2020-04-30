# -*- coding: utf-8 -*-

import telebot
from api_dev import MyKaggleApi, Notifier
import time
import platform

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
api = MyKaggleApi()
api.authenticate()

# In[]:
COMPETITION = 'abstraction-and-reasoning-challenge' # Kaggle Competition Name
TIME_START_MONITOR_GAP = 30 # Timestep for refreshing your submissions list before new submission appears

# In[]:
try:
    
    while True:
    
        submission = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
        
        while submission.status != 'pending':
            submission = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
            time.sleep(TIME_START_MONITOR_GAP)
            
        tb_message = notifier.notify(submission.start_info())
        
        while submission.status == 'pending':
            submission = api.competition_submissions_cli(competition=COMPETITION, num=1)[0]
            time.sleep(submission.update_period)
            
        notifier.notify(submission.finish_info(), tb_message)
        
except KeyboardInterrupt:
    platform_info = platform.uname()
    message = f"Notifier is shut down on {platform_info.node} @ {platform_info.system}"
    notifier.notify(message)