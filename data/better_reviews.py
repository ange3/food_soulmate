import json, os, pickle
from pprint import pprint

def loadJSON(fileName):
  user_data = []
  infile = open(fileName, 'r')
  user_data = json.load(infile)
  infile.close()
  return user_data  

# returns a map of IDs of all food businesses
def getFoodBusinessIDs(business_data):
  print 'orig num businesses', len(business_data)
  businessMap = {}
  restaurant_data = []
  for business in business_data:
    if 'Restaurants' in business['categories']:
      businessMap[business['business_id']] = 1
      restaurant_data.append(business)

  newBusinessDataFile = "../../yelp/restaurants.json"
  with open(newBusinessDataFile, 'w') as outfile:
    json.dump(restaurant_data, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newBusinessDataFile

  updated_business_data = loadJSON(newBusinessDataFile)
  print 'valid json, new num businesses = ', len(updated_business_data)
  return businessMap

def main():
  review_data = loadJSON('../../yelp/review.json')
  business_data = loadJSON('../../yelp/business.json')
  businessMap = getFoodBusinessIDs(business_data)
  print 'original num reviews', len(review_data)
  userMapFile = "user_list_map_2.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  # print userListMap
  good_data = []
  for index, review in enumerate(review_data):
    if review['user_id'] in userListMap and review['business_id'] in businessMap:  #checks if user id in any of the keys of map of users and business is food
      # print review
      good_data.append(review)
  newUserDataFile = "../../yelp/reviews_by_2_users.json"

  with open(newUserDataFile, 'w') as outfile:
    json.dump(good_data, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newUserDataFile

  updated_review_data = loadJSON(newUserDataFile)
  print 'valid json, new num reviews = ', len(updated_review_data)

main()