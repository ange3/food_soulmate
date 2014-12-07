import gen_random_users as genUsers
import gen_food_network as genFoodNet
import gen_eval_network as genEvalNet
import CNMCommunity as CNM
import json, pickle

NUM_USERS = 1000


def createNodeList(userMap):
  nodelist = []
  for key in userMap.keys():
    nodelist.append(userMap[key]['node_id'])
  print nodelist

'''
Generates a random sampling of good users given a sample size
Creates 3 food networks based on three score types
Create eval network to test food networks against
Calculates accuracy of each food network vs eval network
'''
def main():
  # 1) Generate Random User files and get path names
  genUsers.genRandomUsers(NUM_USERS)
  # userJSONFile = "../yelp/user_{}_random.json".format(NUM_USERS)
  userMapFile = "data/user_list_map_{}_random.p".format(NUM_USERS)
  userMap = pickle.load( open( userMapFile, "rb" ) )

  nodelist = createNodeList(userMap)

  genUsers.genReviews(userMapFile, NUM_USERS)
  reviewJSONFile = "../yelp/reviews_by_{}_users_random.json".format(NUM_USERS)

  # 2) Food Network
  # Create Food Network text files
  thresholdJaccard = 0
  thresholdRating = 0
  thresholdAttr = 0
  genFoodNet.createFoodNetworkEdgeLists(userMapFile, reviewJSONFile, thresholdJaccard, thresholdRating, thresholdAttr, NUM_USERS)
  # Load food networks
  jaccardNtwkFile = 'food_ntwk_random/jacc_edge_list_{}users_{}.txt'.format(NUM_USERS, thresholdJaccard)
  attrNtwkFile = 'food_ntwk_random/attr_edge_list_{}users_{}.txt'.format(NUM_USERS, thresholdRating)
  ratiNtwkFile = 'food_ntwk_random/rati_edge_list_{}users_{}.txt'.format(NUM_USERS, thresholdAttr)
  jaccardGraph = snap.LoadEdgeList(snap.PUNGraph, jaccardNtwkFile, 0, 1)
  attrGraph = snap.LoadEdgeList(snap.PUNGraph, attrNtwkFile, 0, 1)
  ratiGraph = snap.LoadEdgeList(snap.PUNGraph, ratiNtwkFile, 0, 1)

  # 3) Load Eval Network (entire graph)
  # TO-DO
  evalNtwkFile = 'eval_ntwk/eval_edge_list_phoenix.txt'

  # 4) Calculate Accuracy
  # TO-DO

main()
