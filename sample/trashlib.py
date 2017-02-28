"""
Grand bazar
"""

import matplotlib.pyplot as plt
from sklearn import datasets
import random
import pandas as pd
import numpy
import pylab


from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

import glob

import matplotlib.cm as cm

import shutil
import os

import platform


def generate_data(numberOfPatients, numberOfParameters, separator, filename):
	"""
	generate random data for
	exemple use
	"""

	# generate data
	fileName = filename + ".txt"
	dataFile = open(fileName, "w")
	for x in xrange(0, numberOfPatients):
		patient = ""
		for y in xrange(0, numberOfParameters):
			parameter = random.randint(0,1)
			if(y < numberOfParameters - 1):
				patient = patient + str(parameter) + str(separator)
			else:
				patient = patient + str(parameter) + "\n"
		dataFile.write(patient)
	dataFile.close()

	# generate label
	labelFileName = filename + "_labels.txt"
	labelFile = open(labelFileName, "w")
	for x in xrange(0, numberOfPatients):
		label = random.randint(1,9)
		labelFile.write(str(label)+"\n")
	labelFile.close()



def load_exempleData(display):
	"""
	"""
	digits = datasets.load_digits()

	print digits.target

	if(display):
		#print(digits)
		# Dimensions
		digits.images.shape
		# Sous forme dun cube dimages 1797 x 8x8
		print(digits.images)
		# Sous forme dune matrice 1797 x 64
		print(digits.data)
		# Label reel de chaque caractere
		print(digits.target)
	return digits


def convertPatientToVector(patientFile, patientInVectorFile):
	"""
	=> OBSOLETE
	take a patient filename
	write a new "vector" file
	only consider the "ABSOLUTE" parameters
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
			if(dataType == "ABSOLUTE"):
				parameter = lineInArray[1]
				parameterValue = lineInArray[4]
				parameterValue = parameterValue[:-1]
				vectorFile.write(parameter+";"+parameterValue+"\n")
	patientData.close()
	vectorFile.close()


def generate_DataMatrixFromPatientFiles(inputFolder):
	"""
	=> OBSOLETE
	Use all patients files present in
	DATA/PATIENT folder.
	return a numpy.array (data matrice)
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfVectorFiles = []

	listOfVector = ([])

	for patientFile in listOfPatientFiles:
		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFilesInArray = patientFilesInArray[-1]
		vectorFileName = "DATA/VECTOR/"+str(patientFilesInArray)+"_VECTOR.csv"
		convertPatientToVector(patientFile, vectorFileName)
		listOfVectorFiles.append(vectorFileName)
	listOfVector = []
	for vectorFile in listOfVectorFiles:
		vectorData = open(vectorFile, "r")
		listOfvalue = []
		for line in vectorData:
			lineInArray = line.split(";")
			if(lineInArray[0]!="id"):
				parameterValue = lineInArray[1]
				try:
					parameterValue = int(parameterValue[:-1])
				except ValueError:
					parameterValue = 0
				listOfvalue.append(int(parameterValue))
		vectorData.close()
	
		if len(listOfvalue) > 15:
			print vectorFile		

		#listOfVector = list(listOfVector)
		listOfVector.append(listOfvalue)
		#listOfVector = tuple(listOfVector)
		#print listOfVector
		#listOfVector = (listOfVector,) + listOfvalue

	tupleOfVector = tuple(list(x) for x in listOfVector)
	#print tupleOfVector
	data = numpy.array(tupleOfVector)
	return data



def get_listOfParameters(inputFolder):
	"""
	=> OBSOLETE
	return the list of parameters in patient file
	-> inputFolder is a string, indicate the folder where are patients files
	-> only work on "ABSOLUTE" parameters for now
	"""

	listOfParameters = []
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	for patientFile in listOfPatientFiles:
		dataInPatientFile = open(patientFile, "r")
		for line in dataInPatientFile:
			lineInArray = line.split(";")
			if(lineInArray[2] == "ABSOLUTE"):
				parameter = lineInArray[1]
				if(parameter not in listOfParameters):
					listOfParameters.append(parameter)
		dataInPatientFile.close()

	return listOfParameters



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




"""Test Space"""


def print_parametersInRules():

	"""
	IN PROGRESS
	"""

	data = open("DATA/RULES/DECRYPTED/discreteVariables_rules_95.csv", "r")
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]

		lineInArray = lineWithoutBackN.split("->")
		

		for element in lineInArray:
			elementInArray = element.split(";")
			print elementInArray
	

	data.close()











import numpy as np
from cytokines import *

def describe_variable(variableOfInterest):
	"""
	IN PROGRESS
	"""


	DataFile = open("DATA/CYTOKINES/clinical_i2b2trans.txt", "r")
	cmpt = 0
	patientId_index = "undef"
	variableOfInterest = "\\Flow cytometry\\P9\\CD46POS IN PMN"
	variableOfInterest_index = "undef"
	listOfParameters = []
	listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD", "Control"]

	NA_count = 0
	variable_scalars = []
	data_is_numeric = 0
	proportionOfNA = "undef"

	for line in DataFile:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split("\t")
		if(cmpt == 0):
			index = 0
			for element in lineInArray:
				if("OMICID" in element):
					patientId_index = index
				if(element == variableOfInterest):
					variableOfInterest_index = index
				listOfParameters.append(element)
				index += 1

		# parsing data, have to work for both discrete & continue parameter
		else:
			index = 0
			for element in lineInArray:
				if(index == variableOfInterest_index):
					element = element.replace(" ", "")
					if(element == "NA" or element == "N.A"):
						NA_count += 1
					else:
						try:
							element = float(element)
							data_is_numeric = 1
						except:
							print "tardis"
						variable_scalars.append(element)	
				index += 1
		cmpt += 1
	DataFile.close()


	if(data_is_numeric):
		proportionOfNA = (float(NA_count) / float(len(variable_scalars))*100)
		
		fig, ((ax1), (ax2), (ax3),(ax4),(ax5),(ax6),(ax7),(ax8),(ax9),(ax10)) = plt.subplots(nrows=1, ncols=10)
		name = ['NA', 'A']
		data = [ NA_count, len(variable_scalars)]
		explode=(0, 0.15)
		ax1.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
		ax1.axis('equal')

		x = variable_scalars
		x = np.sort(x)
		ax2.hist(x)
		ax2.set_xlabel("Global")


		#####
		
		diagnosticToVariable = {}	

		splitCohorteAccordingToDiagnostic("DATA/CYTOKINES/clinical_i2b2trans.txt", "DATA/patientIndex.csv")
		for disease in listOfDisease:
			diagnosticMatrixFileName = "DATA/CYTOKINES/"+str(disease)+".csv"
			diagnosticMatrixFile = open(diagnosticMatrixFileName, "r")
			variable_scalars = []
			data_is_numeric = 0
			proportionOfNA = "undef"

			cmpt = 0
			for line in diagnosticMatrixFile:
				lineWithoutBackN = line.split("\n")
				lineWithoutBackN = lineWithoutBackN[0]
				lineInArray = lineWithoutBackN.split("\t")
				if(cmpt == 0):
					index = 0
					for element in lineInArray:
						if("OMICID" in element):
							patientId_index = index
						if(element == variableOfInterest):
							variableOfInterest_index = index
						listOfParameters.append(element)
						index += 1

				# parsing data, have to work for both discrete & continue parameter
				else:
					index = 0
					for element in lineInArray:
						if(index == variableOfInterest_index):
							element = element.replace(" ", "")
							if(element == "NA" or element == "N.A"):
								NA_count += 1
							else:
								try:
									element = float(element)
									data_is_numeric = 1
								except:
									print "tardis"
								variable_scalars.append(element)	
						index += 1
				cmpt += 1
			diagnosticMatrixFile.close()

			diagnosticToVariable[disease] = variable_scalars

		####

		k = np.sort(diagnosticToVariable["RA"])
		ax3.hist(k)
		ax3.set_xlabel("RA")

		k = np.sort(diagnosticToVariable["MCTD"])
		ax4.hist(k)
		ax4.set_xlabel("MCTD")

		k = np.sort(diagnosticToVariable["PAPs"])
		ax5.hist(k)
		ax5.set_xlabel("PAPs")

		k = np.sort(diagnosticToVariable["SjS"])
		ax6.hist(k)
		ax6.set_xlabel("SjS")

		k = np.sort(diagnosticToVariable["SLE"])
		ax7.hist(k)
		ax7.set_xlabel("SLE")

		k = np.sort(diagnosticToVariable["SSc"])
		ax8.hist(k)
		ax8.set_xlabel("SSc")

		k = np.sort(diagnosticToVariable["UCTD"])
		ax9.hist(k)
		ax9.set_xlabel("UCTD")

		k = np.sort(diagnosticToVariable["Control"])
		ax10.hist(k)
		ax10.set_xlabel("Control")


		realVariableName_formated = variableOfInterest.replace("\\", " ")
		fig.canvas.set_window_title(realVariableName_formated)

		plt.show()
		plt.close()

	else:
		print "non implemented"



	


#describe_variable("test")

"""
### count NA
dataFile = open("DATA/CYTOKINES/matrix.csv", "r")
#dataFile = open("DATA/CYTOKINES/discreteMatrix_imputed.csv", "r")
nb_patient = 0
nb_variable = 0
nb_NA = 0
for line in dataFile:
	nb_patient += 1
	lineWithoutBackN = line.split("\n")
	lineWithoutBackN = lineWithoutBackN[0]
	lineInArray = lineWithoutBackN.split(";")
	nb_variable = len(lineInArray)
	for scalar in lineInArray:
		if(scalar == "NA"):
			nb_NA += 1

dataFile.close()


total = (nb_patient-1) * nb_variable

machin = (float(nb_NA) / float(total))*100
print machin
"""

"""

listOfDiag = []
diagToCount = {}
total = 0
dataFile = open("DATA/patientIndex.csv", "r")
for line in dataFile:
	total +=1
	lineWithoutBackN = line.split("\n")
	lineWithoutBackN = lineWithoutBackN[0]
	lineInArray = lineWithoutBackN.split(";")
	diag = lineInArray[1]

	if(diag not in listOfDiag):
		listOfDiag.append(diag)
dataFile.close


for diag in listOfDiag:
	diagToCount[diag] = 0


dataFile = open("DATA/patientIndex.csv", "r")
for line in dataFile:
	lineWithoutBackN = line.split("\n")
	lineWithoutBackN = lineWithoutBackN[0]
	lineInArray = lineWithoutBackN.split(";")
	diag = lineInArray[1]

	for k in diagToCount.keys():
		if(k == diag):
			diagToCount[diag] += 1
	
dataFile.close


for k in diagToCount.keys():
	diagToCount[k] = (float(diagToCount[k]) / float(total))*100

print diagToCount
"""

# 32150092=>22
#32152215
 
"""
listOfPatientFiles = glob.glob("DATA/FUSION/*.csv")
for patientFile in listOfPatientFiles:
	lenOfFile = 0
	patientFileInArray = patientFile.split("/")
	patientFileInArray = patientFileInArray[-1].split("_")
	patient_ID = patientFileInArray[1]
	data = open(patientFile, "r")
	for line in data:
		lenOfFile += 1
	data.close()
	print str(patient_ID) +"=>"+ str(lenOfFile) 
"""




"""
import matplotlib.pyplot as plt
def on_pick(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print 'Artist picked:', event.artist
    print '{} vertices picked'.format(len(ind))
    print 'Pick between vertices {} and {}'.format(min(ind), max(ind)+1)
    print 'x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse)
    print 'Data point:', x[ind[0]], y[ind[0]]
    print

fig, ax = plt.subplots()
tolerance = 15 # points
ax.plot(range(20), 'ro-', picker=tolerance)
fig.canvas.callbacks.connect('pick_event', on_pick)
plt.show()
"""





def quickPCA_test(data, y, target_name, projection, saveName, details, show):
	"""
	-> perform and display pca
	-> data is a numpy.array object
	-> y is a numpy.array object (contient aaprtenance data, i.e centre, maladie ...)
		Encoder en int
	-> target_name : le nom des parametre en y
	-> projection: 2d ou 3d
	-> saveName is a string, name of the file where fig is saved
	-> details is a boolean, should be 0 for normal pca, should be 1
	   for Additional Graphics
	 -> show is a boolean, 1 for display graphe 
	"""

	# Get data for the clickable function
	centers_data = get_targetedY("center", "DATA/PATIENT")
	targetName = get_targetNames("center", "DATA/PATIENT")
	disease_data = get_targetedY("disease", "DATA/PATIENT")
	diseaseName = get_targetNames("disease", "DATA/PATIENT")
	id_data = get_targetedY("id", "DATA/PATIENT")
	idName = get_targetNames("id", "DATA/PATIENT")


	# Define the Clickable function
	def onclick(event):
		if(projection == "2d"):
			tolerance = 1
			cmpt = 0
			for vector in C:
				if(event.xdata >= vector[0] - tolerance and event.xdata <= vector[0] + tolerance and event.ydata >= vector[1] - tolerance and event.ydata <= vector[1] + tolerance):
					print "ID: "+str(idName[id_data[cmpt]])
					print "center: "+str(targetName[centers_data[cmpt]])
					print "disease: "+str(diseaseName[disease_data[cmpt]])
					print "---------------------"
				cmpt += 1
		elif(projection == "3d"):
			tolerance = 1
			cmpt = 0
			z = ax.format_coord(event.xdata,event.ydata)
			print z
			for vector in C:
				if(event.xdata >= vector[0] - tolerance and event.xdata <= vector[0] + tolerance and event.ydata >= vector[1] - tolerance and event.ydata <= vector[1] + tolerance):
					print "ID: "+str(idName[id_data[cmpt]])
					print "center: "+str(targetName[centers_data[cmpt]])
					print "disease: "+str(diseaseName[disease_data[cmpt]])
					print "---------------------"
				cmpt += 1



    # Perform PCA
	pca = PCA()
	C = pca.fit(data).transform(data)
	covar = numpy.cov(data.transpose())
	
	# Additional Graphics
	# -> Decroissance de la variance explique
	# -> Diagramme des premieres composante principales
	#-------------------------------------------------
	if(details):

		saveNameInArray = saveName.split(".")
		subSaveName1 = str(saveNameInArray[0]) + "_variance1.jpg"
		subSaveName2 = str(saveNameInArray[0]) + "_variance2.jpg"

		plt.figure()
		plt.plot(pca.explained_variance_ratio_)
		if(show):
			plt.show()
		plt.savefig(subSaveName1)
		plt.close()

		plt.figure()
		plt.boxplot(C[:,0:20])
		if(show):
			plt.show()
		plt.savefig(subSaveName2)
		plt.close()

	if(projection == "2d"):
		fig, ax = plt.subplots()
		for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
			#plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
			ax.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
		plt.legend()
		plt.title("ACP")
		plt.savefig(saveName)
		if(show):
			cid = fig.canvas.mpl_connect('button_press_event', onclick)
			plt.show()
		plt.close()
	elif(projection =="3d"):
		fig = plt.figure(1, figsize=(8, 6))
		ax = Axes3D(fig, elev=-150, azim=110)
		# ax.scatter(C[:, 0], C[:, 1], C[:, 2], c=y, label=target_name)
		for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
			ax.scatter(C[y == i,0], C[y == i,1], C[y == i,2], c=c, label=target_name)
		
		

		ax.set_title("ACP: trois premieres composantes")
		ax.set_xlabel("Comp1")
		ax.w_xaxis.set_ticklabels([])
		ax.set_ylabel("Comp2")
		ax.w_yaxis.set_ticklabels([])
		ax.set_zlabel("Comp3")
		ax.w_zaxis.set_ticklabels([])
		plt.legend()
		plt.savefig(saveName)

		if(show):
			cid = fig.canvas.mpl_connect('button_press_event', onclick)
			plt.show()
		plt.close()




"""
# Xml file generation
indexToVariableName = {}
indexToPossibleValues = {}
xmlFile = open("PARAMETERS/variable_description.xml", "w")
xmlFile.write("<?xml version=\"1.0\"?>" + "\n")
inputData = open("DATA/CYTOKINES/discreteMatrix_imputed.csv", "r")
cmpt=0
for line in inputData:
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
inputData.close()


for key in indexToVariableName.keys():
	#elementToWrite = element.replace("\\", " ")
	element = indexToVariableName[key]
	listOfPossibleValues = indexToPossibleValues[key]
	valuesToWrite = ""
	print "<"+str(element)+">"
	lineOfValues = "\t<Possible Values>"
	for values in listOfPossibleValues:
		valuesToWrite = valuesToWrite + values +";"
	valuesToWrite = valuesToWrite[:-1]
	lineOfValues += valuesToWrite
	lineOfValues += "</Possible Values>"
	print lineOfValues
	print "\t<Discrete Values></Discrete Values>"
	print "\t<Binary Values></Binary Values>"
	print "\t<Observations></Observations>"


	print "</"+str(element)+">"


xmlFile.close()
"""

def write_xmlDescriptionFile(matrixFile):
	"""
	-> Write the Backbone of an xml file for the
	   description of each variable found in matrixFile
	-> xml file have to be fill with other functions.
	-> TODO :
		- add new tag less discrete variables
	"""
	indexToVariableName = {}
	indexToPossibleValues = {}
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
				indexToPossibleValues[index] = []
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

