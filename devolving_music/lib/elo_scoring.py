# Python 3 program for Elo Rating
import math

# Function to calculate the probability
def probability(rating1, rating2,league_score_difference):
	return 1.0 / (1 + float(math.pow(10, float((rating1 - rating2)) / league_score_difference)))
# Function to calculate Elo rating
# k is a constant that determines how much you can gain or lose in one match .
# d is 1 when player A wins 0 when they loseSS
# league score difference determines how large your difference in rating has to be 
	# before you are considered to be in a different league
	# for example if your league score difference is 400
	# leagues  could look like this 
	# crappy garbage:-800 bronze=-400 gold=0 silver:400 really really good:800
def elo_rating(ra, rb, k, d,league_score_difference=400):
	if ra is None:
		ra = 0
	if rb is None:
		rb = 0
	pb = probability(ra, rb,league_score_difference)
	pa = probability(rb, ra,league_score_difference)
	# Case When Player A wins
	# Updating the Elo Ratings
	if d == 1:
		ra = ra + k * (1 - pa)
		rb = rb + k * (0 - pb)
	# Case When Player B wins
	# Updating the Elo Ratings
	else:
		ra = ra + k * (0 - pa)
		rb = rb + k * (1 - pb)
	return ra, rb
