"""
Set of functions to write
and edit the xml description file
in the PARAMETER folder
"""
import os



def write_xmlDescriptionFile(matrixFile):
	"""
	-> Write the Backbone of an xml file for the
	   description of each variable found in matrixFile
	-> xml file have to be fill with other functions.
	-> TODO :
		- add new tag less discrete variables
	"""
	indexToVariableName = {}
	xmlFile = open("PARAMETERS/variable_description.xml", "w")
	xmlFile.write("<?xml version=\"1.0\"?>" + "\n")
	inputData = open(matrixFile, "r")
	cmpt=0
	for line in inputData:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		if(cmpt==0):
			index = 0
			for variable in lineInArray:
				indexToVariableName[index] = variable
				index += 1
		cmpt += 1
	inputData.close()

	for key in indexToVariableName.keys():	
		element = indexToVariableName[key]
		xmlFile.write("<"+str(element)+">" +"\n")
		xmlFile.write("\t<Type></Type>" +"\n")
		xmlFile.write("\t<Possible Values></Possible Values>" +"\n") 
		xmlFile.write("\t<Discrete Values></Discrete Values>" +"\n") 
		xmlFile.write("\t<Binary Values></Binary Values>" +"\n") 
		xmlFile.write("\t<Description></Description>" +"\n")
		xmlFile.write("\t<Observations></Observations>" +"\n") 
		xmlFile.write("</"+str(element)+">" +"\n") 

	xmlFile.close()





def set_typeValueFrom(matrixFile):
	"""
	-> Edit the PARAMETERS/variable_description.xml file, 
	   set the Type line to the type of data, could be:
	   	-Discrete
	   	-Continuous
	-> Determination of the data type is perform from the matrixFile
	-> If a parameter is present in matrixFile but is not in original xml
	   file the parameter is ignore (i.e you should give the same input as write_xmlDescriptionFile
	   	function)

	-> TODO:
		- maybe find a better way to discriminate Continuous and Discrete data
	"""

	# Test if variable is discrete or not
	myDataToParse = open(matrixFile, "r")
	indexToVariableName = {}
	indexToPossibleValues = {}
	variableToType = {}
	classicalDiscreteValues = ["Yes", "No", "negative", "Male", "Female", "pos"]
	cmpt=0
	for line in myDataToParse:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		if(cmpt==0):
			index = 0
			for variable in lineInArray:
				indexToVariableName[index] = variable
				indexToPossibleValues[index] = []
				index += 1
		else:
			index = 0
			for scalar in lineInArray:
				if(scalar not in indexToPossibleValues[index]):
					indexToPossibleValues[index].append(scalar)
				index += 1
		cmpt += 1
	myDataToParse.close()

	for key in indexToPossibleValues.keys():
		variableName = indexToVariableName[key]
		listOfValues = indexToPossibleValues[key]

		isDiscrete = 0

		# Probably Discrete, let's find out
		if(len(listOfValues) < 20):
			for value in listOfValues:
				if(value in classicalDiscreteValues):
					isDiscrete = 1
				elif(len(listOfValues) == 1):
					isDiscrete = 1
				else:
					try:
						float(value)
						isDiscrete = 0
					except ValueError:
						if(value != "NA" and value != "N/A" and value != "MISSING" and value != "N A" and value != "N.A"):
							isDiscrete = 1
		# Probably not discsrete
		# -> see if it can be converted to a number
		else:
			for value in listOfValues:
				try:
					float(value)
					isDiscrete = 0
				except ValueError:
					if(value != "NA" and value != "N/A" and value != "MISSING" and value != "N A" and value != "N.A"):
						isDiscrete = 1

		# Finally, fill the dictionnary
		if(isDiscrete):
			variableToType[variableName] = "Discrete"
		else:
			variableToType[variableName] = "Continuous"

	# Edit the xml file
	xmlFile = open("PARAMETERS/variable_description.xml", "r")
	xmlFile_edited = open("PARAMETERS/variable_description_edited.xml", "w")

	cmpt = 0
	record = 0
	variableOnLine = "undef"
	for line in xmlFile:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		
		newLine = lineWithoutBackN

		if(cmpt != 0):
			for variable in variableToType.keys():
				if(lineWithoutBackN == "<"+variable+">"):
					variableOnLine = variable
					record = 1
				
				if(lineWithoutBackN == "</"+variable+">"):
					record = 0

		if(record):
			if(lineWithoutBackN == "\t<Type></Type>"):
				newLine = "\t<Type>"+variableToType[variableOnLine]+"</Type>"
		
		# Write into tmp file
		xmlFile_edited.write(newLine+"\n")
		cmpt += 1

	xmlFile_edited.close()
	xmlFile.close()

	# remove source file and rename new file
	os.remove("PARAMETERS/variable_description.xml")
	os.rename("PARAMETERS/variable_description_edited.xml", "PARAMETERS/variable_description.xml")



# TEST SPACE
write_xmlDescriptionFile("DATA/CYTOKINES/discreteMatrix_imputed.csv")
set_typeValueFrom("DATA/CYTOKINES/discreteMatrix_imputed.csv")