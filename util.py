import json, math
import numpy as np
import matplotlib.pyplot as plt

'''
  Load JSON file and return as a list of dicts
'''
def loadJSON(fileName):
  user_data = []
  infile = open(fileName, 'r')
  data = json.load(infile)
  infile.close()
  return data 

'''
  Prints out a plot showing the frequency distribution of edge compatibility/similarity values in buckets of [0.1, 0.2, ... 1]

  @param edgeVals: map of the form {(node1ID, node2ID): similarityValue}, 
    where 0 <= similarityValue <= 1
  @return: None
'''
def plotBucketDistribution(edgeVals, scoreType, numUsers):
  valsList = [edgeVals[key] for key in edgeVals if edgeVals[key] != 0]
  buckets = [0] * 101
  for val in valsList:
    if not math.isnan(val):
      index = math.ceil(val*100)
      buckets[int(index)] += 1
  print buckets
  x = np.arange(0,1.01,0.01)
  titleStr = '{} Distribution for {} Yelp users'.format(scoreType, numUsers)
  plt.title(titleStr)
  plt.xlabel(scoreType)
  plt.ylabel('Count of edges')
  plt.scatter(x, buckets)
  plt.plot(x, buckets)
  plt.xlim(0,1)
  plt.ylim(0, max(valsList)+10)
  # plt.axis([0,1,0, 350000])
  plt.show()



# plot out all jaccard values
def plotDistributionJaccard(jaccardVals):
  jaccardList = [jaccardVals[key] for key in jaccardVals if jaccardVals[key] != 0]
  print jaccardList
  print 'number of edges with non-zero similarity', len(jaccardList)
  x = np.arange(len(jaccardList))
  plt.title('Jaccard Non-Zero Similarity Distribution for 1000 Yelp users')
  plt.ylabel('Jaccard Similarity')
  plt.xlabel('Pairs of nodes')
  plt.scatter(x, jaccardList)
  plt.show()