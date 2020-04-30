# -*- coding: utf-8 -*-

from kaggle.api.kaggle_api_extended import KaggleApi

class MyKaggleApi(KaggleApi):
    
    def competition_submissions(self, competition):
        """ get the list of Submission for a particular competition

            Parameters
            ==========
            competition: the name of the competition
        """
        submissions_result = self.process_response(
            self.competitions_submissions_list_with_http_info(id=competition))
        
        return submissions_result
    
    def competition_submissions_cli(self, competition=None, num=5):

        if competition is None:
            raise ValueError('No competition specified')
        else:
            submissions = self.competition_submissions(competition)
            if submissions:
                return submissions[:num]
            else:
                print('No submissions found')