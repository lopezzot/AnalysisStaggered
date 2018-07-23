from ROOT import gStyle, TCanvas, TH1F, TH2F, TF1, gPad, TGraph, Fit
import Staggeredmap
import time

def create_scatterplots(PrimaryParticleName, LongVectorSignals, LongVectorSignalsCher,
	ShortVectorSignals, ShortVectorSignalsCher, ScinTreshold,
	CherTreshold):
	"""Function to perform scatter plots"""

	#Set ROOT plots
	TH2LongScinSignals = TH2F("LongScatterplotSignals", PrimaryParticleName, 46, 0., 93., 93, 0., 93.)
	TH2ShortScinSignals = TH2F("ShortScatterplotSignals", PrimaryParticleName, 46, 0., 93., 93, 0., 93.)
	TH2LongCherSignals = TH2F("LongCherScatterplotSignals", PrimaryParticleName, 46, 0., 93., 92, 0., 93.)
	TH2ShortCherSignals = TH2F("ShortCherScatterplotSignals", PrimaryParticleName, 46, 0., 93., 92, 0., 93.)
	TH2Uniformity = TH2F("Uniformity", "Uniformity", 46, 0., 93., 92, 0., 93.)

	#Fill plots in for loop
	for index in range(len(LongVectorSignals)):
		if LongVectorSignals[index] > ScinTreshold:
			X,Y = Staggeredmap.mapXYLongScin(index)
			TH2LongScinSignals.Fill(X,Y,LongVectorSignals[index])
		if LongVectorSignalsCher[index] > CherTreshold:
			X,Y = Staggeredmap.mapXYLongCherenkov(index)
			TH2LongCherSignals.Fill(X,Y,LongVectorSignalsCher[index])
		if ShortVectorSignals[index] > ScinTreshold:
			X,Y = Staggeredmap.mapXYShortScin(index)
			TH2ShortScinSignals.Fill(X,Y, ShortVectorSignals[index])
		if ShortVectorSignalsCher[index] > CherTreshold:
			X,Y = Staggeredmap.mapXYShortCherenkov(index)
			TH2ShortCherSignals.Fill(X,Y, ShortVectorSignalsCher[index])

	#Fill uniformity plot
	for index in range(len(LongVectorSignals)):
		X,Y = Staggeredmap.mapXYLongScin(index)
		TH2Uniformity.Fill(X,Y,1.)	
		X,Y = Staggeredmap.mapXYShortScin(index)
		TH2Uniformity.Fill(X,Y,1.)
		X,Y = Staggeredmap.mapXYLongCherenkov(index)
		TH2Uniformity.Fill(X,Y,1.)
		X,Y = Staggeredmap.mapXYShortCherenkov(index)
		TH2Uniformity.Fill(X,Y,1.)

	#Draw + DrawOptions plots
	Style = gStyle
	Style.SetPalette(1) #Root palette style
	Style.SetOptStat(0) #Do not show statistics
	TH2LongScinSignals.SetLineWidth(0) #TH2LongScinSignals #No line width
	TH2LongScinSignals.SetLineColor(2)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2LongScinSignals.GetXaxis()
	XAxis.SetTitle("x (mm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2LongScinSignals.GetYaxis()
	YAxis.SetTitle("y (mm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2LongScinSignals.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2LongScinSignals.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageLongScintillation.eps")
	TH2ShortScinSignals.SetLineWidth(0) #TH2ShortScinSignals #No line width
	TH2ShortScinSignals.SetLineColor(2)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2ShortScinSignals.GetXaxis()
	XAxis.SetTitle("x (mm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2ShortScinSignals.GetYaxis()
	YAxis.SetTitle("y (mm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2ShortScinSignals.GetZaxis()
	ZAxis.SetTitle("Energy (MeV)")
	ZAxis.SetTitleOffset(1.4)
	TH2ShortScinSignals.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageShortScintillation.eps")
	TH2ShortCherSignals.SetLineWidth(0) #TH2ShortCherSignals #No line width
	TH2ShortCherSignals.SetLineColor(4)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2ShortCherSignals.GetXaxis()
	XAxis.SetTitle("x (mm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2ShortCherSignals.GetYaxis()
	YAxis.SetTitle("y (mm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2ShortCherSignals.GetZaxis()
	ZAxis.SetTitle("Cher p.e.")
	ZAxis.SetTitleOffset(1.4)
	TH2ShortCherSignals.Draw("LEGO2Z 0 FB")
	gPad.SaveAs("ImageShortCherenkov.eps")
	TH2LongCherSignals.SetLineWidth(0) #TH2LongCherSignals #No line width
	TH2LongCherSignals.SetLineColor(4)
	XAxis = TH2LongCherSignals.GetXaxis()
	XAxis.SetTitle("x (mm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2LongCherSignals.GetYaxis()
	YAxis.SetTitle("y (mm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2LongCherSignals.GetZaxis()
	ZAxis.SetTitle("Cher p.e.")
	ZAxis.SetTitleOffset(1.4)
	TH2LongCherSignals.Draw("LEGO2Z FB 0")
	gPad.SaveAs("ImageLongCherenkov.eps")
	TH2Uniformity.SetLineWidth(0) #TH2Uniformity #No line width
	TH2Uniformity.SetLineColor(2)
	#TH2Signals.SetFillColorAlpha(2, 0.)
	XAxis = TH2Uniformity.GetXaxis()
	XAxis.SetTitle("x (mm)")
	XAxis.CenterTitle()
	XAxis.SetTitleOffset(1.8)
	YAxis = TH2Uniformity.GetYaxis()
	YAxis.SetTitle("y (mm)")
	YAxis.CenterTitle()
	YAxis.SetTitleOffset(1.8)
	ZAxis = TH2Uniformity.GetZaxis()
	ZAxis.SetTitle("Set to 1")
	ZAxis.SetTitleOffset(1.4)
	TH2Uniformity.Draw("LEGO2Z 0 FB")
	#gPad.SaveAs("ImageUniformity.eps")

def create_histograms(PrimaryParticleName, LongVectorSignals, LongVectorSignalsCher,
	ShortVectorSignals, ShortVectorSignalsCher, LongScinMaxFiber, LongCherMaxFiber, 
	ShortScinMaxFiber, ShortCherMaxFiber, EnergyTotContainer, MaxEnergyTotContainer):
	"""Function to perform histograms"""

	#Set ROOT histograms
	TH1LongScin = TH1F("LongScintillation", PrimaryParticleName, 100, 0.0, LongScinMaxFiber+200.)
	TH1LongCher = TH1F("LongCherenkov", PrimaryParticleName, 100, 0.0, LongCherMaxFiber+200.)
	TH1ShortScin = TH1F("ShortScintillation", PrimaryParticleName, 100, 0.0, ShortScinMaxFiber+200.)
	TH1ShortCher = TH1F("ShortCherenkov", PrimaryParticleName, 100, 0.0, ShortCherMaxFiber+200.)
	TH1EnergyTot = TH1F("EnergyTot", PrimaryParticleName, 100, MaxEnergyTotContainer-10000., MaxEnergyTotContainer+500.) 

	#Fill histograms in for loop
	for index in range(len(LongVectorSignals)):
		TH1LongScin.Fill(LongVectorSignals[index])
		TH1LongCher.Fill(LongVectorSignalsCher[index])
		TH1ShortScin.Fill(ShortVectorSignals[index])
		TH1ShortCher.Fill(ShortVectorSignalsCher[index])
		TH1EnergyTot.Fill(EnergyTotContainer[index])

	#Draw + DrawOptions
	Style = gStyle
	Style.SetOptStat(1) #Show statistics
	Style.SetLineWidth(1)
	XAxis = TH1LongScin.GetXaxis()  #TH1LongScin
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1LongScin.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1LongScin.Draw()
	gPad.SaveAs("EnergyLongScin.eps")
	XAxis = TH1LongCher.GetXaxis() #TH1LongCher
	XAxis.SetTitle("# Cher p.e.")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1LongCher.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1LongCher.Draw()
	gPad.SaveAs("CherpeLong.eps")
	XAxis = TH1ShortScin.GetXaxis() #TH1ShortScin
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1ShortScin.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1ShortScin.Draw()
	gPad.SaveAs("EnergyShortScin.eps")
	XAxis = TH1ShortCher.GetXaxis() #TH1ShortCher
	XAxis.SetTitle("# Cher p.e.")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1ShortCher.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1ShortCher.Draw()
	gPad.SaveAs("CherpeShort.eps")
	XAxis = TH1EnergyTot.GetXaxis() #TH1EnergyTot
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1EnergyTot.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1EnergyTot.Draw()
	gPad.SaveAs("EnergyTot.eps")

def create_energyhistograms(PrimaryParticleName, LongEnergyScin, LongEnergyCher,
	ShortEnergyScin, ShortEnergyCher, ShortEnergy, LongEnergy, LongShortEnergy,
	C_S_short, C_S_long, enereclong_short):
	"""Function to perform histograms"""

	#Set ROOT histograms
	TH1LongScin = TH1F("LongEnergyScin", PrimaryParticleName, 100, 0.0, max(LongEnergyScin)+200.)
	TH1LongCher = TH1F("LongEnergyCher", PrimaryParticleName, 100, 0.0, max(LongEnergyCher)+200.)
	TH1ShortScin = TH1F("ShortEnergyScin", PrimaryParticleName, 100, 0.0, max(ShortEnergyScin)+200.)
	TH1ShortCher = TH1F("ShortEnergyCher", PrimaryParticleName, 100, 0.0, max(ShortEnergyCher)+200.)
	TH1Short = TH1F("ShortEnergy", PrimaryParticleName, 100, 0.0, max(ShortEnergy)+200.)
	TH1Long = TH1F("LongEnergy", PrimaryParticleName, 100, 0.0, max(LongEnergy)+200.)
	TH1LongShort = TH1F("LongShortEnergy", PrimaryParticleName, 100, 0.0, max(LongShortEnergy)+200.) 
	TH1CSShort = TH1F("C/SShort", PrimaryParticleName, 100, 0.0, max(C_S_short)+3.)
	TH1CSLong = TH1F("C/SLong", PrimaryParticleName, 100, 0.0, max(C_S_long)+3.)
	TH1Long_Short = TH1F("Long-Short", PrimaryParticleName, 100, 0.0, max(enereclong_short)+200.)

	#Fill histograms in for loop
	for index in range(len(LongEnergyScin)):
		TH1LongScin.Fill(LongEnergyScin[index])
		TH1LongCher.Fill(LongEnergyCher[index])
		TH1ShortScin.Fill(ShortEnergyScin[index])
		TH1ShortCher.Fill(ShortEnergyCher[index])
		TH1Short.Fill(ShortEnergy[index])
		TH1Long.Fill(LongEnergy[index])
		TH1LongShort.Fill(LongShortEnergy[index])
		TH1CSShort.Fill(C_S_short[index])
		TH1CSLong.Fill(C_S_long[index])
		TH1Long_Short.Fill(enereclong_short[index])

	#Draw + DrawOptions
	Style = gStyle
	Style.SetOptStat(1) #Show statistics
	Style.SetLineWidth(1)
	XAxis = TH1LongScin.GetXaxis()  #TH1LongScin
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1LongScin.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1LongScin.Draw()
	gPad.SaveAs("EnergyRecLongScin.eps")
	XAxis = TH1LongCher.GetXaxis() #TH1LongCher
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1LongCher.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1LongCher.Draw()
	gPad.SaveAs("EnergyRecLongCher.eps")
	XAxis = TH1ShortScin.GetXaxis() #TH1ShortScin
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1ShortScin.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1ShortScin.Draw()
	gPad.SaveAs("EnergyRecShortScin.eps")
	XAxis = TH1ShortCher.GetXaxis() #TH1ShortCher
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1ShortCher.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1ShortCher.Draw()
	gPad.SaveAs("EnergyRecShortCher.eps")
	XAxis = TH1Short.GetXaxis() #TH1Short
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1Short.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1Short.Draw()
	gPad.SaveAs("EnergyRecShort.eps")
	XAxis = TH1Long.GetXaxis() #TH1Long
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1Long.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1Long.Draw()
	gPad.SaveAs("EnergyRecLong.eps")
	XAxis = TH1LongShort.GetXaxis() #TH1LongShort
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1LongShort.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1LongShort.Draw()
	gPad.SaveAs("EnergyRecLongShort.eps")
	XAxis = TH1CSShort.GetXaxis() #TH1CSShort
	XAxis.SetTitle("C/S (C p.e./MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1CSShort.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1CSShort.Draw()
	gPad.SaveAs("C_SShort.eps")
	XAxis = TH1CSLong.GetXaxis() #TH1CSLong
	XAxis.SetTitle("C/S (C p.e./MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1CSLong.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1CSLong.Draw()
	gPad.SaveAs("C_SLong.eps")
	XAxis = TH1Long_Short.GetXaxis() #TH1Long_Short
	XAxis.SetTitle("Energy (MeV)")
	XAxis.SetTitleOffset(1.2)
	YAxis = TH1Long_Short.GetYaxis()
	YAxis.SetTitle("Entries")
	TH1Long_Short.Draw()
	gPad.SaveAs("Long_Short.eps")