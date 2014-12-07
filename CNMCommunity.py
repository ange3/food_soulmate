import snap


NUMNODES = 1000
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
	nodeIndices = {x: [-1, -1] for x in range(NUMNODES)}

	foodCmtyCount = len(foodCmtyV) #first unused cluster number in food network
	evalCmtyCount = len(evalCmtyV) #first unused cluster number in eval network

	print "Adding food indices"
	for i in xrange(len(foodCmtyV)):
		for NI in foodCmtyV[i]:
			print "Current NID: %d" % NI
			nodeIndices[NI][0] = i
			print "NID: %d, Cluster: %d" % (NI, i)


	print "Adding eval indices"
	for i in xrange(len(evalCmtyV)):
		for NI in evalCmtyV[i]:
			nodeIndices[NI][1] = i
			print "NID: %d, Food Cluster: %d, Eval Cluster: %d" % (NI, nodeIndices[NI][0], i)


	print "Replacing -1s"
	for i in xrange(NUMNODES):
		if nodeIndices[i][0] == -1:
			nodeIndices[i][0] = foodCmtyCount #set to next unused cluster
			foodCmtyCount += 1 #increment available cluster
		if nodeIndices[i][1] == -1:
			nodeIndices[i][1] = evalCmtyCount #set to next unused cluster
			evalCmtyCount += 1 #increment available cluster
		print "NID: %d, Food Cluster: %d, Eval Cluster: %d" % (i, nodeIndices[i][0], nodeIndices[i][1])

	return nodeIndices


def main():
	# evalFile = "../evalEdgeList.txt"
	# foodFile = "../foodEdgeList.txt"

	# foodGraph = snap.LoadEdgeList(snap.PUNGraph, foodFile, 0, 1)
	# evalGraph = snap.LoadEdgeList(snap.PUNGraph, evalFile, 0, 1)

	# For testing
	# foodGraph = snap.GenRndGnm(snap.PUNGraph, 10, 25)
	# evalGraph = snap.GenRndGnm(snap.PUNGraph, 10, 25)
	foodEdgesFile = 'food_ntwk/food_ntwk_edge_list_1000.txt'
	foodGraph = snap.LoadEdgeList(snap.PUNGraph, foodEdgesFile, 0, 1)

	evalEdgesFile = 'eval_ntwk/eval_ntwk_edge_list_1000.txt'
	evalGraph = snap.LoadEdgeList(snap.PUNGraph, evalEdgesFile, 0, 1)

	foodCmtyV = snap.TCnComV()
	evalCmtyV = snap.TCnComV()

	foodMod = snap.CommunityCNM(foodGraph, foodCmtyV)
	evalMod = snap.CommunityCNM(evalGraph, evalCmtyV)

	#Generate map of indices of each node within each community vector
	nodeIndices = generateIndices(foodCmtyV, evalCmtyV)
	jaccardSum = 0

	numFoodCmtys = len(foodCmtyV)
	numEvalCmtys = len(evalCmtyV)
	for i in xrange(NUMNODES):
		#Keep running total of jaccard scores

		if nodeIndices[i][0] >= numFoodCmtys:
			#Not actually in the CmtyV, was manually indexed as its own cluster
			foodCmtyToPass = [i]
		else:
			foodCmtyToPass = foodCmtyV[nodeIndices[i][0]]

		if nodeIndices[i][1] >= numEvalCmtys:
			evalCmtyToPass = [i]
		else:
			evalCmtyToPass = evalCmtyV[nodeIndices[i][1]]
		#jaccardSum += jaccard(foodCmtyV[nodeIndices[i][0]], evalCmtyV[nodeIndices[i][1]])
		jaccardSum += jaccard(foodCmtyToPass, evalCmtyToPass)

	jaccardAverage = float(jaccardSum)/NUMNODES
	print "Accuracy: %f" % jaccardAverage




	

main()