import snap

# def populateIndices(foodCmtyV, evalCmtyV):

def jaccard(cmty1, cmty2):
  setA = set(cmty1)
  setB = set(cmty2)
  if len(setA) == 0 or len(setB) == 0:
    return 0
  # print 'setA', setA, len(setA)
  # print 'setB', setB, len(setB)
  intersectingSet = set.intersection(setA, setB)
  unionSet = set.union(setA, setB)
  ratio = float(len(intersectingSet))/len(unionSet)
  # print ratio
  return ratio

def generateIndices(foodCmtyV, evalCmtyV):
	nodeIndices = {}

	for i in xrange(len(foodCmtyV)):
		for NI in foodCmtyV[i]:
			nodeIndices[NI] = [i]
			print "NID: %d, Cluster: %d" % (NI, i)

	for i in xrange(len(evalCmtyV)):
		for NI in evalCmtyV[i]:
			nodeIndices[NI].append(i)
			print "NID: %d, Food Cluster: %d, Eval Cluster: %d" % (NI, nodeIndices[NI][0], i)

	return nodeIndices


def main():
	# evalFile = "../evalEdgeList.txt"
	# foodFile = "../foodEdgeList.txt"

	# foodGraph = snap.LoadEdgeList(snap.PUNGraph, foodFile, 0, 1)
	# evalGraph = snap.LoadEdgeList(snap.PUNGraph, evalFile, 0, 1)

	# For testing
	foodGraph = snap.GenRndGnm(snap.PUNGraph, 10, 25)
	evalGraph = snap.GenRndGnm(snap.PUNGraph, 10, 25)

	foodCmtyV = snap.TCnComV()
	evalCmtyV = snap.TCnComV()

	foodMod = snap.CommunityCNM(foodGraph, foodCmtyV)
	evalMod = snap.CommunityCNM(evalGraph, evalCmtyV)

	#Generate map of indices of each node within each community vector
	nodeIndices = generateIndices(foodCmtyV, evalCmtyV)

	numnodes = len(nodeIndices)
	jaccardSum = 0

	for i in xrange(numnodes):
		#Keep running total of jaccard scores
		jaccardSum += jaccard(foodCmtyV[nodeIndices[i][0]], evalCmtyV[nodeIndices[i][1]])

	jaccardAverage = float(jaccardSum)/numnodes
	print "Accuracy: %f" % jaccardAverage




	

main()