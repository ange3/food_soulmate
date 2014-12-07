import json
import snap
from pprint import pprint
import pickle
import os

#test

def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    # pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values

def write_edges_file(user_data, user_map, edgesFile):
  friend_list = []
  file = open(edgesFile, "w")

  for i in xrange(len(user_data)):
    friend_list.append(user_data[i]['friends'])
    for j in xrange(len(friend_list[i])):
      if friend_list[i][j] in user_map: # if user should be in the network
        src_tmp = user_map[user_data[i]['user_id']] # not quite sure what data type this return value is, but it's converted to string 
        dst_tmp = user_map[friend_list[i][j]]       # not quite sure what data type this return value is, but it's converted to string 
        src = str(src_tmp)[12:-1] # extract node_id for src of edge
        dst = str(dst_tmp)[12:-1] # extract node_id for dst of edge
        line = "{0} {1}\n".format(src, dst) 
        file.write(line)
  file.close()

def main(): 
  edgesFile = 'eval_ntwk/eval_ntwk_edge_list_100.txt'
  userMapFile = 'data/user_list_map_100.p'
  user_data = []
  user_data = load_data('../yelp/user_100.json', user_data)

  # step 1
  g = snap.TUNGraph.New()

  user_map = pickle.load(open(userMapFile,"rb"))

  # step 1
  write_edges_file(user_data, user_map, edgesFile)

  # step 2
  # g = snap.LoadEdgeList(snap.PUNGraph, edgesFile, 0, 1)
  # step 2
  # snap.PrintInfo(g, "Evaluation Network Info", "eval_ntwk/eval_netwk_info_100.txt", False)
  # step 2
  # snap.SaveEdgeList(g, "eval_ntwk/eval_ntwk_100.txt")

# if necessary, this function can create an eval network based on number of users given
def genEvalNetwork(numUsers): 
  userMapFile = 'data/user_list_map_{}.p'.format(numUsers)
  user_map = pickle.load(open(userMapFile,"rb"))
  userJSONFile = '../yelp/user_{}.json'.format(numUsers)
  user_data = load_data(userJSONFile, user_data)

  # step 1
  edgesFile = 'eval_ntwk/eval_ntwk_edge_list_{}.txt'.format(numUsers)
  write_edges_file(user_data, user_map, edgesFile)


if __name__ == '__main__':
  main()
