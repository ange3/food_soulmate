import json, os, pickle
from pprint import pprint

FILE = '../../yelp/user.json'

# Loads JSON data
# to access data: index into user element and then use key
# for ex: print user_data[0]['user_id']
def loadJSON(fileName = FILE):
  user_data = []
  infile = open(fileName, 'r')
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
def createMap(user_data, placeLimit, numNodes = 100):
  userListMap = {}
  good_data = []
  for index, user in enumerate(user_data):
    userID = user['user_id']
    if goodUser(user):
      # userID = userID[2:] # strip beginning u' and ending ' that JSON file adds
      userListMap[userID] = {}
      userListMap[userID]['node_id'] = index
      good_data.append(user)
    if placeLimit:
      if len(userListMap) >= numNodes:
        break

  # IF WE WANT TO CREATE A NEW USER JSON FILE:
  newUserDataFile = "../../yelp/user_allgood.json"

  with open(newUserDataFile, 'w') as outfile:
    json.dump(good_data, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newUserDataFile

  updated_user_data = loadJSON(newUserDataFile)
  print 'valid JSON, num users =', len(updated_user_data)
  
  return userListMap

def main():
  user_data = loadJSON()
  userListMap = createMap(user_data, 1000000)
  print 'num nodes in map', len(userListMap)
  pickleFile = "user_list_map.p"
  pickle.dump( userListMap, open( pickleFile, "wb" ) )
  print 'created pickle file:', pickleFile
  # SANITY CHECK
  userListMapLoaded = pickle.load( open( pickleFile, "rb" ) )
  if userListMapLoaded is not None:
    print 'sanity check: user list map loaded correctly with {} users'.format(len(userListMapLoaded))


main()
