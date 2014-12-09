import random, json, pickle

# Loads JSON data
# to access data: index into user element and then use key
# for ex: print user_data[0]['user_id']
def loadJSON(fileName):
  user_data = []
  infile = open(fileName, 'r')
  user_data = json.load(infile)
  infile.close()
  return user_data  

# Creates a userListMap which maps from userID -> nodeID
# userListMap is a table that allows us to easily index into the user_data (nodeID is the index)
# Assumption: these users have been pre-checked to make sure they are good users (user_allgood.JSON was created in the better_users.py file)
def createMap(user_data, numNodes):
  print len(user_data)
  userListMap = {}
  # good_data = []
  randomGroup = random.sample(user_data, numNodes)
  for index, randomUser in enumerate(randomGroup):
    randomUserID = str(randomUser['user_id'])
    # print randomUserID
    userListMap[randomUserID] = {}
    userListMap[randomUserID]['node_id'] = index
    # good_data.append(randomUser)

  # Create new User JSON File
  newUserDataFile = "../yelp/user_{}_random.json".format(numNodes)
  with open(newUserDataFile, 'w') as outfile:
    json.dump(randomGroup, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newUserDataFile
  updated_user_data = loadJSON(newUserDataFile)
  print 'valid JSON, num users =', len(updated_user_data)
  
  return userListMap

def genRandomUsers(numUsers):
  user_data = loadJSON("../yelp/user_allgood.json")
  userListMap = createMap(user_data, numUsers)
  print 'num nodes in map', len(userListMap)
  # print 'ORIGINAL USER LIST'
  # print userListMap

  # Create pickle file
  pickleFile = "data/user_list_map_{}_random.p".format(numUsers)
  pickle.dump( userListMap, open( pickleFile, "wb" ) )
  print 'created pickle file:', pickleFile

  # SANITY CHECK
  userListMapLoaded = pickle.load( open( pickleFile, "rb" ) )
  if userListMapLoaded is not None:
    print 'sanity check: user list map loaded correctly with {} users'.format(len(userListMapLoaded))
    # print 'NEW USER LIST'
    # print userListMapLoaded

# returns a map of IDs of all food businesses
def getFoodBusinessIDs(business_data):
  print 'orig num businesses', len(business_data)
  businessMap = {}
  restaurant_data = []
  for business in business_data:
    if 'Restaurants' in business['categories']:
      businessMap[business['business_id']] = 1
      restaurant_data.append(business)

  newBusinessDataFile = "../yelp/restaurants.json"
  with open(newBusinessDataFile, 'w') as outfile:
    json.dump(restaurant_data, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newBusinessDataFile

  updated_business_data = loadJSON(newBusinessDataFile)
  print 'valid json, new num businesses = ', len(updated_business_data)
  return businessMap

# Generate reviews based on the given user list file (only save reviews that are made by the given list of users) 
def genReviews(userMapFile, numUsers):
  review_data = loadJSON('../yelp/review.json')
  business_data = loadJSON('../yelp/business.json')
  businessMap = getFoodBusinessIDs(business_data)
  print 'original num reviews', len(review_data)
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  # print userListMap
  good_data = []
  for index, review in enumerate(review_data):
    if review['user_id'] in userListMap and review['business_id'] in businessMap:  #checks if user id in any of the keys of map of users and business is food
      # print review
      good_data.append(review)
  newUserDataFile = "../yelp/reviews_by_{}_users_random.json".format(numUsers)

  with open(newUserDataFile, 'w') as outfile:
    json.dump(good_data, outfile, sort_keys=True, indent=4)
  print 'created JSON file:', newUserDataFile

  updated_review_data = loadJSON(newUserDataFile)
  print 'valid json, new num reviews = ', len(updated_review_data)


# genRandomUsers(1000)