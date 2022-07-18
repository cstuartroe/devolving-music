from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison


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

    @staticmethod
    def get_voteable_submissions(Event):

        voteable_submissions = [
            sub

            for sub in SongSubmission.objects.filter(event__exact=Event).order_by('id')
            if sub.voteable()

        ]
        return voteable_submissions

    @staticmethod
    def get_song_scores_dict(Event):

        song_subs = ScoreSuite.get_voteable_submissions(Event)

        score_objects = list(ScoreSuite(sub) for sub in song_subs)

        song_subs_id = list(sub.id for sub in song_subs)

        voteable_submissions_dict = dict(zip(song_subs_id, score_objects))
        return voteable_submissions_dict

    @staticmethod
    def get_event_comparisons(Event):

        comparison_event_submissions = list(
            SongComparison.objects.select_related('first_submission') .filter(
                first_submission__event__exact=Event).order_by('id'))
        return comparison_event_submissions
