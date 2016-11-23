"""
preprocessing data
for RD project
"""


import numpy as np
import matplotlib.pyplot as plt
from random import shuffle
from random import choice
from scipy.stats import norm
from scipy.stats import pearsonr
from scipy.stats import shapiro
from scipy.stats import kstest
from scipy.stats import anderson
import scipy.stats as stats

from sklearn import preprocessing

import numpy.random as random
from sklearn import datasets

import glob
import platform
from trashlib2 import *






def show_distribution(data):
	"""
	IN PROGRESS

	-> plot the box plot and QQ plot for data x
	-> x is a 1 dimmensional array

	-> TODO:
		- return numercial values
		- save graphe file
	"""

	x = data

	x = np.sort(x)
	plt.hist(x)
	plt.show()
	plt.close()

	norm=random.normal(0,2,len(x))
	norm.sort()
	plt.figure(figsize=(12,8),facecolor='1.0') 
	plt.plot(norm,x,"o")
	plt.title("Normal Q-Q plot", size=28)
	plt.xlabel("Theoretical quantiles", size=24)
	plt.ylabel("Expreimental quantiles", size=24)
	plt.show()
	plt.close()





def get_OneDimensionnalData(inputFolder, typeOfParameter, parameter):
	"""
	-> get the 1 dimmensional array of parameter
	-> used to test parameter distribution
	"""

	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfVectorFiles = []
	for patientFile in listOfPatientFiles:
		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		if(platform.system() == "Linux"):
			patientFilesInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFilesInArray = patientFile.split("\\")
		patientFilesInArray = patientFilesInArray[-1]
		vectorFileName = "DATA/VECTOR/"+str(patientFilesInArray)+"_VECTOR.csv"
		convertPatientToVector2(patientFile, vectorFileName, typeOfParameter)
		listOfVectorFiles.append(vectorFileName)
	listOfVector = []
	for vectorFile in listOfVectorFiles:
		vectorData = open(vectorFile, "r")
		listOfvalue = []
		for line in vectorData:
			lineInArray = line.split(";")
			if(lineInArray[0]!="id"):
				parameterName = lineInArray[0]
				if(parameterName == parameter):
					parameterValue = lineInArray[1]
					parameterValue = float(parameterValue[:-1])
					listOfvalue.append(parameterValue)
		vectorData.close()
		listOfVector.append(listOfvalue)
	data = numpy.array(tuple(listOfVector))
	return data


def describe_distribution(x):
	"""
	IN PROGRESS
	-> perform a few test on data
	-> x is a one dimmensional array
	-> low skewness i.e data are centered like a normal distribution
	-> kurtosis indication for flat data
	-> low p value i.e data are not fitting a normal distribution

	TODO:
		-> write doc
	"""

	skewness = stats.skew(x)
	kurtosis = stats.kurtosis(x)
	k_shapiro, p_shapiro = shapiroResult = stats.shapiro(x)
	k,p=stats.mstats.normaltest(x)

	summary = {"skewness":skewness[0],
			   "kurtosis":kurtosis[0],
			   "k_shapiro":k_shapiro,
			   "p_shapiro":p_shapiro,
			   "p":p[0]}
	return summary


def scale_Data(x):
	"""
	IN PROGRESS

	TODO:
		- write doc
	"""

	x_scaled = preprocessing.scale(x)

	return x_scaled


"""TEST SPACE"""




#X = get_OneDimensionnalData("DATA/PATIENT", "PROPORTION", param)



"""
iris = datasets.load_iris()
x = iris.data[:, :1]  # we only take the first two features.
X_scaled = preprocessing.scale(x)
#show_distribution(X_scaled)


result = describe_distribution(X_scaled)


#x = np.loadtxt("DataFileNormalityTest.txt", unpack=True)


x = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,8,8,8,8,9,9,9]

"""

"""
listOfParams = get_listOfParameters2("DATA/PATIENT", "PROPORTION")
for param in listOfParams:
	X = get_OneDimensionnalData("DATA/PATIENT", "PROPORTION", param)
	
	machin = describe_distribution(X)
	truc = describe_distribution(X_scaled)
	status = "undef"
	if(machin["p"] - truc["p"] < 0 ):
		status = "amelioration"

		show_distribution(X)
		show_distribution(X_scaled)

	else:
		status = "decreasing quality"

	print str(machin["p"]) + " || " + str(truc["p"]) + " => "+status

"""











