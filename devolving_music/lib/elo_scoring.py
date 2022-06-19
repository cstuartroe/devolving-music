# Python 3 program for Elo Rating
import math

# Function to calculate the Probability
def Probability(rating1, rating2):

	return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


# Function to calculate Elo rating
# K is a constant that determines how much you can gain or lose in one match .
# d is 1 when player A wins 0 when they loseSS
def EloRating(Ra, Rb, K, d):


	# To calculate the Winning
	# Probability of Player B
	Pb = Probability(Ra, Rb)

	# To calculate the Winning
	# Probability of Player A
	Pa = Probability(Rb, Ra)

	# Case When Player A wins
	# Updating the Elo Ratings
	if (d == 1) :
		Ra = Ra + K * (1 - Pa)
		Rb = Rb + K * (0 - Pb)
	

	# Case When Player B wins
	# Updating the Elo Ratings
	else :
		Ra = Ra + K * (0 - Pa)
		Rb = Rb + K * (1 - Pb)
	return Ra,Rb



# This code is contributed by
# Smitha Dinesh Semwal
