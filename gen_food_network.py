import pickle, json, math, snap
import util
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def calculateAttrPref(node, restaurantSet, business_data):
  # positive are attributes that are true, i.e. customer is looking for
  # negative are attributes that are false, i.e. customer does not care about
  attributePrefPos = Counter()
  attributePrefNeg = Counter()
  if len(restaurantSet) == 0:
    node['attributePosPrefCounter'] = None
    node['attributeNegPrefCounter'] = None
    node['avgPriceRange'] = None
    return None

  numRestausWithPrice = 0
  for business in business_data:
    if business['business_id'] in restaurantSet:
      attributeMap = business['attributes']
      for attribute, val in attributeMap.items():
        if type(val) == dict:  #for cases like parking: {garage: True, street: true}
          # iterate through the elements in the attr dict and pull out each attr/val
          for specificAttr in val:
            valList = [val[specificAttr]]
            attributePrefPos[specificAttr] += sum(valList) 
            attributePrefNeg[specificAttr] += len(valList) - sum(valList)
        elif type(val) == str:
          attrStr = str(attribute)+'_'+val
          attributePrefPos[attribute] += 1
        elif type(val) == unicode:
          continue
        else:
          valList = [val]
          attributePrefPos[attribute] += sum(valList)  #sum of a list of bools = number of True vals for this attribute  (True = 1)
          attributePrefNeg[attribute] += len(valList) - sum(valList)
          if attribute == "Price Range":
            numRestausWithPrice += 1
      # store categories as attributes as well
      for cat in business['categories']:
        attributePrefPos[cat] += 1

  # normalize attribute importance scores to 0-1
  numRestau = len(restaurantSet)
  # print 'num restaus', numRestau
  # if numRestausWithPrice != numRestau:
    # print 'ASSUMPTION WRONG: different num restaurants and num restaurants with price'

  for attr, count in attributePrefPos.items():
    # if count > numRestau:
    #   print 'UH OH attribute seen > numRestau', attr
    score = count/float(numRestau)
    # print 'count is {}, score is {}'.format(count, score)
    attributePrefPos[attr] = score
  for attr, count in attributePrefNeg.items():
    score = count/float(numRestau)
    attributePrefNeg[attr] = score

  node['attributePosPrefCounter'] = attributePrefPos
  node['attributeNegPrefCounter'] = attributePrefNeg
  if numRestausWithPrice != 0:
    node['avgPriceRange'] = attributePrefPos['Price Range']/float(numRestausWithPrice)
  else:
    node['avgPriceRange'] = None

'''
  Create meta-data for each user.
  Each user node has the following pieces of information:
    # restaurantMap: {businessID: [reviewID, reviewID ]}
    # reviewMap: {reviewID: rating}
    # attributePosPrefCounter: {restauAttribute: score} --> showing like, scores from 0-1
    # attributeNegPrefCounter: {restauAttribute: score} --> showing dislike
    # avgPriceRange: int

Note: restaurants that are added to the restaurantMap are only food establishments because the reviews.JSON file is pre-screened to only include reviews made for a restaurant 
'''
def createMetaData(review_data, userListMap):
  globalBusinessMap = {}
  for review in review_data:
    userID = review['user_id']
    if userID in userListMap:
      reviewID = str(review['review_id'])
      businessID = str(review['business_id'])
      if businessID not in userListMap[userID]['restaurantMap']:
        userListMap[userID]['restaurantMap'][businessID] = []
      userListMap[userID]['restaurantMap'][businessID].append(reviewID)
      userListMap[userID]['reviewMap'][reviewID] = (review['stars'], review['date'])
    if businessID not in globalBusinessMap.keys():
      globalBusinessMap[businessID] = [userID]
      print 'business added!'
    elif userID not in globalBusinessMap[businessID]:
      globalBusinessMap[businessID].append(userID)
      print 'user added!'
  
  user_map_file = open('userMap.json', 'w')
  json.dump(userListMap, user_map_file, indent=4)
  user_map_file.close()

  business_map_file = open('globalBusinessMap.json', 'w')
  json.dump(globalBusinessMap, business_map_file, indent=4)
  business_map_file.close()

  business_data = util.loadJSON('../yelp/restaurants.JSON')
  for user_id, user in userListMap.items():
    # print user
    restaurantSet = set(user['restaurantMap'].keys())
    # print restaurantSet
    calculateAttrPref(user, restaurantSet, business_data)

# returns the ratio of size of overlapping restaurants set / union of all restaurants
def calculateJaccardSim(node1, node2, restaurantSetA, restaurantSetB):
  # print 'restaurantSetA', restaurantSetA, len(restaurantSetA)
  # print 'restaurantSetB', restaurantSetB, len(restaurantSetB)
  intersectingSet = set.intersection(restaurantSetA, restaurantSetB)
  unionSet = set.union(restaurantSetA, restaurantSetB)
  ratio = float(len(intersectingSet))/len(unionSet)
  # print ratio
  return ratio

# return average of comp score for all attributes
def getAttrCompScore(node1, node2):
  attributePrefA = node1['attributePosPrefCounter']
  attributePrefB = node2['attributePosPrefCounter']
  # allAttributes = attributePrefA.most_common(3) + attributePrefB.most_common(3) # only picking the top 3 most important attributes for A and B and calculating score based on that
  allAttributes = attributePrefA.most_common(len(attributePrefA)) + attributePrefB.most_common(len(attributePrefB))  #picks ALL attributes
  compVals = []
  for attr, totalScore in allAttributes:
    valA = attributePrefA[attr]
    valB = attributePrefB[attr]
    if valB != 0 and valA != 0:
      comp = min(valA/float(valB), valB/float(valA))
      compVals.append(comp)
    # otherwise the comp will def be 0, in which case no need to add to the average
  # print 'compVals', compVals
  return np.mean(compVals)

def calculateRatingSimForBusiness(node1, node2, businessID):
  reviewSetA = node1['restaurantMap'][businessID] # node1's reviews of common restaurant
  reviewSetB = node2['restaurantMap'][businessID] # node2's reviews of common restaurant

  latestDateA = latestDateB = datetime.datetime(2004, 1, 1)
  ratingA = 0.0
  ratingB = 0.0

  for reviewID in reviewSetA: # find node1's most recent review for that restaurant
    date = datetime.datetime.strptime(node1['reviewMap'][reviewID][1], '%Y-%m-%d')
    if date > latestDateA: 
      latestDateA = date
      ratingA = node1['reviewMap'][reviewID][0]

  for reviewID in reviewSetB: # find node2's most recent review for that restaurant
    date = datetime.datetime.strptime(node2['reviewMap'][reviewID][1], '%Y-%m-%d')
    if date > latestDateB: 
      latestDateB = date
      ratingB = node2['reviewMap'][reviewID][0]

  # score for this commonly reviewed restaurant
  score = (2.0 - abs(ratingA - ratingB)) * ( math.pow(abs(ratingA - 3.0), 2.0) + math.pow(abs(ratingB - 3.0), 2.0) ) / 2.0
  return score

# returns the similarity score between node1 and node2 based on the first part of our composite score formula (see Project Milestone)
def calculateRatingSim(node1, node2):
  reviewScores = []
  restaurantSet1 = set(node1['restaurantMap'].keys()) # all restaurants reviewed by user 1
  restaurantSet2 = set(node2['restaurantMap'].keys()) # all restaurants reviewed by user 2

  if len(restaurantSet1) == 0 or len(restaurantSet2) == 0: # if either user has not reviewed any restaurants
    print 'no restaurant overlap'
    return 0

  if len(set.intersection(restaurantSet1, restaurantSet2)) == 0: # no commonly reviewed restaurants
    return 0

  for restaurantA in restaurantSet1: # for each restaurant reviewed by node2
    for restaurantB in restaurantSet2: # for each restaurant reviewed by node2
      if restaurantA == restaurantB: # if the reviewed restaurant is the same
      	score = calculateRatingSimForBusiness(node1, node2, restaurantA)
        reviewScores.append(score)
  # print 'len: ',len(reviewScores)
  # print 'compatibility_score: ',sum(reviewScores) / len(reviewScores) / 8.0
  compatibility_score = sum(reviewScores) / len(reviewScores) / 8.0
  return compatibility_score

# @param: edgeVals = (node1ID, node2ID): score
# create edge list given list of jaccard values for each pair of nodes
def createFoodNetwork(edgeVals, user_map, edgesFile, threshold):
  file = open(edgesFile, "w")
  count = 0
  for pair in edgeVals:
    val = edgeVals[pair] 
    # DECIDE WHAT SCORE THRESHOLD TO USE WHEN CREATING AN EDGE
    if val > threshold:   #create an edge if pair score > __
      node1ID = pair[0]
      node2ID = pair[1]
      # node1ID = user_map[pair[0]]['node_id']
      # node2ID = user_map[pair[1]]['node_id']
      line = "{0} {1}\n".format(node1ID, node2ID)
      file.write(line)
      count += 1
  # print 'number of edges with non-zero similarity', count
  file.close()

def createEdgeVals(userListMap, isJaccardScore, isAttrScore, isRatingScore):
  if isJaccardScore:
    print 'Calculating Jaccard Score Edge Values...'
  elif isAttrScore: 
    print 'Calculating Attribute Score Edge Values...'
  elif isRatingScore:
    print 'Calculating Rating Score Edge Values...'

  edgeVals = {}  # {(node1ID, node2ID): jaccardSimValue}
  # node1 and node 2 are the user_id's
  for index, node1 in enumerate(userListMap.keys()):
    # print 'looking at {}th node with ID {}'.format(index, node1)
    restaurantSetA = set(userListMap[node1]['restaurantMap'].keys())
    if len(restaurantSetA) == 0:
      continue
    for node2 in userListMap.keys():
      restaurantSetB = set(userListMap[node2]['restaurantMap'].keys())
      if len(restaurantSetB) == 0:
        continue
      node1ID = userListMap[node1]['node_id']
      node2ID = userListMap[node2]['node_id']
      if node1ID == node2ID:
        continue
      pair = (node1ID, node2ID)  # pair always in increasing node ID order
      if int(node2ID) > int(node1ID):
        pair = (node2ID, node1ID)
      if pair not in edgeVals:  #undirected graph
        # 1) Jaccard Vals
        if isJaccardScore:
          pairValue = calculateJaccardSim(node1, node2, restaurantSetA, restaurantSetB)
        # 2) Attribute Vals
        elif isAttrScore:
        # print 'PAIR IS', node1, node2        
          pairValue = getAttrCompScore(userListMap[node1], userListMap[node2])
        elif isRatingScore:
          pairValue = calculateRatingSim(userListMap[node1], userListMap[node2])
        edgeVals[pair] = pairValue
  print 'number of edges calculated', len(edgeVals)
  return edgeVals

'''
  Creates 3 txt files that are the edge lists of each type of food network (based on Jaccard Val, Rating Score, Attribute Score)

 @param userMapFile: filename of the pickle file (dict of users and their node IDs)
 @param reviewJSONFile: filename of reviews that pertain to all users in userMapFile
 @param thresholdJaccard: value between [0-1], if node pair score >= threshold, an edge will be created
 @param thresholdRating: threshold for the rating score
 @param thresholdAttr: threshold for the restaurant attribute score

 @return None
'''
def createFoodNetworkEdgeLists(userMapFile, reviewJSONFile, thresholdJaccard, thresholdRating, thresholdAttr, numUsers):
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  review_data = util.loadJSON(reviewJSONFile)

  # 1) add meta-data
  for userID in userListMap.keys():
    userListMap[userID]['restaurantMap'] = {}  # create empty restaurantMap for each user
    userListMap[userID]['reviewMap'] = {} # create empty reviewMap for each user
  createMetaData(review_data, userListMap)
  print 'number of users', len(userListMap)
  print userListMap

  # 2) calculate scores for each edge
  jaccardVals = createEdgeVals(userListMap, True, False, False)
  attrVals = createEdgeVals(userListMap, False, True, False)
  ratiVals = createEdgeVals(userListMap, False, False, True)

  # 3) create food network for each score type
  jaccardNtwkFile = 'food_ntwk_random/jacc_edge_list_{}users_{}.txt'.format(numUsers, thresholdJaccard)
  ratiNtwkFile = 'food_ntwk_random/rati_edge_list_{}users_{}.txt'.format(numUsers, thresholdAttr)
  attrNtwkFile = 'food_ntwk_random/attr_edge_list_{}users_{}.txt'.format(numUsers, thresholdRating)
  createFoodNetwork(jaccardVals, userListMap, jaccardNtwkFile, thresholdJaccard)
  createFoodNetwork(ratiVals, userListMap, ratiNtwkFile, thresholdRating)
  createFoodNetwork(attrVals, userListMap, attrNtwkFile, thresholdAttr)

  # 4) check if valid edge list and print info about each network
  g = snap.LoadEdgeList(snap.PUNGraph, jaccardNtwkFile, 0, 1)
  print 'Jaccard Network: Num Nodes = {}, Num Edges = {}'.format(g.GetNodes(), g.GetEdges())
  g = snap.LoadEdgeList(snap.PUNGraph, attrNtwkFile, 0, 1)
  print 'Attribute Network: Num Nodes = {}, Num Edges = {}'.format(g.GetNodes(), g.GetEdges())
  g = snap.LoadEdgeList(snap.PUNGraph, ratiNtwkFile, 0, 1)
  print 'Rating Network: Num Nodes = {}, Num Edges = {}'.format(g.GetNodes(), g.GetEdges())

  # 5) plot distribution frequency of each score type
  # IF IMPORT UTIL IS NOT WORKING FOR YOU, COMMENT OUT THESE LINES BELOW.
  # util.plotBucketDistribution(jaccardVals, 'Jaccard Score', numUsers, 0, 1)
  # util.plotBucketDistribution(attrVals, 'Attribute Compatibility', numUsers, 0, 1)
  # util.plotBucketDistribution(ratiVals, 'Rating Score', numUsers, -1, 1)


# Sample script
# createFoodNetworkEdgeLists("data/user_list_map_2.p", '../yelp/reviews_by_2_users.json', 0.04, 0.4, 0.9, 2)
