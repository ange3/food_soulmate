import pickle, json
import util


# iterate through all reviews and add the business to the restauMap IF it is a food establishment
# restaurantMap: {businessID: [reviewID, reviewID ]}
def createMetaData(review_data, userListMap):
  for review in review_data:
    userID = review['user_id']
    if userID in userListMap:
      reviewID = str(review['review_id'])
      businessID = str(review['business_id'])
      # check if business is food
      if businessID not in userListMap[userID]['restaurantMap']:
        userListMap[userID]['restaurantMap'][businessID] = []
      userListMap[userID]['restaurantMap'][businessID].append(reviewID)


# add meta data to the userListMap 
# --> restauMap
def main():
  userMapFile = "data/user_list_map_1.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  review_data = util.loadJSON('data/review_by_1_users.json')
  for userID in userListMap.keys():
    userListMap[userID]['restaurantMap'] = {}  # create empty restaurantMap for each user
  createMetaData(review_data, userListMap)
  print userListMap


main()