import math

def mapXYShortCherenkov(index):
	"""Function to return X Y of Short Cherenkov fibers"""
	row = index//23
	column = index - ((index//23)*23)
	X = 0.5 + 0.5 + 4*column
	Y = 0.5 + 0.5 + 2*row
	return X,Y

def mapXYLongCherenkov(index):
	"""Function to return X Y of Long Chernekov fibers"""
	row = index//23
	column = index - ((index//23)*23)
	X = 2.5 + 0.5 + 4*column
	Y = 0.5 + 0.5 + 2*row
	return X,Y

def mapXYShortScin(index):
	"""Function to return X Y of Short Scintillating fibers"""
	row = index//23
	column = index - ((index//23)*23)
	X = 1.5 + 0.5 + 4*column
	Y = 1.5 + 0.5 + 2*row
	return X,Y

def mapXYLongScin(index):
	"""Function to return X Y of Long Scintillating fibers"""
	row = index//23
	column = index - ((index//23)*23)
	X = 3.5 + 0.5 + 4*column
	Y = 1.5 + 0.5 + 2*row
	return X,Y
