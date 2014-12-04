import json, os, pickle
from pprint import pprint

FILE = '../../yelp/user.json'
# FILE = '../small_data/users_sample_small.json'
# FILE = 'users_sample_small.json'

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

def replaceApostrophes(line):
  inQuotes = False
  toReturn = ""
  for charIndex in xrange(len(line)):
    if inQuotes:
      #Only looking for an end quote
      if line[charIndex] == '\"':
        if line[charIndex-1] == '\\':
          inQuotes = False
      toReturn += line[charIndex]
    if not inQuotes:
      if line[charIndex] == '\'':
        if line[charIndex-1] == 'u':
          toReturn -= toReturn[:len(toReturn)-1]
        line[charIndex] = '\"'
      if line[charIndex] == '\"':
        inQuotes = true
      toReturn += line[charIndex]

  return line


# Creates a userListMap which maps from userID -> nodeID
# userListMap is a table that allows us to easily index into the user_data (nodeID is the index)
def createMap(user_data, numNodes):
  userListMap = {}
  good_data = []
  for index, user in enumerate(user_data):
    userID = user['user_id']
    if goodUser(user):
      # userID = userID[2:] # strip beginning u' and ending ' that JSON file adds
      userListMap[userID] = {}
      userListMap[userID]['node_id'] = index
      good_data.append(user)
    if len(userListMap) >= numNodes:
      break

  newUserDataFile = "../../yelp/user_1000.json"

  file = open(newUserDataFile, "w")
  file.write("[")
  for i in xrange(len(good_data) - 1): # remember that the last line has special formatting (no comma after last record)
    line = "{0},\n".format(good_data[i])
    line = replaceApostrophes(line)
    #line = line.replace("u'", "'");
    #line = line.replace("'", "\"");
    file.write(line)
  lastLine = str(good_data[len(good_data) - 1])  + "]"
  lastLine = replaceApostrophes(lastLine)
  #lastLine = lastLine.replace("u'", "'");
  #lastLine = lastLine.replace("'", "\"");
  file.write(lastLine)
  file.close()
  
  return userListMap

def main():
  user_data = loadJSON()
  userListMap = createMap(user_data, 1000)
  print 'num_nodes', len(userListMap)
  pickle.dump( userListMap, open( "user_list_map_1000.p", "wb" ) )


main()
