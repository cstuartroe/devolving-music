from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.song_submission import SongSubmission
from collections.abc import Iterable

class SongScores():
    def __init__(self,submission:SongSubmission):
        self._song_submission=submission
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
        string_output=f"Song:{self._song_submission} \n Energy Score:{self._energy_score}\
                        \n Quality Score:{self._quality_score} \n Post Peak Score:{self._post_peak_score}\
                        \n Info Score:{self._info_score} "
        return string_output
        
    @staticmethod
    def get_scores(comparison_submissions: Iterable[SongSubmission]):
        #incomplete implement get_scores
        ra,rb = elo_rating(10, 1, 30, 1)
        return ra,rb
