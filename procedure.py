"""
A few procedures
ready to use
"""

import os
from analysis import *
from machineLearning import *
from reorder import *
from preprocessing import *
from patternMining import *



def show_PCA(inputFolder, target, projection, saveFile, dataType, details, show):
	"""
	-> Perform and display PCA
	-> inputFolder is a string, indicate the folder where are patients files
	-> target is a string, currently only "center" and "date" are availabe
	-> projection can be set to "3d" or "2d"
	-> saveFile is a string, used to save graphical
	-> dataType is a string, ndicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	-> details is a boolean, 1 to have details, else 0
	-> show is a boolean, 1 to display graphe, else 0
	"""
	data = generate_DataMatrixFromPatientFiles2(inputFolder, dataType)
	data = scale_Data(data) # Add for test
	y = get_targetedY(target, inputFolder)
	target_name = get_targetNames(target, inputFolder)
	quickPCA(data, y, target_name, projection, saveFile, details, show)
	#quickPCA_test(data, y, target_name, projection, saveFile, details, show)


def show_cluster(inputFolder, numberOfCluster, saveFile):
	"""
	Perform kmean clustering
	-> inputFolder is a string, name of the folder containing data
	-> numberOfCluster is an int, number of cluster to generate
	-> saveFile is a string, filename where graphical output is saved
	"""
	data = generate_DataMatrixFromPatientFiles(inputFolder)
	quickClustering(data, numberOfCluster, saveFile)


def show_correlationMatrix(inputFolder, saveName, dataType, show):
	"""
	-> Compute the correlation matrix for data present in the inputFolder
	-> inputFolder is a string, name of the folder containing data
	-> saveName is a string, used to save graphical
	->  dataType is a string, ndicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	-> show is a boolean, 1 to display graphe, else 0
	"""
	data = generate_DataMatrixFromPatientFiles2(inputFolder, dataType)
	listOfParametres = get_listOfParameters2(inputFolder, dataType)
	display_correlationMatrix(data.transpose(), listOfParametres, saveName, show)


def checkAndFormat(inputFolder, outputFolder):
	"""
	-> clean outputFolder, clean VECTOR folder, convert
	   tab separated files present in inputFolder to semi-column
	   separated diles in outputFolder.
	-> inputFolder is a string
	-> outputFolder is a string
	"""
	
	listOfFilesToDelete = glob.glob(outputFolder+"/*.csv")
	for fileName in listOfFilesToDelete:
		os.remove(fileName)
	listOfFilesToDelete = glob.glob("DATA/VECTOR/*.csv")
	for fileName in listOfFilesToDelete:
		os.remove(fileName)
	convert_tabSepratedFile(inputFolder, outputFolder)



def OverviewOnPanel(panel, dataType, target):
	"""
	-> Peform a few analysis on panel, datatype, focus on
	   target.
	-> panel is a string, folder name
	->  dataType is a string, ndicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	-> targetType is a string, could be:
		- center
		- date
		- disease
	"""
	folder = "DATA/"+str(panel)
	saveName1 = "IMAGES/"+str(panel)+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+str(panel)+"_PCA2D.jpg"
	saveName3 = "IMAGES/"+str(panel)+"_PCA3D.jpg"
	checkAndFormat(folder, "DATA/PATIENT")
	show_correlationMatrix("DATA/PATIENT", saveName1, dataType)
	show_PCA("DATA/PATIENT", target, "2d", saveName2, dataType, 0)
	show_PCA("DATA/PATIENT", target, "3d", saveName3, dataType, 1)


def OverviewOnDisease(disease, control, dataType, target, show):
	"""
	-> Perform a few PCA analysis on a specific disease, compare to a specific
	   control, focus on specific dataType.
	-> disease is a string, specific disease to investigate.
	-> control is a string, specific disease to compare
	->  dataType is a string, ndicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	-> target is a string, could be:
		- center
		- date
		- disease
	-> show is a boolean, 1 to display graphe, else 0
	"""
	saveName1 = "IMAGES/"+str(disease)+"_vs_"+str(control)+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+str(disease)+"_vs_"+str(control)+"_PCA2D.jpg"
	saveName3 = "IMAGES/"+str(disease)+"_vs_"+str(control)+"_PCA3D.jpg"
	show_correlationMatrix("DATA/PATIENT", saveName1, dataType, show)
	show_PCA("DATA/PATIENT", target, "2d", saveName2, dataType, 0, show)
	show_PCA("DATA/PATIENT", target, "3d", saveName3, dataType, 1, show)



def use_SupportVectorMachine(panel, dataType, targetType, target, saveFileName, kernel):
	"""
	IN PROGRESS

	TODO : - pass argument to svmClassification function
		   - resolve module problem on windows
	"""

	checkAndFormat("DATA/"+str(panel), "DATA/PATIENT")
	X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X = PCA(n_components=2).fit_transform(X)
	y = get_targetAgainstTheRest(targetType, target, "DATA/PATIENT")
	scores = svmClassification(X, y, kernel, saveFileName, 0, 1, 0)	



def outlierDetection(targetType1, target1, targetType2, target2, dataType, show):
	"""
	-> targetType (1 & 2) is a string, could be:
		- center
		- date
		- disease
	-> target is a string, the actual center, disease, date
	   you're looking for ( e.g : UBO, RA ... )
	-> dataType is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	-> show is a boolean, if 1: display graphe
	-> TODO:
		- deal with restire_Data() : create bug image for OverviewOnDisease
	"""

	saveFileName = "IMAGES/"+target1+"_vs_"+target2+"_outlierDetection.jpg"

	# training set
	restore_Data()
	apply_filter(targetType1, target1)
	X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X = scale_Data(X)
	X = PCA(n_components=2).fit_transform(X)

	# new observation
	restore_Data()
	apply_filter(targetType2, target2)
	X_test = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X_test = scale_Data(X_test)
	X_test = PCA(n_components=2).fit_transform(X_test)

	show_outlierDetection(X, X_test, target1, target2, saveFileName, show)




def inlierDetection(targetType1, target1, targetType2, target2, dataType, saveFileName):
	"""
	IN PROGRESS

	-> targetType (1 & 2) is a string, could be:
		- center
		- date
		- disease
	-> target is a string, the actual center, disease, date
	   you're looking for ( e.g : UBO, RA ... )
	-> dataType is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	-> saveFileName is a string, filename where the model is saved 

	TODO:
		-> implement panel gestion
	"""

	# training set
	restore_Data()
	apply_filter(targetType1, target1)
	X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X = scale_Data(X)
	X = PCA(n_components=2).fit_transform(X)

	# new observation
	restore_Data()
	apply_filter(targetType2, target2)
	X_test = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X_test = scale_Data(X_test)
	X_test = PCA(n_components=2).fit_transform(X_test)

	show_inlierDetection(saveFileName, X, X_test)



def noveltyDetection(targetType1, target1, targetType2, target2, dataType, show):
	"""
	IN PROGRESS

	-> targetType (1 & 2) is a string, could be:
		- center
		- date
		- disease
	-> target is a string, the actual center, disease, date
	   you're looking for ( e.g : UBO, RA ... )
	-> dataType is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	-> show is a boolean, if 1: display graphe

	-> TODO:
		- deal with restire_Data() : create bug image for OverviewOnDisease

	"""

	saveFileName = "IMAGES/"+target1+"_vs_"+target2+"_noveltyDetection.jpg"

	# training set
	restore_Data()
	apply_filter(targetType1, target1)
	X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X = scale_Data(X)
	X = PCA(n_components=2).fit_transform(X)

	# new observation
	restore_Data()
	apply_filter(targetType2, target2)
	X_test = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", dataType)
	X_test = scale_Data(X_test)
	X_test = PCA(n_components=2).fit_transform(X_test)

	oneClassSvm(X, X_test, target1, target2, saveFileName, show)




	"""GENERAL PROCEDURE"""

def diseaseExplorationProcedure(listOfDisease, listOfPanelToConcat):
	"""
	IN PROGRESS
	"""
	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE")


	print "----PCA Analysis----"
	clean_report()
	clean_image()
	for disease in listOfDisease:

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		optimalThreshold = get_controledValueOfThreshold(cohorte, 60, 5, 3)
		listOfNormalParameters = get_listOfNormalParameters(cohorte, optimalThreshold)


		print "----Perform PCA----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", ["Control", disease])
		remove_parameter("PROPORTION", "mDC1_IN_leukocytes")
		#remove_parameter("ABSOLUTE", "Lymphocytes")
		for parameter in listOfNormalParameters:
			remove_parameter("ABSOLUTE", parameter)
		check_patient()
		save_data()
		OverviewOnDisease("Control", disease, "ABSOLUTE", "disease", 1)


def RunOnFullData():
	"""
	IN PROGRESS
	"""
	listOfElements = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6","PANEL_7","PANEL_8","PANEL_9"]
	for panel in listOfElements:
		folder = "DATA/"+str(panel)
		saveName = str(panel)+"_matrixCorrelation.jpg"
		checkAndFormat(folder, "DATA/PATIENT")
		show_correlationMatrix("DATA/PATIENT", saveName)


def patternMining_run1():
	"""
	- ABSOLUTE data
	- poor discretisation
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE", 0, "Classic")


	for disease in listOfDisease:

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_ABSOLUTE_discretisationAlArrache.csv"
		minNumberOfParamToRemove = 5
		maxTry = 60
		maxNumberOfPattern = 1000
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		searchForPattern(cohorte, maxTry, maxNumberOfPattern, "DATA/PATTERN/"+patternSaveFile)


def patternMining_run2():
	"""
	- ABSOLUTE data
	- discretisation on scaled data
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE", 1, "Classic")


	for disease in listOfDisease:

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		scaleDataInPatientFolder("ABSOLUTE")
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_ABSOLUTE_poorDiscretization_scaledData.csv"
		minNumberOfParamToRemove = 5
		maxTry = 60
		maxNumberOfPattern = 1000
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		searchForPattern(cohorte, maxTry, maxNumberOfPattern, "DATA/PATTERN/"+patternSaveFile)


def patternMining_run2Reverse():
	"""
	- ABSOLUTE data
	- discretisation on scaled data
	"""
	listOfDisease = ["UCTD", "SSc", "SLE", "SjS", "PAPs", "MCTD", "RA"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE", 1, "Classic")


	for disease in listOfDisease:

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		scaleDataInPatientFolder("ABSOLUTE")
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_ABSOLUTE_scaledData_reverseOrder.csv"
		minNumberOfParamToRemove = 5
		maxTry = 60
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		searchForPattern(cohorte, maxTry, "DATA/PATTERN/"+patternSaveFile)


def patternMining_run3():
	"""
	- ABSOLUTE data
	- discretisation using mean Generated threshold
	"""
	listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE", 0, "Mean")


	for disease in listOfDisease:

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_ABSOLUTE_MeanGeneratedThreshold.csv"
		minNumberOfParamToRemove = 10
		maxTry = 60
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		searchForPattern(cohorte, maxTry, "DATA/PATTERN/"+patternSaveFile)


def patternMining_run4():
	"""
	- ABSOLUTE data
	- discretisation using mean Generated threshold
	- dynamic generation threshold
	- delta is a used as a %
	- maxNumberOfPattern limitation is set to 100, i.e
	  when start to generate more than 1000 pattern, stop
	  the mining. (trying to avoid memory issues)
	"""
	listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
	

	for disease in listOfDisease:

		delta = 0
		print "----Distribution Analysis----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", "Control")
		threshold = get_ThresholdValue_DynamicDelta("ABSOLUTE", 1, "Mean", delta)

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		discretization(threshold)

		print "----Pattern Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_ABSOLUTE_MeanGeneratedThreshold.csv"
		minNumberOfParamToRemove = 10
		maxTry = 60
		maxNumberOfPattern = 1000
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		searchForPattern(cohorte, maxTry, maxNumberOfPattern, "DATA/PATTERN/"+patternSaveFile)

		# control number of pattern after filter
		fileName = "DATA/PATTERN/"+patternSaveFile
		filter_Pattern("DATA/PATTERN/"+patternSaveFile)
		filterDataName = fileName.split(".")
		heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
		lowFilterName = filterDataName[0] + "_LowFilter.csv"

		cmpt = 0
		dataToInspect = open(lowFilterName, "r")
		for line in dataToInspect:
			cmpt = cmpt + 1
		dataToInspect.close()

		if(cmpt < 0):
			goodDiscretization = 0
		else:
			goodDiscretization = 1


		while(not goodDiscretization):

			print "----Distribution Analysis (delta exploration)----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", "Control")
			delta = delta + 0.05
			threshold = get_ThresholdValue_DynamicDelta("ABSOLUTE", 1, "Mean", delta)

			print "----Pattern Mining on "+str(disease)+" (delta exploration)----"

			print "----Discretization (delta exploration)----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", disease)
			check_patient()
			discretization(threshold)

			print "----Pattern Mining (delta exploration)----"
			cohorte = assemble_Cohorte()
			patternSaveFile = disease+"_ABSOLUTE_MeanGeneratedThreshold.csv"
			minNumberOfParamToRemove = 10
			maxTry = 60
			maxNumberOfPattern = 1000
			machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
			cohorte = alleviate_cohorte(cohorte, machin)
			searchForPattern(cohorte, maxTry, maxNumberOfPattern, "DATA/PATTERN/"+patternSaveFile)

			# control number of pattern after filter
			fileName = "DATA/PATTERN/"+patternSaveFile
			filter_Pattern("DATA/PATTERN/"+patternSaveFile)
			filterDataName = fileName.split(".")
			heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
			lowFilterName = filterDataName[0] + "_LowFilter.csv"

			cmpt = 0
			dataToInspect = open(lowFilterName, "r")
			for line in dataToInspect:
				cmpt = cmpt + 1
			dataToInspect.close()

			if(cmpt == 0):
				goodDiscretization = 0
			else:
				goodDiscretization = 1

			if(delta == 1):
				break



def FrequentItemMining():
	"""
	- ABSOLUTE data
	- discretisation on scaled data
	- frequent item retrieval, no pattern mining
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	print "----Distribution Analysis----"
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", "Control")
	threshold = get_ThresholdValue("ABSOLUTE", 1, "Classic")


	for disease in listOfDisease:

		print "----Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		scaleDataInPatientFolder("ABSOLUTE")
		discretization(threshold)

		print "----Frequent Item Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_FrequentItem_ABSOLUTE_poorDiscretization_scaledData.csv"
		minNumberOfParamToRemove = 5
		maxTry = 60
		maxNumberOfPattern = 1000
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		search_FrequentItem(cohorte, patternSaveFile)


def FrequentItemMining2(minSupport, dataType):
	"""
	IN PROGRESS (adapt to PROPORTION data)
	- ABSOLUTE data
	- discretisation using mean Generated threshold
	- dynamic generation threshold
	- delta is a used as a %
	- frequent item retrieval, no pattern mining
	- minSupport is a float, % of patient in cohorte that must
	  suppport the item
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
	

	# Initilaise log file
	logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+"_"+dataType+".log", "w")
	logFile.close()

	for disease in listOfDisease:

		delta = 0
		print "----Distribution Analysis----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", "Control")
		threshold = get_ThresholdValue_DynamicDelta(dataType, 1, "Mean", delta)

		print "----Pattern Mining on "+str(disease)+"----"

		print "----Discretization----"
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", disease)
		check_patient()
		scaleDataInPatientFolder(dataType)
		discretization(threshold)

		print "----Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold.csv"
		minNumberOfParamToRemove = 10
		maxTry = 60
		maxNumberOfPattern = 1000
		machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
		cohorte = alleviate_cohorte(cohorte, machin)
		search_FrequentItem(cohorte, patternSaveFile, minSupport)

		# control number of pattern after filter
		fileName = "DATA/PATTERN/"+patternSaveFile
		filter_Pattern("DATA/PATTERN/"+patternSaveFile)
		filterDataName = fileName.split(".")
		heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
		lowFilterName = filterDataName[0] + "_LowFilter.csv"

		cmpt = 0
		dataToInspect = open(lowFilterName, "r")
		for line in dataToInspect:
			cmpt = cmpt + 1
		dataToInspect.close()

		if(cmpt == 0):
			goodDiscretization = 0
		else:
			goodDiscretization = 1


		while(not goodDiscretization):

			print "----Distribution Analysis (delta exploration)----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", "Control")
			delta = delta + 0.05
			threshold = get_ThresholdValue_DynamicDelta(dataType, 1, "Mean", delta)

			print "----Mining on "+str(disease)+" (delta exploration)----"

			print "----Discretization (delta exploration)----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", disease)
			check_patient()
			scaleDataInPatientFolder(dataType)
			discretization(threshold)

			print "----Mining (delta exploration)----"
			cohorte = assemble_Cohorte()
			patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold.csv"
			minNumberOfParamToRemove = 10
			maxTry = 60
			maxNumberOfPattern = 1000
			machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
			cohorte = alleviate_cohorte(cohorte, machin)
			search_FrequentItem(cohorte, patternSaveFile, minSupport)

			# control number of pattern after filter
			fileName = "DATA/PATTERN/"+patternSaveFile
			filter_Pattern("DATA/PATTERN/"+patternSaveFile)
			filterDataName = fileName.split(".")
			heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
			lowFilterName = filterDataName[0] + "_LowFilter.csv"

			cmpt = 0
			dataToInspect = open(lowFilterName, "r")
			for line in dataToInspect:
				cmpt = cmpt + 1
			dataToInspect.close()

			if(cmpt == 0):
				goodDiscretization = 0
			else:
				goodDiscretization = 1

			if(delta == 1):
				break

		# write in log file
		numberOfItem = 0
		dataToInspect = open(heavyFilterName, "r")
		for line in dataToInspect:
			numberOfItem = numberOfItem + 1
		dataToInspect.close()
		logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+"_"+dataType+".log", "a")
		logFile.write(disease+";"+str(numberOfItem)+";"+str(minSupport)+";"+str(delta)+"\n")
		logFile.close()






def FrequentItemMining3(minSupport, controlDisease, dataType):
	"""
	IN PROGRESS
	- discretisation using mean Generated threshold
	- dynamic generation threshold
	- delta is a used as a %
	- frequent item retrieval, no pattern mining
	- minSupport is a float, % of patient in cohorte that must
	  suppport the item
	- use controlDisease as a control for discretization process
	TODO:
		- test with dataType
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
	

	# Initilaise log file
	logFile = open("DATA/PATTERN/FrequentItemMining_"+str(minSupport)+"_discretizationWith"+str(controlDisease)+"_"+dataType+".log", "w")
	logFile.close()

	for disease in listOfDisease:
		if(disease != controlDisease):
			delta = 0
			print "----Distribution Analysis----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", controlDisease)
			check_patient()
			threshold = get_ThresholdValue_DynamicDelta(dataType, 1, "Mean", delta)

			print "----Pattern Mining on "+str(disease)+"----"

			print "----Discretization----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", disease)
			check_patient()
			scaleDataInPatientFolder(dataType)
			discretization(threshold)

			print "----Mining----"
			cohorte = assemble_Cohorte()
			patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_discretizationWith"+controlDisease+"_"+dataType+"_meanGeneratedThreshold.csv"
			minNumberOfParamToRemove = 10
			maxTry = 60
			maxNumberOfPattern = 1000
			machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
			cohorte = alleviate_cohorte(cohorte, machin)
			search_FrequentItem(cohorte, patternSaveFile, minSupport)

			# control number of pattern after filter
			fileName = "DATA/PATTERN/"+patternSaveFile
			filter_Pattern("DATA/PATTERN/"+patternSaveFile)
			filterDataName = fileName.split(".")
			heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
			lowFilterName = filterDataName[0] + "_LowFilter.csv"

			cmpt = 0
			dataToInspect = open(lowFilterName, "r")
			for line in dataToInspect:
				cmpt = cmpt + 1
			dataToInspect.close()

			if(cmpt == 0):
				goodDiscretization = 0
			else:
				goodDiscretization = 1


			while(not goodDiscretization):

				print "----Distribution Analysis (delta exploration)----"
				clean_folders("ALL")
				fusion_panel(listOfPanelToConcat)
				checkAndFormat("DATA/FUSION", "DATA/PATIENT")
				apply_filter("disease", controlDisease)
				check_patient()
				delta = delta + 0.05
				threshold = get_ThresholdValue_DynamicDelta(dataType, 1, "Mean", delta)

				print "----Mining on "+str(disease)+" (delta exploration)----"

				print "----Discretization (delta exploration)----"
				clean_folders("ALL")
				fusion_panel(listOfPanelToConcat)
				checkAndFormat("DATA/FUSION", "DATA/PATIENT")
				apply_filter("disease", disease)
				check_patient()
				scaleDataInPatientFolder(dataType)
				discretization(threshold)

				print "----Mining (delta exploration)----"
				cohorte = assemble_Cohorte()
				patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_discretizationWith"+controlDisease+"_"+dataType+"_meanGeneratedThreshold.csv"
				minNumberOfParamToRemove = 10
				maxTry = 60
				maxNumberOfPattern = 1000
				machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
				cohorte = alleviate_cohorte(cohorte, machin)
				search_FrequentItem(cohorte, patternSaveFile, minSupport)

				# control number of pattern after filter
				fileName = "DATA/PATTERN/"+patternSaveFile
				filter_Pattern("DATA/PATTERN/"+patternSaveFile)
				filterDataName = fileName.split(".")
				heavyFilterName = filterDataName[0] + "_HeavyFilter.csv"
				lowFilterName = filterDataName[0] + "_LowFilter.csv"

				cmpt = 0
				dataToInspect = open(lowFilterName, "r")
				for line in dataToInspect:
					cmpt = cmpt + 1
				dataToInspect.close()

				if(cmpt == 0):
					goodDiscretization = 0
				else:
					goodDiscretization = 1

				if(delta == 1):
					break

			# write in log file
			numberOfItem = 0
			dataToInspect = open(heavyFilterName, "r")
			for line in dataToInspect:
				numberOfItem = numberOfItem + 1
			dataToInspect.close()
			logFile = open("DATA/PATTERN/FrequentItemMining_"+str(minSupport)+"_discretizationWith"+str(controlDisease)+"_"+dataType+".log", "a")
			logFile.write(disease+";"+str(numberOfItem)+";"+str(minSupport)+";"+str(delta)+"\n")
			logFile.close()



def visualisation3(disease, control):
	"""
	IN PROGRESS
	"""

	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", [disease, control])
	check_patient()

	filter_Pattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold.csv")
	convert_PatternFile("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter.csv")
	parametersOfInterest_disease = extract_parametersFromPattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)
	parametersOfInterest_control = []
	if(control != "Control"):
		parametersOfInterest_control = extract_parametersFromPattern("DATA/PATTERN/"+control+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)
	
	parametersOfInterest = parametersOfInterest_control + parametersOfInterest_disease
	listOfAllParameters = get_allParam("ABSOLUTE")
	for parameter in listOfAllParameters:
		if(parameter not in parametersOfInterest):
			remove_parameter("ABSOLUTE", parameter)

	filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	filter_ArtefactValue("ABSOLUTE", "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells", 1000000)
	filter_ArtefactValue("ABSOLUTE", "gdpos_Tcells", 20000)

	#filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "Monocytes", 1200)
	#filter_ArtefactValue("ABSOLUTE", "CD14highCD16neg_classicalMonocytes", 1000)
	#filter_ArtefactValue("ABSOLUTE", "CD15highCD16neg_Eosinophils", 800)
	#filter_ArtefactValue("ABSOLUTE", "CD15lowCD16high_Neutrophils", 1100)
	#filter_ArtefactValue("ABSOLUTE", "CD69pos_activated_CD4pos_Tcells", 600)
	#filter_ArtefactValue("ABSOLUTE", "CD8pos_CD57pos_Cytotoxic_Tcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "CD14pos_monocytes", 1200)

	check_patient()
	save_data()

	saveName1 = "IMAGES/"+disease+"_vs_"+control+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+disease+"_vs_"+control+"_PCA2D.jpg"
	show_correlationMatrix("DATA/PATIENT", saveName1, "ABSOLUTE", 1)
	show_PCA("DATA/PATIENT", "disease", "2d", saveName2, "ABSOLUTE", 1, 1)


def visualisation2(disease, control, dataType, minSupport):
	"""
	IN PROGRESS
	"""

	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]

	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", [disease, control])
	check_patient()

	filter_Pattern("DATA/PATTERN/"+disease+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold.csv")
	convert_PatternFile("DATA/PATTERN/"+disease+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold_HeavyFilter.csv")
	parametersOfInterest_disease = extract_parametersFromPattern("DATA/PATTERN/"+disease+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)	
	parametersOfInterest_control = []
	if(control != "Control"):
		parametersOfInterest_control = extract_parametersFromPattern("DATA/PATTERN/"+control+"_FrequentItem_"+str(minSupport)+"_"+dataType+"_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)

	parametersOfInterest = parametersOfInterest_control + parametersOfInterest_disease
	listOfAllParameters = get_allParam(dataType)

	listOfAllParameters = get_allParam(dataType)
	for parameter in listOfAllParameters:
		if(parameter not in parametersOfInterest):
			remove_parameter(dataType, parameter)

	filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	filter_ArtefactValue("ABSOLUTE", "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells", 1000000)
	filter_ArtefactValue("ABSOLUTE", "gdpos_Tcells", 20000)

	#filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "Monocytes", 1200)
	#filter_ArtefactValue("ABSOLUTE", "CD14highCD16neg_classicalMonocytes", 1000)
	#filter_ArtefactValue("ABSOLUTE", "CD15highCD16neg_Eosinophils", 800)
	#filter_ArtefactValue("ABSOLUTE", "CD15lowCD16high_Neutrophils", 1100)
	#filter_ArtefactValue("ABSOLUTE", "CD69pos_activated_CD4pos_Tcells", 600)
	#filter_ArtefactValue("ABSOLUTE", "CD8pos_CD57pos_Cytotoxic_Tcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "CD14pos_monocytes", 1200)

	check_patient()
	save_data()

	saveName1 = "IMAGES/"+disease+"_vs_"+control+"_"+dataType+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+disease+"_vs_"+control+"_"+dataType+"_PCA2D.jpg"
	show_correlationMatrix("DATA/PATIENT", saveName1, dataType, 1)
	show_PCA("DATA/PATIENT", "disease", "2d", saveName2, dataType, 1, 1)




def plot_autoantibodiesData(diagnostic, displayAll):
	"""
	-> Plot 4 bar graphe to show the number
	   of patient positive and negatove for each
	   autoantobodies
	-> diagnostuc could be a string:
		- Control
	   	- RA
	   	- MCTD 
	   	- PAPs 
	   	- SjS 
	   	- SLE 
	   	- SSc 
	   	- UCTD
	   	- all
	  Could be a list of string.
	  Set to all, i.e list of all elements.
	  Set to overview, list of all elements, display % (not raw count)
	  
	-> displayAll is a boolean, set to 1 all the data
	   (i.e positive and negative count) are display, set to 0
	   only the positive count are displayed
	   only for multiple disease plot.
	"""
	displayAll = int(displayAll)

	if isinstance(diagnostic, list):
		
		db = TinyDB("DATA/DATABASES/machin.json")
		AutoantibodyTable = db.table('Autoantibody')
		Patient = Query()

		DiseaseToData = {}
		DiseaseToParameterToCount = {}
		for disease in diagnostic:
			test_function = lambda s: s in get_listOfPatientWithDiagnostic(disease)
			machin = AutoantibodyTable.search(Patient.OMIC_ID.test(test_function))
			listOfSelectedParameter = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL", "B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL", "SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL", "U1_RNP_CALL", "ENA_CALL", "RF_CALL", "B2M_CALL", "CLM_CALL"]
			data = parse_request(machin, listOfSelectedParameter)
			DiseaseToData[disease] = data

			# Initialise count dictionnary
			parameterToCount = {}
			for param in data[0]:
				param_negative = str(param)+"_negative"
				param_positive = str(param)+"_positive"
				parameterToCount[param_negative] = 0
				parameterToCount[param_positive] = 0

			# Remplir dictionnary
			for patient in data:
				for key in patient.keys():
					
					key_negative = str(key)+"_negative"
					key_positive = str(key)+"_positive"

					if(patient[key] == "negative"):
						parameterToCount[key_negative] += 1
					elif(patient[key] == "positive"):
						parameterToCount[key_positive] += 1

			DiseaseToParameterToCount[disease] = parameterToCount

		paramForSubPlot1 = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL"]
		paramForSubPlot2 = ["B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL"]
		paramForSubPlot3 = ["SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL"]
		paramForSubPlot4 = ["U1_RNP_CALL", "ENA_CALL", "B2M_CALL", "CLM_CALL"]

		listOfParametres = paramForSubPlot1 + paramForSubPlot2 + paramForSubPlot3 + paramForSubPlot4

		fig = plt.figure()
		ax = fig.add_subplot(111,projection='3d')
		width = 1.5

		for z in range(len(diagnostic)):
			disease = diagnostic[z]
			xs_positive = range(0, len(listOfParametres)*5, 5)
			xs_negative = []
			for position in xs_positive:
				xs_negative.append(position + width)

			ys_positive = []
			ys_negative = []
			for param in listOfParametres:
				param_positive = str(param)+"_positive"
				param_negative = str(param)+"_negative"
				ys_positive.append(DiseaseToParameterToCount[disease][param_positive])
				ys_negative.append(DiseaseToParameterToCount[disease][param_negative])		

			ax.bar(xs_positive, ys_positive, zs=z, zdir='y', color="blue", alpha=0.8)
			if(displayAll):
				ax.bar(xs_negative, ys_negative, zs=z, zdir='y', color="red", alpha=0.8)

			xTickMarks = [param for param in listOfParametres]
			ax.set_xticks(xs_positive)
			xtickNames = ax.set_xticklabels(xTickMarks)
			plt.setp(xtickNames, rotation=90, fontsize=10)

			yTickMarks = [param for param in diagnostic]
			ax.set_yticks(range(len(diagnostic)))
			ytickNames = ax.set_yticklabels(yTickMarks)
			plt.setp(ytickNames, rotation=45, fontsize=10)

		ax.set_zlabel('Count')
		fig.canvas.set_window_title("Autoantobodies")
		plt.show()
		
	elif(diagnostic == "all"):
		db = TinyDB("DATA/DATABASES/machin.json")
		AutoantibodyTable = db.table('Autoantibody')
		Patient = Query()
		diagnostic = ["Control", "RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
		DiseaseToData = {}
		DiseaseToParameterToCount = {}
		for disease in diagnostic:
			test_function = lambda s: s in get_listOfPatientWithDiagnostic(disease)
			machin = AutoantibodyTable.search(Patient.OMIC_ID.test(test_function))
			listOfSelectedParameter = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL", "B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL", "SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL", "U1_RNP_CALL", "ENA_CALL", "RF_CALL", "B2M_CALL", "CLM_CALL"]
			data = parse_request(machin, listOfSelectedParameter)
			DiseaseToData[disease] = data

			# Initialise count dictionnary
			parameterToCount = {}
			for param in data[0]:
				param_negative = str(param)+"_negative"
				param_positive = str(param)+"_positive"
				parameterToCount[param_negative] = 0
				parameterToCount[param_positive] = 0

			# Remplir dictionnary
			for patient in data:
				for key in patient.keys():
					key_negative = str(key)+"_negative"
					key_positive = str(key)+"_positive"
					if(patient[key] == "negative"):
						parameterToCount[key_negative] += 1
					elif(patient[key] == "positive"):
						parameterToCount[key_positive] += 1

			DiseaseToParameterToCount[disease] = parameterToCount
		paramForSubPlot1 = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL"]
		paramForSubPlot2 = ["B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL"]
		paramForSubPlot3 = ["SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL"]
		paramForSubPlot4 = ["U1_RNP_CALL", "ENA_CALL", "B2M_CALL", "CLM_CALL"]
		listOfParametres = paramForSubPlot1 + paramForSubPlot2 + paramForSubPlot3 + paramForSubPlot4

		fig = plt.figure()
		ax = fig.add_subplot(111,projection='3d')
		width = 1.5
		for z in range(len(diagnostic)):
			disease = diagnostic[z]
			xs_positive = range(0, len(listOfParametres)*5, 5)
			xs_negative = []
			for position in xs_positive:
				xs_negative.append(position + width)

			ys_positive = []
			ys_negative = []
			for param in listOfParametres:
				param_positive = str(param)+"_positive"
				param_negative = str(param)+"_negative"
				ys_positive.append(DiseaseToParameterToCount[disease][param_positive])
				ys_negative.append(DiseaseToParameterToCount[disease][param_negative])		

			ax.bar(xs_positive, ys_positive, zs=z, zdir='y', color="blue", alpha=0.8)
			if(displayAll):
				ax.bar(xs_negative, ys_negative, zs=z, zdir='y', color="red", alpha=0.8)

			xTickMarks = [param for param in listOfParametres]
			ax.set_xticks(xs_positive)
			xtickNames = ax.set_xticklabels(xTickMarks)
			plt.setp(xtickNames, rotation=90, fontsize=10)

			yTickMarks = [param for param in diagnostic]
			ax.set_yticks(range(len(diagnostic)))
			ytickNames = ax.set_yticklabels(yTickMarks)
			plt.setp(ytickNames, rotation=45, fontsize=10)

		ax.set_zlabel('Count')
		fig.canvas.set_window_title("Autoantobodies")
		plt.show()

	

	elif(diagnostic == "overview"):
		
		db = TinyDB("DATA/DATABASES/machin.json")
		AutoantibodyTable = db.table('Autoantibody')
		Patient = Query()
		diagnostic = ["Control", "RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
		DiseaseToData = {}
		DiseaseToParameterToCount = {}
		for disease in diagnostic:
			test_function = lambda s: s in get_listOfPatientWithDiagnostic(disease)
			machin = AutoantibodyTable.search(Patient.OMIC_ID.test(test_function))
			listOfSelectedParameter = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL", "B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL", "SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL", "U1_RNP_CALL", "ENA_CALL", "RF_CALL", "B2M_CALL", "CLM_CALL"]
			data = parse_request(machin, listOfSelectedParameter)
			DiseaseToData[disease] = data

			# Initialise count dictionnary
			parameterToCount = {}
			for param in data[0]:
				param_negative = str(param)+"_negative"
				param_positive = str(param)+"_positive"
				parameterToCount[param_negative] = 0
				parameterToCount[param_positive] = 0

			# Remplir dictionnary
			for patient in data:
				for key in patient.keys():
					key_negative = str(key)+"_negative"
					key_positive = str(key)+"_positive"
					if(patient[key] == "negative"):
						parameterToCount[key_negative] += 1
					elif(patient[key] == "positive"):
						parameterToCount[key_positive] += 1

			DiseaseToParameterToCount[disease] = parameterToCount
		paramForSubPlot1 = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL"]
		paramForSubPlot2 = ["B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL"]
		paramForSubPlot3 = ["SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL"]
		paramForSubPlot4 = ["U1_RNP_CALL", "ENA_CALL", "B2M_CALL", "CLM_CALL"]
		listOfParametres = paramForSubPlot1 + paramForSubPlot2 + paramForSubPlot3 + paramForSubPlot4
		listOfParametres_part1 = paramForSubPlot1 + paramForSubPlot2
		listOfParametres_part2 = paramForSubPlot3 + paramForSubPlot4

		fig, ((ax1), (ax2)) = plt.subplots(nrows=2, ncols=1)

		N = 8
		positiveCount_Control = []
		positiveCount_RA = []
		positiveCount_MCTD = []
		positiveCount_PAPs = []
		positiveCount_SjS = []
		positiveCount_SLE = []
		positiveCount_SSc = []
		positiveCount_UCTD = []
		for param in listOfParametres_part1:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
		
			parameterToCount = DiseaseToParameterToCount["Control"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_Control.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["RA"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_RA.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["MCTD"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_MCTD.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["PAPs"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_PAPs.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SjS"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SjS.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SLE"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SLE.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SSc"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SSc.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["UCTD"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_UCTD.append((float(parameterToCount[param_positive])/float(total_count))*100)

		ind = np.arange(N)                # the x locations for the groups
		width = 0.10                      # the width of the bars
		
		rects_Control = ax1.bar(ind, positiveCount_Control, width, color='blue')
		rects_RA = ax1.bar(ind+width, positiveCount_RA, width, color='red')
		rects_MCTD = ax1.bar(ind+width*2, positiveCount_MCTD, width, color='green')
		rects_PAPs = ax1.bar(ind+width*3, positiveCount_PAPs, width, color='yellow')
		rects_SjS = ax1.bar(ind+width*4, positiveCount_SjS, width, color='grey')
		rects_SLE = ax1.bar(ind+width*5, positiveCount_SLE, width, color='black')
		rects_SSc = ax1.bar(ind+width*6, positiveCount_SSc, width, color='orange')
		rects_UCTD = ax1.bar(ind+width*7, positiveCount_UCTD, width, color='cyan')


		ax1.set_xlim(-width,len(ind)+width)
		ax1.set_ylim(0,100)
		ax1.set_ylabel("% of positive")
		#ax1.set_title('Autoantibody')
		xTickMarks = [param for param in listOfParametres_part1]
		ax1.set_xticks(ind+width*4)
		xtickNames = ax1.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()

		N = 8
		positiveCount_Control = []
		positiveCount_RA = []
		positiveCount_MCTD = []
		positiveCount_PAPs = []
		positiveCount_SjS = []
		positiveCount_SLE = []
		positiveCount_SSc = []
		positiveCount_UCTD = []
		for param in listOfParametres_part2:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
		
			parameterToCount = DiseaseToParameterToCount["Control"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_Control.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["RA"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_RA.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["MCTD"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_MCTD.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["PAPs"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_PAPs.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SjS"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SjS.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SLE"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SLE.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["SSc"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_SSc.append((float(parameterToCount[param_positive])/float(total_count))*100)

			parameterToCount = DiseaseToParameterToCount["UCTD"]
			total_count = parameterToCount[param_positive] + parameterToCount[param_negative]
			positiveCount_UCTD.append((float(parameterToCount[param_positive])/float(total_count))*100)


		ind = np.arange(N)                # the x locations for the groups
		width = 0.10                      # the width of the bars
		
		rects_Control = ax2.bar(ind+10, positiveCount_Control, width, color='blue')
		rects_RA = ax2.bar(ind+width, positiveCount_RA, width, color='red')
		rects_MCTD = ax2.bar(ind+width*2, positiveCount_MCTD, width, color='green')
		rects_PAPs = ax2.bar(ind+width*3, positiveCount_PAPs, width, color='yellow')
		rects_SjS = ax2.bar(ind+width*4, positiveCount_SjS, width, color='grey')
		rects_SLE = ax2.bar(ind+width*5, positiveCount_SLE, width, color='black')
		rects_SSc = ax2.bar(ind+width*6, positiveCount_SSc, width, color='orange')
		rects_UCTD = ax2.bar(ind+width*7, positiveCount_UCTD, width, color='cyan')


		ax2.set_xlim(-width,len(ind)+width)
		ax2.set_ylim(0,100)
		ax2.set_ylabel("% of positive")
		#ax2.set_title('Autoantibody')
		xTickMarks = [param for param in listOfParametres_part2]
		ax2.set_xticks(ind+width*4)
		xtickNames = ax2.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()


		ax1.legend( (rects_Control[0], rects_RA[0], rects_MCTD[0], rects_SSc[0], rects_UCTD[0], rects_SLE[0], rects_SjS[0], rects_PAPs[0]), 
			('Control', 'RA', 'MCTD', 'SSc', 'UCTD', 'SLE', 'SjS', 'PAPs') )
		fig.canvas.set_window_title("Overview")
		plt.show()

	else:
		db = TinyDB("DATA/DATABASES/machin.json")
		AutoantibodyTable = db.table('Autoantibody')
		Patient = Query()
		test_function = lambda s: s in get_listOfPatientWithDiagnostic(diagnostic)
		machin = AutoantibodyTable.search(Patient.OMIC_ID.test(test_function))
		listOfSelectedParameter = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL", "B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL", "SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL",
		"U1_RNP_CALL", "ENA_CALL", "RF_CALL", "B2M_CALL", "CLM_CALL"]
		data = parse_request(machin, listOfSelectedParameter)

		# Initialise count dictionnary
		parameterToCount = {}
		for param in data[0]:
			param_negative = str(param)+"_negative"
			param_positive = str(param)+"_positive"
			parameterToCount[param_negative] = 0
			parameterToCount[param_positive] = 0

		# Remplir dictionnary
		for patient in data:
			for key in patient.keys():
				
				key_negative = str(key)+"_negative"
				key_positive = str(key)+"_positive"

				if(patient[key] == "negative"):
					parameterToCount[key_negative] += 1
				elif(patient[key] == "positive"):
					parameterToCount[key_positive] += 1

		structureToPlot = parameterToCount

		paramForSubPlot1 = ["CLG_CALL", "RF_CALL", "SSB_CALL", "SCL70_CALL"]
		paramForSubPlot2 = ["B2G_CALL", "CCP2_CALL", "SSA_CALL", "DNA_CALL"]
		paramForSubPlot3 = ["SM_CALL", "MPO_CALL", "JO1_CALL", "PR3_CALL"]
		paramForSubPlot4 = ["U1_RNP_CALL", "ENA_CALL", "B2M_CALL", "CLM_CALL"]

		# Graphic representation
		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

		# Subplot 1
		N = 4
		positiveCount = []
		negativeCount = []
		for param in paramForSubPlot1:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
			positiveCount.append(parameterToCount[param_positive])
			negativeCount.append(parameterToCount[param_negative])
		ind = np.arange(N)                # the x locations for the groups
		width = 0.35                      # the width of the bars
		rects1 = ax1.bar(ind, positiveCount, width, color='blue')
		rects2 = ax1.bar(ind+width, negativeCount, width, color='red')
		ax1.set_xlim(-width,len(ind)+width)
		ax1.set_ylim(0,45)
		ax1.set_ylabel('Count')
		ax1.set_title('Autoantibody')
		xTickMarks = [param for param in paramForSubPlot1]
		ax1.set_xticks(ind+width)
		xtickNames = ax1.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()

		# Subplot 2
		N = 4
		positiveCount = []
		negativeCount = []
		for param in paramForSubPlot2:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
			positiveCount.append(parameterToCount[param_positive])
			negativeCount.append(parameterToCount[param_negative])
		ind = np.arange(N)                # the x locations for the groups
		width = 0.35                      # the width of the bars
		rects1 = ax2.bar(ind, positiveCount, width, color='blue')
		rects2 = ax2.bar(ind+width, negativeCount, width, color='red')
		ax2.set_xlim(-width,len(ind)+width)
		ax2.set_ylim(0,45)
		ax2.set_ylabel('Count')
		ax2.set_title('Autoantibody')
		xTickMarks = [param for param in paramForSubPlot2]
		ax2.set_xticks(ind+width)
		xtickNames = ax2.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()

		# Subplot 3
		N = 4
		positiveCount = []
		negativeCount = []
		for param in paramForSubPlot3:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
			positiveCount.append(parameterToCount[param_positive])
			negativeCount.append(parameterToCount[param_negative])
		ind = np.arange(N)                # the x locations for the groups
		width = 0.35                      # the width of the bars
		rects1 = ax3.bar(ind, positiveCount, width, color='blue')
		rects2 = ax3.bar(ind+width, negativeCount, width, color='red')
		ax3.set_xlim(-width,len(ind)+width)
		ax3.set_ylim(0,45)
		ax3.set_ylabel('Count')
		ax3.set_title('Autoantibody')
		xTickMarks = [param for param in paramForSubPlot3]
		ax3.set_xticks(ind+width)
		xtickNames = ax3.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()

		# Subplot 4
		N = 4
		positiveCount = []
		negativeCount = []
		for param in paramForSubPlot4:
			param_positive = str(param)+"_positive"
			param_negative = str(param)+"_negative"
			positiveCount.append(parameterToCount[param_positive])
			negativeCount.append(parameterToCount[param_negative])
		ind = np.arange(N)                # the x locations for the groups
		width = 0.35                      # the width of the bars
		rects1 = ax4.bar(ind, positiveCount, width, color='blue')
		rects2 = ax4.bar(ind+width, negativeCount, width, color='red')
		ax4.set_xlim(-width,len(ind)+width)
		ax4.set_ylim(0,45)
		ax4.set_ylabel('Count')
		ax4.set_title('Autoantibody')
		xTickMarks = [param for param in paramForSubPlot3]
		ax4.set_xticks(ind+width)
		xtickNames = ax4.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=45, fontsize=10)
		plt.tight_layout()

		ax1.legend( (rects1[0], rects2[0]), ('Positive', 'Negative') )
		fig.canvas.set_window_title(diagnostic)
		plt.show()

def describe_discreteVariable(discreteCohorte, discreteVariableName):
	"""
	-> Describe discrete variable, enumerate possible status
	   and dispplay proportion of NA values
	-> discreteCohorte is a cohorte of discrete parameter
	   (obtain with the assemble_CohorteFromDiscreteAllFiles function)
	-> discreteVariableName the name of the discrete variable to check
	   (could be the real name or just the pX associated)
	"""
	numberOfPatientINCohorte = len(discreteCohorte)
	paramToNonAvailableCount = {}

	# Init paramToNonAvailableCount 
	for patient in discreteCohorte:
		cmpt = 1
		for scalar in patient:
			scalarInArray = scalar.split("_")
			if(len(scalarInArray) > 1):
				paramToNonAvailableCount[scalarInArray[0]] = 0
			cmpt += 1

	# Remplir Dict
	for patient in discreteCohorte:
		cmpt = 1
		for scalar in patient:
			scalarInArray = scalar.split("_")
			if(len(scalarInArray) > 1):
				if(scalarInArray[1] == "NA"):
					paramToNonAvailableCount[scalarInArray[0]] += 1
			cmpt += 1
	# Parse variable
	if("\\" in discreteVariableName):

		realVariableName = discreteVariableName
		parameterIndexNumber = "undef"
		parameterIndex = open("PARAMETERS/Control_variable_index.csv")

		for line in parameterIndex:
			line = line.split("\n")
			lineInArray = line[0].split(";")
			if(lineInArray[1] == discreteVariableName):
				parameterIndexNumber = lineInArray[0]
		parameterIndex.close()

		if(parameterIndex != "undef"):


			listOfPossibleStatus = []
			statusToCount = {}
			for patient in discreteCohorte:
				for scalar in patient:
					scalarInArray = scalar.split("_")
					if(len(scalarInArray) > 1):
						param = scalarInArray[0]
						if(param == parameterIndexNumber):
							if(scalarInArray[1] != "NA" and scalarInArray[1] not in listOfPossibleStatus):
								listOfPossibleStatus.append(scalarInArray[1])
			
			for status in listOfPossibleStatus:
				statusToCount[status] = 0
			for patient in discreteCohorte:
				for scalar in patient:
					scalarInArray = scalar.split("_")
					if(len(scalarInArray) > 1):
						param = scalarInArray[0]
						if(param == parameterIndexNumber):
							if(scalarInArray[1] in listOfPossibleStatus):
								statusToCount[scalarInArray[1]] += 1


			fig, ((ax1), (ax2)) = plt.subplots(nrows=1, ncols=2)
			nonAvailableProportion = (float(paramToNonAvailableCount[parameterIndexNumber]) / float(len(discreteCohorte)))*100
			name = ['NA', 'A']
			data = [ paramToNonAvailableCount[parameterIndexNumber], (len(discreteCohorte) - paramToNonAvailableCount[parameterIndexNumber])]
			explode=(0, 0.15)
			ax1.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
			ax1.axis('equal')
				
			data = []
			for status in listOfPossibleStatus:
				data.append(statusToCount[status])
			ind = np.arange(len(listOfPossibleStatus))
			width = 0.10

			rects1 = ax2.bar(ind, data, width, color='cyan')
			ax2.set_xlim(-width,len(ind)+width)
			ax2.set_ylabel("Count")
			xTickMarks = [param for param in listOfPossibleStatus]
			ax2.set_xticks(ind+width)
			xtickNames = ax2.set_xticklabels(xTickMarks)
			plt.setp(xtickNames, rotation=45, fontsize=10)
			plt.tight_layout()

			realVariableName_formated = realVariableName.replace("\\", " ")
			fig.canvas.set_window_title(realVariableName_formated)
			plt.show()
		else:
			print "[WARNINGS] => Parameter " +str(discreteVariableName) + " not found"

	else:
		if(discreteVariableName in paramToNonAvailableCount.keys()):
			
			realVariableName = "undef"
			parameterIndex = open("PARAMETERS/Control_variable_index.csv")

			for line in parameterIndex:
				line = line.split("\n")
				lineInArray = line[0].split(";")
				if(lineInArray[0] == discreteVariableName):
					realVariableName = lineInArray[1]

			parameterIndex.close()
			listOfPossibleStatus = []
			statusToCount = {}
			for patient in discreteCohorte:
				for scalar in patient:
					scalarInArray = scalar.split("_")
					if(len(scalarInArray) > 1):
						param = scalarInArray[0]
						if(param == discreteVariableName):
							if(scalarInArray[1] != "NA" and scalarInArray[1] not in listOfPossibleStatus):
								listOfPossibleStatus.append(scalarInArray[1])
			
			for status in listOfPossibleStatus:
				statusToCount[status] = 0
			for patient in discreteCohorte:
				for scalar in patient:
					scalarInArray = scalar.split("_")
					if(len(scalarInArray) > 1):
						param = scalarInArray[0]
						if(param == discreteVariableName):
							if(scalarInArray[1] in listOfPossibleStatus):
								statusToCount[scalarInArray[1]] += 1

			fig, ((ax1), (ax2)) = plt.subplots(nrows=1, ncols=2)
			nonAvailableProportion = (float(paramToNonAvailableCount[discreteVariableName]) / float(len(discreteCohorte)))*100
			name = ['NA', 'A']
			data = [ paramToNonAvailableCount[discreteVariableName], (len(discreteCohorte) - paramToNonAvailableCount[discreteVariableName])]
			explode=(0, 0.15)
			ax1.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
			ax1.axis('equal')
			
			data = []
			for status in listOfPossibleStatus:
				data.append(statusToCount[status])
			ind = np.arange(len(listOfPossibleStatus))
			width = 0.10

			rects1 = ax2.bar(ind, data, width, color='cyan')
			ax2.set_xlim(-width,len(ind)+width)
			ax2.set_ylabel("Count")
			xTickMarks = [param for param in listOfPossibleStatus]
			ax2.set_xticks(ind+width)
			xtickNames = ax2.set_xticklabels(xTickMarks)
			plt.setp(xtickNames, rotation=45, fontsize=10)
			plt.tight_layout()

			realVariableName_formated = realVariableName.replace("\\", " ")
			fig.canvas.set_window_title(realVariableName_formated)

			plt.show()

		else:
			print "[WARNINGS] => Parameter " +str(discreteVariableName) + " not found"


