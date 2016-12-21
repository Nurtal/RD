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
		minimum = mean - 3*ecartType
		maximum = mean + 3*ecartType
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






def PlotProcedure_fittingDisease():
	"""	
	-> Create a cohorte with the AssembleMatrixFromFile() function
	-> Create Dict IdToPositionInCohorte from the data . csv file
	   (in the exemple case: testData.csv)
	-> Create Dict patient id to diagnostic from index file 
	   (in the exemple case : patientIndex_test.csv)
	-> Split the cohorte, i.e create the Dict diagnostic to SubCohorte
	-> Use the different SubCohorte generated to plot the data


	TODO:
		-Adapt To real Data

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



"""TEST SPACE"""


def CreateIndexFile():
	"""
	-> Create an index file for patient in the
	   DATA folder.
	-> All filename present in PANEL folder are scanned,


	Write doc
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
		patientInArray = patient.split("/")
		patientInArray = patientInArray[-1]
		patientInArray = patientInArray.split("_")
		patient_id = patientInArray[1]
		patient_diagnostic = patientInArray[0]
		if(patient_id not in listOfPatientId):
			indexFile.write(patient_id+";"+patient_diagnostic+"\n")
			listOfPatientId.append(patient_id)
	indexFile.close()




"""
# Create Data
#CreateMatrix()
#extractBinaryMatrix()
#extractQuantitativeMatrix()
data = AssembleMatrixFromFile("DATA/CYTOKINES/quantitativeMatrix.csv")
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
pca = PCA(n_components=50)
pca.fit(cohorte)
plot_explainedVariance(cohorte)
print len(cohorte[0])
cohorteInNewSpace = pca.fit_transform(cohorte)
plot_explainedVariance(cohorteInNewSpace)


# keep only the first 10 parameters
cohorte_reduced = []
for patient in cohorteInNewSpace:
	newPatient = patient[:10]
	cohorte_reduced.append(newPatient)
cohorte_reduced = np.array(cohorte_reduced)

quickClustering(cohorte_reduced, 4, "cytokineTest.png")
#quickPCA(cohorte_reduced, y, ["Male","Female"], "2d", "cytokinesPcaTest.png", 1, 1)
show_biplot(cohorte_reduced)
#show_biplot(cohorte)
"""

"""
data = AssembleMatrixFromFile("DATA/CYTOKINES/testData.csv")
cohorte = preprocessing.robust_scale(data)
cohorte = filter_outlier(data)


pca = PCA()
pca.fit(cohorte)
#plot_explainedVariance(cohorte)
cohorteInNewSpace = pca.fit_transform(cohorte)
#plot_explainedVariance(cohorteInNewSpace)
"""


#show_biplot(cohorte)
#show_biplot(cohorteInNewSpace)

#quickClustering(cohorte, 4, "cytokineTest.png")





"""
target_name = ["malade", "sain", "autre"]
y = [0,0,0,1,1,1,2]
C = pca.fit(cohorte).transform(cohorte)

plt.figure()
colors = ["r", "r", "r", "b", "b", "b", "g"]
plt.scatter(C[:, 0], C[:, 1], cmap=plt.cm.Paired, label=target_name, c=colors)
#for c, i, target_name in zip("rgb", [0,1,2], target_name):
#	plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
plt.legend()
plt.title("ACP")
plt.show()
"""





"""
target_name = ["malade", "sain", "autre"]
y = [0,0,0,1,1,1,2]
pca = PCA()
C = pca.fit(cohorte).transform(cohorte)
est=KMeans(n_clusters=3)
est.fit(cohorte)
classe=est.labels_


fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)

#ax.scatter(C[:, 0], C[:, 1], C[:, 2], c=classe, cmap=plt.cm.Paired)
#for c, i, target_name in zip("rgb", [0,1,2], target_name):
#	ax.scatter(C[y == i,0], C[y == i,1], C[y == i,2], c=c)


ax.set_title("kmean : "+str(3)+" clusters")
ax.set_xlabel("Comp1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("Comp2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("Comp3")
ax.w_zaxis.set_ticklabels([])
ax.legend()
plt.show()
"""





"""
N = len(cohorteInNewSpace)
data = cohorteInNewSpace
labels = ["malade", "malade", "malade", "sain", "sain", "sain", "autre"]

colors = ["r", "r", "r", "b", "b", "b", "g"]

plt.subplots_adjust(bottom = 0.1)
plt.scatter(
    data[:, 0], data[:, 1], marker = 'o', cmap = plt.get_cmap('Spectral'))
for label, x, y in zip(labels, data[:, 0], data[:, 1]):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.show()
"""

"""
import numpy as np
import sklearn.datasets, sklearn.decomposition

#X = sklearn.datasets.load_iris().data

X = cohorte
mu = np.mean(X, axis=0)

pca = sklearn.decomposition.PCA()
pca.fit(X)

nComp = 2
Xhat = np.dot(pca.transform(X)[:,:nComp], pca.components_[:nComp,:])
Xhat += mu
print Xhat
#print(Xhat[0,])

"""




