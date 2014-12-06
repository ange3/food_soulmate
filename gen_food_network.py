import pickle, json, math, snap
import util
import numpy as np
import matplotlib.pyplot as plt

# iterate through all reviews and add the business to the restauMap IF it is a food establishment
# restaurantMap: {businessID: [reviewID, reviewID ]}
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

# returns the ratio of size of overlapping restaurants set / union of all restaurants
def calculateJaccardSim(node1, node2):
  restaurantSetA = set(node1['restaurantMap'].keys())
  restaurantSetB = set(node2['restaurantMap'].keys())
  if len(restaurantSetA) == 0 or len(restaurantSetB) == 0:
    return 0
  # print 'restaurantSetA', restaurantSetA, len(restaurantSetA)
  # print 'restaurantSetB', restaurantSetB, len(restaurantSetB)
  intersectingSet = set.intersection(restaurantSetA, restaurantSetB)
  unionSet = set.union(restaurantSetA, restaurantSetB)
  ratio = float(len(intersectingSet))/len(unionSet)
  # print ratio
  return ratio

# plots the frequency distribution of each Jaccard Similarity value
# buckets = [0.1, 0.2, ... 1]
def plotBucketDistributionJaccard(jaccardVals):
  jaccardList = [jaccardVals[key] for key in jaccardVals if jaccardVals[key] != 0]
  jaccardListBuckets = [0] * 101
  for val in jaccardList:
    index = math.ceil(val*100)
    jaccardListBuckets[int(index)] += 1
  print jaccardListBuckets
  print 'number of edges with non-zero similarity', len(jaccardListBuckets)
  x = np.arange(0,1.01,0.01)
  plt.title('Jaccard Non-Zero Similarity Distribution for 1000 Yelp users')
  plt.xlabel('Jaccard Similarity')
  plt.ylabel('Count of edges')
  plt.scatter(x, jaccardListBuckets)
  plt.plot(x, jaccardListBuckets)
  # plt.axis([0,1,0, 30])
  plt.show()

# plot out all jaccard values
def plotDistributionJaccard(jaccardVals):
  jaccardList = [jaccardVals[key] for key in jaccardVals if jaccardVals[key] != 0]
  print jaccardList
  print 'number of edges with non-zero similarity', len(jaccardList)
  x = np.arange(len(jaccardList))
  plt.title('Jaccard Non-Zero Similarity Distribution for 1000 Yelp users')
  plt.ylabel('Jaccard Similarity')
  plt.xlabel('Pairs of nodes')
  plt.scatter(x, jaccardList)
  plt.show()

# calculate similarity of users based on their Jaccard similarity
def calculateJaccardVals(userListMap):
  jaccardVals = {}  # {(node1ID, node2ID): jaccardSimValue}
  for node1ID in userListMap.keys():
    for node2ID in userListMap.keys():
      if node1ID == node2ID:
        continue
      pair = (node1ID, node2ID)
      pair2 = (node2ID, node1ID)
      if pair not in jaccardVals and pair2 not in jaccardVals:  #undirected graph
        jaccardSimValue = calculateJaccardSim(userListMap[node1ID], userListMap[node2ID])
        jaccardVals[pair] = jaccardSimValue
  return jaccardVals

# calculate similarity of users based on how much they value a certain attribute in a restaurant
def calculateAttrVals(userListMap):
  attrVals = {}
  return attrVals

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
# --> restauMap
def main():
  userMapFile = "data/user_list_map_100.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  review_data = util.loadJSON('../yelp/reviews_by_100_users.json')
  for userID in userListMap.keys():
    userListMap[userID]['restaurantMap'] = {}  # create empty restaurantMap for each user
  createMetaData(review_data, userListMap)
  print 'number of users', len(userListMap)
  # IMPLEMENT SCORE CALCULATION HERE: 
  edgeVals = calculateJaccardVals(userListMap)  # !) Jaccard Vals
  # edgeVals = calculateAttrVals(userListMap)
  
  print 'number of edges calculated', len(edgeVals)

  # plotBucketDistributionJaccard(jaccardVals)
  edgesFile = 'food_ntwk/food_ntwk_edge_list_100.txt'
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