import json, os, pickle
from pprint import pprint

def loadJSON(fileName):
  user_data = []
  infile = open(fileName, 'r')
  user_data = json.load(infile)
  infile.close()
  return user_data  

def main():
  review_data = loadJSON('../../yelp/review.json')
  business_data = loadJSON('../../yelp/business.json')
  print 'original num reviews', len(review_data)
  userMapFile = "user_list_map_100.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  print userListMap
  good_data = []
  for index, review in enumerate(review_data):
    # business = business
    if review['user_id'] in userListMap:  #checks if user id in any of the keys of map of users
      print review
      good_data.append(review)
  file = open('review_by_100_users.json', "w")
  file.write("[")
  for i in xrange(len(good_data) - 1): # remember that the last line has special formatting (no comma after last record)
    line = "{0},\n".format(good_data[i])
    line = line.replace("u'", "'");
    line = line.replace("'", "\"");
    file.write(line)
  lastLine = str(good_data[len(good_data) - 1])  + "]"
  lastLine = lastLine.replace("u'", "'");
  lastLine = lastLine.replace("'", "\"");
  file.write(lastLine)
  file.close()
  updated_review_data = loadJSON('review_by_100_users.json')
  print 'new num reviews', len(updated_review_data)

main()