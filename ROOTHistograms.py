from ROOT import gStyle, TCanvas, TH1F, TH2F, TF1, gPad, TGraph, Fit
import map
import mapgroup

def create_firstroothistograms(PrimaryParticleName, VectorSignals, VectorSignalsCher, 
	GroupedVectorSignals, GroupedVectorSignalsCher, ScinTreshold, 
	CherTreshold, ScinMaxFiber, CherMaxFiber, NumFibers, NumModules):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH2Signals = TH2F("ScatterplotSignals",PrimaryParticleName,71*8,1.2*0,1.2*71,71*8,1.2*0,1.2*71)
	TH2SignalsGrouped = TH2F("ScatterplotSignalsGrouped",PrimaryParticleName,71,1.2*0,1.2*71,71,1.2*0,1.2*71)
	TH2SignalsCher = TH2F("ScatterplotSignalsCher",PrimaryParticleName,71*8,0.0*71,1.2*71,71*8,0.0*71,1.2*71)
	TH2SignalsCherGrouped = TH2F("ScatterplotSignalsCherGrouped",PrimaryParticleName,71,1.2*0,1.2*71,71,1.2*0,1.2*71)
	TH1Signals = TH1F("Scintillation",PrimaryParticleName,100,0.0,ScinMaxFiber+200.0)
	TH1SignalsCher = TH1F("Cherenkov",PrimaryParticleName,100,0.0,CherMaxFiber+5)

	#Fill histograms in for loop
	for fiberindex in range(NumFibers):
		X,Y = map.mapXY(fiberindex)
		if VectorSignals[fiberindex] > ScinTreshold:
			TH2Signals.Fill(X,Y,VectorSignals[fiberindex])
			TH1Signals.Fill(VectorSignals[fiberindex])
		if VectorSignalsCher[fiberindex] > CherTreshold:
			TH2SignalsCher.Fill(X,Y,VectorSignalsCher[fiberindex])
			TH1SignalsCher.Fill(VectorSignalsCher[fiberindex])

	for moduleindex in range(NumModules):
		X,Y = mapgroup.mapgroupedXY(moduleindex)
		TH2SignalsGrouped.Fill(X,Y,GroupedVectorSignals[moduleindex])
		TH2SignalsCherGrouped.Fill(X,Y,GroupedVectorSignalsCher[moduleindex])
	    
	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetPalette(1) #Root palette style
	Style.SetOptStat(0) #Do not show statistics
	TH2Signals.SetLineWidth(0) #TH2Signals #No line width
	TH2Signals.SetLineColor(2)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2Signals.GetXaxis()
	XAxis.SetTitle("x (cm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2Signals.GetYaxis()
	YAxis.SetTitle("y (cm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2Signals.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2Signals.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageScintillation.eps")
	TH2SignalsGrouped.SetLineWidth(0) #TH2GroupedSignals #No line width
	TH2SignalsGrouped.SetLineColor(2)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2SignalsGrouped.GetXaxis()
	XAxis.SetTitle("x (cm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2SignalsGrouped.GetYaxis()
	YAxis.SetTitle("y (cm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2SignalsGrouped.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2SignalsGrouped.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageScintillationGrouped.eps")
	TH2SignalsCherGrouped.SetLineWidth(0) #TH2GroupedCherSignals #No line width
	TH2SignalsCherGrouped.SetLineColor(4)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2SignalsCherGrouped.GetXaxis()
	XAxis.SetTitle("x (cm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2SignalsCherGrouped.GetYaxis()
	YAxis.SetTitle("y (cm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2SignalsCherGrouped.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2SignalsCherGrouped.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageCherenkovGrouped.eps")
	TH2SignalsCher.SetLineWidth(0) #TH2SignalsCher #No line width
	TH2SignalsCher.SetLineColor(4)
	XAxis = TH2SignalsCher.GetXaxis()
	XAxis.SetTitle("x (cm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2SignalsCher.GetYaxis()
	YAxis.SetTitle("y (cm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2SignalsCher.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2SignalsCher.Draw("LEGO2Z FB 0")
	gPad.SaveAs("ImageCherenkov.eps")
	Style.SetLineWidth(1) #TH1Signals
	Style.SetOptStat(1) #Show statistics
	gPad.SetLogy()
	gPad.SetLogx()
	XAxis = TH1Signals.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1Signals.GetYaxis()
	YAxis.SetTitle("# fibers")
	TH1Signals.Draw()
	gPad.SaveAs("EnergyFibers.eps")
	XAxis = TH1SignalsCher.GetXaxis() #TH1SignalsCher
	XAxis.SetTitle("# Cher p.e.")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1SignalsCher.GetYaxis()
	YAxis.SetTitle("# fibers")
	TH1SignalsCher.Draw()
	gPad.SaveAs("CherpeFibers.eps")

def create_secondroothistograms(traditionalreconstructedenergy, machinelearningreconstructedenergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1TraditionalEnergy = TH1F("DR Energy","",100,0.0, max(traditionalreconstructedenergy)+20000)
	TH1MLEnergy = TH1F("ML Energy","",100,0.0, max(machinelearningreconstructedenergy)+20000)

	#Set ROOT 2D histogram
	TH2FScatter = TH2F("", "", 100, 0.0, max(traditionalreconstructedenergy), 100, 0.0, max(machinelearningreconstructedenergy)) 

	#Fill histograms in for loop
	for Event in range(len(traditionalreconstructedenergy)):
		TH1TraditionalEnergy.Fill(traditionalreconstructedenergy[Event])
		TH1MLEnergy.Fill(machinelearningreconstructedenergy[Event])
		TH2FScatter.Fill(traditionalreconstructedenergy[Event], machinelearningreconstructedenergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1TraditionalEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1TraditionalEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1TraditionalEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1TraditionalEnergy.Draw()
	gPad.SaveAs("DREnergy.eps")
	XAxis = TH1MLEnergy.GetXaxis() #TH1SignalsCher
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1MLEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1MLEnergy.Draw()
	gPad.SaveAs("MLEnergy.eps")	
	Style.SetOptStat(0) #Dont shown statistics
	XAxis = TH2FScatter.GetXaxis() #TH2FScatter
	XAxis.SetTitle("DR Energy (MeV)")
	YAxis = TH2FScatter.GetYaxis()
	YAxis.SetTitle("ML Energy (MeV)")
	TH2FScatter.Draw("COLZ")
	gPad.SaveAs("ScatterEnergies.eps")

def create_thirdroothistograms(traditionalscinreconstructedenergy, machinelearningscinreconstructedenergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1TraditionalScinEnergy = TH1F("Scin Energy","",100,0.0, max(traditionalscinreconstructedenergy)+5000)
	TH1MLScinEnergy = TH1F("ML Scin Energy","",100,0.0, max(machinelearningscinreconstructedenergy)+5000)

	#Fill histograms in for loop
	for Event in range(len(traditionalscinreconstructedenergy)):
		TH1TraditionalScinEnergy.Fill(traditionalscinreconstructedenergy[Event])
		TH1MLScinEnergy.Fill(machinelearningscinreconstructedenergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1TraditionalEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1TraditionalScinEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1TraditionalScinEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1TraditionalScinEnergy.Draw()
	gPad.SaveAs("TraditionalScinEnergy.eps")
	XAxis = TH1MLScinEnergy.GetXaxis() #TH1SignalsCher
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1MLScinEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1MLScinEnergy.Draw()
	gPad.SaveAs("MLScinEnergy.eps")	

def create_fourthroothistograms(traditionalcherreconstructedenergy, machinelearningcherreconstructedenergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1TraditionalCherEnergy = TH1F("Cher Energy","",100,0.0, max(traditionalcherreconstructedenergy)+5000)
	TH1MLCherEnergy = TH1F("ML Cher Energy","",100,0.0, max(machinelearningcherreconstructedenergy)+5000)

	#Fill histograms in for loop
	for Event in range(len(traditionalcherreconstructedenergy)):
		TH1TraditionalCherEnergy.Fill(traditionalcherreconstructedenergy[Event])
		TH1MLCherEnergy.Fill(machinelearningcherreconstructedenergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1TraditionalCherEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1TraditionalCherEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1TraditionalCherEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1TraditionalCherEnergy.Draw()
	gPad.SaveAs("TraditionalCherEnergy.eps")
	XAxis = TH1MLCherEnergy.GetXaxis() #TH1SignalsCher
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1MLCherEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1MLCherEnergy.Draw()
	gPad.SaveAs("MLCherEnergy.eps")	

def create_fifthroothistograms(CombinedEnergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1CombinedEnergy = TH1F("Comb Energy","",100,0.0, max(CombinedEnergy)+5000)

	#Fill histograms in for loop
	for Event in range(len(CombinedEnergy)):
		TH1CombinedEnergy.Fill(CombinedEnergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1TraditionalCherEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1CombinedEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1CombinedEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1CombinedEnergy.Draw()
	gPad.SaveAs("CombinedEnergy.eps")

def create_sixthroothistograms(SecondCombinedEnergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1SecondCombinedEnergy = TH1F("Second Comb Energy","",100,0.0, max(SecondCombinedEnergy)+5000)

	#Fill histograms in for loop
	for Event in range(len(SecondCombinedEnergy)):
		TH1SecondCombinedEnergy.Fill(SecondCombinedEnergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1TraditionalCherEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1CombinedEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1CombinedEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1CombinedEnergy.Draw()
	gPad.SaveAs("SecondCombinedEnergy.eps")

def create_seventhroothistograms(secondmlreconstructedenergy, secondmlscinreconstructedenergy, secondmlcherreconstructedenergy):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1SMLEnergy = TH1F("Sec ML Energy","",100,0.0, max(secondmlreconstructedenergy)+5000)
	TH1SMLScinEnergy = TH1F("Sec ML Scin Energy","",100,0.0, max(secondmlscinreconstructedenergy)+5000)
	TH1SMLCherEnergy = TH1F("Sec ML Cher Energy","",100,0.0,max(secondmlcherreconstructedenergy)+5000)

	#Fill histograms in for loop
	for Event in range(len(secondmlreconstructedenergy)):
		TH1SMLEnergy.Fill(secondmlreconstructedenergy[Event])
		TH1SMLScinEnergy.Fill(secondmlscinreconstructedenergy[Event])
		TH1SMLCherEnergy.Fill(secondmlcherreconstructedenergy[Event])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1SMLEnergy
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1SMLEnergy.GetXaxis()
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1SMLScinEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1SMLScinEnergy.Draw()
	gPad.SaveAs("SecondMLEnergy.eps")
	XAxis = TH1SMLScinEnergy.GetXaxis() #TH1SMLScinEnergy
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1SMLScinEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1SMLScinEnergy.Draw()
	gPad.SaveAs("SecondMLScinEnergy.eps")	
	XAxis = TH1SMLCherEnergy.GetXaxis() #TH1SMLCherEnergy
	XAxis.SetTitle("Energy (MeV)")
	YAxis = TH1SMLCherEnergy.GetYaxis()
	YAxis.SetTitle("# events")
	TH1SMLCherEnergy.Draw()
	gPad.SaveAs("SecondMLCherEnergy.eps")

def create_eigthroothistogram(machinelearningscinreconstructedenergy, machinelearningcherreconstructedenergy):
	"""Function to perform ROOT histograms"""

	#Set ROOT 2D histogram
	TH2FMLScinCherEnergy = TH2F("", "", 100, 0.0, max(machinelearningscinreconstructedenergy), 100, 0.0, max(machinelearningcherreconstructedenergy)) 

	#Fill histogram in for loop
	for event in range(len(machinelearningscinreconstructedenergy)):
		TH2FMLScinCherEnergy.Fill(machinelearningscinreconstructedenergy[event], machinelearningcherreconstructedenergy[event])

	#Draw + Draw Options
	XAxis = TH2FMLScinCherEnergy.GetXaxis() #TH2FMLScinCherEnergy
	XAxis.SetTitle("ML Scin Energy (MeV)")
	YAxis = TH2FMLScinCherEnergy.GetYaxis()
	YAxis.SetTitle("ML Cher Energy (MeV)")
	TH2FMLScinCherEnergy.Draw("COLZ")
	gPad.SaveAs("ScatterMLScinCherEnergies.eps")

def create_ninethroothistogram(traditionalscinreconstructedenergy, traditionalcherreconstructedenergy):
	"""Function to perform ROOT histograms"""

	#Set ROOT 2D histogram
	TH2FScinCherEnergy = TH2F("", "", 100, 0.0, max(traditionalscinreconstructedenergy), 100, 0.0, max(traditionalcherreconstructedenergy)) 

	#Fill histogram in for loop
	for event in range(len(traditionalscinreconstructedenergy)):
		TH2FScinCherEnergy.Fill(traditionalscinreconstructedenergy[event], traditionalcherreconstructedenergy[event])

	#Draw + Draw Options
	XAxis = TH2FScinCherEnergy.GetXaxis() #TH2FScinCherEnergy
	XAxis.SetTitle("Scin Energy (MeV)")
	YAxis = TH2FScinCherEnergy.GetYaxis()
	YAxis.SetTitle("Cher Energy (MeV)")
	TH2FScinCherEnergy.Draw("COLZ")
	gPad.SaveAs("ScatterScinCherEnergies.eps")

def create_graph(Fastscinenergy, Fastcherenergy, Scinenergy, Cherenergy, fem, PrimaryParticleEnergy):
	"""Function to perform ROOT graphs and compute he values"""

	#Graph points
	n = len(Fastscinenergy)

	TGraphfasthescin = TGraph(n, fem, Fastscinenergy)
	TGraphfasthecher = TGraph(n, fem, Fastcherenergy)
	TGraphhescin = TGraph(n, fem, Scinenergy)
	TGraphhecher = TGraph(n, fem, Cherenergy)

	#Draw + DrawOptions, Fit + parameter estimation
	Style = gStyle
	XAxis = TGraphfasthescin.GetXaxis() #TGraphfasthescin
	TGraphfasthescin.SetMarkerColor(4)
	TGraphfasthescin.SetMarkerStyle(20)
	TGraphfasthescin.SetMarkerSize(3)
	XAxis.SetTitle("fem")
	YAxis = TGraphfasthescin.GetYaxis()
	YAxis.SetTitle("Energy scin (MeV)")
	TGraphfasthescin.Fit("pol1")
	myfit = TGraphfasthescin.GetFunction("pol1")
	Fasthescin = myfit.GetParameter(0)/PrimaryParticleEnergy             
	TGraphfasthescin.Draw("AP")
	gPad.SaveAs("Fasthescin.eps")
	XAxis = TGraphfasthecher.GetXaxis() #TGraphfasthecher
	TGraphfasthecher.SetMarkerColor(4)
	TGraphfasthecher.SetMarkerStyle(20)
	TGraphfasthecher.SetMarkerSize(3)
	XAxis.SetTitle("fem")
	YAxis = TGraphfasthecher.GetYaxis()
	YAxis.SetTitle("Energy Cher (MeV)")
	TGraphfasthecher.Fit("pol1")
	myfit = TGraphfasthecher.GetFunction("pol1")
	Fasthecher = myfit.GetParameter(0)/PrimaryParticleEnergy  
	TGraphfasthecher.Draw("AP")
	gPad.SaveAs("Fasthecher.eps")
	XAxis = TGraphhescin.GetXaxis() #TGraphhescin
	TGraphhescin.SetMarkerColor(4)
	TGraphhescin.SetMarkerStyle(20)
	TGraphhescin.SetMarkerSize(3)
	XAxis.SetTitle("fem")
	YAxis = TGraphhescin.GetYaxis()
	YAxis.SetTitle("Energy scin (MeV)")
	TGraphhescin.Fit("pol1")
	myfit = TGraphhescin.GetFunction("pol1")
	hescin = myfit.GetParameter(0)/PrimaryParticleEnergy  
	TGraphhescin.Draw("AP")
	gPad.SaveAs("hescin.eps")
	XAxis = TGraphhecher.GetXaxis() #TGraphhecher
	TGraphhecher.SetMarkerColor(4)
	TGraphhecher.SetMarkerStyle(20)
	TGraphhecher.SetMarkerSize(3)
	XAxis.SetTitle("fem")
	YAxis = TGraphhecher.GetYaxis()
	YAxis.SetTitle("Energy cher (MeV)")
	TGraphhecher.Fit("pol1")
	myfit = TGraphhecher.GetFunction("pol1")
	hecher = myfit.GetParameter(0)/PrimaryParticleEnergy  
	TGraphhecher.Draw("AP")
	gPad.SaveAs("hecher.eps")

	return Fasthescin, Fasthecher, hescin, hecher

def create_fastroothistograms(vector, histogramtitle, xtitle, ytitle, histogramname):
	"""Function to perform ROOT histograms"""
	
	#Set ROOT histograms
	TH1Hist = TH1F(histogramtitle,"",100,0.0, max(vector)+int(max(vector)/3))

	#Fill histograms in for loop
	for entry in range(len(vector)):
		TH1Hist.Fill(vector[entry])

	#Draw + DrawOptions histograms		
	Style = gStyle
	Style.SetLineWidth(1) #TH1Hist
	Style.SetOptStat(1) #Show statistics
	XAxis = TH1Hist.GetXaxis()
	XAxis.SetTitle(xtitle)
	YAxis = TH1Hist.GetYaxis()
	YAxis.SetTitle(ytitle)
	TH1Hist.Draw()
	gPad.SaveAs(histogramname)
 

   


	

