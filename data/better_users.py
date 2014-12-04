import json, os, pickle
from pprint import pprint

FILE = '../../yelp/user.json'
# FILE = '../small_data/users_sample_small.json'

# Loads JSON data
# to access data: index into user element and then use key
# for ex: print user_data[0]['user_id']
def loadJSON():
  user_data = []
  infile = open(FILE, 'r')
  user_data = json.load(infile)
  infile.close()
  return user_data  

# checks if the given user is a user that we want in our network
# removes users with no friends or who have not written any reviews
def goodUser(user):
  friendsList = user['friends']
  numReviews = user['review_count']
  if len(friendsList) < 1 or numReviews < 1:
    return False
  return True


# Creates a userListMap which maps from userID -> nodeID
# userListMap is a table that allows us to easily index into the user_data (nodeID is the index)
def createMap(user_data, numNodes):
  userListMap = {}
  for index, user in enumerate(user_data):
    userID = user['user_id']
    if goodUser(user):
      userID = str(userID) # strip beginning u' and ending ' that JSON file adds
      userListMap[userID] = {}
      userListMap[userID]['node_id'] = index
    if len(userListMap) >= numNodes:
      break
  return userListMap

def main():
  user_data = loadJSON()
  userListMap = createMap(user_data, 1)
  print 'num nodes', len(userListMap)
  print userListMap
  # print userListMap.keys()
  pickle.dump( userListMap, open( "user_list_map_1.p", "wb" ) )


main()