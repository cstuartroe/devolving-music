from devolving_music.models.song_comparison import SongComparison
from devolving_music.lib.elo_scoring import elo_rating
from typing import Iterable
from devolving_music.models.song_submission import SongSubmission
cached_submissions=SongSubmission.get_voteable_submissions(3)
Comparison_submissions = SongComparison.get_event_comparisons(3)
def check_compare(comparison_submission:"SongComparison"):
    song1=comparison_submission.first_submission
    song2=comparison_submission.second_submission
    return not song1.compare_present(comparison_submission) and \
    not song2.compare_present(comparison_submission)


def elo_song_rating(comparison_submission:"SongComparison", score_range=30):
    song1=comparison_submission.first_submission
    song2=comparison_submission.second_submission
    song1.energy_score,song2.energy_score=elo_rating(song1.energy_score,song2.energy_score,\
        score_range,comparison_submission.first_peakier)
    if(check_compare(comparison_submission)):
        pass
        # song1.update_info(comparison_submission)
        # song2.update_info(comparison_submission)
        # song1.quality_score,song2.quality_score=elo_rating(song1.quality_score,song2.quality_score,\
        #     score_range,comparison_submission.first_better)
        # song1.energy_score,song2.energy_score=elo_rating(song1.energy_score,song2.energy_score,\
        #     score_range,comparison_submission.first_peakier)
        # song1.post_peak_score,song2.post_peak_score=elo_rating(song1.post_peak_score,song2.post_peak_score,\
        #     score_range,comparison_submission.first_post_peakier)
    
        
def get_scores(comparison_submissions:Iterable[SongComparison]):
    #incomplete implement get_scores
    for compare in comparison_submissions:
        elo_song_rating(compare)