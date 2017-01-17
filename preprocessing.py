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
from math import sqrt

from analysis import *
from reorder import *





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

	norm=numpy.random.normal(0,2,len(x))
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



def get_ThresholdValue(typeOfParameter, scaleValue, GenerationMethod):
	"""
	-> Return a dictionnary  param : min, max
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	
	-> scaleValue is a boolean, 1 to scale control value, else 0
	-> GenerationMethod is a string, could be:
		-Classic
		-Mean
	
	-> TODO:
		implement new threshold detection
	"""
	parameterToTreshold = {}
	listOfAllParameters = get_allParam(typeOfParameter)
	for param in listOfAllParameters:
		X = get_OneDimensionnalData("DATA/PATIENT", typeOfParameter, param)
		
		############################################################
		# Si les data sont scale ici, les donnes a tester doivent  #
		# aussi etre "scale", lasser brut pour le moment		   #
		############################################################
		if(scaleValue):
			X = scale_Data(X)
		

		description = stats.describe(X)

		# Classic Threshold
		if(GenerationMethod == "Classic"):
			minmax = description[1]
			minimum = minmax[0]
			maximum = minmax[1]

		# Mean Threshold
		elif(GenerationMethod == "Mean"):
			mean = description[2]
			variance = description[3]
			ecartType = sqrt(variance)
			minimum = mean - ecartType
			maximum = mean + ecartType

		parameterToTreshold[param] = {"min":float(minimum), "max":float(maximum)}

	return parameterToTreshold



def discretization(thresholds):
	"""
	-> convert numerical value in patient file into
	   discrete qualtitative value, according do threshold in thresholds.
	-> thresholds is a dictionnary structure, create from the get_ThresholdValue
	   function 
	-> currently qualtitative values are:
		-low
		-high
		-normal
	-> For now work only on non-scaled data

	-> TODO:
		- implement new discretization methods (quantiles ...)
		- increase discretization resolution (more than 3 values)
		- implement discretization on scaled data.
	"""
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFileName = patientFileInArray[-1]
		newPatientFileName = "DATA/PATIENT/"+str(patientFileName)+".tmp"
		shutil.copy(patientFile, newPatientFileName)

		sourceData = open(newPatientFileName, "r")
		destinationFile = open(patientFile, "w")
		for line in sourceData:
			lineInArray = line.split(";")
			typeOfParameter = lineInArray[2]
			parameterValue = lineInArray[4]
			parameterValue = parameterValue[:-1]
			parameterName = "undef"
			if(typeOfParameter == "PROPORTION"):
				parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
			elif(typeOfParameter == "MFI"):
				parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
			else:
				parameterName = lineInArray[1]
			for parameter in thresholds.keys():
				if(parameterName == parameter):
					thresholdValues = thresholds[parameter]
					if(float(parameterValue) < thresholdValues["min"]):
						newParameterValue = "low"
					elif(float(parameterValue) > thresholdValues["max"]):

						#print str(parameterValue) + "||" + str(thresholdValues["max"])
						
						newParameterValue = "high"
					else:
						newParameterValue = "normal"

					newLine = lineInArray[0]+";"+lineInArray[1]+";"+lineInArray[2]+";"+lineInArray[3]+";"+newParameterValue+"\n"
					destinationFile.write(newLine)

		destinationFile.close()
		sourceData.close()
		os.remove(newPatientFileName)





def scaleDataInPatientFolder(dataType):
	"""
	IN PROGRESS

	TODO:
		-write doc
	"""

	#############################################
	# Create Matrix from data in PATIENT folder #
	#############################################
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	listOfVectorFiles = []
	for patientFile in listOfPatientFiles:
		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		if(platform.system() == "Linux"):
			patientFilesInArray = patientFilesInArray.split("/")
		elif(platform.system() == "Windows"):
			patientFilesInArray = patientFilesInArray.split("\\")
		patientFilesInArray = patientFilesInArray[-1]
		vectorFileName = "DATA/VECTOR/"+str(patientFilesInArray)+"_VECTOR.csv"
		convertPatientToVector2(patientFile, vectorFileName, dataType)
		listOfVectorFiles.append(vectorFileName)
	listOfVector = []
	for vectorFile in listOfVectorFiles:
		vectorData = open(vectorFile, "r")
		listOfvalue = []
		for line in vectorData:
			lineInArray = line.split(";")
			if(lineInArray[0]!="id"):
				parameterValue = lineInArray[1]
				parameterValue = float(parameterValue[:-1])
				listOfvalue.append(parameterValue)
		vectorData.close()
		listOfVector.append(listOfvalue)

	# scale data
	data = numpy.array(tuple(listOfVector))
	data = scale_Data(data)

	# get list of parameters 
	listOfParameters = []
	patientData = open(listOfPatientFiles[0], "r")
	for line in patientData:
		lineInArray = line.split(";")
		if(lineInArray[1] != "POPULATION"):
			if(lineInArray[2] == dataType or dataType == "ALL"):
				lineInArray = lineInArray[:-1]
				newLine = ""
				for element in lineInArray:
					newLine = newLine + element + ";"
				listOfParameters.append(newLine)
	patientData.close()


	# Overwrite patient file
	for x in xrange (0, len(listOfPatientFiles)):
		patientFile = listOfPatientFiles[x]
		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		if(platform.system() == "Linux"):
			patientFilesInArray = patientFilesInArray.split("/")
		elif(platform.system() == "Windows"):
			patientFilesInArray = patientFilesInArray.split("\\")
		patientFilesInArray = patientFilesInArray[-1]
		newPatientFileName = "DATA/PATIENT/"+str(patientFilesInArray)+".csv"
		dataToOverWrite = open(newPatientFileName, "w")
		for y in xrange(0, len(listOfParameters)):
			lineToWrite = listOfParameters[y]+str(data[x][y])+"\n"
			dataToOverWrite.write(lineToWrite)
		dataToOverWrite.close()

def get_ThresholdValue_DynamicDelta(typeOfParameter, scaleValue, GenerationMethod, delta):
	"""
	-> Return a dictionnary  param : min, max
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	
	-> scaleValue is a boolean, 1 to scale control value, else 0
	-> GenerationMethod is a string, could be:
		-Classic
		-Mean

	-> delta is an int, add to min thresold and substract from max threshold
	   i.e used to get a smaller "normal zone" 
	
	TODO:
		- reorder function
		- test diffenrent generation method
		- reorder doc
	
	"""
	parameterToTreshold = {}
	listOfAllParameters = get_allParam(typeOfParameter)
	for param in listOfAllParameters:
		X = get_OneDimensionnalData("DATA/PATIENT", typeOfParameter, param)
		
		############################################################
		# Si les data sont scale ici, les donnes a tester doivent  #
		# aussi etre "scale", lasser brut pour le moment		   #
		############################################################
		if(scaleValue):
			X = scale_Data(X)
		

		description = stats.describe(X)

		# Classic Threshold using delta correcton
		if(GenerationMethod == "Classic"):
			minmax = description[1]
			minimum = minmax[0] + delta
			maximum = minmax[1] - delta

		# Mean Threshold using delta correcton
		elif(GenerationMethod == "Mean"):
			mean = description[2]
			variance = description[3]
			ecartType = sqrt(variance)
			minimum = mean - ecartType + delta*ecartType
			maximum = mean + ecartType - delta*ecartType

		parameterToTreshold[param] = {"min":float(minimum), "max":float(maximum)}

		#print "["+param+"] "+str(minimum) + " || " +str(maximum)

	return parameterToTreshold





"""TEST SPACE"""

#X = get_OneDimensionnalData("DATA/PATIENT", "ABSOLUTE", "CD25pos_activated_CD4pos_Tcells")
#description = stats.describe(X)
#print description
#show_distribution(X)





