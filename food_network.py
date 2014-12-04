import pickle, json
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

def plotDistributionJaccard(jaccardVals):
  jaccardList = [jaccardVals[key] for key in jaccardVals if jaccardVals[key] != 0]
  # jaccardList = np.sort(jaccardList)
  # print jaccardList
  print 'number of edges with non-zero similarity', len(jaccardList)
  x = np.arange(len(jaccardList))
  plt.title('Jaccard Non-Zero Similarity Distribution for 1000 Yelp users')
  plt.ylabel('Jaccard Similarity')
  plt.xlabel('Pairs of nodes')
  plt.scatter(x, jaccardList)
  plt.show()

# add meta data to the userListMap 
# --> restauMap
def main():
  userMapFile = "data/user_list_map_1000.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  review_data = util.loadJSON('../yelp/reviews_by_1000_users.json')
  for userID in userListMap.keys():
    userListMap[userID]['restaurantMap'] = {}  # create empty restaurantMap for each user
  createMetaData(review_data, userListMap)
  # print 'sample user', userListMap['QZWo-viRnL9EmsIAN6vHtg']
  print 'number of users', len(userListMap)
  # node1 = userListMap['3Z2c8dL_nRXc7dd5_sFsPw']
  # node2 = userListMap['f01B5tRtqf3k6ak1pPSAWw']
  # calculateJaccardSim(node1, node2)
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
  print 'number of edges calculated', len(jaccardVals)

  plotDistributionJaccard(jaccardVals)

  


main()