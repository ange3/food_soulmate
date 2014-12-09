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


NUM_THRESHOLD_VALS = 20 # test 3 threshold values
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

def createNodeToUserIDMap(userMap):
	nodeToUserIDMap = {}
	for userID in userMap.keys(): 
		nodeID = userMap[userID]['node_id']
		nodeToUserIDMap[nodeID] = userID
	return nodeToUserIDMap

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
	print 'len(globalBusinessMap)',len(globalBusinessMap)
	counter = 0
	numNewElem = 0
	for businessID in globalBusinessMap.keys():
		numUsersInBusiness = len(globalBusinessMap[businessID])
		for userIDindex1 in xrange(numUsersInBusiness):
			for userIDindex2 in xrange(userIDindex1 + 1, numUsersInBusiness):
				userID1 = globalBusinessMap[businessID][userIDindex1]
				userID2 = globalBusinessMap[businessID][userIDindex2]
				# print 'userID1: ',userID1
				# print 'userID2: ',userID2
				if userID1 == userID2:
					print 'nope!'
					continue
				pair = frozenset([userID1, userID2])
				ratingScore = gen_food_network.calculateRatingSimForBusiness(userMap[userID1], userMap[userID2], businessID)
				counter += 1
				if counter % 1000 == 0: 
					print 'calculation #: ',counter,' ratingScore for this calc: ',ratingScore
				if pair not in ratingsMap.keys():
					ratingsMap[pair] = ratingScore
					numNewElem += 1
					if numNewElem % 1000 == 0:
						numNewElem,' newElem!'
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

#def runTrial(ratingEdgeList, userMap):
def runTrial():	
	#thresholdVals = [0.0] * NUM_THRESHOLD_VALS
	thresholdVals = [0, 0.005, 0.01, 0.015, 0.02, 0.0025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
	thresholdData = {}

	# review_data = util.loadJSON('../yelp/review.json')
	# userMapFile = "data/user_list_map_phoenix_friendsAndReview.p"
	# userMapToDump = pickle.load( open( userMapFile, "rb" ) )
	# for userID in userMapToDump.keys():
	# 	userMapToDump[userID]['restaurantMap'] = {}
	# 	userMapToDump[userID]['reviewMap'] = {}

	# # print 'Generating MetaData...'
	# gen_food_network.createMetaData(review_data, userMapToDump) # this step takes some time (~2 mins)

	userMap = importJsonUM()
	globalBusinessMap = importJsonGBM()
	numBusinesses = len(globalBusinessMap)

	nodeToUserIDMap = createNodeToUserIDMap(userMap)

	#for i in xrange(NUM_THRESHOLD_VALS):
		#thresholdVals[i] = i * 0.01 # [0.1, 0.2, 0.3, 0.4, 0.5] as test values for threshold

	print 'Selecting 1000 random edges from ratingEdgeList...'
	sample_size = 10
	randomEdges = {}
	for i in xrange(sample_size):
		businessList = random.sample(globalBusinessMap, 1)
		business = businessList[0]

		while len(globalBusinessMap[business]) < 2:
			business = random.sample(globalBusinessMap.keys(), 1)
		pair = frozenset(random.sample(globalBusinessMap[business], 2))
		#nodeIDpair = frozenset([ nodeToUserIDMap[pair[0]], nodeToUserIDMap[pair[1]] ])
		userID1, userID2 = pair
		pair = frozenset([str(userID1), str(userID2)])
		ratingScore = gen_food_network.calculateRatingSimForBusiness(userMap[userID1], userMap[userID2], business)
		attrScore = gen_food_network.getAttrCompScore(userMap[userID1], userMap[userID2])
		print "Rating score: %f, Attr score: %f" % (ratingScore, attrScore)
		randomEdges[pair] = {"Rating":ratingScore, "Attribute":attrScore}

	thresholdScore = {}
	highestAccuracy = 0
	highestAccuracyThreshold = 0

	for threshold in thresholdVals:
		correctCount = 0
		for pair in randomEdges.keys():
			correct = ((ratingScore > 0) == (attrScore > thresholdVal))
			if correct:
				correctCount += 1
		print "Correctly classified: %d" % correctCount
		if correctCount > highestAccuracy:
			highestAccuracy = correctCount
			highestAccuracyThreshold = threshold
		thresholdScore[threshold] = correctCount

	print "Print highestAccuracy: %f" % float(highestAccuracy)/1000
	print "Threshold with highestAccuracy: %f" % highestAccuracyThreshold

	thresholdScoresFile.open("thresholdScores", "w")
	json.dump(thresholdScore, thresholdScoresFile, indent=4)
	thresholdScoresFile.close()




	# while len(randomEdges) < 1000: # want 1000 random edges 
	# 	rand_edge = random.choice(ratingEdgeList) # randomly select 1000 edges from ratingEdgeList
	# 	if rand_edge not in randomEdges:
	# 		randomEdges.append(rand_edge)
	
	#randomEdges = random.sample(randomEdgeList, sample_size)
	



	# for thresholdVal in thresholdVals: # for each potential threshold
	# 	print 'Calculating Attr Comp Scores for thresholdVal: ',thresholdVal,'...'
	# 	correct = 0
	# 	for edge in randomEdges:
	# 		user1ID = ''
	# 		user2ID = ''
	# 		for key in userMap.keys(): # find the correct user IDs from the node ID given
	# 			if userMap[key]['node_id'] == edge[0]:
	# 				user1ID = key
	# 			if userMap[key]['node_id'] == edge[1]:
	# 				user2ID = key
	# 		user1 = userMap[user1ID]
	# 		user2 = userMap[user2ID]
	# 		attrCompScore = gen_food_network.getAttrCompScore(user1, user2)
	# 		# print 'Attr Comp Score for ',edge,' is: ',attrCompScore
	# 		if attrCompScore > thresholdVal: # Draw edge in the Attribute Similarity network
	# 			attrEdgeList[thresholdVal].append([edge[0], edge[1], attrCompScore])
	# 			if edge[2] > 0: # Edge exists in Rating Similarity Network
	# 				correct += 1 # Hit
	# 		else: # No edge in the Attribute Similarity network
	# 			if edge[2] <= 0: # No edge in Rating Similarity Network
	# 				correct += 1 # Correct rejection
	# 	thresholdData[thresholdVal] = {"Correct":correct, "Accuracy":float(correct)/1000}

	# return attrEdgeList, thresholdData

def main():
	# Initialize business data (happens once) (Blanca)

	##################################COMMENT THIS OUT AFTER RUNNING IT ONE TIME#########################################
	#print 'running oneTimeInit...'
	#ratingEdgeList, userMap = oneTimeInit()
	
	#for i in xrange(NUM_TRIALS):
		#runTrial(ratingEdgeList, userMap)
	runTrial()

	# Find potential threshold that yields maximum accuracy (Larry)

	# Generate the (<30255)-complete graph using attribute scores with that threshold (expensive)

	# Get the clustering of the (<30255)-complete graph using CNM (expensive)

	# Compare clusters on the (<30255)-complete graph against true friends.
		# Recommend any members of node's cluster that isn't a friend.

if __name__ == '__main__':
  main()