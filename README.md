## Requirements
The code requires pyTelegramBotAPI and Kaggle API to be installed\
Tested with Python 3.6.9
```
$ pip install -r requirements.txt
```

You need to configure your Kaggle API Credentials as described [here](https://github.com/Kaggle/kaggle-api/blob/master/README.md) if you haven't done it before.\
You also need to create own Telegram Bot to get its token. This is [one](https://firstwarning.net/vanilla/discussion/4/create-telegram-bot-and-get-bots-token-and-the-groups-chat-id) of many instructions available online.

## Run
Change the following parameters inside [notifier.py](https://github.com/vladostan/kaggle-telegram-notifier/blob/master/notifier.py):
```python
TOKEN = '1234567890:ABCDEFGHIJ' # Your telegram bot token
CHAT_ID = 1234567890 # Your chat id with bot
COMPETITION = 'abstraction-and-reasoning-challenge' # Kaggle Competition Name
```

For now pyTelegramBotAPI is configured to use proxy. If it fails, change the proxy parameters:
```python
IP = '96.113.176.101' # Proxy IP
PORT = '1080' # Proxy Port
```
There are also few parameters that you could change:

```python
TIME_START_MONITOR_GAP = 15 # Timestep for refreshing your submissions list before new submission appears
TIME_SUBMISSION_END_GAP = 5 # Timestep for refreshing your submissions list while your submission is being executed
```
Run the script:
```
$ python notifier.py
```

The program will continuously monitor your submissions list. When new submission appears, you will receive the Telegram notification. After the submission ending you will receive the Telegram message as well. The program also outputs message to terminal, because sometimes Telegram services may not work or proxy may fail. For now, the program only monitors ONE last submission.

## Notification example

```
Kernel: sample submission
Submission time: 2020-04-28 13:43:50 UTC
Status: pending
Public score: None
```

```
Kernel: sample submission
Submission time: 2020-04-28 14:13:28 UTC
Status: complete
Public score: 0.99
```
