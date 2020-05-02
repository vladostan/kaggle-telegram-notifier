# -*- coding: utf-8 -*-

from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.models.kaggle_models_extended import parse
from datetime import datetime, timedelta
from pytz import timezone
import platform

def get_time():
        
    return datetime.now(timezone('UTC')).replace(microsecond=0).replace(tzinfo=None)

class MyKaggleApi(KaggleApi):
    
    def __init__(self):
        super().__init__()
        self.authenticate()
    
    def competition_submissions(self, competition=None, num=5):

        if competition is None:
            raise ValueError('No competition specified')
        else:
            submissions = []
            for submission in self.process_response(self.competitions_submissions_list_with_http_info(id=competition)):
                submissions.append(Submission(submission, competition))
            if submissions:
                return submissions[:num]
            else:
                print('No submissions found')
                
class Submission():
    
    def __init__(self, info, competition, update_period=5):
        
        self.competition = competition
        self.id = info['ref']
        self.name = info['fileName']
        self.url = info['url']
        self.time_start = parse(info['date'])
        self.status = info['status']
        self.public_score = info['publicScore']
        self.update_period = update_period
    
    def __repr__(self):
        
        return f"Submission({self.id})"
    
    def __str__(self):
        
        return f"Competition: {self.competition}\n"\
        f"Submission name: {self.name}\n" \
        f"Submission id: {self.id}\n" \
        f"Submission url: {self.url}\n" \
        f"Submission status: {self.status}"
    
    def start_info(self):
        
        message = str(self) + f"\nSubmission start time: {self.time_start} UTC\n"
        
        return message
        
    def finish_info(self):
        
        self.time_finish = get_time() - timedelta(seconds=self.update_period)
        
        message = str(self) + f"\nSubmission public score: {self.public_score}\n" \
        f"Submission finish time: {self.time_finish} UTC\n" \
        f"Submission runtime: {int((self.time_finish-self.time_start).total_seconds())} seconds\n"
        
        return message
    
class Notifier():
    
    def __init__(self, tb, chat_id, to_console=True):
        self.tb = tb
        self.chat_id = chat_id
        self.to_console = to_console
        self.platform = platform.uname()
        self.start()
        
    def notify(self, message, reply=None):
        
        if self.to_console:
            print(message)
            
        try:
            if reply:
                self.tb.reply_to(reply, message)
            else:
                return self.tb.send_message(self.chat_id, message)
        except Exception as e:
            if self.to_console:
                print(e)
                
    def start(self):
        
        message = f"Kaggle Telegram Notifier initialized on {self.platform.node} @ {self.platform.system}\n" \
        f"Time: {get_time()} UTC\n" \
        f"Starting to monitor submissions\n"
        
        self.notify(message)
        
    def shutdown(self):
        
        message = f"Notifier is shut down on {self.platform.node} @ {self.platform.system}\n" \
        f"Time: {get_time()} UTC\n"
        
        self.notify(message)
        
    def api_error(self):
        
        message = f"Kaggle API is not respoding\n" \
        f"Time: {get_time()} UTC\n"
        
        self.notify(message)