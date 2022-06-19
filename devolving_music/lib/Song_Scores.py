from devolving_music.lib.elo_scoring import *
class Song_Scores():
    
    def __init__(self,Song):
        self._song_submision=Song
        self._energy_score=0
        self._quality_score=0
        self._post_peak_score=0
        self._info_score=0

    @property
    def energy_score(self):
        return self._energy_score
    @property
    def quality_score(self):
        return self._energy_score
    @property
    def post_peak_score(self):
        return self._post_peak_score
    @property
    def info_score(self):
        return self._info_score
    def __str__(self):
        string_output=f"Song:{self._song_submision} \n Energy Score:{self._energy_score}\
                        \n Quality Score:{self._quality_score} \n Post Peak Score:{self._post_peak_score}\
                        \n Info Score:{self._info_score} "
        return string_output
    @staticmethod
    def get_Scores(Comparison_submissions):
        #incomplete implement get_scores
        x,y=EloRating(10, 1, 30, 1)
        return x,y