"""
RD Project
"""


from reorder import *

import glob


def assemble_Cohorte():
	"""
	-> Assemble cohorte (i.e list of list)
	   of patient
	-> create index file for variable in PARAMETERS folder
	-> return a list of patient patient vector
	"""

	#####################
	# Create index file #
	#####################

	listOfParameters = get_allParam("ALL")
	indexFile = open("PARAMETERS/variable_index.csv", "w")
	cmpt = 0
	for parameter in listOfParameters:
		cmpt = cmpt + 1
		indexFile.write(parameter+";"+"p"+str(cmpt)+"\n")
	indexFile.close()

	#########################
	# Assemblage en cohorte #
	#########################

	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	cohorte = []
	for patientFile in listOfPatientFiles:
		patientVector = []
		data = open(patientFile, "r")
		for line in data:
			variable = ""
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0]
			lineInArray = lineInArray.split(";")
			typeOfParameter = lineInArray[2]
			parameterName = ""
			parameterValue = lineInArray[4]
			if(typeOfParameter == "PROPORTION"):
				parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
			elif(typeOfParameter == "MFI"):
				parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
			else:
				parameterName = lineInArray[1]
			indexFile = open("PARAMETERS/variable_index.csv", "r")
			for lineInIndexFile in indexFile:
				lineInIndexFileInArray = lineInIndexFile.split("\n")
				lineInIndexFileInArray = lineInIndexFileInArray[0]
				lineInIndexFileInArray = lineInIndexFileInArray.split(";")
				parameterNameInIndexFile = lineInIndexFileInArray[0]
				parameterId = lineInIndexFileInArray[1]
				if(parameterName == parameterNameInIndexFile):
					variable = parameterId+"_"+str(parameterValue)
			patientVector.append(variable)
			indexFile.close()
		data.close()
		cohorte.append(patientVector)

	return cohorte



def alleviate_cohorte(cohorte, threshold_alleviate):
	"""
	-> alleviate patient vector in cohorte : check the
	   discrete value of all parameter, if the count of
	   "normal" value is above the threshold_alleviate
	   the variable is deleted from all patient vector.

	-> cohorte is a list of patient vector (i.e a list of lists)
	-> threshold_alleviate is an int
	-> return a cohorte ( i.e a list of lists)
	"""

	###################################
	# Denombrement des variables avec # 
	# possedant une valeur normal     #
	###################################
	
	paramToNormalCount = {}
	for variable in cohorte[0]:
		variableInArray = variable.split("_")
		variableId = variableInArray[0]
		paramToNormalCount[variableId] = 0

	for patient in cohorte:
		for variable in patient:
			variableInArray = variable.split("_")
			variableValue = variableInArray[1]
			variableId = variableInArray[0]
			if(variableValue == "normal"):
				paramToNormalCount[variableId] = paramToNormalCount[variableId] + 1
    
    ###########################################
	# Suppression des variables "trop normal" #
	###########################################

	listOfParameterToDelete = []
	for variable in paramToNormalCount.keys():
		if(paramToNormalCount[variable] > threshold_alleviate):
			listOfParameterToDelete.append(variable)

	for patient in cohorte:
		for variable in patient:
			variableInArray = variable.split("_")
			variableValue = variableInArray[1]
			variableId = variableInArray[0]
			if(variableId in listOfParameterToDelete):
				patient.remove(variable)

	return cohorte


def get_listOfNormalParameters(cohorte, threshold):
	"""
	-> check the discrete value of all parameter, if the count of
	   "normal" value is above the threshold the variable is added
	   to the list of "Normal Parameters"
	-> cohorte is a list of patient vector (i.e a list of lists)
	-> threshold is an int
	-> return a list
	"""

	###################################
	# Denombrement des variables avec # 
	# possedant une valeur normal     #
	###################################
	
	paramToNormalCount = {}
	for variable in cohorte[0]:
		variableInArray = variable.split("_")
		variableId = variableInArray[0]
		paramToNormalCount[variableId] = 0

	for patient in cohorte:
		for variable in patient:
			variableInArray = variable.split("_")
			variableValue = variableInArray[1]
			variableId = variableInArray[0]
			if(variableValue == "normal"):
				paramToNormalCount[variableId] = paramToNormalCount[variableId] + 1
	
	###########################
	# Selection des variables #
	###########################
	
	listOfParameterToDelete = []
	for variable in paramToNormalCount.keys():
		if(paramToNormalCount[variable] > threshold):
			listOfParameterToDelete.append(variable)

	####################################
	# Conversion des variables avec le #
	# fichier index                    #
	####################################
	
	listOfVariableToReturn = []
	for variable in listOfParameterToDelete:
		variableName = "undef"
		variableIndex = open("PARAMETERS/variable_index.csv")
		for line in variableIndex:
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0]
			lineInArray = lineInArray.split(";")
			parameterName = lineInArray[0]
			parameterId = lineInArray[1]
			if(parameterId == variable):
				variableName = parameterName

		listOfVariableToReturn.append(variableName)
		variableIndex.close()

	return listOfVariableToReturn



def get_optimalValueOfThreshold(cohorte, maxTry, expectedNumberOfRemovedParameter):
	"""
	-> search the optimal value of threshold for the function
	   get_listOfNormalParameters(). The optimal value is the 
	   one providing the expectedNumberOfRemovedParameter
	-> maxTry is an int, maximum number of try
	-> expectedNumberOfRemovedParameter is an int
	"""
	listOfParameters = get_allParam("ALL")
	threshold = len(cohorte[0])
	listOfNormalParameters = []
	numberOfTry = 0
	while(1 > 0):
		if(numberOfTry >= maxTry):
			print "=> reach maximum number of tries"
			threshold = -1
			break
		listOfNormalParameters = get_listOfNormalParameters(cohorte, threshold)
		if(len(listOfNormalParameters) ==  len(listOfParameters)):
			#print "=> Nothing left to proceed"
			if(threshold + 1 <= len(cohorte[0])):
				threshold = startValue + 1
			else:
				print "Can't do better" # i.e everything is super normal
				break
		elif(len(listOfNormalParameters) == 0):
			#print "=> No reduction performed"
			if(threshold > 0):
				threshold = threshold - 1
			else:
				print "Can't do better" # i.e nothing is normal
		elif(len(listOfNormalParameters) < expectedNumberOfRemovedParameter):
			#print "=> Not enough parameter removed"
			threshold = threshold - 1
		else:
			print "=> Good enough"
			break
		numberOfTry = numberOfTry + 1

	return threshold

"""TEST SPACE"""


"""
from fp_growth import find_frequent_itemsets
transactions = [["p1_low", "p2_normal", "p3_normal"], ["p1_high", "p2_normal", "p3_normal"], ["p1_high", "p2_high","p3_high"]]


for itemset in find_frequent_itemsets(transactions, 2):
    print itemset

"""