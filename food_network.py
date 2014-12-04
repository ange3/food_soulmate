import pickle


def createMetaData(restaurantMap):

def main():
  userMapFile = "data/user_list_map_100.p"
  userListMap = pickle.load( open( userMapFile, "rb" ) )
  for user in userListMap.keys():
    restaurantMap = {}
    createMetaData(restaurantMap)