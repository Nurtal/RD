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

import operator

from preprocessing import *

import scipy.stats as stats
import platform

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

	Drop the column PATIENT ID
	format and keep the OMIC ID

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


def AssembleMatrixFromFile(fileName):
	"""
	IN PROGRESS
	"""

	# assemble une numpy matrix
	matrixFile = open(fileName, "r")
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
	#print(imp.transform(X))
	data = imp.transform(X)


	# compute % of na in Luminex
	#score = float( float(numberOfNa) / (float(cmpt) * float(len(LuminexVariableIndex)))*100)
	#print "=> " +str(score)


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


def filter_outlier(data, delta):
	"""
	IN PROGRESS
	"""
	listOfFilterPatient = []
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
		minimum = mean - delta*ecartType
		maximum = mean + delta*ecartType
		Threshold["max"] = maximum
		Threshold["min"] = minimum
		VariableIndexToThresholds[index_variable] = Threshold
		index_variable = index_variable + 1

	newCohorte = []
	patientPositionInCohorte = 0
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
		else:
			listOfFilterPatient.append(patientPositionInCohorte)

		patientPositionInCohorte += 1
	data = np.array(newCohorte)
	secondCount =len(data)

	print str(firstCount) + " || " + str(secondCount)
	return (data, listOfFilterPatient)


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



def CreateIndexFile():
	"""
	-> Create an index file for patient in the
	   DATA folder.
	-> Format of the index file:
	   patientId;Diagnostic
	"""
	# Create index File for real Data
	# a few structure
	listOfPanel = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6","PANEL_7","PANEL_8","PANEL_9"]
	listOfPatientFiles = []
	for panel in listOfPanel:
		tmpList = glob.glob("DATA/"+panel+"/*.csv")
		for element in tmpList:
			if(element not in listOfPatientFiles):
				listOfPatientFiles.append(element)


	indexFile = open("DATA/patientIndex.csv", "w")
	listOfPatientId = []
	for patient in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientInArray = patient.split("/")
		elif(platform.system() == "Windows"):
			patientInArray = patient.split("\\")
		patientInArray = patientInArray[-1]
		patientInArray = patientInArray.split("_")
		patient_id = patientInArray[1]
		patient_diagnostic = patientInArray[0]
		if(patient_id not in listOfPatientId):
			indexFile.write(patient_id+";"+patient_diagnostic+"\n")
			listOfPatientId.append(patient_id)
	indexFile.close()



def format_OMICID():
	"""
	-> Format OMIC ID the matrix.csv file, rewrite
	   the file with a functionnal OMIC ID (i.e remove the "N"
	   	letter in the ID)
	-> WARNING: the OMIC ID can now be processed as a quantitave variable

	"""

	# copy the matrix file
	inputData = open("DATA/CYTOKINES/matrix.csv", "r")
	tmpData = open("DATA/CYTOKINES/matrix_tmp.csv", "w")
	for line in inputData:
		tmpData.write(line)
	inputData.close()
	tmpData.close()

	matrixData = open("DATA/CYTOKINES/matrix_tmp.csv", "r")
	matrixFormated = open("DATA/CYTOKINES/matrix.csv", "w")
	listOfIndex = []
	cmpt = 0
	id_index = "undef"
	for line in matrixData:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		index = 0
		if(cmpt == 0):
			index = 0
			for element in lineInArray:
				if("OMIC" in element):
					id_index = index
				index = index + 1
			matrixFormated.write(line)

		elif(id_index != "undef"):
			lineToWrite = ""
			indexInData = 0
			for scalar in lineInArray:

				if(indexInData != id_index):
					lineToWrite = lineToWrite + scalar + ";"
				
				else:
					OmicId = lineInArray[id_index]
					newOmicId = OmicId[1:]
					lineToWrite = lineToWrite + newOmicId + ";"

				indexInData +=1
			matrixFormated.write(lineToWrite[:-1]+"\n")
		cmpt +=1
	matrixFormated.close()
	matrixData.close()

	# remove tmp file
	os.remove("DATA/CYTOKINES/matrix_tmp.csv")




def PlotProcedure_fittingDisease_test():
	"""	
	-> Create a cohorte with the AssembleMatrixFromFile() function
	-> Create Dict IdToPositionInCohorte from the data . csv file
	   (in the exemple case: testData.csv)
	-> Create Dict patient id to diagnostic from index file 
	   (in the exemple case : patientIndex_test.csv)
	-> Split the cohorte, i.e create the Dict diagnostic to SubCohorte
	-> Use the different SubCohorte generated to plot the data


	TODO:
		- Adapt To real Data
		- Preprocessing cohorte
		- PCA on Cohorte

	"""

	# Split Cohorte according to Diagnostic
	listOfDiagnostic = ["sain", "malade", "autre"]

	cohorte = AssembleMatrixFromFile("DATA/CYTOKINES/testData.csv")

	# Get patient id and associated position in cohorte
	IdToPositionInCohorte = {}
	dataFile = open("DATA/CYTOKINES/testData.csv", "r")
	cmptInDataFile = 0
	indexOfID = "undef"
	position = 0
	for line in dataFile:
		if(cmptInDataFile == 0):
			indexInHeader = 0 
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")
			for param in lineInArray:
				if(param == "ID"): # ADAPT to REAL DATA
					indexOfID = indexInHeader
				indexInHeader += 1
		elif(indexOfID != "undef"):
			position += 1
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")

			IdToPositionInCohorte[lineInArray[indexOfID]] = position

		cmptInDataFile += 1
	dataFile.close()

	# get patient id to diagnostic from index file
	IdToDiagnostic = {}
	indexFile = open("DATA/CYTOKINES/patientIndex_test.csv", "r")
	for line in indexFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		IdToDiagnostic[lineInArray[0]] = lineInArray[1]
	indexFile.close()

	# Remove ID column from matrix
	new_cohorte = []
	for patient in cohorte:
		new_patient = []
		index = 0
		for scalar in patient:
			if(index != indexOfID):
				new_patient.append(scalar)
			index += 1
		new_cohorte.append(new_patient)
	cohorte = new_cohorte

	# Preprocessing Cohorte
	cohorte = preprocessing.robust_scale(cohorte)
	cohorte = filter_outlier(cohorte)

	# Perform PCA
	pca = PCA()
	pca.fit(cohorte)
	plot_explainedVariance(cohorte)
	cohorte = pca.fit_transform(cohorte)

	# Split cohorte
	DiagnosticToSubCohorte = {}
	for diagnostic in listOfDiagnostic:
		SubCohorte = []
		patientInSubCohorte = []
		for key in IdToDiagnostic.keys():
			if(IdToDiagnostic[key] == diagnostic):
				patientInSubCohorte.append(key)
		for key in IdToPositionInCohorte.keys():
			if(key in patientInSubCohorte):
				SubCohorte.append(cohorte[IdToPositionInCohorte[key]-1])
		DiagnosticToSubCohorte[diagnostic] = SubCohorte


	# Plot data point according to Diagnostic
	diagnosticToColor = {"sain":"b","malade":"r", "autre":"g"}
	diagnosticToSymbol = {"sain":"o","malade":"x", "autre":"x"}
	ax = plt.subplot(111, projection='3d')
	for diagnostic in DiagnosticToSubCohorte.keys():
		x = []
		y = []
		z = []
		for patient in DiagnosticToSubCohorte[diagnostic]:
			x.append(patient[0])
			y.append(patient[1])
			z.append(patient[2])
		ax.plot(x, y, z, diagnosticToSymbol[diagnostic], color=diagnosticToColor[diagnostic], label=diagnostic)
	plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0, 0))
	plt.show()





def PlotProcedure_fittingDisease():
	"""	
	-> Create a cohorte with the AssembleMatrixFromFile() function
	-> Create Dict IdToPositionInCohorte from the data . csv file
	   (in the exemple case: testData.csv)
	-> Create Dict patient id to diagnostic from index file 
	   (in the exemple case : patientIndex_test.csv)
	-> Split the cohorte, i.e create the Dict diagnostic to SubCohorte
	-> Use the different SubCohorte generated to plot the data

	"""

	# Split Cohorte according to Diagnostic
	listOfDiagnostic = ["Control", "MCTD", "PAPs", "RA", "SjS", "SLE", "SSc", "UCTD"]

	cohorte = AssembleMatrixFromFile("DATA/CYTOKINES/quantitativeMatrix.csv")
	
	# Preprocessing Cohorte
	cohorte = preprocessing.robust_scale(cohorte)
	filtered = filter_outlier(cohorte, 6)
	cohorte = filtered[0]
	listOfPositionFiltered = filtered[1]

	# Get patient id and associated position in cohorte
	IdToPositionInCohorte = {}
	dataFile = open("DATA/CYTOKINES/quantitativeMatrix.csv", "r")
	cmptInDataFile = 0
	indexOfID = "undef"
	position = 0
	for line in dataFile:
		if(cmptInDataFile == 0):
			indexInHeader = 0 
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")
			for param in lineInArray:
				if(param == "\Clinical\Sampling\OMICID"):
					indexOfID = indexInHeader
				indexInHeader +=1
		elif(indexOfID != "undef"):
			position += 1
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")

			if(position not in listOfPositionFiltered):
				truePosition = position
				numberOfPositionToDelete = 0
				for pos in listOfPositionFiltered:
					if(pos < position):
						numberOfPositionToDelete += 1
				truePosition = position - numberOfPositionToDelete
				IdToPositionInCohorte[lineInArray[indexOfID]] = truePosition
		cmptInDataFile += 1
	dataFile.close()


	# get patient id to diagnostic from index file
	IdToDiagnostic = {}
	indexFile = open("DATA/patientIndex.csv", "r")
	for line in indexFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		IdToDiagnostic[lineInArray[0]] = lineInArray[1]
	indexFile.close()

	# Remove ID column from matrix
	new_cohorte = []
	for patient in cohorte:
		new_patient = []
		index = 0
		for scalar in patient:
			if(index != indexOfID):
				new_patient.append(scalar)
			index += 1
		new_cohorte.append(new_patient)
	cohorte = new_cohorte

	# Perform PCA
	pca = PCA()
	pca.fit(cohorte)
	plot_explainedVariance(cohorte)
	cohorte = pca.fit_transform(cohorte)

	# Split cohorte
	DiagnosticToSubCohorte = {}
	for diagnostic in listOfDiagnostic:
		SubCohorte = []
		patientInSubCohorte = []
		for key in IdToDiagnostic.keys():
			if(IdToDiagnostic[key] == diagnostic):
				patientInSubCohorte.append(key)
		for key in IdToPositionInCohorte.keys():
			if(key in patientInSubCohorte):
				SubCohorte.append(cohorte[IdToPositionInCohorte[key]-1])
		DiagnosticToSubCohorte[diagnostic] = SubCohorte


	# Plot data point according to Diagnostic
	diagnosticToColor = {"Control":"b", "MCTD":"r", "PAPs":"r", "RA":"y", "SjS":"y", "SLE":"g", "SSc":"g", "UCTD":"c"}
	diagnosticToSymbol = {"Control":"o", "MCTD":"o", "PAPs":"x", "RA":"o", "SjS":"x", "SLE":"o", "SSc":"x", "UCTD":"o"}
	ax = plt.subplot(111, projection='3d')
	for diagnostic in DiagnosticToSubCohorte.keys():
		x = []
		y = []
		z = []
		for patient in DiagnosticToSubCohorte[diagnostic]:
			x.append(patient[0])
			y.append(patient[1])
			z.append(patient[2])

		ax.plot(x, y, z, diagnosticToSymbol[diagnostic], color=diagnosticToColor[diagnostic], label=diagnostic)
	ax.set_xlabel("Factor 1")
	ax.set_ylabel("Factor 2")
	ax.set_zlabel("Factor 3")
	plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0, 0))
	plt.show()


def get_compositionOfEigenVector(dataFileName, numberOfComponent):
	"""
	-> Identification des variables qui composent les
	   composantes principales
	-> Creation du tableau correlation variables-facteurs
	   sous forme dictionnaire {facteur:{variable:correlation}}
	-> dataFileName is the name of the matrix file
	-> numberOfComponent is the number of components used
	   for PCA
	-> return a dictionnary
	"""

	# Get Variable Name present in header
	dataFile = open(dataFileName, "r")
	cmpt = 0
	headerInArray = []
	for line in dataFile:
		if(cmpt == 0):
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")
			headerInArray = lineInArray
		cmpt +=1
	dataFile.close()

	# Create eigenvectors (i.e perform PCA)
	data = AssembleMatrixFromFile(dataFileName)
	data = preprocessing.robust_scale(data)
	filtered = filter_outlier(data, 5)
	cohorte = filtered[0]

	pca = PCA(n_components=numberOfComponent)
	cohorteInNewSpace = pca.fit_transform(cohorte)

	# Create tableau correlation variables-facteurs
	correlationFactorToVariable = {}
	numberOfFactor = 1
	for factor in pca.components_:
		factorName = "factor"+str(numberOfFactor)
		numberOfFactor += 1

		variableToCorrelation = {}
		variable_index = 0
		for variable in headerInArray:
			variableToCorrelation[variable] = factor[variable_index]
			variable_index += 1

		correlationFactorToVariable[factorName] = variableToCorrelation

	return correlationFactorToVariable


def filter_independantVariableFromEigenVector(table):
	"""
	-> Scan the correlation variance factor table,
	   store all independant variable ( i.e correlation = 0)
	   in a list of variable to delete from the table
	
	-> Return a dictionnary 
	"""

	factorToVariableToDelete = {}
	vectorNumber = 1
	for vector in table.values():
		factorName = "factor"+str(vectorNumber)
		vectorNumber += 1
		variableToDelete = []
		for variable in vector:
			if(vector[variable] == 0):
				variableToDelete.append(variable)

		factorToVariableToDelete[factorName] = variableToDelete

	for vectorName in table.keys():
		for variable in factorToVariableToDelete[factorName]:
			del table[vectorName][variable]

	return table


def plot_composanteOfEigenVector(matrixFileName, maxNumberOfVariables, numberOfComponent):
	"""
	-> Plot the major contribution to the eigenvectors
	-> matrixFileName is name of the file where the matrix is stored
	-> maxNumberOfVariables is the number of variables to display in plot
		- can be set to "all"
	-> numberOfComponent is the number of comonents used for PCA
	"""

	# Work on eigenvalue
	table = get_compositionOfEigenVector(matrixFileName, numberOfComponent)
	table = filter_independantVariableFromEigenVector(table)

	# Reduction to max and min value
	for factor in table.keys():

		if(maxNumberOfVariables == "all" or maxNumberOfVariables > len(table[factor])):
			limit = len(table[factor])
			reste = limit % 2
		else:
			limit = maxNumberOfVariables
			reste = limit % 2

		x = table[factor]
		sorted_x = sorted(x.items(), key=operator.itemgetter(1))
		end = sorted_x[-((limit-reste) / 2):]
		begin = sorted_x[:((limit-reste) / 2) + reste]
		reduced_data = begin + end

		# Converstion To Dictionnary
		structureToPlot = {}
		for couple in reduced_data:
			structureToPlot[couple[0]] = couple[1]

		# Graphic representation
		dictionary = plt.figure()
		plt.bar(range(len(structureToPlot)), structureToPlot.values(), align='center')
		plt.xticks(range(len(structureToPlot)), structureToPlot.keys())
		plt.title(factor)
		plt.show()



def extract_variableOfInterest(threshold):
	"""
	-> Extract the variables name from eigenvectos
	   if the absolute value of variable is above a
	   threshold
	-> threshold is a float, between 0 and 1 
	-> return a list of variable name
	"""
	# extract variable of interest
	table = get_compositionOfEigenVector("DATA/CYTOKINES/quantitativeMatrix.csv", 10)
	filter_independantVariableFromEigenVector(table)

	listOfParamToSave = []
	for factor in table.keys():
		vector = table[factor]
		for param in vector.keys():
			if(abs(vector[param]) >= threshold and param not in listOfParamToSave):
				listOfParamToSave.append(param)

	return listOfParamToSave


def extract_variable(fileName, variableToExtract):
	"""
	-> Extact the values of variable variableToExtract in
	   the file fileName
	-> fileName is a string, the name of matrix file
	-> variableToExtract is a string, the name of the variable
	   to extract
	-> return a list containing all values of the variable
	"""

	positionOfVariable = "undef"
	extractedValues = []
	data = open(fileName, "r")
	cmpt = 0
	for line in data:
		line = line.split("\n")
		lineInArray = line[0].split(";")
		if(cmpt == 0):
			positionInHeader = 0
			for variable in lineInArray:
				if(variableToExtract == variable):
					positionOfVariable = positionInHeader
				positionInHeader += 1
		elif(positionOfVariable != "undef"):
			positionInLine = 0
			for value in lineInArray:
				if(positionInLine == positionOfVariable):
					extractedValues.append(value)
				positionInLine += 1
		cmpt += 1
	data.close()
	return extractedValues


def splitCohorteAccordingToDiagnostic(originalMatrixFile, patientIndexFile):
	"""
	-> Split the main main matrixFile into 
	   a subset of matrix files specific to a diagnostic
	-> use the patient Index file (DATA/patientIndexFile)
	-> send a warning message when encounter a patient not in
	   index file
	-> originalMatrixFile is a string, name of the matrix file to split
	-> patientIndexFile is a string, name of the patient index file
	"""

	# create dictionnary
	IdToDiagnostic = {}
	indexFile = open(patientIndexFile, "r")
	for line in indexFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		IdToDiagnostic[lineInArray[0]] = lineInArray[1]
	indexFile.close()

	# Get header
	data = open(originalMatrixFile, "r")
	cmpt = 0
	header = "undef"
	for line in data:
		if(cmpt == 0):
			header = line
		cmpt += 1
	data.close()

	# Initialise les news matrix files
	for diagnostic in IdToDiagnostic.values():
		matrixFileName = "DATA/CYTOKINES/"+str(diagnostic)+"_quantitativeMatrix.csv"
		matrixFile = open(matrixFileName, "w")
		matrixFile.write(header)
		matrixFile.close()

	# Remplir new matrix files
	data = open(originalMatrixFile, "r")
	for line in data:
		line = line.split("\n")
		lineInArray = line[0].split(";")
		patientId = lineInArray[52]
		if(patientId != "\Clinical\Sampling\OMICID"):
			try:
				diagnostic = IdToDiagnostic[patientId]
				destinationFileName = "DATA/CYTOKINES/"+str(diagnostic)+"_quantitativeMatrix.csv"
				destinationFile = open(destinationFileName, "a")
				destinationFile.write(line[0]+"\n")
				destinationFile.close()
			except:
				print "[WARNINGS] => No Diagnostic found for patient "+str(patientId)

	data.close()


def Imputation(method, values):
	"""
	-> Perform an imputation on values
	-> method define the imputation process, could be:
		- basic: replace all NA by 0 (used when NA stand for "below the detection threshold")
	-> values is a one dimensionnal array containing the values of the variable to Impute
	-> return a list
	
	=>TODO: implement new methods
	"""

	new_values = []

	if(method == "basic"):
		new_values = [float(x) if x != "NA" else 0 for x in values]

	return new_values


def get_ThresholdValuesForCytokines(listOfVariableOfInterest, controlMatrixFile):
	"""
	-> get thresholds values for discretisation of
	   cytokines variables
	-> return a dictionnary

	TODO:
		- implement new way of for threshold calculation
		- learn the best threshold values
	"""
	parameterToTreshold = {}
	for variableOfInterest in listOfVariableOfInterest:
		values = extract_variable(controlMatrixFile, variableOfInterest)
		values = Imputation("basic", values)
		description = stats.describe(values)

		mean = description[2]
		variance = description[3]
		ecartType = sqrt(variance)
		minimum = mean - ecartType
		maximum = mean + ecartType

		parameterToTreshold[variableOfInterest] = {"min":float(minimum), "max":float(maximum)}

	return parameterToTreshold

def create_discreteMatrixFile(listOfVariableOfInterest, variableToThreshold):
	"""
	-> Write reduced discrete value files from the splitted into diagnostic
	   matrix files. Only the variables present in listOfVariableOfInterest are
	   kept, discretisation is performed according to the thresholds defined in
	   the dict variableToThreshold.
	-> listOfVariableOfInterest is a list of variable we want to keep
	-> variableToThreshold is a dictionnary where each variable of interest is assign
	   to a min and a max value

	 -> TODO:
	 	- implement new imputation methods

	"""
	listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD", "Control"]
	for disease in listOfDisease:
		fileName = "DATA/CYTOKINES/"+disease+"_quantitativeMatrix.csv"
		newFileName = "DATA/CYTOKINES/"+disease+"_quantitativeMatrix_discrete.csv"
		originalData = open(fileName, "r")
		cmpt = 0
		positionToVariable = {}
		for line in originalData:
			line = line.split("\n")
			lineInArray = line[0].split(";")
				
			# Write header
			if(cmpt == 0):

				# Construct new header
				newHeader = ""
				index = 0
				for scalar in lineInArray:
					if(scalar in listOfVariableOfInterest):
						newHeader = newHeader + scalar + ";"
						positionToVariable[index] = scalar
					index += 1

				# Write new header
				discreteData = open(newFileName, "w")
				discreteData.write(newHeader[:-1]+"\n")
				discreteData.close()
			
			else:
				# Construct new line
				newLine = ""
				index = 0 
				for scalar in lineInArray:
					if(index in positionToVariable.keys()):
						
						# Imputation
						if(scalar == "NA"):
							scalar = 0

						# Discretisation
						minimum = variableToThreshold[positionToVariable[index]]["min"]
						maximum = variableToThreshold[positionToVariable[index]]["max"]
						discreteValue = "undef"
						if(float(scalar) > maximum):
							discreteValue = "high"
						elif(float(scalar) < minimum):
							discreteValue = "low"
						else:
							discreteValue = "normal"
						newLine = newLine + discreteValue + ";"
					index += 1
					
				# Write new line
				discreteData = open(newFileName, "a")
				discreteData.write(newLine[:-1]+"\n")
				discreteData.close()
			cmpt += 1
		originalData.close()


def discretisation_Procedure():
	"""
	-> Create Discrete reduced Matrix File from DATA/CYTOKINES/quantitativeMatrix.csv
	TODO:
		- develop doc
		- pass arguments
	"""
	listOfVariableOfInterest = extract_variableOfInterest(0.5) 
	splitCohorteAccordingToDiagnostic("DATA/CYTOKINES/quantitativeMatrix.csv", "DATA/patientIndex.csv")
	variableToThreshold = get_ThresholdValuesForCytokines(listOfVariableOfInterest, "DATA/CYTOKINES/Control_quantitativeMatrix.csv")
	create_discreteMatrixFile(listOfVariableOfInterest, variableToThreshold)

"""TEST SPACE"""

# Create Data
#CreateIndexFile()
#CreateMatrix()
#format_OMICID()
#extractBinaryMatrix()
#extractQuantitativeMatrix()
#PlotProcedure_fittingDisease()
#cohorteInNewSpace = pca.fit_transform(cohorte)
#show_biplot(cohorte)
#show_biplot(cohorteInNewSpace)
#quickClustering(cohorte, 4, "cytokineTest.png")
# Create Index File
#CreateIndexFile()

#plot_composanteOfEigenVector("DATA/CYTOKINES/quantitativeMatrix.csv", "all", 5)
#plot_composanteOfEigenVector("DATA/CYTOKINES/quantitativeMatrix.csv", 3, 5)

#discretisation_Procedure()

#machin = AssembleMatrixFromFile("DATA/CYTOKINES/SLE_quantitativeMatrix_discrete.csv")
#print machin