"""
convert, save, filter 
operation on data files
"""

#-------------------------------#
# Importation					#
#-------------------------------#
import glob						#
import shutil					#
import os 						#
import platform 				#
import subprocess          		#
#-------------------------------#




def convert_tabSepratedFile(inputFolder, outputFolder):
	
	"""
	convert all tab separated files present in
	inputfolder to ";" separated file in outputFolder
	-> inputFolder is a string
	-> outputFolder is a string
	-> return nothing
	"""

	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFileName = patientFileInArray[-1]
		newPatientFileName = outputFolder+"/"+str(patientFileName)
		dataInPatientFile = open(patientFile, "r")
		newPatientFile = open(newPatientFileName, "w")
		for originalLine in dataInPatientFile:
			originalLineInArray = originalLine.split("\t")
			cmpt = 0
			for element in originalLineInArray:
				if(cmpt < len(originalLineInArray)-1):
					newPatientFile.write(str(element)+";")
				else:
					newPatientFile.write(str(element))
				cmpt = cmpt + 1

		dataInPatientFile.close()
		newPatientFile.close()





def apply_filter(targetType, target):
	
	"""
	-> Delete all files in DATA/PATIENT not passing the apply_filter
	   (i.e all files with a targetType not matching target)
	   (e.g : aplly_filter(center, ubo) will delete all non-ubo files)

	-> targetType is a string, could be:
		- center
		- date
		- disease
	"""

	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")
		patient_disease = patientFileInArray[0]
		patient_id = patientFileInArray[1]
		patient_center = patientFileInArray[2]
		patient_date = patientFileInArray[3]

		if(list(target)):
			if(targetType == "center" and patient_center not in target):	
				os.remove(patientFile)
			elif(targetType == "date" and patient_date not in target):
				os.remove(patientFile)
			elif(targetType == "disease" and patient_disease not in target):
				os.remove(patientFile)
		else:
			if(targetType == "center" and patient_center != target):	
				os.remove(patientFile)
			elif(targetType == "date" and patient_date != target):
				os.remove(patientFile)
			elif(targetType == "disease" and patient_disease != target):
				os.remove(patientFile)





def restore_Data():
	"""
	-> Delete all files in DATA/PATIENT
	-> Copy all files from DATA/PATIENT_SAVE to DATA/PATIENT
	"""

	#---------------------------------#
	# -> Clean destination directory  #
	# (i.e DATA/PATIENT directory) 	  #
	#---------------------------------#
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		os.remove(patientFile)

	#------------------------------------------------#
	# -> Copy from backup folder (DATA/PATIENT_SAVE) #
	# to destination (DATA/PATIENT) 				 #
	#------------------------------------------------#
	listOfPatientSaved = glob.glob("DATA/PATIENT_SAVE/*.csv")
	for patientSaved in listOfPatientSaved:
		shutil.copy(patientSaved, "DATA/PATIENT/")





def fusion_panel(listOfPanels):
	"""
	-> Concat patient files, use all panel present in listOfPanels
	-> Delete all files in FUSION folder
	-> write new files in FUSION folder from
	   files present in listOfPanels folders
	-> Clean new files (remove header lines from other files)
	-> reject a file if the patient is not present in all directory
	   of listOfPanels

	-> listOfPanels is a list of string
	"""

	# Nettoyer le dossier FUSION
	listOfFilesToClean = glob.glob("DATA/FUSION/*.csv")
	for fileToClean in listOfFilesToClean:
		os.remove(fileToClean)

	# initialiser les files
	listOfPatientFiles = glob.glob("DATA/"+str(listOfPanels[0])+"/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
				patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")

		patientFileName = patientFileInArray[-1]
		patientFileNameInArray = patientFileName.split("_")
		center = patientFileNameInArray[2]
		date = patientFileNameInArray[3]
		#patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+"CENTER"+"_"+"DATE"+".csv"
		patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+center+"_"+"DATE"+".csv"
		newPatientFileName = "DATA/FUSION/"+str(patientFileName)
		newFile = open(newPatientFileName, "w")
		newFile.close()

	# remplir le fichier
	for panel in listOfPanels:
		listOfPatientFiles = glob.glob("DATA/"+str(panel)+"/*.csv")
		for patientFile in listOfPatientFiles:
			if(platform.system() == "Linux"):
				patientFileInArray = patientFile.split("/")
			elif(platform.system() == "Windows"):
				patientFileInArray = patientFile.split("\\")
			patientFileName = patientFileInArray[-1]

			patientFileNameInArray = patientFileName.split("_")
			center = patientFileNameInArray[2]
			date = patientFileNameInArray[3]
			#patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+"CENTER"+"_"+"DATE"+".csv"
			patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+center+"_"+"DATE"+".csv"
			newPatientFileName = "DATA/FUSION/"+str(patientFileName)

			sourceFile = open(patientFile, "r")
			dataToCopy = []
			for line in sourceFile:
				dataToCopy.append(line)
			sourceFile.close()
			destinationFile = open(newPatientFileName, "a")
			for line in dataToCopy:
				destinationFile.write(line)
			destinationFile.close()

	# Nettoyer les fichiers
	# delete header from files used for
	# the previous concatenation
	listOfPatientFiles = glob.glob("DATA/FUSION/*.csv")
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		shutil.copy(patientFile, str(patientFile_save))
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		dataToInspect = open(patientFile_save, "r")
		dataToCorrect = open(patientFile, "w")
		cmpt = 0
		correctedData = []
		for line in dataToInspect:
			cmpt = cmpt +1
			lineInArray = line.split("\t")
			if(cmpt == 1):
				correctedData.append(line)
			else:
				if(lineInArray[1] != "POPULATION"):
					correctedData.append(line)
		for line in correctedData:
			dataToCorrect.write(line)

		dataToCorrect.close()
		dataToInspect.close()
		os.remove(patientFile_save)
		
	
	# Fusionner les fichiers avec un Id identique
	# mais un centre differents (...)
	# garde le nom du premier centre.
	# Genere des effets centres !
	listOfPatientFilesToCheck = glob.glob("DATA/FUSION/*.csv")
	for patientToCheck in listOfPatientFilesToCheck:
		patientToCheck_nameInArray = ""
		listOfPatientWithSameId = []
		if(platform.system() == "Linux"):
			patientToCheckInArray = patientToCheck.split("/")
			patientToCheck_nameInArray = patientToCheckInArray[-1]
		elif(platform.system() == "Windows"):
			patientToCheckInArray =patientToCheck.split("\\")
			patientToCheck_nameInArray = patientToCheckInArray[-1]
		patientToCheck_nameInArray = patientToCheck_nameInArray.split("_")
		patientToCheck_id = patientToCheck_nameInArray[1]

		listOfPatientFiles = glob.glob("DATA/FUSION/*.csv")
		for patientFile in listOfPatientFiles:
			patient_nameInArray = ""
			if(platform.system() == "Linux"):
				patientInArray = patientFile.split("/")
				patient_nameInArray = patientInArray[-1]
			elif(platform.system() == "Windows"):
				patientInArray =patientFile.split("\\")
				patient_nameInArray = patientInArray[-1]
			patient_nameInArray = patient_nameInArray.split("_")
			patient_id = patient_nameInArray[1]

	
			if(patient_id == patientToCheck_id):
				if(patientFile not in listOfPatientWithSameId):
					listOfPatientWithSameId.append(patientFile)

	
		if(len(listOfPatientWithSameId) > 1):
			modelFile = listOfPatientWithSameId[0]
			listOfPatientWithSameId.remove(modelFile)		
			for patientFile in listOfPatientWithSameId:
				destination = open(modelFile, "a")
				source = open(patientFile, "r")
				cmptInSource = 0
				for line in source:
					if(cmptInSource > 0):
						destination.write(line)
					cmptInSource += 1
				source.close()
			
				os.remove(patientFile)
				destination.close()




	# Trier les fichiers
	# Verifier que le patient apparait bien dans
	# tout les panels a fusionner
	listOfPatientFiles = glob.glob("DATA/FUSION/*.csv")
	for patientFile in listOfPatientFiles:
		rejected = 0
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
			nameInArray = patientFileInArray[2]
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
			nameInArray = patientFileInArray[1]
		nameInArray = nameInArray.split("_")
		patient_id = nameInArray[1]

		for panel in listOfPanels:
			if(not rejected):
				listOfPatientIdInPanel =[]		
				listOfPatientFilesInPanel = glob.glob("DATA/"+str(panel)+"/*.csv")
				
				for patientFileInPanel in listOfPatientFilesInPanel:
					if(platform.system() == "Linux"):
						patientFileInArrayInPanel = patientFileInPanel.split("/")
					elif(platform.system() == "Windows"):
						patientFileInArrayInPanel = patientFileInPanel.split("\\")
					nameInArrayInPanel = patientFileInArrayInPanel[-1]
					nameInArrayInPanel = nameInArrayInPanel.split("_")
					patient_idInPanel = nameInArrayInPanel[1]
					listOfPatientIdInPanel.append(patient_idInPanel)


				if(patient_id not in listOfPatientIdInPanel):
					print str(patient_id) + "=> not in panel " +str(panel)
					#print str(patient_id) + " rejected"
					shutil.copy(patientFile, "DATA/REJECTED/")
					os.remove(patientFile)
					rejected = 1





def save_data():
	"""
	-> copy all patient file (i.e all csv files in DATA/PATIENT)
	   in the DATA/PATIENT_SAVE directory (after deleting all files
	   in DATA/PATIENT_SAVE directory)

	"""

	# clean destination
	listOfPatientFiles = glob.glob("DATA/PATIENT_SAVE/*.csv")
	for patientFile in listOfPatientFiles:
		os.remove(patientFile)

	# copy to destination
	listOfPatientFiles2 = glob.glob("DATA/PATIENT/*.csv")	
	for patientFile in listOfPatientFiles2:
		shutil.copy(patientFile, "DATA/PATIENT_SAVE/")





def check_patient():
	"""
	-> Perform a few control on patient,
	   make sure there is no "MISSING" or "NA" value
	   in data.
	-> delete all patient files containing undef value (i.e "MISSING",
		or "NA")
	"""
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patient in listOfPatientFiles:
		rejected = 0
		patientData = open(patient, "r")
		line_cmpt = 0
		patient_id = "undef"
		for line in patientData:
			line_cmpt = line_cmpt + 1
			lineInArray = line.split(";")
			if(line_cmpt == 1):
				patient_id = lineInArray[0]
			else:
				if(len(lineInArray) < 5):
					print "[WARNINGS] "+ str(patient_id) +" can't parse line"
					rejected = 1
				else:
					dataType = lineInArray[2]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					if("N" in str(parameterValue)):
						rejected = 1

		patientData.close()

		if(rejected):
			print patient_id + " rejected"
			shutil.copy(patient, "DATA/REJECTED/")
			os.remove(patient)





def clean_folders(folder):
	"""
	-> remove all (csv or jpg) files in folder
	-> folder is a string, could be:
		- PATIENT
		- VECTOR
		- FUSION
		- IMAGES
		- ALL
	"""

	if(folder == "ALL"):
		# clean PATIENT folder
		listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
		for patientFile in listOfPatientFiles:
			os.remove(patientFile)

		# clean VECTOR folder
		listOfPatientFiles = glob.glob("DATA/VECTOR/*.csv")
		for patientFile in listOfPatientFiles:
			os.remove(patientFile)

		# clean FUSION folder
		listOfPatientFiles = glob.glob("DATA/FUSION/*.csv")
		for patientFile in listOfPatientFiles:
			os.remove(patientFile)

		# clean IMAGES folder
		listOfImage = glob.glob("IMAGES/*.jpg")
		for image in listOfImage:
			os.remove(image)

	elif(folder != "ALL" and folder != "IMAGES"):
		# clean PATIENT folder
		listOfPatientFiles = glob.glob("DATA/"+str(folder)+"/*.csv")
		for patientFile in listOfPatientFiles:
			os.remove(patientFile)

	elif(folder == "IMAGES"):
		listOfImage = glob.glob("IMAGES/*.jpg")
		for image in listOfImage:
			os.remove(image)





def clean_image():
	"""
	Delete all .jpg files in the
	IMAGES folder
	*Obsolete*
	"""
	listOfImage = glob.glob("IMAGES/*.jpg")
	for image in listOfImage:
		os.remove(image)





def remove_parameter(typeOfParameter, parameter):
	"""
	-> Remove a specific parameter from files in PATIENT folder
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL (not tested yet)
	-> parameter is a string, the specific parameter
	   to remove (e.g : mDC1_IN_leukocytes)
	"""

	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		shutil.copy(patientFile, str(patientFile_save))
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		dataToInspect = open(patientFile_save, "r")
		dataToCorrect = open(patientFile, "w")
		correctedData = []
		for line in dataToInspect:
			lineInArray = line.split(";")
			parameterName = ""
			if(lineInArray[2] == typeOfParameter):
				if(typeOfParameter == "PROPORTION"):
					parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
				elif(typeOfParameter == "MFI"):
					parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
				else:
					parameterName = lineInArray[1]
				
			elif(typeOfParameter == "ALL" and lineInArray[1] != "Population"):
				if(lineInArray[2] == "PROPORTION"):
					parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
				elif(lineInArray[2] == "MFI"):
					parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
				else:
					parameterName = lineInArray[1]

			if(parameterName != parameter):
				correctedData.append(line)
		
		for line in correctedData:
			dataToCorrect.write(line)

		dataToCorrect.close()
		dataToInspect.close()
		os.remove(patientFile_save)




def remove_typeOfParameter(typeOfParameter):
	"""
	IN PROGRESS
	"""

	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		shutil.copy(patientFile, str(patientFile_save))
	for patientFile in listOfPatientFiles:
		patientFile_save = str(patientFile)+"_save.tmp"
		dataToInspect = open(patientFile_save, "r")
		dataToCorrect = open(patientFile, "w")
		correctedData = []
		for line in dataToInspect:
			lineInArray = line.split(";")
			parameterName = ""
			if(lineInArray[2] != typeOfParameter):
				correctedData.append(line)
		for line in correctedData:
			dataToCorrect.write(line)
		dataToCorrect.close()
		dataToInspect.close()
		os.remove(patientFile_save)





def count_line():
	"""
	-> return the number of line in the programm
	assuming all source file are in the current directory (not good !!! )
	"""
	line_cmpt = 0
	listOfPythonFiles = glob.glob("*.py")
	for pythonFile in listOfPythonFiles:
		code = open(pythonFile, "r")
		for line in code:
			line_cmpt = line_cmpt + 1

	return line_cmpt





def get_allParam(typeOfParameter):
	"""
	-> return the list of parameter of type typeOfParameter
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-MFI
		-ALL
	"""
	listOfParameters = []
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		dataToInspect = open(patientFile, "r")
		for line in dataToInspect:
			lineInArray = line.split(";")
			parameterName = ""

			if(lineInArray[1] != "POPULATION"):

				if(lineInArray[2] == typeOfParameter):
					if(typeOfParameter == "PROPORTION"):
						parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)
					elif(typeOfParameter == "MFI"):
						parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)
					else:
						parameterName = lineInArray[1]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)
					
				elif(typeOfParameter == "ALL" and lineInArray[1] != "Population"):
					if(lineInArray[2] == "PROPORTION"):
						parameterName = lineInArray[1]+"_IN_"+lineInArray[3]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)
					elif(lineInArray[2] == "MFI"):
						parameterName = lineInArray[1]+"_MFI_"+lineInArray[3]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)
					else:
						parameterName = lineInArray[1]
						if(parameterName not in listOfParameters):
							listOfParameters.append(parameterName)		

		dataToInspect.close()
	return listOfParameters





def convert_PatternFile(fileName):
	"""
	-> Convert the parameter present in fileName
	   (i.e pX parmater where X is an int) into 
	   real parameters, using PARAMETERS/variable_index.csv file

	-> Used on PATTERN/ files
	-> Create a new _converted file in PATTERN directory.

	"""
	convertedFileName = fileName.split(".")
	convertedFileName = convertedFileName[0]
	convertedFileName = convertedFileName+"_converted.csv"
	convertedFile = open(convertedFileName, "w")
	fileToConvert = open(fileName, "r")

	for line in fileToConvert:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")
		support = lineInArray[-1]
		lineInArray = lineInArray[:-1]

		convertedLine = ""
		for element in lineInArray:
			elementInArray = element.split("_")
			elementToConvert = elementInArray[0]
			elementStatus = elementInArray[1]

			conversionTable = open("PARAMETERS/variable_index.csv", "r")
			for indexLine in conversionTable:
				indexLineInArray = indexLine.split("\n")
				indexLineInArray = indexLineInArray[0]
				indexLineInArray = indexLineInArray.split(";")
				indexParameter = indexLineInArray[1]

				if(indexParameter == elementToConvert):
					convertedParameter = indexLineInArray[0]
			conversionTable.close()

			convertedLine = convertedLine + str(convertedParameter)+":"+str(elementStatus)+";"
		convertedLine = convertedLine + str(support)
		convertedFile.write(convertedLine+"\n")


	fileToConvert.close()
	convertedFile.close()





def filter_ArtefactValue(dataType, parameter, threshold):
	"""
	-> Scan DATA/PATIENT folder, delete patient file where
	parameter of type dataType is >= threshold
	->  dataType is a string, ndicate the type of parameter
		-ABSOLUTE
		-PROPORTION (not test yet)
		-MFI (not test yet)
	-> parameter is a string
	-> threshold could be an int or a float

	"""

	listOfPatientToDelete = []

	listOfPatient = glob.glob("DATA/PATIENT/*.csv")
	for patient in listOfPatient:
		data = open(patient, "r")
		for line in data:
			lineInArray = line.split("\n")
			lineInArray = lineInArray[0].split(";")
			value = str(lineInArray[-1])
			if(lineInArray[1] == parameter and lineInArray[2] == dataType and lineInArray[1] != "POPULATION"):
				if(float(value) >= threshold):
					if(patient not in listOfPatientToDelete):
						listOfPatientToDelete.append(patient)
		data.close()

	# delete patient file
	for element in listOfPatientToDelete:
		print "outlier "+element
		os.remove(element)





def compile_report():
	"""
	-> compile .tex report, create a pdf
	"""

	# remove REPORT/IMAGES
	shutil.rmtree('REPORT/IMAGES')
	shutil.copytree("IMAGES", "REPORT/IMAGES")


	listOfTexFiles = glob.glob("REPORT/*.tex")
	for element in listOfTexFiles:
		if(platform.system() == "Linux"):
			fileName = element.split("/")
		elif(platform.system() == "Windows"):
			fileName = element.split("\\")
		fileName = fileName[-1]
		fileName = fileName.split(".")
		fileName = fileName[0]

		# compile
		command = "pdflatex -output-directory REPORT " +str(element)
		os.system(command)

		# copy
		source = element.split(".")
		source = source[0] + ".pdf"
		shutil.copy(source, "RESULTATS/"+fileName+".pdf")





def clean_report():
	"""
	-> delete all .tex, .aux, .log and .pdf files (generated
	   with the compile_report function)
	"""
	listOfTexFiles = glob.glob("REPORT/*.tex")
	for texFile in listOfTexFiles:
		os.remove(texFile)

	listOfTexFiles = glob.glob("REPORT/*.aux")
	for texFile in listOfTexFiles:
		os.remove(texFile)

	listOfTexFiles = glob.glob("REPORT/*.log")
	for texFile in listOfTexFiles:
		os.remove(texFile)

	listOfTexFiles = glob.glob("REPORT/*.pdf")
	for texFile in listOfTexFiles:
		os.remove(texFile)



def add_diagnosticTag(panel):
	"""
	-> Add diagnostic tag to filename in 
	DATA/panel folder
	-> use DATA/patientIndex file 
	-> panel is a string, name of folder where
	   the files are converted
	"""

	listOfFiles = glob.glob("DATA/"+str(panel)+"/*.csv")
	for files in listOfFiles:

		patientDiagnostic = "undef"

		fileNameInArray = files.split("\\")
		fileNameInArray2 = fileNameInArray[1].split("_")
		patientID = fileNameInArray2[0]

		indexFile = open("DATA/patientIndex.csv", "r")
		for line in indexFile:
			line = line.split("\n")
			lineInArray = line[0].split(";")
			indexId = lineInArray[0]
			diagnostic = lineInArray[1]
			if(patientID == indexId):
				patientDiagnostic = diagnostic
		indexFile.close()

		newFileName = fileNameInArray[0]+"/"+patientDiagnostic+"_"+fileNameInArray[1]
		shutil.copy(files, newFileName)
		os.remove(files)



def convert_DRFZ_to_CHARITE():
	"""
	-> Convert all "DRFZ" file inti "CHARITE" file
	-> use it before try to fusion the data
	"""
	listOfPanel = ["PANEL_1", "PANEL_2", "PANEL_3", "PANEL_4", "PANEL_5", "PANEL_6", "PANEL_7", "PANEL_8", "PANEL_9"]
	for panel in listOfPanel:
		listOfPatient = glob.glob("DATA/"+str(panel)+"/*.csv")
		for patientFile in listOfPatient:
			if(platform.system() == "Linux"):
				patientFileInArray = patientFile.split("/")
			elif(platform.system() == "Windows"):
				patientFileInArray = patientFile.split("\\")
			patientFileName = patientFileInArray[-1]

			patientFileNameInArray = patientFileName.split("_")
			center = patientFileNameInArray[2]
			date = patientFileNameInArray[3]
			patient_id = patientFileNameInArray[1]

			if(center == "DRFZ"):
				print str(patient_id) + " => convert from DRFZ to CHARITE center"
				newPatientFile = patientFile.replace("DRFZ", "CHARITE")
				shutil.copy(patientFile, newPatientFile)
				os.remove(patientFile)




#---------------------#
# DATABASE GENERATION ################################################################
#---------------------#

from tinydb import TinyDB, Query

def construct_database(inputFileName, DBFilename):
	"""
	IN PROGRESS
	
	-> Construct a noSQL database with the tinydb module
	-> use inputFileName as an input Data file (currently
	   the function is designed to work with the clinical_i2b2trans
	   file)
	-> use DBFilename to write databaseFile (.json file)
	-> purge existing tables, create new ones
	-> currently only work with Flow cytometry data.
	-> Create an index file parameter To position
	TODO:
		- remplir les autres tables

	"""

	# Create Table
	db = TinyDB(DBFilename)
	db.purge_tables()
	ListOfFirstIndication = ["Antibody", "Autoantibody", "Flow cytometry", "Luminex", "Clinical", "HLA"]
	for dataType in ListOfFirstIndication:
		table = db.table(str(dataType))
	cmpt = 0

	# Create Vectors
	positionToParameter = {}

	listOfVector_cytometry = []
	positionToParameter_cytometry = {}

	listOfVector_autoantibody = []
	positionToParameter_autoantibody = {}

	dataFile = open(inputFileName, "r")
	for line in dataFile:
		line = line.split("\n")
		lineInArray = line[0].split("\t")
		if(cmpt == 0):
			col = 0
			for element in lineInArray:
				elementInArray = element.split("\\")
				elementInArray = elementInArray[1:]
				if(len(elementInArray) > 1):
					if(elementInArray[0] == "Flow cytometry"):
						param = elementInArray[2].replace(" ", "_")
						positionToParameter_cytometry[col] = param
						positionToParameter[col] = param
					elif(elementInArray[0] == "Autoantibody"):
						param = elementInArray[1].replace(" ", "_")
						positionToParameter_autoantibody[col] = param
						positionToParameter[col] = param
				
				col +=1

		omic_id = lineInArray[71]
		omic_id = omic_id[1:]
		omic_id = omic_id.replace(" ", "")

		if(cmpt > 0):
			#Flow Cytometry Vector
			vector_cytometry = {}
			col = 0
			for scalar in lineInArray:
				scalar = scalar.replace(" ", "")
				if(col in positionToParameter_cytometry.keys()):
					vector_cytometry[positionToParameter_cytometry[col]] = scalar
				col +=1
			vector_cytometry["OMIC_ID"] = omic_id
			listOfVector_cytometry.append(vector_cytometry)
			
			#Autoantibody Vector
			vector_autoantibody = {}
			col = 0
			for scalar in lineInArray:
				scalar = scalar.replace(" ", "")
				if(col in positionToParameter_autoantibody.keys()):
					vector_autoantibody[positionToParameter_autoantibody[col]] = scalar
				col +=1
			vector_autoantibody["OMIC_ID"] = omic_id
			listOfVector_autoantibody.append(vector_autoantibody)
	
		cmpt +=1

	dataFile.close()

	# Create Index file for db
	indexFileName = DBFilename.split(".")
	indexFileName = indexFileName[0]+"_index.csv"
	indexFile = open(indexFileName, "w")
	for pos in positionToParameter.keys():
		lineToWrite = str(positionToParameter[pos])+";"+str(pos)+"\n"
		indexFile.write(lineToWrite)
	
	# Add OMIC ID
	indexFile.write("OMIC_ID;71\n")
	indexFile.close()

	CytometryTable = db.table('Flow cytometry')
	for vector in listOfVector_cytometry:
		print "=> INSERT Patient "+str(vector["OMIC_ID"])+" INTO TABLE Flow cytometry"
		CytometryTable.insert(vector)
	AutoantibodyTable = db.table('Autoantibody')
	for vector in listOfVector_autoantibody:
		print "=> INSERT Patient "+str(vector["OMIC_ID"])+" INTO TABLE Autoantibody"
		AutoantibodyTable.insert(vector)




def parse_request(request, listOfSelectedParameter):
	"""
	-> Parse result of a request and return only the paramaters
	   present in listOfSelectedParameter.
	-> Request is a dict generated by a search() operation from
	   the tinyDB package
	-> listOfSelectedParameter is a list of selected parameters
	-> return a list of dict, each dict is a vector with paramaters
	   present in listOfSelectedParameter. 
	"""
	structureToReturn = []
	for patient in request:
		vectorToReturn = {}
		for parameter in listOfSelectedParameter:
			vectorToReturn[parameter] = patient[parameter]

		structureToReturn.append(vectorToReturn)

	return structureToReturn





def get_listOfPatientWithDiagnostic(diagnostic):
	"""
	IN PRGRESS
	-> get the list of OMIC ID for patients
	   matching diagnostic
	-> diagnostic is a string, could be:
	   - Control
	   - RA
	   - MCTD 
	   - PAPs 
	   - SjS 
	   - SLE 
	   - SSc 
	   - UCTD
	-> return a list of OMIC ID
	"""
	patientIdList = []

	indexFile = open("DATA/patientIndex.csv", "r")
	for line in indexFile:
		line = line.split("\n")
		lineInArray = line[0].split(";")
		ID = lineInArray[0]
		status = lineInArray[1]
		if(status == diagnostic):
			patientIdList.append(ID)
	indexFile.close()
	
	return patientIdList



"""
#construct_database("DATA/CYTOKINES/clinical_i2b2trans.txt", "DATA/DATABASES/machin.json")
#print CytometryTable.all()
db = TinyDB("DATA/DATABASES/machin.json")
AutoantibodyTable = db.table('Autoantibody')
#CytometryTable = db.table('Flow cytometry')
Patient = Query()

test_function = lambda s: s in get_listOfPatientWithDiagnostic("Control")
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

print parameterToCount


#machin = CytometryTable.search(Patient.OMIC_ID == '32152217')
#listOfSelectedParameter = ["CD35POS_IN_PMN", "OMIC_ID"]
#truc = parse_request(machin, listOfSelectedParameter)

"""


def write_matrixFromPatientFolder():
	"""
	IN PROGRESS
	"""

	# initialise list of variableName
	listfOfVariables = []
	listOfInputFiles = glob.glob("DATA/PATIENT/*.csv")
	for patient in listOfInputFiles:
		dataInPatient = open(patient, "r")
		for line in dataInPatient:
			line = line.split("\n")
			lineInArray = line[0].split(";")
			variableName = lineInArray[1]+"_"+lineInArray[2]
			if(lineInArray[2] == "PROPORTION"):
				variableName = variableName + "_in_"+lineInArray[3]
			if(variableName not in listfOfVariables):
				if(variableName != "POPULATION_TYPE"):
					listfOfVariables.append(variableName)
		dataInPatient.close()

	matrixFile = open("DATA/CYTOKINES/matrixTestFromCyto.csv", "w")
	# write header
	header = ""
	for variable in listfOfVariables:
		header = header + variable +";"
	header = header[:-1]+"\n"
	matrixFile.write(header)

	# write vector
	listOfInputFiles = glob.glob("DATA/PATIENT/*.csv")
	for patient in listOfInputFiles:
		vector = ""
		dataInPatient = open(patient, "r")
		cmpt = 0
		for line in dataInPatient:
			if(cmpt != 0):
				line = line.split("\n")
				lineInArray = line[0].split(";")
				scalar = "undef"
				variableName = lineInArray[1]+"_"+lineInArray[2]
				if(lineInArray[2] == "PROPORTION"):
					variableName = variableName + "_in_"+lineInArray[3]
					scalar = lineInArray[4]
				else:
					scalar = lineInArray[4]
				vector = vector + scalar + ";"
			cmpt += 1
		dataInPatient.close()
		vector = vector[:-1]+"\n"
		matrixFile.write(vector)	
	matrixFile.close()



def remove_variableFromMatrixFile(matrixFile, variableToDelete):
	"""
	-> rewrite a matrix file without a selected variable
	-> matrixFile is the input matrixFile
	-> variableToDelete is the name of the variableToDelete
	"""

	inputMatrixFileName = matrixFile
	inputMatrixFileNameInArray = inputMatrixFileName.split(".")
	tmpFileName = inputMatrixFileNameInArray[0]+"_tmp.csv"
	shutil.copy(inputMatrixFileName, tmpFileName)
	inputMatrixFile = open(tmpFileName, "r")
	outputMatrix = open(inputMatrixFileName, "w")
	cmpt = 0
	variableToDelete_index = "undef"
	for line in inputMatrixFile:
		line = line.split("\n")
		lineInArray = line[0].split(";")

		if(cmpt == 0):
			index = 0
			new_header = ""
			for parameterName in lineInArray:
				if(parameterName == variableToDelete):
					variableToDelete_index = index
				else:
					new_header = new_header + parameterName + ";"
				index += 1
			outputMatrix.write(new_header[:-1]+"\n")
		else:
			index = 0
			new_line = ""
			for value in lineInArray:
				if(index != variableToDelete_index):
					new_line = new_line + value + ";"
				index += 1
			outputMatrix.write(new_line[:-1]+"\n")

		cmpt +=1
	outputMatrix.close()
	inputMatrixFile.close()
	os.remove(tmpFileName)




def remove_PatientsWithNAValues(matrixFile):
	"""
	-> rewrite a matrix file without any patient containing NA values
	-> matrixFile is a string, name of the input matrix file.
	"""

	inputMatrixFileName = matrixFile
	inputMatrixFileNameInArray = inputMatrixFileName.split(".")
	tmpFileName = inputMatrixFileNameInArray[0]+"_tmp.csv"
	shutil.copy(inputMatrixFileName, tmpFileName)
	inputMatrixFile = open(tmpFileName, "r")
	outputMatrix = open(inputMatrixFileName, "w")
	cmpt = 0
	delete_cmpt = 0
	index_id = "undef"
	for line in inputMatrixFile:
		line = line.split("\n")
		lineInArray = line[0].split(";")

		patient_id = "undef"

		if(cmpt == 0):
			index = 0
			for parameterName in lineInArray:
				parameterNameInArray = parameterName.split("\\")
				if("OMICID" in parameterName):
					index_id = index
				index+=1
			outputMatrix.write(line[0]+"\n")
		else:
			patientIsClean = 1
			patient_id = lineInArray[index_id]
			for value in lineInArray:
				if(value == "NA"):
					patientIsClean = 0
			if(patientIsClean):
				outputMatrix.write(line[0]+"\n")
			else:
				print "=> Remove patient "+str(patient_id)
		cmpt +=1

	outputMatrix.close()
	inputMatrixFile.close()
	os.remove(tmpFileName)




def convert_NonAvailableClinicalVariable_forControl(inputMatrixFileName):
	"""
	-> Convert all "NA" values for Clinical variable into "control"
	   values for control patient. Part of the imputation procedure,
	   i.e data CAN'T be available for control patient.

	-> inputMatrixFileName is the name of the matrixFile used as input
	-> write a new matrixFile "_imputed"

	TODO:
		-> could find more relevant value for each variables (assuming
			the phenotype is "normal" for control patient) 
	"""

	inputMatrixFileNameInArray = inputMatrixFileName.split(".")
	outputMatrixFileName = inputMatrixFileNameInArray[0] + "_imputed.csv"

	matrixFile = open(inputMatrixFileName, "r")
	outputMatrix = open(outputMatrixFileName, "w")

	indexToClinicalValue = {}
	cmpt = 0
	index_id = "undef"
	for line in matrixFile:
		line = line.split("\n")
		lineInArray = line[0].split(";")

		patient_id = "undef"
		patient_diagnostic = "undef"

		if(cmpt == 0):
			index = 0
			for parameterName in lineInArray:
				parameterNameInArray = parameterName.split("\\")
				if("Clinical" in parameterNameInArray):
					indexToClinicalValue[index] = parameterName
				if("OMICID" in parameterName):
					index_id = index
				index+=1

			outputMatrix.write(line[0]+"\n")
		
		else:
			# Get ID and Diagnostic
			patient_id = lineInArray[index_id]		
			patientIndexFile = open("DATA/patientIndex.csv", "r")
			for entry in patientIndexFile:
				entry = entry.split("\n")
				entryInArray = entry[0].split(";")
				if(entryInArray[0] == patient_id):
					patient_diagnostic = entryInArray[1]
			patientIndexFile.close()

			if(patient_diagnostic == "Control"):
				index = 0
				new_line = ""
				for scalar in lineInArray:
					if(index in indexToClinicalValue.keys()):
						for key in indexToClinicalValue.keys():
							if(index == key):
								if(scalar == "NA"):
									new_scalar = "control"
									new_line = new_line + new_scalar + ";"
								else:
									new_line = new_line + scalar + ";"
					else:
						new_line = new_line + scalar + ";"
					index += 1
				new_line = new_line[:-1]+"\n"
				outputMatrix.write(new_line)
			else:
				outputMatrix.write(line[0]+"\n")
		cmpt +=1
	outputMatrix.close()
	matrixFile.close()


def generate_binaryDiscretizeData_forNN():
	"""
	-> Generate clean files (matrix and label) in
	DATA/MATRIX directory for NN use

	TODO:
		-> disretization on more variable
	"""

	# Get the list of variable to convert
	data = open("DATA/CYTOKINES/discreteMatrix_imputed.csv", "r")
	indexToVariableName = {}
	indexOfVariableToSave = []
	cmpt = 0
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		#print line
		if(cmpt==0):
			index = 0
			for variable in lineInArray:
				indexToVariableName[index] = variable
				index += 1

		else:
			index = 0
			for scalar in lineInArray:
				if(scalar == "No" or scalar == "yes"):
					if(index not in indexOfVariableToSave):
						indexOfVariableToSave.append(index)
				
				elif(scalar == "negative"):
					if(index not in indexOfVariableToSave):
						indexOfVariableToSave.append(index)

				elif(scalar == "Female" or scalar == "Male"):
					if(index not in indexOfVariableToSave):
						indexOfVariableToSave.append(index)
				
				#if(indexToVariableName[index] == "\\Clinical\\Vascular\\MHGANGRENE"):
				#	print scalar

				index +=1

		cmpt += 1
	data.close()


	# Clean list of candidate
	data = open("DATA/CYTOKINES/discreteMatrix_imputed.csv", "r")
	cmpt = 0
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		lineIsSuspect = 0

		if(cmpt!=0):
			index = 0
			for scalar in lineInArray:
				if(scalar == "Unknown" or scalar == "Past" or scalar == "Present"):
					#print indexToVariableName[96]
					lineIsSuspect = 1
					if(index in indexOfVariableToSave):
						indexOfVariableToSave.remove(index)

				index +=1

		cmpt += 1
	data.close()


	# Write new data file
	# Write label file
	data = open("DATA/CYTOKINES/discreteMatrix_imputed.csv", "r")
	newData = open("DATA/MATRIX/discrete_processed_binary.csv", "w")
	labelFile = open("DATA/MATRIX/discrete_processed_binary_label.csv", "w")
	cmpt = 0
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		newLine = ""

		if(cmpt!=0):
			index = 0
			for scalar in lineInArray:
				if(index == 96):
					labelFile.write(scalar+"\n")
				if(index in indexOfVariableToSave):
					if(scalar == "No" or scalar == "negative" or scalar == "Female" or scalar == "control"):
						newScalar = "0;"
					elif(scalar == "Yes" or scalar == "Male" or scalar == "positive"):
						newScalar = '1;'
					else:
						print "[!] can't attribute binary value to "+str(scalar)+ " ("+str(indexToVariableName[index])+")"

					newLine = newLine + newScalar
					
				index +=1
			newLine = newLine[:-1]
			newData.write(newLine+"\n")
		cmpt += 1

	labelFile.close()
	newData.close()
	data.close()
