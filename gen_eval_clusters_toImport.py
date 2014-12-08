import snap, json


NUMNODES = 30255


def generateEvalIndices(evalCmtyV):

	evalIndices = {x: -1 for x in range(NUMNODES)}

	evalCmtyCount = len(evalCmtyV) #first unused cluster number in eval network

	#print "Adding eval indices"
	for i in xrange(len(evalCmtyV)):
		for NI in evalCmtyV[i]:
			evalIndices[NI] = i
			#print "NID: %d, Eval Cluster: %d" % (NI, i)

	#print "Replacing -1s"
	for i in xrange(NUMNODES):
		if evalIndices[i] == -1:
			evalIndices[i] = evalCmtyCount #set to next unused cluster
			evalCmtyCount += 1 #increment available cluster
		#print "NID: %d, Eval Cluster: %d" % (i, evalIndices[i])

	return evalIndices

def outputCmtys(evalIndices):
	
	file = open("../yelp/eval_network_communities_full.txt", "w")
	# for i in xrange(NUMNODES):
	# 	line = "%d\n" % evalIndices[i]
	# 	file.write(line)
	json.dump(evalIndices, file)
	file.close()

def inputEvalCmtys():
	file = open("../yelp/eval_network_communities_full.txt", "r")
	evalIndicesUnicode = json.load(file)
	evalIndices = {}
	for i in xrange(NUMNODES):
		#print evalIndicesUnicode[repr(i)]
		evalIndices[i] = evalIndicesUnicode[repr(i)]
	file.close()
	return evalIndices

def createClusterDict(evalIndices):
	clusterDict = {}
	for NID in evalIndices.keys():
		if evalIndices[NID] not in clusterDict.keys():
			clusterDict[evalIndices[NID]] = [NID]
		else:
			clusterDict[evalIndices[NID]].append(NID)
	#print clusterDict
	return clusterDict

def main():
	evalEdgesFile = 'eval_ntwk/eval_edge_list_phoenix.txt'
	evalGraph = snap.LoadEdgeList(snap.PUNGraph, evalEdgesFile, 0, 1)

	evalCmtyV = snap.TCnComV()

	evalMod = snap.CommunityCNM(evalGraph, evalCmtyV)
	evalIndices = generateEvalIndices(evalCmtyV)

	outputCmtys(evalIndices)
	#evalIndices = inputCmtys()


	

#main()