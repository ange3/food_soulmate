import json, sets
import numpy as np
from sklearn.metrics import jaccard_similarity_score

FILE = '../../yelp/user_1000.json'

def compScore(one, two):
	return jaccard_similarity_score(one, two)

def loadJSON():
  user_data = []
  infile = open(FILE, 'r')
  user_data = json.load(infile)
  print user_data[1]
  infile.close()
  return user_data  

def main():
	user_data = loadJSON()
	print compScore(user_data[0], user_data[1])

main()