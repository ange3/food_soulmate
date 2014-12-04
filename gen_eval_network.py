import json
import snap
from pprint import pprint
import pickle
import os

#test

def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values

def write_edges_file(user_data, user_map, edgesFile):
  friend_list = []
  file = open(edgesFile, "w")

  for i in xrange(len(user_data)):
    friend_list.append(user_data[i]['friends'])
    # print friend_list[i]
    for j in xrange(len(friend_list[i])):
      # print "user_data[",i,"]['user_id']: ",user_data[i]['user_id']
      # print "friend_list[",i,"][",j,"]: ",friend_list[i][j]
      line = "{0} {1}\n".format(user_map[user_data[i]['user_id']], user_map[friend_list[i][j]]) 
      file.write(line)
  # print len(user_data)
  # print "nodeID: ",user_map['7Erd8wom0MYbetSjxvoufQ']
  file.close()

def main(): 
  edgesFile = 'evaluation_network_edgelist.txt'
  userMapFile = 'data/user_list_map_100.p'
  user_data = []
  user_data = load_data('../yelp/new_user.json', user_data)
  # print "friends of a single record: ",user_data[0]['friends']

  user_map = pickle.load(open(userMapFile,"rb"))

  # write_edges_file(user_data, user_map, edgesFile)

  g = snap.LoadEdgeList(snap.PUNGraph, edgesFile, 0, 1)
  snap.PrintInfo(g, "Evaluation Network Info", "evaluation_network_info.txt", False)
  # snap.SaveEdgeList(g, "evaluation_network.txt")

if __name__ == '__main__':
  main()
