import json, os, pickle
from pprint import pprint

# Reads data from a JSON file into an array of elements each of which can be accessed like a map using the element's attributes
def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    # pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values

# Loads JSON data
# to access data: index into user element and then use key
# print user_data[0]['user_id']
def loadJSON(fileName):
  user_data = []
  user_data = load_data(fileName, user_data)
  return user_data

# Creates a userListMap which maps from userID -> nodeID
# userListMap is a table that allows us to easily index into the user_data (nodeID is the index)
def createMap(user_data):
  userListMap = {}
  for index, user in enumerate(user_data):
    userID = user['user_id']
    userListMap[userID] = index
  return userListMap


# MAIN FUNCTION
# creates a map that is a user list
def main():
  userMapFile = "user_list_map_full.p"
  # if dictionary does not already exist, load the data
  if not os.path.isfile(userMapFile):
    user_data = loadJSON('../comma_separated_dataset/yelp_academic_dataset_user_comma.json')
    userListMap = createMap(user_data)
    pickle.dump( userListMap, open( "user_list_map_full.p", "wb" ) )  # save user list map to a file
  else:
    userListMap = pickle.load( open( userMapFile, "rb" ) )
  print len(userListMap)
  
# RUN
main()  