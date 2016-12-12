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


def FrequentItemMining2(minSupport):
	"""
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
	logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+".log", "w")
	logFile.close()

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
		scaleDataInPatientFolder("ABSOLUTE")
		discretization(threshold)

		print "----Mining----"
		cohorte = assemble_Cohorte()
		patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_ABSOLUTE_meanGeneratedThreshold.csv"
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
			threshold = get_ThresholdValue_DynamicDelta("ABSOLUTE", 1, "Mean", delta)

			print "----Mining on "+str(disease)+" (delta exploration)----"

			print "----Discretization (delta exploration)----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", disease)
			check_patient()
			scaleDataInPatientFolder("ABSOLUTE")
			discretization(threshold)

			print "----Mining (delta exploration)----"
			cohorte = assemble_Cohorte()
			patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_ABSOLUTE_meanGeneratedThreshold.csv"
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
		logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+".log", "a")
		logFile.write(disease+";"+str(numberOfItem)+";"+str(minSupport)+";"+str(delta)+"\n")
		logFile.close()




def FrequentItemMining3(minSupport, controlDisease):
	"""
	- ABSOLUTE data
	- discretisation using mean Generated threshold
	- dynamic generation threshold
	- delta is a used as a %
	- frequent item retrieval, no pattern mining
	- minSupport is a float, % of patient in cohorte that must
	  suppport the item
	- use controlDisease as a control for discretization process
	"""
	#listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
	listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
	

	# Initilaise log file
	logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+"_discretizationWith"+str(controlDisease)+".log", "w")
	logFile.close()

	for disease in listOfDisease:
		if(disease != controlDisease):
			delta = 0
			print "----Distribution Analysis----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", controlDisease)
			threshold = get_ThresholdValue_DynamicDelta("ABSOLUTE", 1, "Mean", delta)

			print "----Pattern Mining on "+str(disease)+"----"

			print "----Discretization----"
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", disease)
			check_patient()
			scaleDataInPatientFolder("ABSOLUTE")
			discretization(threshold)

			print "----Mining----"
			cohorte = assemble_Cohorte()
			patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_discretizationWith"+controlDisease+"_ABSOLUTE_meanGeneratedThreshold.csv"
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
				delta = delta + 0.05
				threshold = get_ThresholdValue_DynamicDelta("ABSOLUTE", 1, "Mean", delta)

				print "----Mining on "+str(disease)+" (delta exploration)----"

				print "----Discretization (delta exploration)----"
				clean_folders("ALL")
				fusion_panel(listOfPanelToConcat)
				checkAndFormat("DATA/FUSION", "DATA/PATIENT")
				apply_filter("disease", disease)
				check_patient()
				scaleDataInPatientFolder("ABSOLUTE")
				discretization(threshold)

				print "----Mining (delta exploration)----"
				cohorte = assemble_Cohorte()
				patternSaveFile = disease+"_FrequentItem_"+str(minSupport)+"_discretizationWith"+controlDisease+"_ABSOLUTE_meanGeneratedThreshold.csv"
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
			logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(minSupport)+"_discretizationWith"+str(controlDisease)+".log", "a")
			logFile.write(disease+";"+str(numberOfItem)+";"+str(minSupport)+";"+str(delta)+"\n")
			logFile.close()



def visualisation2(disease, control):
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
	parametersOfInterest_control = extract_parametersFromPattern("DATA/PATTERN/"+control+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)
	parametersOfInterest = parametersOfInterest_control + parametersOfInterest_disease
	listOfAllParameters = get_allParam("ABSOLUTE")

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