import random
import os
import shutil
import glob
from array import array
from ROOT import gROOT, TFile, TTree
import map
import mapgroup
import clustering
import machinelearning
import ROOTHistograms
import service
import Staggeredmap
import StaggeredROOTHistograms

#Hardcoded calibration constants and Chi factor
scincalibconstant = 23.92 #MeV/MeV
chercalibconstant = 23.00 #MeV/Cpe
Chi = 0.50 #to be better defined
HEcher = 0.360
HEscin = 0.679

#Set root file and tree
gROOT.Reset()

file = raw_input("Insert namefile: ")
filename = "data/"+str(file)+"/B4.root"
inputFile = TFile(str(filename)) #root input file
tree = TTree()
inputFile.GetObject("B4", tree)
'''
#---------------------------------------------------------------------------------------------------
#Section used only if you want to estimate the calibration constants and Chi factor of a module.
#DREAM is calibrated with electrons. The input file must be from electron events with the same energy.
#To estimate h/e Cher and scin values and the Chi factor a second root file with pions (+ or -) is needed.

#To later perform h/e Cher and scin computation and Chi factor
namepionfile = raw_input("Insert name of ROOT pion (+ or -) file: ")

#Set parameters
NofEvents = tree.GetEntries()
fastchercalibconstant = 0
fastscincalibconstant = 0
fastChi = 0
chercalibconstant = 0
scincalibconstant = 0
Chi = 0
firstcounter = 0
secondcounter = 0

#Estimate Cherenkov and Scintillation calibration constants
for Event in range(100):

	tree.GetEntry(Event)

	#Set values of tree
	PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
	PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
	EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
	Energyem = tree.Energyem # Energy deposited by the em component
	EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
	EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
	NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
	VectorSignals = tree.VectorSignals # Vector of energy deposited in Scin fibers (Birk corrected)
	VectorSignalsCher = tree.VectorSignalsCher # Vector of Cher p.e. detected in Cher fibers

	#Create grouped vectors (1.2 x 1.2 cm^2)
	GroupedVectorSignals = mapgroup.group(VectorSignals)
	GroupedVectorSignalsCher = mapgroup.group(VectorSignalsCher)

	#For output file
	FirstPrimaryParticleName = PrimaryParticleName
	FirstPrimaryParticleEnergy = PrimaryParticleEnergy

	#Estimating calibration constants using all the calorimeter signal
	if sum(GroupedVectorSignalsCher) == 0.0:
		continue
		print "One event with no Cherenkov signal"

	fastchercalibconstant += PrimaryParticleEnergy/sum(GroupedVectorSignalsCher)
	fastscincalibconstant += PrimaryParticleEnergy/sum(GroupedVectorSignals)

	firstcounter = firstcounter+1

	#Estimating calibration constants using cluster signals
	fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
	cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)
	cluster.find_modules(GroupedVectorSignals)
	cluster.compute_chersignal(GroupedVectorSignalsCher)

	if cluster.chersignal == 0.0:
		continue
		print "One cluster with no Cherenkov signal!"

	chercalibconstant += PrimaryParticleEnergy/cluster.chersignal
	scincalibconstant += PrimaryParticleEnergy/cluster.scinsignal

	secondcounter = secondcounter+1

fastchercalibconstant = fastchercalibconstant/firstcounter
fastscincalibconstant = fastscincalibconstant/firstcounter
chercalibconstant = chercalibconstant/secondcounter
scincalibconstant = scincalibconstant/secondcounter

print "End of calibration constants -> now estimating h/e values."

#Estimating h/e Cher and scin values and Chi factor
#Set root file and tree
gROOT.Reset()
inputFile = TFile(namepionfile) #root input file
tree = TTree()
inputFile.GetObject("B4", tree)

#Set parameters and counters
NofEvents = tree.GetEntries()
Scinenergy1 = 0
Scinenergy2 = 0
Scinenergy3 = 0
Cherenergy1 = 0
Cherenergy2 = 0
Cherenergy3 = 0
FastScinenergy1 = 0
FastScinenergy2 = 0
FastScinenergy3 = 0
FastCherenergy1 = 0
FastCherenergy2 = 0
FastCherenergy3 = 0
counter1 = 0
counter2 = 0
counter3 = 0

for Event in range(100):

	tree.GetEntry(Event)

	#Set values of tree
	PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
	PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
	EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
	Energyem = tree.Energyem # Energy deposited by the em component
	EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
	EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
	NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
	VectorSignals = tree.VectorSignals # Vector of energy deposited in Scin fibers (Birk corrected)
	VectorSignalsCher = tree.VectorSignalsCher # Vector of Cher p.e. detected in Cher fibers

	#Create grouped vectors (1.2 x 1.2 cm^2)
	GroupedVectorSignals = mapgroup.group(VectorSignals)
	GroupedVectorSignalsCher = mapgroup.group(VectorSignalsCher)

	#Create hisogtrams
	Fem = Energyem/EnergyTot
	if Fem < 0.33 and Fem > 0.0:
		FastScinenergy1 += fastscincalibconstant*sum(GroupedVectorSignals)
		FastCherenergy1 += fastchercalibconstant*sum(GroupedVectorSignalsCher)

		fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
		cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)
		if cluster.radius < 20:
			continue
		cluster.find_modules(GroupedVectorSignals)
		cluster.compute_chersignal(GroupedVectorSignalsCher)

		Scinenergy1 += scincalibconstant*cluster.scinsignal
		Cherenergy1 += chercalibconstant*cluster.chersignal

		counter1 += 1
	elif Fem < 0.66 and Fem > 0.33:
		FastScinenergy2 += fastscincalibconstant*sum(GroupedVectorSignals)
		FastCherenergy2 += fastchercalibconstant*sum(GroupedVectorSignalsCher)

		fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
		cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)
		if cluster.radius < 20:
			continue
		cluster.find_modules(GroupedVectorSignals)
		cluster.compute_chersignal(GroupedVectorSignalsCher)

		Scinenergy2 += scincalibconstant*cluster.scinsignal
		Cherenergy2 += chercalibconstant*cluster.chersignal

		counter2 += 1
	elif Fem < 1.0 and Fem > 0.66:
		FastScinenergy3 += fastscincalibconstant*sum(GroupedVectorSignals)
		FastCherenergy3 += fastchercalibconstant*sum(GroupedVectorSignalsCher)

		fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
		cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)
		if cluster.radius < 20:
			continue
		cluster.find_modules(GroupedVectorSignals)
		cluster.compute_chersignal(GroupedVectorSignalsCher)

		Scinenergy3 += scincalibconstant*cluster.scinsignal
		Cherenergy3 += chercalibconstant*cluster.chersignal

		counter3 += 1

#Average energy reconstructed
FastScinenergy1 = FastScinenergy1/counter1
FastCherenergy1 = FastCherenergy1/counter1
Scinenergy1 = Scinenergy1/counter1
Cherenergy1 = Cherenergy1/counter1
FastScinenergy2 = FastScinenergy2/counter2
FastCherenergy2 = FastCherenergy2/counter2
Scinenergy2 = Scinenergy2/counter2
Cherenergy2 = Cherenergy2/counter2
FastScinenergy3 = FastScinenergy3/counter3
FastCherenergy3 = FastCherenergy3/counter3
Scinenergy3 = Scinenergy3/counter3
Cherenergy3 = Cherenergy3/counter3

#Values grouped in list for ROOT graphs
FastScinenergy = array('d',[FastScinenergy1, FastScinenergy2, FastScinenergy3])
FastCherenergy = array('d',[FastCherenergy1, FastCherenergy2, FastCherenergy3])
Scinenergy = array('d',[Scinenergy1, Scinenergy2, Scinenergy3])
Cherenergy = array('d',[Cherenergy1, Cherenergy2, Cherenergy3])
fem = array('d',[0.165, 0.495, 0.825])

#Create graphs, compute he Cher and scin values and Chi factor
Fasthescin, Fasthecher, hescin, hecher = ROOTHistograms.create_graph(FastScinenergy, FastCherenergy, Scinenergy, Cherenergy, fem, PrimaryParticleEnergy)
fastChi = (1 - Fasthescin)/(1 - Fasthecher)
Chi = (1 - hescin)/(1 - hecher)

#Print calibration results on file
outputfile = open("calibration.txt","w+")
outputfile.write("Calibration constants for electron + hadron of energies: \n")
outputfile.write(str(FirstPrimaryParticleEnergy) + " MeV\n")
outputfile.write(str(PrimaryParticleEnergy) + " MeV\n")
outputfile.write("-------------------------FAST ANALYSIS---------------------------------------------------------\n")
outputfile.write("fastchercalibconstant = " + str(fastchercalibconstant) + "MeV/Cpe" + " fastscincalibconstant = " + str(fastscincalibconstant) + " MeV/MeV\n")
outputfile.write("fasthescin = " + str(Fasthescin) + " fasthecher = " + str(Fasthecher) + " fastChi = " + str(fastChi) + " \n")
outputfile.write("-------------------------CLUSTER ANALYSIS------------------------------------------------------\n")
outputfile.write("chercalibconstant = " + str(chercalibconstant) + " MeV/Cpe " + "scincalibconstant = " + str(scincalibconstant) + " MeV/MeV\n")
outputfile.write("hescin = " + str(hescin) + " hecher = " + str(hecher) + " Chi = " + str(Chi))
outputfile.close()

#Create folder calibration and move output file into
if not os.path.exists("calibration"):
	os.makedirs("calibration")
foldername = raw_input("Insert folder name (take care folder does not exist!): ")
foldername = "calibration/"+foldername
os.makedirs(str(foldername))
for eps_file in glob.iglob('*.eps'):
	shutil.move(eps_file, str(foldername))
for txt_file in glob.iglob('*.txt'):
	shutil.move(txt_file, str(foldername))
print "End of h/e values estimation."
#---------------------------------------------------------------------------------------------------	

#---------------------------------------------------------------------------------------------------
#Section used only if you want to ceate a trained list of clusters to later perform machine learning
#ID and energy reconstruction. ROOT events must be single particle events to be classified in as "electron"
#or "hadron" with a given MC truth energy. Enable this part with Docopt.

#Set name of pickle file containing trained clusters
namefile = raw_input("Input pickle namefile (with .p extension): ")
particletype = raw_input("Input particle type (electron or hadron): ")

#Set parameters and containers
NofEvents = tree.GetEntries()
listoftrainedclusters = []

for Event in range(1000):
	
	tree.GetEntry(Event)

	#Set values of tree
	PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
	PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
	EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
	Energyem = tree.Energyem # Energy deposited by the em component
	EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
	EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
	NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
	VectorSignals = tree.VectorSignals # Vector of energy deposited in Scin fibers (Birk corrected)
	VectorSignalsCher = tree.VectorSignalsCher # Vector of Cher p.e. detected in Cher fibers

	#Create grouped vectors (1.2 x 1.2 cm^2)
	GroupedVectorSignals = mapgroup.group(VectorSignals)
	GroupedVectorSignalsCher = mapgroup.group(VectorSignalsCher)

	print "--------------------------------------------------------\n"
	print "Processing event" + str(Event) + ": " + PrimaryParticleName + " energy " + str(PrimaryParticleEnergy) + " MeV" +"\n"

	#Create cluster
	fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
	cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)
	cluster.find_modules(GroupedVectorSignals)
	cluster.compute_chersignal(GroupedVectorSignalsCher)
	cluster.computeEnergyScin(scincalibconstant)
	cluster.computeEnergyCher(chercalibconstant)
	if cluster.chersignal == 0.0:
		print "One cluster with no Cherenkov signal"
		continue
	cluster.Energy = PrimaryParticleEnergy
	if particletype == "electron":
		cluster.ID = "electron"
	else:
		cluster.ID = "hadron"

	#Creat list of trained clusters, random shuffle it and save in pickle file
	listoftrainedclusters.append(cluster)

random.shuffle(listoftrainedclusters)
machinelearning.picklelistofclusters(listoftrainedclusters, namefile)
print "Pickled " + str(len(listoftrainedclusters)) + " trained clusters in " + namefile +"."
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
#Section used for the complete analysis. 

#Set name of pickle file containing trained clusters
#namefile = raw_input("Input name of file for machine learning: ")
#particletype = raw_input("Input particle type (electron or hadron): ")

#Ask for how many events to be processed
NofEvents = tree.GetEntries()
NofEventsProcessed = raw_input(str(NofEvents) + " Events, how many to process: ")

#Set Parameters, containers and counters

traditionalreconstructedenergy = []
machinelearningreconstructedenergy = []
secondmlreconstructedenergy = []
traditionalscinreconstructedenergy = []
machinelearningscinreconstructedenergy = []
secondmlscinreconstructedenergy = []
traditionalcherreconstructedenergy = []
machinelearningcherreconstructedenergy = []
secondmlcherreconstructedenergy = []
correctML_ID = 0
wrongML_ID = 0
trueemfraction = []
dremfraction = []
differenceemfraction = []
totalenergy = []
energyscin = []

	#This version of the code deals with single particle events
	#Find a single maximum and build a cluster around it
	fixedindex = GroupedVectorSignals.index(max(GroupedVectorSignals))
	cluster = clustering.buildcluster(fixedindex, GroupedVectorSignals)

	#Compute cluster informations (Cherenkov signal, Energy Scin, Energy Cher)
	cluster.find_modules(GroupedVectorSignals)
	cluster.compute_chersignal(GroupedVectorSignalsCher)
	if cluster.chersignal == 0.0:
		print "Cluster with no Cherenkov signal"
		continue
	cluster.computeEnergyScin(scincalibconstant)
	cluster.computeEnergyCher(chercalibconstant)
	traditionalscinreconstructedenergy.append(cluster.EnergyScin)
	traditionalcherreconstructedenergy.append(cluster.EnergyCher)
	
	#FIND FAKE ID TO PERFORM TRADITIONAL CALORIMETRIC MEASUREMENTS
	#Perform traditional calorimetric measurement
	#Must be done after compute_chersignal, computeEnergyScin and Cher
	if particletype == "electron":
		cluster.ID = "electron"
	else:
		cluster.ID = "hadron"
	truth_ID = cluster.ID
	cluster.computeEnergy(Chi)
	traditionalreconstructedenergy.append(cluster.Energy)
	print "Traditional energy = " + str(cluster.Energy) 

	#Find cluster ID with machine learning
	cluster.compute_ID(namefile)

	#Find cluster ML energy with machine learning
	#Must be done after cluster.compute_ID
	cluster.compute_MLEnergy(namefile)
	machinelearningreconstructedenergy.append(cluster.MLEnergy)
	machinelearningscinreconstructedenergy.append(cluster.MLScinEnergy)
	machinelearningcherreconstructedenergy.append(cluster.MLCherEnergy)
	secondmlreconstructedenergy.append(cluster.secondMLEnergy)
	secondmlscinreconstructedenergy.append(cluster.secondMLScinEnergy)
	secondmlcherreconstructedenergy.append(cluster.secondMLCherEnergy)
	print "ML energy = " + str(cluster.MLEnergy)
	print "Second ML energy = " + str(cluster.secondMLEnergy)

	#Compute correct and wrong ML IDs
	if cluster.ID == truth_ID:
		correctML_ID += 1
	elif cluster.ID != truth_ID:
		wrongML_ID += 1

	#Em fraction analysis
	trueemfraction.append(Energyem/EnergyTot)
	e = traditionalcherreconstructedenergy[Event]/traditionalscinreconstructedenergy[Event]
	dremfraction.append((-e*HEcher+HEscin)/(e-e*HEcher-1+HEscin))
	differenceemfraction.append(trueemfraction[Event]-dremfraction[Event])

	#Total energy and energy in scintillator analysis
	totalenergy.append(EnergyTot)
	energyscin.append(EnergyScin)

#End of machine learning analysis	
print "End of machine analysis"

#Combine DR Energy and 	ML Energy
combinedenergy = []
for Event in range(len(machinelearningreconstructedenergy)):
	combinedenergy.append((machinelearningreconstructedenergy[Event]+traditionalreconstructedenergy[Event])/2)

#Combine DR Energy and second ML Energy
secondcombinedenergy = []
for Event in range(len(secondmlreconstructedenergy)):
	secondcombinedenergy.append((secondmlreconstructedenergy[Event]+traditionalreconstructedenergy[Event])/2)

#Print ROOT histograms of DR Energy anf ML Energy, Scin energy and ML Scin energy, Cher energy and ML Cher energy
ROOTHistograms.create_thirdroothistograms(traditionalscinreconstructedenergy, machinelearningscinreconstructedenergy)
ROOTHistograms.create_fourthroothistograms(traditionalcherreconstructedenergy, machinelearningcherreconstructedenergy)
ROOTHistograms.create_secondroothistograms(traditionalreconstructedenergy, machinelearningreconstructedenergy)
ROOTHistograms.create_fifthroothistograms(combinedenergy)
ROOTHistograms.create_sixthroothistograms(secondcombinedenergy)
ROOTHistograms.create_seventhroothistograms(secondMLEnergy, secondMLScinEnergy, secondMLCherEnergy)
ROOTHistograms.create_eightroothistograms(machinelearningscinreconstructedenergy, machinelearningcherreconstructedenergy)
ROOTHistograms.create_ninethroothistograms(traditionalscinreconstructedenergy, traditionalcherreconstructedenergy)

#Print ROOT histograms of EM fraction
ROOTHistograms.create_fastroothistogram(trueemfraction, "True Fem", "Fem", "# Events", "TrueFem.eps")
ROOTHistograms.create_fastroothistogram(dremfraction, "Dr Fem", "Fem", "# Events", "DRFem.eps")
ROOTHistograms.create_fastroothistogram(differenceemfraction, "Difference Fem", "Fem", "# Events", "DiffFem.eps")

#Print ROOT histograms of total energy and energy in scintillator
ROOTHistograms.create_fastroothistogram(totalenergy,"En Tot", "Energy (MeV)", "# Events", "EnergyTot.eps")
ROOTHistograms.create_fastroothistogram(energyscin,"En Scin", "Energy (MeV)", "# Events", "EnergyScin.eps")

#Compute correlation and print into file
correlationTRML = service.compute_correlation(traditionalreconstructedenergy, machinelearningreconstructedenergy)
correlationScinCher = service.compute_correlation(traditionalscinreconstructedenergy, traditionalcherreconstructedenergy)
correlationMLScinCher = service.compute_correlation(machinelearningscinreconstructedenergy, machinelearningcherreconstructedenergy)
outputfile = open("result.txt","w+")
outputfile.write(str(FirstPrimaryParticleEnergy) + " MeV\n")
outputfile.write(str(PrimaryParticleEnergy) + " MeV\n")
outputfile.write("Correlation DR Energy - ML Energy = " + str(correlationTRML) + " \n") 
outputfile.write("Correlation DR Scin - DR Cher = " + str(correlationScinCher) + " \n")
outputfile.write("Correlation ML Scin - ML Cher = " + str(correlationMLScinCher) + " \n")
outputfile.close()

#Print ML IDs counters
#print str(NofEventsProcessed) + " Events: " + str(correctML_ID) + " correct ID " + str(wrongML_ID) + " wrong ID."

#Create lego plot for first event
tree.GetEntry(5)

#Set values of tree
PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
Energyem = tree.Energyem # Energy deposited by the em component
EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
VectorSignals = tree.VectorSignals # Vector of energy deposited in Scin fibers (Birk corrected)
VectorSignalsCher = tree.VectorSignalsCher # Vector of Cher p.e. detected in Cher fibers

#Create grouped vectors (1.2 x 1.2 cm^2)
GroupedVectorSignals = mapgroup.group(VectorSignals)
GroupedVectorSignalsCher = mapgroup.group(VectorSignalsCher)

print "--------------------------------------------------------\n"
print "Processing event: " + PrimaryParticleName + " energy " + str(PrimaryParticleEnergy) + " MeV" +"\n"

#Set analysis and event parameters and create root histograms
ScinTreshold = 0.03 #30 KeV, energy treshold for single photoelectron production
CherTreshold = 0 #We assume to detect single Cherenkov p.e.
ScinMaxFiber = max(list(VectorSignals)) #maximum energy deposit in scintillating fibers
CherMaxFiber = max(list(VectorSignalsCher)) #maximum Cherenkov p.e. in clear fibers
NumFibers = len(list(VectorSignals)) #number of fibers (Cherenkov+Scintillating) 
NumModules = len(list(GroupedVectorSignals)) #number of modules

#Show lego plots ("images") of one event
ROOTHistograms.create_firstroothistograms(PrimaryParticleName, VectorSignals, VectorSignalsCher, GroupedVectorSignals, 
GroupedVectorSignalsCher, ScinTreshold, CherTreshold, ScinMaxFiber, CherMaxFiber, NumFibers, NumModules)

#Create folder result and move output file into
if not os.path.exists("result"):
	os.makedirs("result")
foldername = raw_input("Insert folder name (take care folder does not exist yet!): ")
foldername = "result/"+foldername
os.makedirs(str(foldername))
for eps_file in glob.iglob('*.eps'):
	shutil.move(eps_file, str(foldername))
for txt_file in glob.iglob('*.txt'):
	shutil.move(txt_file, str(foldername))
#---------------------------------------------------------------------------------------------------------
'''
#---------------------------------------------------------------------------------------------------------
#Fast analysis part

#Ask for how many events to be processed
NofEvents = tree.GetEntries()
NofEventsProcessed = raw_input(str(NofEvents) + " Events, how many to process: ")

#Containers to be filled event by event
LongScinSignal = []
LongCherSignal = []
ShortScinSignal = []
ShortCherSignal = []
EnergyTotContainer = []

#Calibration constants to compute
shortcalibscin = 0
shortcalibcher = 0
longcalibscin = 0
longcalibcher = 0

#Calibration constants computed with 50 GeV electrons
longcalibscin_comp = 46.42 # MeV/MeV
longcalibcher_comp = 43.9959 # MeV/C p.e.
shortcalibscin_comp = 56.7787 # MeV/MeV
shortcalibcher_comp = 54.76377 # MeV/C p.e.

#Energy reconstructed containers
shortscinenerec = []
shortcherenerec = []
longcherenerec = []
longscinenerec = []
shortenerec = []
longenerec = []
shortlongenerec = []
enereclong_short = []

#C/S containers
C_S_short = []
C_S_long = []

#Set Parameters, containers and counters

for Event in range(int(NofEventsProcessed)):

	tree.GetEntry(Event)

	#Set values of tree
	PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
	PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
	EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
	Energyem = tree.Energyem # Energy deposited by the em component
	EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
	EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
	NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
	LongVectorSignals = tree.LongVectorSignals # Vector of energy deposited in LONG Scin fibers (Birk corrected)
	LongVectorSignalsCher = tree.LongVectorSignalsCher # Vector of Cher p.e. detected in LONG Cher fibers
	ShortVectorSignals = tree.ShortVectorSignals # Vector of energy deposited in SHORT Scin fibers (Birk corrected)
	ShortVectorSignalsCher = tree.ShortVectorSignalsCher # Vector of energy deposited in SHORT Cher fibers 

	#Create grouped vectors (1.2 x 1.2 cm^2)
	#GroupedVectorSignals = mapgroup.group(VectorSignals)
	#GroupedVectorSignalsCher = mapgroup.group(VectorSignalsCher)

	print "--------------------------------------------------------\n"
	print "Processing event" + str(Event) + " of " + str(NofEventsProcessed) + ": " + PrimaryParticleName + " energy " + str(PrimaryParticleEnergy) + " MeV" +"\n"

	#Set analysis and event parameters and create root histograms
	ScinTreshold = 0.03 #30 KeV, energy treshold for single photoelectron production
	CherTreshold = 0 #We assume to detect single Cherenkov p.e.
	LongScinMaxFiber = max(list(LongVectorSignals)) #maximum energy deposit in LONG scintillating fibers
	LongCherMaxFiber = max(list(LongVectorSignalsCher)) #maximum Cherenkov p.e. in LONG clear fibers
	ShortScinMaxFiber = max(list(ShortVectorSignals)) #maximum energy deposit in SHORT scintillating fibers
	ShortCherMaxFiber = max(list(ShortVectorSignalsCher)) #maximum Cherenkov p.e. in SHORT clear fibers
	NumFibers = 1058*4 #number of fibers (Cherenkov+Scintillating (long+short)) 
	NumModules = 1 #number of modules

	#Fill containers with energy reconstruction
	longscinenerec.append(longcalibscin_comp*sum(LongVectorSignals))
	longcherenerec.append(longcalibcher_comp*sum(LongVectorSignalsCher))
	shortscinenerec.append(shortcalibscin_comp*sum(ShortVectorSignals))
	shortcherenerec.append(shortcalibcher_comp*sum(ShortVectorSignalsCher))
	longenerec.append((longscinenerec[Event]+longcherenerec[Event])/2)
	shortenerec.append((shortscinenerec[Event]+shortcherenerec[Event])/2)
	shortlongenerec.append((shortenerec[Event]+longenerec[Event])/2)
	enereclong_short.append(longenerec[Event]-shortenerec[Event])

	#Fill containers with C/S
	if sum(ShortVectorSignals) > 0. and sum(LongVectorSignals) > 0.:
		C_S_short.append(sum(ShortVectorSignalsCher)/sum(ShortVectorSignals))
		C_S_long.append(sum(LongVectorSignalsCher)/sum(LongVectorSignals))

	#Fill containers with signals
	LongScinSignal.append(sum(LongVectorSignals))
	LongCherSignal.append(sum(LongVectorSignalsCher))
	ShortScinSignal.append(sum(ShortVectorSignals))
	ShortCherSignal.append(sum(ShortVectorSignalsCher))
	EnergyTotContainer.append(EnergyTot)

	#Add calibration constants
	longcalibscin += sum(LongVectorSignals)
	longcalibcher += sum(LongVectorSignalsCher)
	shortcalibscin += sum(ShortVectorSignals)
	shortcalibcher += sum(ShortVectorSignalsCher) 

#Compute calibration constants
tree.GetEntry(0)
PrimaryParticleEnergy = tree.PrimaryParticleEnergy #need it to complete calibration constants
NofEventsProcessed = int(NofEventsProcessed)
longcalibscin = longcalibscin/NofEventsProcessed
longcalibcher = longcalibcher/NofEventsProcessed
shortcalibcher = shortcalibcher/NofEventsProcessed
shortcalibscin = shortcalibscin/NofEventsProcessed
longcalibscin = PrimaryParticleEnergy/longcalibscin
longcalibcher = PrimaryParticleEnergy/longcalibcher
shortcalibscin = PrimaryParticleEnergy/shortcalibscin
shortcalibcher = PrimaryParticleEnergy/shortcalibcher

print "Calibration-> Long scin " + str(longcalibscin) + "MeV/MeV" + " Long cher "+ str(longcalibcher) + "MeV/p.e.\n"
print "Calibration-> Short Scin" + str(shortcalibscin) + "MeV/MeV" + " Short cher "+ str(shortcalibcher) + "MeV/p.e.\n"

#Print statistics over all event
StaggeredROOTHistograms.create_histograms(PrimaryParticleName, LongScinSignal,
	LongCherSignal, ShortScinSignal, ShortCherSignal, max(LongScinSignal),
	max(LongCherSignal), max(ShortScinSignal), max(ShortCherSignal),
	EnergyTotContainer, max(EnergyTotContainer))

StaggeredROOTHistograms.create_energyhistograms(PrimaryParticleName, longscinenerec, longcherenerec,
	shortscinenerec, shortcherenerec, shortenerec, longenerec, shortlongenerec, C_S_short, C_S_long,
	enereclong_short)

#Print scatter plots of a single event
tree.GetEntry(0)

#Set values of tree
PrimaryParticleName = tree.PrimaryParticleName # MC truth: primary particle Geant4 name
PrimaryParticleEnergy = tree.PrimaryParticleEnergy # MC truth: primary particle energy
EnergyTot = tree.EnergyTot # Total energy deposited in calorimeter
Energyem = tree.Energyem # Energy deposited by the em component
EnergyScin = tree.EnergyScin # Energy deposited in Scin fibers (not Birk corrected)
EnergyCher = tree.EnergyCher # Energy deposited in Cher fibers (not Birk corrected)
NofCherenkovDetected = tree.NofCherenkovDetected # Total Cher p.e. detected
LongVectorSignals = tree.LongVectorSignals # Vector of energy deposited in LONG Scin fibers (Birk corrected)
LongVectorSignalsCher = tree.LongVectorSignalsCher # Vector of Cher p.e. detected in LONG Cher fibers
ShortVectorSignals = tree.ShortVectorSignals # Vector of energy deposited in SHORT Scin fibers (Birk corrected)
ShortVectorSignalsCher = tree.ShortVectorSignalsCher # Vector of energy deposited in SHORT Cher fibers 

print "--------------------------------------------------------\n"
print "Processing event " + str(Event) + " of " + str(NofEventsProcessed) + ": " + PrimaryParticleName + " energy " + str(PrimaryParticleEnergy) + " MeV" +"\n"

#Set analysis and event parameters and create root histograms
ScinTreshold = 0.03 #30 KeV, energy treshold for single photoelectron production
CherTreshold = 0 #We assume to detect single Cherenkov p.e.
LongScinMaxFiber = max(list(LongVectorSignals)) #maximum energy deposit in LONG scintillating fibers
LongCherMaxFiber = max(list(LongVectorSignalsCher)) #maximum Cherenkov p.e. in LONG clear fibers
ShortScinMaxFiber = max(list(ShortVectorSignals)) #maximum energy deposit in SHORT scintillating fibers
ShortCherMaxFiber = max(list(ShortVectorSignalsCher)) #maximum Cherenkov p.e. in SHORT clear fibers
NumFibers = 1058*4 #number of fibers (Cherenkov+Scintillating (long+short)) 
NumModules = 1 #number of modules

#Print scatter plots with signals
StaggeredROOTHistograms.create_scatterplots(PrimaryParticleName, LongVectorSignals,
	LongVectorSignalsCher, ShortVectorSignals, ShortVectorSignalsCher,
	ScinTreshold, CherTreshold)

#Create folder result and move output file into
if not os.path.exists("result"):
	os.makedirs("result")
foldername = raw_input("Insert folder name (take care folder does not exist yet!): ")
foldername = "result/"+foldername
os.makedirs(str(foldername))
for eps_file in glob.iglob('*.eps'):
	shutil.move(eps_file, str(foldername))
for txt_file in glob.iglob('*.txt'):
	shutil.move(txt_file, str(foldername))
#---------------------------------------------------------------------------------------------------------