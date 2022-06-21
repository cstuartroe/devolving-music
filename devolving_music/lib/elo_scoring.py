# Python 3 program for Elo Rating
import math

# Function to calculate the probability
def probability(rating1, rating2):
	return 1.0 / (1 + float(math.pow(10, float((rating1 - rating2)) / 400)))
# Function to calculate Elo rating
# k is a constant that determines how much you can gain or lose in one match .
# d is 1 when player A wins 0 when they loseSS
def elo_rating(ra, rb, k, d):

	pb = probability(ra, rb)
	pa = probability(rb, ra)
	# Case When Player A wins
	# Updating the Elo Ratings
	if (d == 1) :
		ra = ra + k * (1 - pa)
		rb= rb+ k * (0 - pb)
	# Case When Player B wins
	# Updating the Elo Ratings
	else :
		ra = ra + k * (0 - pa)
		rb= rb+ k * (1 - pb)
	return ra,rb

