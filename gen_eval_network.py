import json
import snap
from pprint import pprint
import pickle
import os
import util
import gen_food_network

def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    # pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values

def createUsersToBizMap():
  review_data = util.loadJSON('../yelp/review.json')
  restaurantMap = load_data('../yelp/restaurants.json')
  UsersToBizMap = {}
  # userID: set(bizID1, bizID2, ...)   --> maps every user that's been to every restaurant
  for review in review_data:
    review_userID = review['user_id']
    businessID = str(review['business_id'])
    if businessID not in restaurantMap:
      continue
    if businessID not in UsersToBizMap[businessID]:
      UsersToBizMap[review_userID] = set()
    UsersToBizMap[review_userID].add(businessID)
  return UsersToBizMap

def createMetaData(review_data, userListMap):
  for review in review_data:
    userID = review['user_id']
    if userID in userListMap:
      reviewID = str(review['review_id'])
      businessID = str(review['business_id'])
      if businessID not in userListMap[userID]['restaurantMap']:
        userListMap[userID]['restaurantMap'][businessID] = []
      userListMap[userID]['restaurantMap'][businessID].append(reviewID)
      userListMap[userID]['reviewMap'][reviewID] = (review['stars'], review['date'])

def getRatingSimScore(user1_id, user2_id, user_map):
  user1 = user_map[user1_id]
  user2 = user_map[user2_id]
  ratingSimScore = gen_food_network.calculateRatingSim(user1, user2)
  return ratingSimScore

def write_edges_file(user_data, user_map, edgesFile, edgesWithScoreFile):
  # UsersToBizMap = createUsersToBizMap()
  for userID in user_map.keys():
    user_map[userID]['restaurantMap'] = {}
    user_map[userID]['reviewMap'] = {}
  createMetaData(util.loadJSON('../yelp/review.json'), user_map)
  friend_list = []
  file = open(edgesFile, "w")
  file2 = open(edgesWithScoreFile, "w")

  scoreMap = {}

  for i in xrange(len(user_data)):
    friend_list.append(user_data[i]['friends'])
    # print friend_list[i]
    for j in xrange(len(friend_list[i])):
      if friend_list[i][j] in user_map.keys():
        pair = (user_data[i]['user_id'], friend_list[i][j])
        pair2 = (friend_list[i][j], user_data[i]['user_id'])
        if pair in scoreMap:
          score = scoreMap[pair]
        elif pair2 in scoreMap:
          score = scoreMap[pair2]
        else:
          score = getRatingSimScore(friend_list[i][j], user_data[i]['user_id'], user_map) # if user should be in the network
        if score > 0:
          src_tmp = user_map[user_data[i]['user_id']] # not quite sure what data type this return value is, but it's converted to string 
          dst_tmp = user_map[friend_list[i][j]]       # not quite sure what data type this return value is, but it's converted to string 
          src = src_tmp['node_id'] # extract node_id for src of edge
          dst = dst_tmp['node_id']
          # src = str(src_tmp)[12:-1] # extract node_id for src of edge
          # dst = str(dst_tmp)[12:-1] # extract node_id for dst of edge
          line = "{0} {1}\n".format(src, dst) 
          lineWithScore = "{0} {1} {2}\n".format(src, dst, score) 
          file.write(line)
          file2.write(lineWithScore)
  file.close()
  file2.close()

def main(): 
  edgesFile = 'eval_ntwk_food_friends/eval_ntwk_edge_list_phoenix.txt'
  edgesWithScoreFile = 'eval_ntwk_food_friends/eval_ntwk_edge_list_phoenix_with_score.txt'
  userMapFile = 'data/user_list_map.p'
  user_data = []
  user_data = load_data('../yelp/user_allgood.json', user_data)

  # step 1
  g = snap.TUNGraph.New()

  user_map = pickle.load(open(userMapFile,"rb"))

  # step 1
  write_edges_file(user_data, user_map, edgesFile, edgesWithScoreFile)

  # step 2
  g = snap.LoadEdgeList(snap.PUNGraph, edgesFile, 0, 1)
  # step 2
  snap.PrintInfo(g, "Evaluation Network Info", "eval_ntwk_food_friends/eval_netwk_info_phoenix.txt", False)
  # step 2
  # snap.SaveEdgeList(g, "eval_ntwk/eval_ntwk_1000.txt")

# if necessary, this function can create an eval network based on number of users given
def genEvalNetwork(numUsers): 
  userMapFile = 'data/user_list_map_{}.p'.format(numUsers)
  user_map = pickle.load(open(userMapFile,"rb"))
  userJSONFile = '../yelp/user_{}.json'.format(numUsers)
  user_data = load_data(userJSONFile, user_data)

  # step 1
  edgesFile = 'eval_ntwk/eval_ntwk_edge_list_{}.txt'.format(numUsers)
  write_edges_file(user_data, user_map, edgesFile)


if __name__ == '__main__':
  main()

main()