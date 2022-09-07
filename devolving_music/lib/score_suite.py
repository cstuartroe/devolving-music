from math import inf

from devolving_music.lib.elo_scoring import elo_rating
from devolving_music.models.event import Event
from devolving_music.models.serializers.song_submission import SongSubmissionSerializer
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison


def _update_song_rating(
        comparison_submission: "SongComparison",
        song1: "ScoreSuite",
        song2: "ScoreSuite",
        score_range=30) -> None:

    if (not song1.compare_present(comparison_submission)) and not (song2.compare_present(comparison_submission)):
        song1.log_comparison(comparison_submission)

        song2.log_comparison(comparison_submission)

        song1.quality_score, song2.quality_score = elo_rating(
            song1.quality_score, song2.quality_score, score_range, comparison_submission.first_better)

        song1.energy_score, song2.energy_score = elo_rating(
            song1.energy_score, song2.energy_score, score_range, comparison_submission.first_peakier)

        song1.post_peak_score, song2.post_peak_score = elo_rating(
            song1.post_peak_score, song2.post_peak_score, score_range, comparison_submission.first_post_peakier)


class ScoreSuite:

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
        song_sub = self.song_submission
        song = song_sub.song
        artist_list = list(musician.name for musician in song.artists.all())
        string_output = f"Song Submission ID: {song_sub.id} \n Song: {song.title} by {artist_list} \n Energy Score: {self.energy_score}\n Quality Score: {self.quality_score} \n Post Peak Score: {self.post_peak_score}\n Info Score: {self.info_score} "
        return string_output

    def to_json(self):
        return {
            "song_submission": self.song_submission.to_json(),
            "energy_score": self.energy_score,
            "quality_score": self.quality_score,
            "post_peak_score": self.post_peak_score,
            "info_score": self.info_score,
        }
    
    def devolve_distance(self, sub2: "ScoreSuite") -> int:
        sub2_valid = sub2.energy_score is not None and sub2.post_peak_score is not None
        self_valid = self.energy_score is not None and self.post_peak_score is not None
        if sub2_valid and self_valid:
            # Use rectilinear distance rather than Euclidean because one of the dimensions may
            # have some significant error, but less likely that both do
            energy = abs(self.energy_score - sub2.energy_score)
            weirdness = abs(self.post_peak_score - sub2.post_peak_score)
            distance = energy + weirdness
        else:
            distance = inf
        return distance

    @staticmethod
    def get_voteable_submissions(event: Event):
        qs = (SongSubmission.objects.select_related('song').prefetch_related('song__artists')
              .select_related('event').select_related('submitter').prefetch_related('possible_prior_duplicates')
              .filter(event__exact=event).order_by('id'))

        return [
            sub
            for sub in qs
            if sub.voteable()
        ]

    @staticmethod
    def get_song_scores(event: Event) -> list["ScoreSuite"]:
        scores_dict = {
            sub.id: ScoreSuite(sub)
            for sub in ScoreSuite.get_voteable_submissions(event)
        }

        qs = list(SongComparison.objects
                  .select_related('first_submission')
                  .filter(first_submission__event__exact=event)
                  .order_by('id'))

        for comparison in qs:
            song_suite_1 = scores_dict[comparison.first_submission_id]
            song_suite_2 = scores_dict[comparison.second_submission_id]
            _update_song_rating(comparison, song_suite_1, song_suite_2)

        return list(scores_dict.values())

   