import gen_random_users as genUsers
import gen_food_network as genFoodNet
import gen_eval_network as genEvalNet
import CNMCommunity as CNM
import gen_eval_clusters_toImport as genEvalClst
import json, pickle, snap
import numpy as np

def oneTimeInit():
	#Placeholder code
	file = open( _COMMA_SEPARATED_BUSINESSES_JSON_ , "r")
	businesses = json.load(file)
	file.close()

	# For each business (happens once) (Blanca)
	
		# Calculate rating score between all combinations of 2 authors of that business's reviews
		# Add rating score to list of [NID, NID, Rating Score], i.e. the training edge list.

	return ratingEdgeList

def runTrial(ratingEdgeList):
	# Randomly select 1000 edges from ratingEdgeList (Blanca)
		# For each potential threshold
			# Calculate attribute score (Blanca)

			# Store into list of [NID, NID, Attribute Score]

		# Classify edges in list (Larry)

		# Calculate accuracy of attribute classifications (Larry)

def main():
	#Initialize business data (happens once) (Blanca)
	ratingEdgeList = oneTimeInit()

	for i in xrange(100):
		runTrial(ratingEdgeList)
	
	# Find potential threshold that yields maximum accuracy (Larry)

	# Generate the (<30255)-complete graph using attribute scores with that threshold (expensive)

	# Compare clusters on the (<30255)-complete graph against true friends.
		# Recommend any members of node's cluster that isn't a friend.
