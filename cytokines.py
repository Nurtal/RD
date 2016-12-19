"""
work on cytokines data
unstructured file
have to dispatch functions
"""

import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from analysis import *

import matplotlib.pyplot as plt

from preprocessing import *

import scipy.stats as stats

def CreateMatrix():
	"""
	IN PROGRESS

	scan raw data and Create a matrix
	without NA

	TODO:
		- write doc
	"""

	# catch header line
	cytokineFile = open("DATA/CYTOKINES/clinical_i2b2trans.txt")
	listOfPatient = []
	cmpt = 0
	for line in cytokineFile:
		if(cmpt == 0):
			headerLine = line
	cytokineFile.close()



	# Store variables in a list of variables
	listOfVariable = []
	headerLineInArray = headerLine.split("\n")
	headerLineInArray = headerLineInArray[0]
	headerLineInArray = headerLineInArray.split("\t")
	indexInHeader = 0
	for element in headerLineInArray:
		variable = []
		cytokineFile = open("DATA/CYTOKINES/clinical_i2b2trans.txt")
		listOfPatient = []
		cmpt = 0
		for line in cytokineFile:
			if(cmpt == 0):
				headerLine = line
			else:
				patient = line
				patientInArray = patient.split("\n")
				patientInArray = patientInArray[0]
				patientInArray = patientInArray.split("\t")
				variable.append(patientInArray[indexInHeader])
			cmpt = cmpt +1
		cytokineFile.close()
		listOfVariable.append(variable)
		indexInHeader = indexInHeader + 1

	# Check Variable
	# ne retient pas les variables contenant des "N.A"
	listOfVariable_checked = []
	indexInlistOfVariable = 0
	for variable in listOfVariable:
		passCheck = 1
		for value in variable:

			"""
			if("NA" in value):
				passCheck = 0
			if("Unknown" in value):
				passCheck = 0
			"""

		if(passCheck):
			listOfVariable_checked.append(indexInlistOfVariable)
		indexInlistOfVariable = indexInlistOfVariable + 1


	# Ecriture des donnees filtrees dans un nouveau fichier
	matrixFile = open("DATA/CYTOKINES/matrix.csv", "w")
	rawDataFile = open("DATA/CYTOKINES/clinical_i2b2trans.txt")

	for line in rawDataFile:
		lineToWrite = ""
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0]
		lineInArray = lineInArray.split("\t")
		
		indexInRawData = 0
		for element in lineInArray:
			element = element.replace(" ", "")
			if(indexInRawData in listOfVariable_checked):
				lineToWrite = lineToWrite + element + ";"
			indexInRawData = indexInRawData + 1

		matrixFile.write(lineToWrite[:-1]+"\n")

	rawDataFile.close()
	matrixFile.close()


def extractBinaryMatrix():
	"""
	IN PROGRESS
	"""
	matrixData = open("DATA/CYTOKINES/matrix.csv", "r")
	# catch the binary variable
	listOfIndex = []
	for line in matrixData:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		index = 0 
		for element in lineInArray:
			if(element == "No" or element == "Yes" or element == "Male" or element == "Female"):
				
				if(index not in listOfIndex):
					listOfIndex.append(index)
			index = index + 1
	matrixData.close()

	matrixData = open("DATA/CYTOKINES/matrix.csv", "r")
	newMatrix = open("DATA/CYTOKINES/binaryMatrix.csv", "w")
	for line in matrixData:
		lineToWrite = ""
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		index = 0
		for element in lineInArray:
			if(index in listOfIndex):
				if(element == "No" or element == "Female"):
					element = 0
				elif(element == "Yes" or element == "Male"):
					element = 1
				lineToWrite = lineToWrite + str(element) + ";"
			index = index + 1
		newMatrix.write(lineToWrite[:-1]+"\n")

	newMatrix.close()
	matrixData.close()



def extractQuantitativeMatrix():
	"""
	IN PROGRESS
	"""


	matrixData = open("DATA/CYTOKINES/matrix.csv", "r")
	# catch the binary variable
	listOfIndex = []
	for line in matrixData:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		index = 0 
		for element in lineInArray:
			isQuantitative = 1
			try:
				float(element)
			except:
				isQuantitative = 0
			if(isQuantitative):
				if(index not in listOfIndex and index != 0):
					listOfIndex.append(index)
			index = index + 1
	matrixData.close()

	matrixData = open("DATA/CYTOKINES/matrix.csv", "r")
	newMatrix = open("DATA/CYTOKINES/quantitativeMatrix.csv", "w")
	for line in matrixData:
		lineToWrite = ""
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		index = 0
		for element in lineInArray:
			if(index in listOfIndex):
				lineToWrite = lineToWrite + str(element) + ";"
			index = index + 1	
		newMatrix.write(lineToWrite[:-1]+"\n")

	newMatrix.close()
	matrixData.close()


def AssembleMatrixFromFile():
	"""
	IN PROGRESS
	"""

	# assemble une numpy matrix
	matrixFile = open("DATA/CYTOKINES/quantitativeMatrix.csv", "r")
	cohorte = []
	cmpt = 0
	LuminexVariableIndex = []

	numberOfNa = 0

	for line in matrixFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")

		if(cmpt == 0):
			indexInHeader = 0
			for param in lineInArray:
				if("Luminex" in param):
					LuminexVariableIndex.append(indexInHeader)
				indexInHeader += 1

		elif(cmpt != 0):
			patient = []
			indexInPatient = 0
			for value in lineInArray:
				try:
					float(value)
					patient.append(float(value))
				except:
					# Set NA mesure to 0 for Luminex Variable
					if(indexInPatient in LuminexVariableIndex):
						patient.append(0.0)
						numberOfNa += 1
					else:
						patient.append(np.nan)
				indexInPatient += 1
			cohorte.append(patient)
		cmpt = cmpt + 1
	matrixFile.close()

	# Imputation on NaN Values
	imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
	X = cohorte
	imp.fit(X)
	print(imp.transform(X))
	data = imp.transform(X)


	# compute % of na in Luminex

	score = float( float(numberOfNa) / (float(cmpt) * float(len(LuminexVariableIndex)))*100)

	print "=> " +str(score)


	return data


def get_discreteLabel():
	"""
	IN PROGRESS
	"""

	# catch index of the label
	rawData = open("DATA/CYTOKINES/matrix.csv", "r")
	label = "\\Clinical\\Demography\\SEX"
	cmpt = 0
	index_label = "undef"
	for line in rawData:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		if(cmpt == 0):
			index = 0
			for param in lineInArray:
				if(param == label):
					index_label = index
				index = index + 1
		cmpt = cmpt + 1
	rawData.close()

	# catch label value
	labelValues = []
	rawData = open("DATA/CYTOKINES/matrix.csv", "r")
	cmpt = 0
	for line in rawData:
		if(cmpt != 0):
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")
			labelValues.append(lineInArray[index_label])
		cmpt = cmpt + 1
	rawData.close()

	# discretization
	# specific to gender
	discreteLabel = []
	for element in labelValues:
		if(element == "Male"):
			element = 1
		if(element == "Female"):
			element = 0
		discreteLabel.append(element)
	return discreteLabel


def filter_outlier(data):
	"""
	IN PROGRESS
	"""
	cohorte = np.array(data)
	firstCount = len(cohorte)
	cmpt = 0
	variables = data.transpose()
	index_variable = 0
	VariableIndexToThresholds = {}
	for variable in variables:
		Threshold = {}
		description = stats.describe(variable)
		mean = description[2]
		variance = description[3]
		ecartType = sqrt(variance)
		minimum = mean - 5*ecartType
		maximum = mean + 5*ecartType
		Threshold["max"] = maximum
		Threshold["min"] = minimum
		VariableIndexToThresholds[index_variable] = Threshold
		index_variable = index_variable + 1


	newCohorte = []
	for patient in cohorte:
		cmpt = 0
		passCheck = 1
		for scalar in patient:
			Thresholds = VariableIndexToThresholds[cmpt]
			maximum = Thresholds["max"]
			minimum = Thresholds["min"]
			if(scalar > maximum or scalar < minimum):
				passCheck = 0
			cmpt += 1
		if(passCheck):
			newCohorte.append(patient)

	data = np.array(newCohorte)
	secondCount =len(data)

	print str(firstCount) + " || " + str(secondCount)
	return data


def plot_explainedVariance(cohorte):
	"""
	IN PROGRESS
	"""
	#Explained variance
	pca = PCA().fit(cohorte)
	plt.plot(np.cumsum(pca.explained_variance_ratio_))
	plt.xlabel('number of components')
	plt.ylabel('cumulative explained variance')
	plt.show()



def show_biplot(cohorte, labels=None):
	"""
	IN PROGRESS

	-WARNING: use matplotlib.mlab PCA

	"""
	from matplotlib.mlab import PCA as mPCA

	plt.xlim(-1,1)
	plt.ylim(-1,1)
	plt.xlabel("PC{}".format(1))
	plt.ylabel("PC{}".format(2))
	plt.grid()

	pca=mPCA(cohorte)

	score = pca.Y[:,0:2]
	coeff = pca.Wt[:,0:2]
	xs = score[:,0]
	ys = score[:,1]
	n=coeff.shape[0]
	scalex = 1.0/(xs.max()- xs.min())
	scaley = 1.0/(ys.max()- ys.min())
	plt.scatter(xs*scalex,ys*scaley)
	for i in range(n):
		plt.arrow(0, 0, coeff[i,0], coeff[i,1],color='r',alpha=0.5)
		if labels is None:
			plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color='g', ha='center', va='center')
		else:
			plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color='g', ha='center', va='center')
	plt.show()


"""TEST SPACE"""

# Create Data
#CreateMatrix()
#extractBinaryMatrix()
#extractQuantitativeMatrix()
data = AssembleMatrixFromFile()
data = preprocessing.robust_scale(data)
cohorte = filter_outlier(data)

#y = get_discreteLabel()


matrix_cleaned = open("DATA/CYTOKINES/myTestMatrix.csv", "w")
# write header
input_matrix = open("DATA/CYTOKINES/quantitativeMatrix.csv", "r")
cmpt = 0
for line in input_matrix:
	if(cmpt == 0):
		header = ""
		for param in line:
			header = str(param) + ","
		matrix_cleaned.write(header[:-1]+"\n")
	cmpt += 1
input_matrix.close()


for patient in cohorte:
	lineToWrite = ""
	for scalar in patient:
		lineToWrite = lineToWrite + str(scalar) +","
	matrix_cleaned.write(str(lineToWrite[:-1])+"\n")
matrix_cleaned.close()

# Perform PCA
pca = PCA()
pca.fit(cohorte)
plot_explainedVariance(cohorte)
cohorteInNewSpace = pca.fit_transform(cohorte)

# keep only the first 10 parameters
cohorte_reduced = []
for patient in cohorteInNewSpace:
	newPatient = patient[:10]
	cohorte_reduced.append(newPatient)
cohorte_reduced = np.array(cohorte_reduced)

quickClustering(cohorte_reduced, 4, "cytokineTest.png")
#quickPCA(cohorte_reduced, y, ["Male","Female"], "2d", "cytokinesPcaTest.png", 1, 1)
show_biplot(cohorte_reduced)
