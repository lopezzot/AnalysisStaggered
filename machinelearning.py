import clustering
import cPickle as pickle

def picklesinglecluster(vectorsignals, chervectorsignals, ID, MCEnergy, namefile):
	"""Function to pickle a cluster, vector signals scintillation 
	and cherenkov must be provided. Provide also known ID, MC truth energy and 
	name of pickle file"""
	startindex = vectorsignals.index(max(vectorsignals))
	cluster = clustering.buildcluster(startindex, vectorsignals)
	cluster.find_modules(vectorsignals)
	cluster.compute_chersignal(chervectorsignals)
	cluster.ID = str(ID)
	cluster.Energy = MCEnergy
	print(cluster.modules, cluster.chersignal, cluster.ID)
	file = open(str(namefile),"wb")
	pickle.dump(cluster, file)
	file.close()

def unpicklesinglecluster(namefile):
	"""Unpickle signle cluster"""
	file = open(str(namefile), "rb")
	cluster = pickle.load(file)
	print(cluster.modules, cluster.chersignal, cluster.ID)

def picklelistofclusters(listofclusters, namefile):
	"""Function to pickle list of clusters trained for 
	machine learning"""
	file = open(str(namefile),"wb")
	pickle.dump(listofclusters, file)
	file.close()

def unpicklelistofclusters(namefile):
	"""Function to unpickle list of clusters trained for
	machine learning"""
	file = open(str(namefile), "rb")
	listofclusters = pickle.load(file)
	return listofclusters

def differencebetweenclusters(cluster, trainedcluster):
	"""Function to compute difference between clusters"""
	difference1 = (trainedcluster.EnergyScin/trainedcluster.EnergyCher) - (cluster.EnergyScin/cluster.EnergyCher)
	difference2 = trainedcluster.radius - cluster.radius
	return abs(difference1) # Not using (+ difference2) #return absolute value of difference

def seconddifferencebetweenclusters(cluster, trainedcluster):
	differece = trainedcluster.EnergyScin - cluster.EnergyScin
	return abs(differece) #return absolute value of difference

def find_ID(cluster, namefile):
	"""Function to find cluster ID with machine learning"""
	trainedlistofclusters = unpicklelistofclusters(namefile)
	listofdifferences = []
	electroncounter = 0
	hadroncounter = 0
	for trainedcluster in trainedlistofclusters:
		listofdifferences.append(differencebetweenclusters(cluster, trainedcluster))
	trainedlistofclusters.sort(key=dict(zip(trainedlistofclusters, listofdifferences)).get)
	for i in range(20):
		if trainedlistofclusters[i].ID == "electron":
			electroncounter = electroncounter + 1
		else:
			hadroncounter = hadroncounter + 1
	if electroncounter >= 5:#10
		cluster.ID = "electron"
	else:
		cluster.ID = "hadron"
	return cluster.ID

def find_energy(cluster, namefile):
	"""Function to compute by machine learning the energy of 
	a cluster, the cluster ID must me prior computed"""
	trainedlistofclusters = unpicklelistofclusters(namefile)
	selectedlistofclusters = []
	listofdifferences = []
	secondlistofdifferences = []
	chercalibconstant = 0
	scincalibconstant = 0
	secondchercalibconstant = 0
	secondscincalibconstant = 0
	counter = 0
	for index in range(len(trainedlistofclusters)):
		if trainedlistofclusters[index].ID == cluster.ID:
			selectedlistofclusters.append(trainedlistofclusters[index])
	for trainedcluster in selectedlistofclusters:
		listofdifferences.append(differencebetweenclusters(cluster, trainedcluster))
	selectedlistofclusters.sort(key=dict(zip(selectedlistofclusters, listofdifferences)).get)
	for i in range(20):
		chercalibconstant += selectedlistofclusters[i].Energy/selectedlistofclusters[i].chersignal
		scincalibconstant += selectedlistofclusters[i].Energy/selectedlistofclusters[i].scinsignal
	chercalibconstant = chercalibconstant/20
	scincalibconstant = scincalibconstant/20
	cluster.MLEnergy = (cluster.chersignal*chercalibconstant + cluster.scinsignal*scincalibconstant)/2
	cluster.MLScinEnergy = cluster.scinsignal*scincalibconstant
	cluster.MLCherEnergy = cluster.chersignal*chercalibconstant
	#Now find second ML energies
	secondlistofclusters = selectedlistofclusters[0:20]
	for trainedcluster in secondlistofclusters:
									






		secondlistofdifferences.append(seconddifferencebetweenclusters(cluster, trainedcluster))
	secondlistofclusters.sort(key=dict(zip(secondlistofclusters, secondlistofdifferences)).get)
	for i in range(5):
		secondchercalibconstant += secondlistofclusters[i].Energy/secondlistofclusters[i].chersignal
		secondscincalibconstant += secondscincalibconstant[i].Energy/secondlistofclusters[i].scinsignal
	secondchercalibconstant = secondchercalibconstant/5
	secondscincalibconstant = secondscincalibconstant/5
	cluster.secondMLEnergy = (cluster.chersignal*secondchercalibconstant + cluster.scinsignal*secondscincalibconstant)/2
	cluster.secondMLScinEnergy = cluster.scinsignal*secondscincalibconstant
	cluster.secondMLCherEnergy = cluster.chersignal*secondchercalibconstant
	#return all energies
	return cluster.MLEnergy, cluster.MLScinEnergy, cluster.MLCherEnergy, cluster.secondMLEnergy, cluster.secondMLScinEnergy, cluster.secondMLCherEnergy







