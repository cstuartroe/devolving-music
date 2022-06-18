#test script for sorting



voteable_submissions = [
            sub
            for sub in SongSubmission.objects.filter(event__exact=1).order_by('?')
            if sub.voteable()
        ]
sub1= voteable_submissions[:]
print(sub1[0])