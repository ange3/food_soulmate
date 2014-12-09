# import gen_random_users as genUsers
import gen_food_network as genFoodNet
import gen_eval_network as genEvalNet
import CNMCommunity as CNM
import gen_eval_clusters_toImport as genEvalClst
import json, pickle, snap
import numpy as np
import random
import gen_food_network
import util


NUM_THRESHOLD_VALS = 5 # test 3 threshold values
NUM_USERS = 1000
NUM_TRIALS = 1

def importJsonGBM():
	file = open("globalBusinessMap.json", "r")
	gbm = json.load(file)
	file.close()
	return gbm

def importJsonUM():
	file = open("userMap.json", "r")
	um = json.load(file)
	file.close()
	return um

# returns a list of tuples of srcID and dstID of each edge in the ratingEdgeList
def oneTimeInit():
	ratingEdgeList = []
	ratingsMap = {}

	#
	# don't need the below commented out code because we have some JSON files!
	#

	# review_data = util.loadJSON('../yelp/review.json')
	# userMapFile = "data/user_list_map_phoenix_atLeastOneReview.p"
	# userMap = pickle.load( open( userMapFile, "rb" ) )
	# for userID in userMap.keys():
	# 	userMap[userID]['restaurantMap'] = {}
	# 	userMap[userID]['reviewMap'] = {}

	# print 'Generating MetaData...'
	# gen_food_network.createMetaData(review_data, userMap) # this step takes some time (~2 mins)
	# by this point our userMap is pretty substantial

	userMap = importJsonUM()
	globalBusinessMap = importJsonGBM()
	print 'TEST: ',globalBusinessMap['NAoOOwQS_SQEPQe6-8zC-g']

	print 'Generating Eval Network...'
	for businessID in globalBusinessMap.keys():
		numUsersInBusiness = len(globalBusinessMap[businessID])
		for userIDindex1 in xrange(numUsersInBusiness):
			for userIDindex2 in xrange(userIDindex1 + 1, numUsersInBusiness):
				userID1 = globalBusinessMap[businessID][userIDindex1]
				userID2 = globalBusinessMap[businessID][userIDindex2]
				print 'userID1: ',userID1
				print 'userID2: ',userID2
				if userID1 == userID2:
					print 'nope!'
					continue
				pair = frozenset([userID1, userID2])
				ratingScore = gen_food_network.calculateRatingSimForBusiness(userMap[userID1], userMap[userID2], businessID)
				print 'ratingScore: ',ratingScore
				if pair not in ratingsMap.keys():
					ratingsMap[pair] = ratingScore
				else:
					ratingsMap[pair] += ratingScore

	rati_map_file = open('ratingSimMap.json', 'w')
	json.dump(ratingsMap, rati_map_file, indent=4)
	rati_map_file.close()

	edgesFile = 'eval_ntwk_food_friends/eval_ntwk_edge_list_phoenixRatingScoreOnly.txt'
	edgesWithScoreFile = 'eval_ntwk_food_friends/eval_ntwk_edge_list_phoenixRatingScoreOnly_wScores.txt'
	file = open(edgesFile, "w")
	file2 = open(edgesWithScoreFile, "w")

	print 'Writing the Edge List...'
	for pair in ratingsMap:
		key1, key2 = pair
		print 'pair: ',pair
		print 'value: ',ratingsMap[pair]
		if ratingsMap[pair] > 0.0: 
			line = "{0} {1}\n".format(userMap[key1]['node_id'], userMap[key2]['node_id']) 
			lineWithScore = "{0} {1} {2}\n".format(userMap[key1]['node_id'], userMap[key2]['node_id'], ratingsMap[pair])
			file.write(line)
			file2.write(lineWithScore)
			newEdge = userMap[key1]['node_id'], userMap[key2]['node_id']
			print 'newEdge: ',newEdge
			ratingEdgeList.append(newEdge)
	
	file.close()
	file2.close()

	return ratingEdgeList, userMap

def runTrial(ratingEdgeList, userMap):	
	thresholdVals = [0.0] * NUM_THRESHOLD_VALS
	attrEdgeList = {}

	for i in xrange(NUM_THRESHOLD_VALS):
		thresholdVals[i] = (i + 1) * 0.1 # [0.1, 0.2, 0.3, 0.4, 0.5] as test values for threshold
		attrEdgeList[thresholdVals[i]] = []

	print 'Selecting 1000 random edges from ratingEdgeList...'
	randomEdges = []
	while len(randomEdges) < 1000: # want 1000 random edges 
		rand_edge = random.choice(ratingEdgeList) # randomly select 1000 edges from ratingEdgeList
		if rand_edge not in randomEdges:
			randomEdges.append(rand_edge)

	for thresholdVal in thresholdVals: # for each potential threshold
		print 'Calculating Attr Comp Scores for thresholdVal: ',thresholdVal,'...'
		for edge in randomEdges:
			user1ID = ''
			user2ID = ''
			for key in userMap.keys(): # find the correct user IDs from the node ID given
				if userMap[key]['node_id'] == edge[0]:
					user1ID = key
				if userMap[key]['node_id'] == edge[1]:
					user2ID = key
			user1 = userMap[user1ID]
			user2 = userMap[user2ID]
			attrCompScore = gen_food_network.getAttrCompScore(user1, user2)
			# print 'Attr Comp Score for ',edge,' is: ',attrCompScore
			if (attrCompScore > thresholdVal):
				attrEdgeList[thresholdVal].append([edge[0], edge[1], attrCompScore])
	
	# Randomly select 1000 edges from ratingEdgeList (Blanca)
		# For each potential threshold
			# Calculate attribute score (Blanca)

			# Store into list of [NID, NID, Attribute Score]

		# Classify edges in list (Larry)

		# Calculate accuracy of attribute classifications (Larry)

def main():
	# Initialize business data (happens once) (Blanca)
	print 'running oneTimeInit...'
	ratingEdgeList, userMap = oneTimeInit()

	for i in xrange(NUM_TRIALS):
		runTrial(ratingEdgeList, userMap)

	# Find potential threshold that yields maximum accuracy (Larry)

	# Generate the (<30255)-complete graph using attribute scores with that threshold (expensive)

	# Compare clusters on the (<30255)-complete graph against true friends.
		# Recommend any members of node's cluster that isn't a friend.

if __name__ == '__main__':
  main()