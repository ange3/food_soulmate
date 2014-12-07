import gen_random_users as genUsers
import gen_food_network as genFoodNet
import gen_eval_network as genEvalNet
import json

NUM_USERS = 1000


'''
Generates a random sampling of good users given a sample size
Creates 3 food networks based on three score types
Create eval network to test food networks against
Calculates accuracy of each food network vs eval network
'''
def main():
  # Generate Random User files and get path names
  genUsers.genRandomUsers(NUM_USERS)
  userJSONFile = "../yelp/user_{}_random.json".format(NUM_USERS)
  userMapFile = "data/user_list_map_{}_random.p".format(NUM_USERS)

  # Create Food Network text files
  thresholdJaccard = 0
  thresholdRating = 0
  thresholdAttr = 0
  genFoodNet.createFoodNetworkEdgeLists(userMapFile, userJSONFile, thresholdJaccard, thresholdRating, thresholdAttr, NUM_USERS)

  # Load Eval Network (entire graph)
  # TO-DO

  # Calculate Accuracy
  # TO-DO

main()
