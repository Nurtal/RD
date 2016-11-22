"""
2nd trashlib
for the RD project
"""

import glob
import numpy


def get_listOfParameters2(inputFolder, typeOfParameter):
	"""
	return the list of parameters in patient file
	-> inputFolder is a string, indicate the folder where are patients files
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	"""

	listOfParameters = []
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	for patientFile in listOfPatientFiles:
		dataInPatientFile = open(patientFile, "r")

		print "=> " +str(patientFile)

		for line in dataInPatientFile:
			lineInArray = line.split(";")
			if(lineInArray[2] == typeOfParameter):
				if(typeOfParameter == "PROPORTION"):
					parameter = lineInArray[1]+"_IN_"+lineInArray[3]
				elif(typeOfParameter == "MFI"):
					parameter = lineInArray[1]+"_MFI_"+lineInArray[3]
				else:
					parameter = lineInArray[1]
				if(parameter not in listOfParameters):
					listOfParameters.append(parameter)
			elif(typeOfParameter == "ALL" and lineInArray[1] != "Population"):
				if(lineInArray[2] == "PROPORTION"):
					parameter = lineInArray[1]+"_IN_"+lineInArray[3]
				elif(lineInArray[2] == "MFI"):
					parameter = lineInArray[1]+"_MFI_"+lineInArray[3]
				else:
					parameter = lineInArray[1]
				if(parameter not in listOfParameters):
					listOfParameters.append(parameter)
		dataInPatientFile.close()

	return listOfParameters


def convertPatientToVector2(patientFile, patientInVectorFile, typeOfParameter):
	"""
	take a patient filename
	write a new "vector" file
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	"""
	vectorFile = open(patientInVectorFile, "w")
	patientData = open(patientFile, "r")
	line_cmpt = 0
	patient_id = "undef"
	for line in patientData:
		line_cmpt = line_cmpt + 1
		lineInArray = line.split(";")
		if(line_cmpt == 1):
			patient_id = lineInArray[0]
			vectorFile.write("id;"+str(patient_id)+"\n")
		else:
			dataType = lineInArray[2]
			if(dataType == typeOfParameter):
				if(typeOfParameter == "PROPORTION"):
					parameter = lineInArray[1]+"_IN_"+lineInArray[3]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")
				elif(typeOfParameter == "MFI"):
					parameter = lineInArray[1]+"_MFI_"+lineInArray[3]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")
				else:
					parameter = lineInArray[1]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")
			elif(typeOfParameter == "ALL" and lineInArray[1] !="Population"):
				if(lineInArray[1] == "PROPORTION"):
					parameter = lineInArray[1]+"_IN_"+lineInArray[3]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")
				elif(lineInArray[1] == "MFI"):
					parameter = lineInArray[1]+"_MFI_"+lineInArray[3]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")
				else:
					parameter = lineInArray[1]
					parameterValue = lineInArray[4]
					parameterValue = parameterValue[:-1]
					vectorFile.write(parameter+";"+parameterValue+"\n")



	patientData.close()
	vectorFile.close()


def generate_DataMatrixFromPatientFiles2(inputFolder, typeOfParameter):
	"""
	Use all patients files present in
	DATA/PATIENT folder.
	return a numpy.array (data matrice)
	-> Parsring path file shoud be adapt windows / linux
	-> typeOfParameter is a string, indicate the type of parameter
		-ABSOLUTE
		-PROPORTION
		-RATIO
		-MFI
		-ALL
	=> Warning about Ratio: sometimes just 1 mesure / patient, not enough
	dor 2d or 3d visualisation.
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfVectorFiles = []

	for patientFile in listOfPatientFiles:

		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		patientFilesInArray = patientFilesInArray.split("/") # change on windows
		patientFilesInArray = patientFilesInArray[-1]
		vectorFileName = "DATA/VECTOR/"+str(patientFilesInArray)+"_VECTOR.csv"
		convertPatientToVector2(patientFile, vectorFileName, typeOfParameter)
		listOfVectorFiles.append(vectorFileName)
	listOfVector = []
	for vectorFile in listOfVectorFiles:

		#print vectorFile

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

	data = numpy.array(tuple(listOfVector))
	return data


"""TEST SPACE"""




def get_targetNames2(target, inputFolder):
	"""
	-> return the list of center or the list of date
	occuring in patient file present in data folder
	-> target is a string, could be:
		- center
		- date
		- disease
	"""	
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfCenter = []
	listOfDate = []
	listOfDisease = []
	for patientFile in listOfPatientFiles:
		patientFileInArray = patientFile.split("\\") # change windows / Linux
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")

		patient_disease = patientFileInArray[0]
		patient_id = patientFileInArray[1]
		patient_center = patientFileInArray[2]
		patient_date = patientFileInArray[3]

		if(target == "center"):
			if(patient_center not in listOfCenter):
				listOfCenter.append(patient_center)
		elif(target == "date"):
			if(patient_date not in listOfDate):
				listOfDate.append(patient_date)
		elif(target == "disease"):
			if(patient_disease not in listOfDisease):
				listOfDisease.append(patient_disease)

	if(target == "center"):
		return listOfCenter
	elif(target == "date"):
		return listOfDate
	elif(target == "disease"):
		return listOfDisease




def get_targetedY2(target, inputFolder):
	"""
	-> get an numpy.array containing date or center value
	-> used to display 2 dimensional pca
	-> target is a string, could be:
		- center
		- date
		- disease
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfCenter = []
	listOfDate = []
	listOfDisease = []

	for patientFile in listOfPatientFiles:
		patientFileInArray = patientFile.split("\\") # change on Windows / Linux
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")
			
		patient_disease = patientFileInArray[0]
		patient_id = patientFileInArray[1]
		patient_center = patientFileInArray[2]
		patient_date = patientFileInArray[3]

		target_names = get_targetNames2(target, inputFolder)
			
		cmpt_color = 0
		for element in target_names:
			if(target == "center" and patient_center == element):	
				listOfCenter.append(cmpt_color)
			elif(target == "date" and patient_date == element):
				listOfDate.append(cmpt_color)
			elif(target == "disease" and patient_disease == element):
				listOfDisease.append(cmpt_color)
			cmpt_color = cmpt_color + 1	

	if(target == "center"):
		target_center = numpy.array(tuple(listOfCenter))
		return target_center
	elif(target == "date"):
		target_date = numpy.array(tuple(listOfDate))
		return target_date
	elif(target == "disease"):
		target_disease = numpy.array(tuple(listOfDisease))
		return target_disease



#machin = get_targetedY2("disease", "DATA/PANEL_1")

#print machin


#machin = get_listOfParameters2("DATA/PATIENT", "ALL")
#truc = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "ALL")
	
#print truc