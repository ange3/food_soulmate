import json
from pprint import pprint
import pickle

def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    # pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values
    
user_data = []
user_data = load_data('reviews_sample_small.json', user_data)

# to access data: index into user element and then use key
# print user_data[0]['user_id']

# userListMap is a table that allows us to easily index into the user_data (nodeID is the index)
  # userID -> nodeID
userListMap = {}
for index, user in enumerate(user_data):
  userID = user['user_id']
  userListMap[userID] = index

# print len(userListMap)

