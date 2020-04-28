# -*- coding: utf-8 -*-

from kaggle.api.kaggle_api_extended import KaggleApi

class MyKaggleApi(KaggleApi):
    
    def competition_submissions_cli(self, competition=None, last_only=False):

        if competition is None:
            raise ValueError('No competition specified')
        else:
            submissions = self.competition_submissions(competition)
            fields = [
                'fileName', 'date', 'description', 'status', 'publicScore',
                'privateScore'
            ]
            if submissions:
                return self.submissions_list(submissions, fields, last_only)
            else:
                print('No submissions found')
    
    def submissions_list(self, items, fields, last_only):
        res = []
        for i in items:
            res.append({k: self.string(getattr(i, k)) for k in fields})
            if last_only:
                return res[0]
        return res