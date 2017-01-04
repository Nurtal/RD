"""
RD Project
"""


from reorder import *
from fp_growth import find_frequent_itemsets
import glob
import itertools


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
	threshold = 0
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
				threshold = threshold + 1
			else:
				#print "Can't do better" # i.e everything is super normal
				break
		elif(len(listOfNormalParameters) == 0):
			#print "=> No reduction performed"
			if(threshold > 0):
				threshold = threshold - 1
			else:
				#print "Can't do better" # i.e nothing is normal
				threshold = len(cohorte[0]) + 1
				break;
		elif(len(listOfNormalParameters) < expectedNumberOfRemovedParameter):
			#print "=> Not enough parameter removed"
			threshold = threshold - 1
		else:
			#print "=> Good enough"
			break
		numberOfTry = numberOfTry + 1

	return threshold

"""TEST SPACE"""



def get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, minNumberOfParamToLeft):
	"""
	-> Control the result return by get_optimalValueOfThreshold function,
	   make sure that at least minNumberOfParamToLeft parameters are left
	   for further analysis
	-> cochorte is list of list
	-> maxTry is an int, max number of tries
	-> minNumberOfParamToRemove is an int, could be modify in the function
	   to fit minNumberOfParamToLeft
	-> minNumberOfParamToLeft is an int, tje minimum number of parameter to left if
	   all parameters present in listOfNormalParameters are deleted from the data
	-> return threshold, the best "safe" value to use in function
	   get_listOfNormalParameters.
	"""
	numberOfTry = 0
	while(1 > 0):
		numberOfTry += 1
		if(numberOfTry > maxTry):
			print "=> reach maximum number of tries"
			threshold = len(cohorte[0]) + 1
			break
		threshold = get_optimalValueOfThreshold(cohorte, 60, minNumberOfParamToRemove)
		listOfNormalParameters = get_listOfNormalParameters(cohorte, threshold)
		listOfParameters = get_allParam("ALL")
		if(len(listOfParameters) - len(listOfNormalParameters) < minNumberOfParamToLeft):
			if(minNumberOfParamToRemove - 1 < 0):
				print "=> Can't remove parameters"
				threshold = len(cohorte[0]) + 1
				break
			else:	
				minNumberOfParamToRemove = minNumberOfParamToRemove - 1
		else:
			print "=> Found a good threshold :"+str(threshold)
			print "=> "+str(minNumberOfParamToRemove) + " parameters removed"
			break

	return threshold



def searchForPattern(cohorte, maxTry, maxNumberOfFrequentPattern, patternSaveFileName):
	"""
	-> Generate pattern (i.e frequent itemsets) from cohorte, with maxTry.
	   results are saved in a .csv file (patternSaveFileName).
	-> cohorte is a list of list
	-> maxTry is an int
	-> patternSaveFileName is a string, save file should be located in
	   DATA/PATTERN folder.
	-> maxNumberOfFrequentPattern is an int, the max number of frequent pattern to Generate
	   (setup ti avoid memory problem)

	-> TODO:
		- re-check the algorithm
		- limit the retrieval of the same patterns
		- clean doublon in patternSaveFileName

	"""

	# Initialisation des parametres
	minsup = len(cohorte)
	minLenOfPattern = len(cohorte[0])
	numberOfTry = 0
	tunningPatternLen = 1
	tunnigMinSup = 0
	pattern_save = open(patternSaveFileName, "a")
	pattern_save.close()

	while(1>0):

		######################################
		# controle le nombre de try effectue #
		######################################
		if(numberOfTry >= maxTry):
			break

		###########################
		# Generation des patterns #
		###########################
		listOffrequentItemset = []
		for itemset in find_frequent_itemsets(cohorte, minsup):
		    listOffrequentItemset.append(itemset)

		######################################################
		# controle le nombre de pattern, si aucun pattern    #
		# n est genere on baisse la valeur du minsup employe #
		# pour genere les patterns                           #
		######################################################
		if(len(listOffrequentItemset) > 0):
			listOfItemSize = []
			print "Found "+str(len(listOffrequentItemset))+" frequent itemsets with minsup = "+str(minsup)
			


			##############################################################
			# Ecriture des pattern dans un fichier de sauvegarde         #
			# chaque ligne correspond a un pattern, chaque               #
			# element du pattern est separe des autres par un ;          #
			# le dernier terme de la ligne correspond au minsup          #
			# utilise pour genere le pattern (i.e le support du pattern) #
			##############################################################
			pattern_save = open(patternSaveFileName, "a")			
			for element in listOffrequentItemset:
				lineToWrite = ""
				for item in element:
					lineToWrite = lineToWrite + item + ";"
				listOfItemSize.append(len(element))
				lineToWrite = lineToWrite + str(minsup)
				pattern_save.write(lineToWrite+"\n")
			pattern_save.close()


			if(len(listOffrequentItemset) > maxNumberOfFrequentPattern):
				print "max number of patterns reached, cancel mining"
				break

			######################################################
			# controle de la taille des pattern, si la taille    #
			# du plus gros pattern ne passe pas le controle      #
			# on adapte alternativement le score minsup employer #
			# et la taille des pattern attendues				 #
			######################################################
			maxSize = max(listOfItemSize)
			if(maxSize < minLenOfPattern):
				if(tunnigMinSup):
					tunnigMinSup = 0
					tunningPatternLen = 1
					minsup = minsup - 1
					triedToIcreaseMinLenPattern = 0
				elif(tunningPatternLen):
					tunningPatternLen = 0
					tunnigMinSup = 1
					minLenOfPattern = minLenOfPattern - 1
			else:
				if(not triedToIcreaseMinLenPattern):

					###################################################
					# si la taille des pattern est bonne mais         #
					# on viens juste de changer de minsup alors       #
					# on augmente la taille attendue des pattern      #
					# pour voir si on pas pecher un plus gros pattern #
					###################################################
					minLenOfPattern = minLenOfPattern + 1
					triedToIcreaseMinLenPattern = 1
				
				else:
					######################################################
					# Si la taille des pattern est bonne et on a deja    #
					# essayer d augmenter la taille attendue des pattern #
					# on arrete la recherche ici                         #
					######################################################
					print "found a good pattern"
					break

		else:
			minsup = minsup -1
		numberOfTry += 1



def filter_Pattern(fileName):
	"""
	IN PROGRESS

	TODO:
		-write doc
	"""

	filterDataName = fileName.split(".")
	heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
	lowFilterName = filterDataName[0] + "_LowFilter.csv"


	dataToClean = open(fileName, "r")
	dataHeavyFiltered = open(heavyFilterName, "w")
	dataLowFiltered = open(lowFilterName, "w")

	for line in dataToClean:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0]
		lineInArray = lineInArray.split(";")
		support = lineInArray[-1]
		lineInArray = lineInArray[:-1]

		listOfDiscreteValue = []

		for element in lineInArray:
			element = element.split("_")
			parameter = element[0]
			discreteValue = element[1]
			listOfDiscreteValue.append(discreteValue)

		# control the line
		if("normal" not in listOfDiscreteValue):
			dataHeavyFiltered.write(line)		

		# control the line
		saveTheLine = 0
		for value in listOfDiscreteValue:
			if(value != "normal"):
				saveTheLine = 1
		if(saveTheLine):
			dataLowFiltered.write(line)

	dataToClean.close()
	dataHeavyFiltered.close()
	dataLowFiltered.close()



"""TEST SPACE"""

def extract_parametersFromPattern(fileName, minSupport):
	"""
	IN PROGRESS

	TODO:
	 - write doc
	"""

	data = open(fileName, "r")
	listOfParameters = []
	
	for line in data:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		support = lineInArray[-1]

		if(int(support) >= int(minSupport)):
			lineInArray = lineInArray[:-1]
			for element in lineInArray:
				elementInArray = element.split(":")
				parameter = elementInArray[0]
				if(parameter not in listOfParameters):
					listOfParameters.append(parameter)
	data.close()
	return listOfParameters


from fp_growth import find_frequent_itemsets
cohorte = [["p1_low", "p2_normal", "p3_normal", "p4_normal", "p5_normal"],
 				["p1_high", "p2_normal", "p3_normal", "p4_normal", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_normal", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_normal", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_normal", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_normal", "p5_high"],
 			    ["p1_high", "p2_high","p3_high", "p4_normal", "p5_high"],
 			    ["p1_high", "p2_high","p3_high", "p4_low", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_low", "p5_normal"],
 			    ["p1_high", "p2_high","p3_high", "p4_high", "p5_normal"]]





def search_FrequentItem(cohorte, saveFileName, minSupport):
	"""
	IN PROGRESS
	"""

	valueToCount = {}

	# initialisation
	for patient in cohorte:
		for value in patient:
			valueToCount[value] = 0
	# count
	for patient in cohorte:
		for value in patient:
			for key in valueToCount.keys():
				if(value == key):
					valueToCount[value] = valueToCount[value] + 1

	# write
	dataToWrite = open("DATA/PATTERN/"+str(saveFileName), "w")
	for key in valueToCount.keys():
		support = (float(valueToCount[key])/len(cohorte))*100
		if(support >= minSupport):
			dataToWrite.write(key+";"+str(valueToCount[key])+"\n")
	dataToWrite.close()


#search_FrequentItem(cohorte, "test5.csv", 20)



#searchForPattern(cohorte, 30, 4, "DATA/PATTERN/test2.csv")
#fileName = "DATA/PATTERN/test2.csv"


#--------------------------------------------#
# FUNCTION BUILD FOR CYTOKINES DATA ANALYSIS #######################################
#--------------------------------------------#




def assemble_CohorteFromFile(fileName):
	"""
	-> Assemble discrete cohorte from cytokine data
	-> fileName is the name of the dicrete reduce matrix file
	   (e. g DATA/CYTOKINES/RA_quantitativeMatrix_discrete.csv)
	-> add diagnostic in vectors
	-> Write index variable file in PARAMETERS folder
	-> add "pX" prefix to scalar in vector
	-> return a cohorte (array of arrays)
	"""
	cohorte = []
	listOfVariable = []
	data = open(fileName, "r")
	fileNameInArray = fileName.split("/CYTOKINES/")
	fileNameInArray = fileNameInArray[1].split("_")
	diagnostic = fileNameInArray[0]
	cmpt = 0
	for line in data:
		line = line.split("\n")
		lineInArray = line[0].split(";")
		vector = []
		if(cmpt == 0):
			for variable in lineInArray:
				listOfVariable.append(variable)
		else:
			index = 1
			for scalar in lineInArray:
				newScalar = "p"+str(index)+"_"+scalar
				vector.append(newScalar)
				index += 1
			vector.append(diagnostic)
		cohorte.append(vector)
		cmpt += 1
	data.close()

	# Write indexFile
	indexFile = open("PARAMETERS/"+str(diagnostic)+"_variable_index.csv", "w")
	cmpt = 1
	for variable in listOfVariable:
		indexFile.write("p"+str(cmpt)+";"+variable+"\n")
		cmpt += 1
	indexFile.close()
	return cohorte




def assemble_CohorteFromAllFiles():
	"""
	-> Assemble a "meta" cohorte, with all discrete reduce files
	   in CYTOKINES folder
	-> return a cohorte
	-> Designed for pattern mining
	"""
	listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD", "Control"]
	listOfCohorte = []
	for diagnostic in listOfDisease:
		cohorte = assemble_CohorteFromFile("DATA/CYTOKINES/"+str(diagnostic)+"_quantitativeMatrix_discrete.csv")
		listOfCohorte.append(cohorte)

	metaCohorte = []
	for cohorte in listOfCohorte:
		for vector in cohorte:
			if(len(vector) > 0):
				metaCohorte.append(vector)

	return metaCohorte




def extractPatternFromCohorte(cohorte, minsup):
	"""
	-> Store all frequent pattern (i.e set of items present more than minsup in 
	   cohorte)
	-> cohorte is an array of array, discrete value (obtain via the assemble_CohorteFromAllFiles
	   function)
	-> minsup is an int between 0 and 100
	"""
	saveFileName = "DATA/PATTERN/cytokines_pattern_"+str(minsup)+".csv"
	patternFile = open(saveFileName, "w")
	for itemset in find_frequent_itemsets(cohorte, minsup):
		line = ""
		for element in itemset:
			line = line + str(element) + ";"
		line = line[:-1]
		patternFile.write(line+"\n")
	patternFile.close()




def get_support(patternToTest, controlFile):
	"""
	-> get support (i.e proportion of patient
	   where patternToTest is present)
	-> patternToTest is a list of item
	-> controlFile is the file conatining the cohorte
	   (designed for discrete cohorte), could be "all"
	   for use all the "splited into disease" files
	"""
	if(controlFile == "all"):
		cohorte = assemble_CohorteFromAllFiles()
	else:
		cohorte = assemble_CohorteFromFile(controlFile)
	numberOfPatient = len(cohorte)
	count = 0
	for vector in cohorte:
		patternFound = 1
		for element in patternToTest:
			if element not in vector:
				patternFound = 0
		if(patternFound):
			count +=1
	return (float(count)/float(numberOfPatient))*100




def generate_AssociationRulesFromPatternFile(patternFile, rulesFile, confidenceThreshold, display):
	"""
	-> generate association rules from a list of pattern
	-> patternFile is a fileName (file containing pattern)
	-> rulesFile is the file where pattern are write
	-> confidenceThreshold is the confidence threshold for
	   the rules.
	-> display is a boolean
	TODO:
		-> run a few tests
	"""
	
	listOffrequentItemset = []
	data = open(patternFile, "r")
	for line in data:
		frequentItemSet = []
		line = line.split("\n")
		lineInArray = line[0].split(";")
		for item in lineInArray:
			frequentItemSet.append(item)
		if(len(frequentItemSet) > 1):
			listOffrequentItemset.append(frequentItemSet)
	data.close()

	rulesFile = open(rulesFile, "w")
	for frequentItemSet in listOffrequentItemset:
		tupleLen = 1
		while(tupleLen < len(frequentItemSet)):
			for h in itertools.combinations(frequentItemSet, tupleLen):
				h = list(h)
				complementList = []
				for element in frequentItemSet:
					if(element not in h and element not in complementList):
						complementList.append(element)

				
				rule_confidence = 0
				if(get_support(complementList, "all") != 0):
					rule_confidence = (get_support(frequentItemSet, "all") / get_support(complementList, "all") * 100)

				if(rule_confidence > float(confidenceThreshold)):
					if(display):
						print"-----------------"
						print h
						print complementList
						print frequentItemSet
					rule = ""
					for item in complementList:
					 	rule = rule + item + ";"
					rule = rule[:-1] + " -> "
					for item in h:
						rule = rule + item + ";"
					rule = rule[:-1] + " ["+str(rule_confidence)+"]"
					rulesFile.write(rule+"\n")
					if(display):
						print "----------------"

			tupleLen += 1
	rulesFile.close()




def reformat_RulesFile(rulesFileName):
	"""
	-> Write a new .clp file containing rules
	   for CLIPS.
	-> rulesFileName is a string, the name of
	   the input file (generated by the generate_AssociationRulesFromPatternFile function)
	"""

	inputRulesFileName = rulesFileName
	outputRulesFileName = inputRulesFileName.split(".")
	outputRulesFileName = outputRulesFileName[0]+".clp"
	
	inputRulesFile = open(inputRulesFileName, "r")
	outputRulesFile = open(outputRulesFileName, "w")
	rule_number = 1
	for line in inputRulesFile:
		line = line.split("\n")
		lineInArray = line[0].split(" -> ")
		premice = lineInArray[0]
		
		leftPart = lineInArray[1]
		leftPartInArray = leftPart.split(" ")
		conclusion = leftPartInArray[0]

		rule_number+=1
		
		rule = "(defrule rule_"+str(rule_number)+"\n"
		for element in premice.split(";"):
			rule = rule + " ("+str(element)+")\n"
		rule = rule + "=>\n"
		for element in conclusion.split(";"):
			rule = rule +" (assert ("+str(element)+"))\n"
		rule = rule + ")\n"

		outputRulesFile.write(rule)

	outputRulesFile.close()
	inputRulesFile.close()




def filter_associationRules_confidenceValue(inputFileName, confidenceThreshold):
	"""
	-> Create a filtered file containing rules with
	   a confidence >= confidenceThreshold.
	-> add -cf tag (confidenceThreshold) in output filename
	-> inputFileName is the name of the input file (generated by the generate_AssociationRulesFromPatternFile
	   function)
	-> confidenceThreshold is the ... confidenceThreshold
	"""

	inputRulesFileName = inputFileName
	threshold = confidenceThreshold
	outputRulesFileName = inputRulesFileName.split(".")
	outputRulesFileName = outputRulesFileName[0]+"_cf"+str(threshold)+".csv"
	inputRulesFile = open(inputRulesFileName, "r")
	outputRulesFile = open(outputRulesFileName, "w")
	for line in inputRulesFile:
		line = line.split("\n")
		lineInArray = line[0].split(" -> ")
		premice = lineInArray[0]
			
		leftPart = lineInArray[1]
		leftPartInArray = leftPart.split(" ")
		conclusion = leftPartInArray[0]

		confidence = leftPartInArray[1]
		confidence = confidence[1:-1]
		
		if(float(confidence) >= threshold):
			outputRulesFile.write(line[0]+"\n")

	outputRulesFile.close()
	inputRulesFile.close()




def filter_associationRules_paramaterStatus(inputFileName):
	"""
	-> Create a filtered file containing rules with at least
	   one parameter (in premice or conclusion) not "normal"
	-> add -pf tag (param filtered) in output filename
	-> inputFileName is the name of the input file (generated by the generate_AssociationRulesFromPatternFile
	   function)
	"""

	inputRulesFileName = inputFileName
	outputRulesFileName = inputRulesFileName.split(".")
	outputRulesFileName = outputRulesFileName[0]+"_pf.csv"
	inputRulesFile = open(inputRulesFileName, "r")
	outputRulesFile = open(outputRulesFileName, "w")
	for line in inputRulesFile:
		line = line.split("\n")
		lineInArray = line[0].split(" -> ")
		premice = lineInArray[0]
				
		leftPart = lineInArray[1]
		leftPartInArray = leftPart.split(" ")
		conclusion = leftPartInArray[0]

		allParametersAreNormalInPremice = 1
		for element in premice.split(";"):
			elementInArray = element.split("_")
			if(len(elementInArray) > 1):
				status = elementInArray[1]
				if(status != "normal"):
					allParametersAreNormalInPremice = 0

		allParametersAreNormalInConclusion = 1
		for element in conclusion.split(";"):
			elementInArray = element.split("_")
			if(len(elementInArray) > 1):
				status = elementInArray[1]
				if(status != "normal"):
					allParametersAreNormalInConclusion = 0
		
		if(allParametersAreNormalInPremice and allParametersAreNormalInConclusion):
			print "=> Reject rule"
		else:
			outputRulesFile.write(line[0]+"\n")

	outputRulesFile.close()
	inputRulesFile.close()

