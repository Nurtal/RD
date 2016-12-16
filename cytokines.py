"""
work on cytokines data
unstructured file
have to dispatch functions
"""

import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from analysis import *

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
	for line in matrixFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")

		if(cmpt != 0):
			patient = []
			for value in lineInArray:
				try:
					float(value)
					patient.append(float(value))
				except:
					patient.append(np.nan)
			cohorte.append(patient)
		cmpt = cmpt + 1
	matrixFile.close()
	imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
	X = cohorte
	imp.fit(X)
	print(imp.transform(X))
	data = imp.transform(X)
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


"""TEST SPACE"""

# Create Data
#CreateMatrix()
#extractBinaryMatrix()
#extractQuantitativeMatrix()
data = AssembleMatrixFromFile()
data = preprocessing.robust_scale(data)
cohorte = filter_outlier(data)
y = get_discreteLabel()


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





"""
# Biplot stuff, to check & implement on real data


import pandas as pd
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

## import data

my_csv = 'DATA/CYTOKINES/iris.csv' ## path to your dataset

dat = pd.read_csv(my_csv, index_col=0)
# if no row or column titles in your csv, pass 'header=None' into read_csv
# and delete 'index_col=0' -- but your biplot will be clearer with row/col names



## perform PCA
n = len(dat.columns)

pca = PCA(n_components = n)
# defaults number of PCs to number of columns in imported data (ie number of
# features), but can be set to any integer less than or equal to that value

pca.fit(dat)



## project data into PC space

# 0,1 denote PC1 and PC2; change values for other PCs
xvector = pca.components_[0] # see 'prcomp(my_data)$rotation' in R
yvector = pca.components_[1]

xs = pca.transform(dat)[:,0] # see 'prcomp(my_data)$x' in R
ys = pca.transform(dat)[:,1]



## visualize projections
    
## Note: scale values for arrows and text are a bit inelegant as of now,
##       so feel free to play around with them

for i in range(len(xvector)):
# arrows project features (ie columns from csv) as vectors onto PC axes
    plt.arrow(0, 0, xvector[i]*max(xs), yvector[i]*max(ys),
              color='r', width=0.0005, head_width=0.0025)
    plt.text(xvector[i]*max(xs)*1.2, yvector[i]*max(ys)*1.2,
             list(dat.columns.values)[i], color='r')

for i in range(len(xs)):
# circles project documents (ie rows from csv) as points onto PC axes
    plt.plot(xs[i], ys[i], 'bo')
    plt.text(xs[i]*1.2, ys[i]*1.2, list(dat.index)[i], color='b')

plt.show()


"""





"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
 
# ## Data Import
 
my_csv = 'DATA/CYTOKINES/iris.csv' ## path to your dataset
ds = pd.read_csv(my_csv)
ds.head()
 
 
# ## Normalizing the data
from sklearn.preprocessing import StandardScaler
scale = StandardScaler()
 
 
# ## Create a data frame for feature sets ONLY
X = scale.fit_transform(ds.drop('class', axis = 1)) # drop the label and normalizing
X = pd.DataFrame(df) # It is required to have X converted into a data frame to later plotting need
X.columns = [['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
X.head()
 
# ## Run PCA against feature set dataframe
n = len(X.columns)-1 # set the number
pca = PCA(n_components = n)
X_pca = pca.fit(X).transform(X)
 
df_pca = pd.DataFrame(X_pca)
df_pca['y'] = pd.DataFrame(y)
df_pca.columns = [['pc1', 'pc2', 'pc3', 'y']]
df_pca.head()
 
 
 
# ## Biplot - Leverage `seaborn` package
 
# In[83]:
 
import seaborn as sns
 
# Scatter plot based and assigne color based on 'label - y'
sns.lmplot('pc1', 'pc2', data=df_pca, fit_reg = False, hue = 'y', size = 15, scatter_kws={"s": 100})
 
# set the maximum variance of the first two PCs
# this will be the end point of the arrow of each **original features**
xvector = pca.components_[0]
yvector = pca.components_[1]
 
# value of the first two PCs, set the x, y axis boundary
xs = pca.transform(X)[:,0]
ys = pca.transform(X)[:,1]
 
## visualize projections
 
## Note: scale values for arrows and text are a bit inelegant as of now,
##       so feel free to play around with them
for i in range(len(xvector)):
    # arrows project features (ie columns from csv) as vectors onto PC axes
    # we can adjust length and the size of the arrow
    plt.arrow(0, 0, xvector[i]*max(xs), yvector[i]*max(ys),
              color='r', width=0.005, head_width=0.05)
    plt.text(xvector[i]*max(xs)*1.1, yvector[i]*max(ys)*1.1,
             list(df.columns.values)[i], color='r')
 
for i in range(len(xs)):
    plt.text(xs[i]*1.08, ys[i]*1.08, list(X.index)[i], color='b') # index number of each observations
plt.title('PCA Plot of first PCs')

"""