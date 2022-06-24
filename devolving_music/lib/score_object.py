from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.event import Event



class ScoreObject():
    def __init__(self, song_sub: "SongSubmission"):
            self.song_submission = song_sub
            self.energy_score = None
            self.quality_score = None
            self.post_peak_score = None
            self.counted_compares = set()
    @property
    def info_score(self):
        return len(self.counted_compares)

    def log_comparison(self, comparison: "SongComparison"):
        self.counted_compares.add(comparison.id)

    def compare_present(self, comparison: "SongComparison"):
        return comparison.id in self.counted_compares

    def __str__(self):
        string_output = f"Song:{self.song_submission} \n Energy Score:{self.energy_score}\
                        \n Quality Score:{self.quality_score} \n Post Peak Score:{self.post_peak_score}\
                        \n Info Score:{self.info_score} "
        return string_output
