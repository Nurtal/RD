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
		patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+"CENTER"+"_"+"DATE"+".csv"
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
			patientFileName = patientFileNameInArray[0]+"_"+patientFileNameInArray[1]+"_"+"CENTER"+"_"+"DATE"+".csv"
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