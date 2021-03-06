## Requirements
The code requires pytz, pysocks, pyTelegramBotAPI and Kaggle API to be installed\
The code was tested with Python 3.6.9
```
$ pip install -r requirements.txt
```

You need to configure your Kaggle API Credentials as described [here](https://github.com/Kaggle/kaggle-api/blob/master/README.md) if you haven't done it before.

You also need to create own Telegram Bot to get its token. This is [one](https://firstwarning.net/vanilla/discussion/4/create-telegram-bot-and-get-bots-token-and-the-groups-chat-id) of many instructions available online.

## Run
Change the following parameters inside [notifier.py](https://github.com/vladostan/kaggle-telegram-notifier/blob/master/notifier.py):
```python
TOKEN = '1234567890:ABCDEFGHIJ' # Your telegram bot token
CHAT_ID = 1234567890 # Your chat id with bot
COMPETITION = 'landmark-recognition-2020' # Kaggle Competition Name
```

For now pyTelegramBotAPI is configured to work without proxy. If you want to use proxy, change the following parameters:
```python
PROXY = True
IP = '96.113.176.101' # Proxy IP
PORT = '1080' # Proxy Port
```
There are also few parameters that you could change:

```python
TIME_START_MONITOR_GAP = 30 # Timestep for refreshing your submissions list before new submission appears
```
Run the script:
```
$ python notifier.py
```

The program will continuously monitor your submissions list. When new submission appears, you will receive the Telegram notification. After the submission ending you will receive the Telegram message as well. The program also outputs message to terminal, because sometimes Telegram services may not work or proxy may fail. For now, the program can monitor submissions for only ONE competition.

## Notification example

```
Competition: landmark-recognition-2020
Submission name: sample submission
Submission id: 12345678
Submission url: https://www.kaggle.com/user/sample-submission?scriptVersionId=12345678
Submission status: pending
Submission start time: 2020-09-15 20:34:39 UTC
```
```
Competition: landmark-recognition-2020
Submission name: sample submission
Submission id: 12345678
Submission url: https://www.kaggle.com/user/sample-submission?scriptVersionId=12345678
Submission status: complete
Submission public score: 0.1234
Submission finish time: 2020-09-15 20:55:13 UTC
Submission runtime: 1234 seconds
```