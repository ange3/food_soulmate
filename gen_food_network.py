import pickle, json, math, snap
import util
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import datetime

# iterate through all reviews and add the business to the restauMap IF it is a food establishment
# reviewMap: {reviewID: (star,date))}
def createMetaData(review_data, userListMap):
  for review in review_data:
    userID = review['user_id']
    if userID in userListMap:
      reviewID = str(review['review_id'])
      businessID = str(review['business_id'])
      # check if business is food
      if businessID not in userListMap[userID]['restaurantMap']:
        userListMap[userID]['restaurantMap'][businessID] = []
      userListMap[userID]['restaurantMap'][businessID].append(reviewID)
      userListMap[userID]['reviewMap'][reviewID] = (review['stars'], review['date'])

# returns the ratio of size of overlapping restaurants set / union of all restaurants
def calculateJaccardSim(node1, node2, restaurantSetA, restaurantSetB):
  if len(restaurantSetA) == 0 or len(restaurantSetB) == 0:
    return 0
  # print 'restaurantSetA', restaurantSetA, len(restaurantSetA)
  # print 'restaurantSetB', restaurantSetB, len(restaurantSetB)
  intersectingSet = set.intersection(restaurantSetA, restaurantSetB)
  unionSet = set.union(restaurantSetA, restaurantSetB)
  ratio = float(len(intersectingSet))/len(unionSet)
  # print ratio
  return ratio

# return average of comp score for all attributes
def getAttrCompScore(attributePrefA, attributePrefB, numRestauA, numRestauB):
  allAttributes = Counter(attributePrefA.keys()) + Counter(attributePrefB.keys())
  compVals = []
  for attr in allAttributes:
    valA = attributePrefA[attr]/float(numRestauA)
    valB = attributePrefB[attr]/float(numRestauB)
    if valB != 0 and valA != 0:
      comp = min(valA/float(valB), valB/float(valA))
      compVals.append(comp)
    # otherwise the comp will def be 0, in which case no need to add to the average
  # print 'compVals', compVals
  return np.mean(compVals)

# calculate similarity of users based on how much they value a certain attribute in a restaurant
def calculateAttrSim(node1, node2, restaurantSetA, restaurantSetB):
  restaurantSetAll = set.union(restaurantSetA, restaurantSetB)
  business_data = util.loadJSON('../yelp/restaurants.JSON')
  # attributePref = {restauAttribute: [countA, countB], ... }
  # positive are attributes that are true, i.e. customer is looking for
  # negative are attributes that are false, i.e. customer does not care about
  attributePrefPosA = Counter()
  attributePrefNegA = Counter()
  attributePrefPosB = Counter()
  attributePrefNegB = Counter()  
  numRestausWithPriceA = 0
  numRestausWithPriceB = 0
  # can use this to calculate average price range later
  for business in business_data:
    if business['business_id'] in restaurantSetAll:
      attributeMap = business['attributes']
      for attribute, val in attributeMap.items():
        if type(val) == dict:
          # iterate through the elements in this and pull out each attr/val
          continue
          # val = list(val.values())  #for cases like parking: {garage: True, street: true}, flattens into just a list of the values
        if type(val) == str or type(val) == unicode:
          continue
        valList = [val]
        if business['business_id'] in restaurantSetA:
          attributePrefPosA[attribute] += sum(valList)  #sum of a list of bools = number of True vals for this attribute  (True = 1)
          attributePrefNegA[attribute] += len(valList) - sum(valList)
          if attribute == "Price Range":
            numRestausWithPriceA += 1
        if business['business_id'] in restaurantSetB:
          attributePrefPosB[attribute] += sum(valList)
          attributePrefNegB[attribute] += len(valList) - sum(valList)
          if attribute == "Price Range":
            numRestausWithPriceB += 1
  # print 'ATTRIBUTES A', attributePrefPosA
  # print 'ATTRIBUTES B', attributePrefPosB
  # print 'numRestausWithPriceA', numRestausWithPriceA
  # print 'numRestausWithPriceB', numRestausWithPriceB
  # print 'NEG ATTRIBUTES A', attributePrefNegA
  # print 'NEG ATTRIBUTES B', attributePrefNegB
  # print restaurantSetA
  # print restaurantSetB 
  posCompScore = getAttrCompScore(attributePrefPosA, attributePrefPosB, len(restaurantSetA), len(restaurantSetB))
  # print 'Compatibility Score:', posCompScore
  return posCompScore

# returns the similarity score between node1 and node2 based on the first part of our composite score formula (see Project Milestone)
def calculateRatingSim(node1, node2, restaurantSet1, restaurantSet2):
  reviewScores = []
  if len(set.intersection(restaurantSet1, restaurantSet2)) == 0: # no commonly reviewed restaurants
    return 0

  for restaurantA in restaurantSet1: # for each restaurant reviewed by node2
    for restaurantB in restaurantSet2: # for each restaurant reviewed by node2
      if restaurantA == restaurantB: # if the reviewed restaurant is the same
        reviewSetA = node1['restaurantMap'][restaurantA] # node1's reviews of common restaurant
        reviewSetB = node2['restaurantMap'][restaurantA] # node2's reviews of common restaurant
        
        latestDateA = latestDateB = datetime.datetime(2010, 1, 1)
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
        score = (2.0 - abs(ratingA - ratingB))* math.pow( (abs(ratingA - 3.0) + abs(ratingB - 3.0)) / 2.0, 2.0 )
        reviewScores.append(score)
  # print 'len: ',len(reviewScores)
  # print 'compatibility_score: ',sum(reviewScores) / len(reviewScores) / 8.0 # divided by 8.0 so score is in the range [-1.0,1.0]
  compatibility_score = sum(reviewScores) / len(reviewScores) / 8.0
  return compatibility_score

# calculate similarity of users based on how they rated restaurants
def calculateRatingVals(userListMap):
  ratingVals = {} # {(node1ID, node2ID): ratingSimValue}

  for node1ID in userListMap.keys():
    for node2ID in userListMap.keys():
      if node1ID == node2ID: 
        continue
      pair = (node1ID, node2ID)
      pair2 = (node2ID, node1ID)
      if pair not in ratingVals and pair2 not in ratingVals:# undirected graph
        ratingSimValue = calculateRatingSim(userListMap[node1ID], userListMap[node2ID])
        ratingVals[pair] = ratingSimValue

  return ratingVals

# create edge list given list of jaccard values for each pair of nodes
def createFoodNetwork(edgeVals, user_map, edgesFile):
  file = open(edgesFile, "w")
  for pair in edgeVals:
    val = edgeVals[pair] 
    # DECIDE WHAT SCORE THRESHOLD TO USE WHEN CREATING AN EDGE
    if val > 0:   #create an edge if jaccard val > 0 
      # node1ID = pair[0]
      # node2ID = pair[1]
      node1ID = user_map[pair[0]]['node_id']
      node2ID = user_map[pair[1]]['node_id']
      line = "{0} {1}\n".format(node1ID, node2ID)
      file.write(line)
  file.close()

# add meta data to the userListMap 
# for each node creates: restauMap
def main():
  userMapFile = "data/user_list_map_1000.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  review_data = util.loadJSON('../yelp/reviews_by_1000_users.json')
  for userID in userListMap.keys():
    userListMap[userID]['restaurantMap'] = {}  # create empty restaurantMap for each user
    userListMap[userID]['reviewMap'] = {} # create empty reviewMap for each user
  createMetaData(review_data, userListMap)
  print 'number of users', len(userListMap)
  # print 'USER LIST MAP', userListMap
  
  # IMPLEMENT SCORE CALCULATION HERE: 
  edgeVals = {}  # {(node1ID, node2ID): jaccardSimValue}
  # node1 and node2 are the user_ids
  for node1 in userListMap.keys():
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
        # pairValue = calculateJaccardSim(node1, node2, restaurantSetA, restaurantSetB)
        # 2) Attribute Vals
        # print 'PAIR IS', node1, node2        
        # pairValue = calculateAttrSim(userListMap[node1], userListMap[node2], restaurantSetA, restaurantSetB)
        # 3) Ratings Vals
        pairValue = calculateRatingSim(userListMap[node1], userListMap[node2], restaurantSetA, restaurantSetB)
        edgeVals[pair] = pairValue
  print 'number of edges calculated', len(edgeVals)

  # util.plotBucketDistribution(edgeVals)
  # edgesFile = 'food_ntwk/attr_edge_list_1000.txt'
  # edgesFile = 'food_ntwk/jacc_edge_list_1000.txt'
  edgesFile = 'food_ntwk/rati_edge_list_1000.txt'
  createFoodNetwork(edgeVals, userListMap, edgesFile)
  g = snap.LoadEdgeList(snap.PUNGraph, edgesFile, 0, 1)
  print 'num Nodes', g.GetNodes()
  print 'num Edges', g.GetEdges()


main()


'''
sample test code in main

  print 'sample user', userListMap['QZWo-viRnL9EmsIAN6vHtg']
  node1 = userListMap['3Z2c8dL_nRXc7dd5_sFsPw']
  node2 = userListMap['f01B5tRtqf3k6ak1pPSAWw']
  calculateJaccardSim(node1, node2)

'''