import snap, json
# Yaml found here: http://pyyaml.org/wiki/PyYAML


#NUMNODES = 30255
NUMNODES = 1000
# def populateIndices(foodCmtyV, evalCmtyV):

def jaccard(cmty1, cmty2, nodelist):
	#print "Cmty 1: %d" % len(cmty1)
	#print "Cmty 2: %d" % len(cmty2)
	#print "Nodelist"
	#print nodelist
	setA = set(cmty1)
	setB = set(cmty2)
	random_sample_set = set(nodelist)
	if len(setA) == 0 or len(setB) == 0:
		return 0
	# print 'setA', setA, len(setA)
	# print 'setB', setB, len(setB)
	intersectingSet = set.intersection(setA, setB)
	intersectingSet = set.intersection(intersectingSet, random_sample_set)
	unionSet = set.union(setA, setB)
	unionSet = set.intersection(unionSet, random_sample_set)
	ratio = float(len(intersectingSet))/len(unionSet)
	# print ratio
	return ratio

def friendshipPotential(foodCmty, evalCmty):
	foodSet = set(foodCmty)
	evalSet = set(evalCmty)
	correctSet = set.intersection(foodSet, evalSet)
	ratio = float(len(correctSet))/len(foodSet)
	return ratio

def pareto(foodCmty, evalCmty, nodelist):
	evalSet = set(evalCmty)
	foodSet = set(foodCmty)
	nodelistSet = set(nodelist)
	accuracy = friendshipPotential(foodCmty, evalCmty)
	boldness = len(foodSet)/len(set.intersection(evalSet, nodelistSet))
	pareto = accuracy * boldness
	return pareto

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

def generateEvalIndices(evalCmtyV):

	evalIndices = {x: -1 for x in range(NUMNODES)}

	evalCmtyCount = len(evalCmtyV) #first unused cluster number in eval network

	print "Adding eval indices"
	for i in xrange(len(evalCmtyV)):
		for NI in evalCmtyV[i]:
			evalIndices[NI] = i
			print "NID: %d, Eval Cluster: %d" % (NI, i)

	print "Replacing -1s"
	for i in xrange(NUMNODES):
		if evalIndices[i] == -1:
			evalIndices[i] = evalCmtyCount #set to next unused cluster
			evalCmtyCount += 1 #increment available cluster
		print "NID: %d, Eval Cluster: %d" % (i, evalIndices[i])

	return evalIndices

def generateFoodIndices(foodCmtyV, nodelist):

	#NEED TO GET RANDOM_SAMPLE
	foodIndices = {x: -1 for x in nodelist}

	foodCmtyCount = len(foodCmtyV) #first unused cluster number in eval network

	print "Adding food indices"
	for i in xrange(len(foodCmtyV)):
		for NI in foodCmtyV[i]:
			foodIndices[NI] = i
			#print "NID: %d, Food Cluster: %d" % (NI, i)

	for i in nodelist:
		if foodIndices[i] == -1:
			foodIndices[i] = foodCmtyCount
			foodCmtyCount += 1

	return foodIndices

def outputCmtys(evalIndices):
	
	file = open("../yelp/eval_network_communities.txt", "w")
	# for i in xrange(NUMNODES):
	# 	line = "%d\n" % evalIndices[i]
	# 	file.write(line)
	json.dump(evalIndices, file)
	file.close()

def inputEvalCmtys():

	file = open("../yelp/eval_network_communities.txt", "r")
	evalIndicesUnicode = json.load(file)
	evalIndices = {}
	for i in xrange(NUMNODES):
		#print evalIndicesUnicode[repr(i)]
		evalIndices[i] = evalIndicesUnicode[repr(i)]
	file.close()

def calculateAccuracy(foodCmtyV, foodIndices, evalClusterDict, evalIndices, nodelist):
	numFoodCmtys = len(foodCmtyV)

	runningJScore = 0

	for i in nodelist:
		if foodIndices[i] >= numFoodCmtys:
			#Not actually in the CmtyV, was manually indexed as its own cluster
			foodCmtyToPass = [i]
		else:
			foodCmtyToPass = foodCmtyV[foodIndices[i]]

		evalCmtyToPass = evalClusterDict[evalIndices[i]]
		#print "NID: %d, Cluster index: %d," % (i, evalIndices[i])
		#currJaccard = jaccard(foodCmtyToPass, evalCmtyToPass, nodelist)
		#print "Curr %f" % currJaccard
		#runningJScore += currJaccard

		#currPotential = friendshipPotential(foodCmtyToPass, evalCmtyToPass)
		#runningJScore += currPotential

		currPareto = pareto(foodCmtyToPass, evalCmtyToPass, nodelist)
		runningJScore += currPareto



	jaccardAverage = float(runningJScore)/len(nodelist)
	print "Accuracy: %f" % jaccardAverage


	return jaccardAverage



#def main():`
	# foodEdgesFile = 'food_ntwk/rati_edge_list_1000_threshold2.txt'
	# foodGraph = snap.LoadEdgeList(snap.PUNGraph, foodEdgesFile, 0, 1)

	# evalEdgesFile = 'eval_ntwk/eval_ntwk_edge_list_1000.txt'
	# evalGraph = snap.LoadEdgeList(snap.PUNGraph, evalEdgesFile, 0, 1)

	# foodCmtyV = snap.TCnComV()
	# evalCmtyV = snap.TCnComV()

	# #foodMod = snap.CommunityCNM(foodGraph, foodCmtyV)
	# #evalMod = snap.CommunityCNM(evalGraph, evalCmtyV)

	# evalIndices = generateEvalIndices(evalCmtyV)

	# #Generate map of indices of each node within each community vector
	# #nodeIndices = generateIndices(foodCmtyV, evalCmtyV)
	# nodeIndices = generateFoodIndices(foodCmtyV, xrange(NUMNODES))
	# jaccardSum = 0

	# numFoodCmtys = len(foodCmtyV)
	# numEvalCmtys = len(evalCmtyV)
	# for i in xrange(NUMNODES):
	# 	#Keep running total of jaccadr scores

	# 	if nodeIndices[i] >= numFoodCmtys:
	# 		#Not actually in the CmtyV, was manually indexed as its own cluster
	# 		foodCmtyToPass = [i]
	# 	else:
	# 		foodCmtyToPass = foodCmtyV[nodeIndices[i]]

	# 	if nodeIndices[i][1] >= numEvalCmtys:
	# 		evalCmtyToPass = [i]
	# 	else:
	# 		evalCmtyToPass = evalCmtyV[evalIndices[i]]
	# 	#jaccardSum += jaccard(foodCmtyV[nodeIndices[i][0]], evalCmtyV[nodeIndices[i][1]])
	# 	jaccardSum += jaccard(foodCmtyToPass, evalCmtyToPass)

	# jaccardAverage = float(jaccardSum)/NUMNODES
	# print "Accuracy: %f" % jaccardAverage

	# #Output eval clusters for reading later
	# outputCmtys(evalIndices)
	# evalIndices = inputEvalCmtys()




	

#main()