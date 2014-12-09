import gen_random_users as genUsers
import gen_food_network as genFoodNet
import gen_eval_network as genEvalNet
import CNMCommunity as CNM
import gen_eval_clusters_toImport as genEvalClst
import json, pickle, snap
import numpy as np

NUM_USERS = 1000
jaccardAccuracies = []
attrAccuracies = []
ratiAccuracies = []

def createNodeList(userMap):
  nodelist = []
  for key in userMap.keys():
    nodelist.append(userMap[key]['node_id'])
  # print nodelist
  return nodelist

'''
Generates a random sampling of good users given a sample size
Creates 3 food networks based on three score types
Create eval network to test food networks against
Calculates accuracy of each food network vs eval network
'''
def runTrial(evalIndices, clusterDict):
  # 1) Generate Random User files and get path names
  genUsers.genRandomUsers(NUM_USERS)
  # userJSONFile = "../yelp/user_{}_random.json".format(NUM_USERS)
  userMapFile = "../yelp/user_list_map_{}_random.p".format(NUM_USERS)
  userMap = pickle.load( open( userMapFile, "rb" ) )

  nodelist = createNodeList(userMap)

  genUsers.genReviews(userMapFile, NUM_USERS)
  reviewJSONFile = "../yelp/reviews_by_{}_users_random.json".format(NUM_USERS)

  # 2) Food Network
  # Create Food Network text files
  thresholdJaccard = 0
  thresholdRating = -1
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
  # -----------------------------------

  # Defer to prior to for loop

  # Retrieves a dictionary of NID:Cluster on the entire eval network
  #evalIndices = genEvalClst.inputEvalCmtys()

  # Computes a dictionary of Cluster Number:NIDs on the entire eval network
  #clusterDict = genEvalClst.createClusterDict(evalIndices)
  

  

  # 4) Calculate Accuracy
  # ---------------------

  # Initialize community vectors
  jaccardCmtyV = snap.TCnComV()
  attrCmtyV = snap.TCnComV()
  ratiCmtyV = snap.TCnComV()

  # Get modularities, populate community vectors
  jaccardMod = snap.CommunityCNM(jaccardGraph, jaccardCmtyV)
  attrMod = snap.CommunityCNM(attrGraph, attrCmtyV)
  ratiMod = snap.CommunityCNM(ratiGraph, ratiCmtyV)

  # Generate indices for each community
  jaccardIndices = CNM.generateFoodIndices(jaccardCmtyV, nodelist)
  attrIndices = CNM.generateFoodIndices(attrCmtyV, nodelist)
  ratiIndices = CNM.generateFoodIndices(ratiCmtyV, nodelist)

  # Calculate accuracies
  jaccardAccuracy = CNM.calculateAccuracy(jaccardCmtyV, jaccardIndices, clusterDict, evalIndices, nodelist)
  attrAccuracy = CNM.calculateAccuracy(attrCmtyV, attrIndices, clusterDict, evalIndices, nodelist)
  ratiAccuracy = CNM.calculateAccuracy(ratiCmtyV, ratiIndices, clusterDict, evalIndices, nodelist)

  # Print!
  print "Jaccard accuracy: %f" % jaccardAccuracy
  print "Attribute accuracy: %f" % attrAccuracy
  print "Rating accuracy: %f" % ratiAccuracy

  # Push to vectors
  jaccardAccuracies.append(jaccardAccuracy)
  attrAccuracies.append(attrAccuracy)
  ratiAccuracies.append(ratiAccuracy)

def main():
  # Retrieves a dictionary of NID:Cluster on the entire eval network
  evalIndices = genEvalClst.inputEvalCmtys()

  # Computes a dictionary of Cluster Number:NIDs on the entire eval network
  clusterDict = genEvalClst.createClusterDict(evalIndices)

  for i in xrange(10):
    runTrial(evalIndices, clusterDict)

  output = {"Jaccard":jaccardAccuracies, "Attribute":attrAccuracies, "Rating":ratiAccuracies}

  jaccardStats = {"JaccMean":np.mean(jaccardAccuracies), "JaccMedian":np.median(jaccardAccuracies), "JaccMin":np.amin(jaccardAccuracies), "Jacc25%":np.percentile(jaccardAccuracies,25), "Jacc75%":np.percentile(jaccardAccuracies,75), "JaccMax":np.amax(jaccardAccuracies), "JaccStdev":np.std(jaccardAccuracies), "JaccVar":np.var(jaccardAccuracies),}
  attrStats = {"AttrMean":np.mean(attrAccuracies), "AttrMedian":np.median(attrAccuracies), "AttrMin":np.amin(attrAccuracies), "Attr25%":np.percentile(attrAccuracies,25), "Attr75%":np.percentile(attrAccuracies,75), "AttrMax":np.amax(attrAccuracies),"AttrStdev":np.std(attrAccuracies), "AttrVar":np.var(attrAccuracies)}
  ratiStats = {"RatiMean":np.mean(ratiAccuracies), "RatiMedian":np.median(ratiAccuracies), "RatiMin":np.amin(ratiAccuracies), "Rati25%":np.percentile(ratiAccuracies,25), "Rati75%":np.percentile(ratiAccuracies,75), "RatiMax":np.amax(ratiAccuracies), "RatiStdev":np.std(ratiAccuracies), "RatiVar":np.var(ratiAccuracies)}

  file = open("output_data_threshold_0,00_0_0,0_potentialFriendship.txt", "w")
  json.dump(jaccardStats, file, sort_keys=True, indent=4)
  file.write("\n")
  json.dump(attrStats, file, sort_keys=True, indent=4)
  file.write("\n")
  json.dump(ratiStats, file, sort_keys=True, indent=4)
  file.write("\n")
  json.dump(output, file, sort_keys=True)
  file.close()

  file2 = open("output_data_backup.txt", "w")
  file2.write(repr(jaccardAccuracies))
  file2.write(repr(attrAccuracies))
  file2.write(repr(ratiAccuracies))
  file2.close()

  print "Jaccard accuracies"
  print jaccardAccuracies
  print "Attribute accuracies"
  print attrAccuracies
  print "Rating accuracies"
  print ratiAccuracies

main()
