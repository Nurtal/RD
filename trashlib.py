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








"""
listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
listOfDisease = ["Control", "RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]

for patientFile in listOfPatientFiles:
	patientFileInArray = patientFile.split("/") # change on Windows / Linux
	patientFileName = patientFileInArray[-1]
	randindex = random.randint(0, 7)
	newFileName = listOfDisease[randindex]+"_"+patientFileName
	print newFileName

	shutil.copy(patientFile, "DATA/PATIENT_1/"+newFileName)
"""

#inputFolder = "DATA/INPUT"
#outputFolder = "DATA/PATIENT"



#data = generate_DataMatrixFromPatientFiles("DATA/PATIENT")
#print data

"""
	patientFileInArray = patientFileInArray.split("_")

		patient_id = patientFileInArray[0]
		patient_center = patientFileInArray[1]
		patient_date = patientFileInArray[2]
			
		if(target == "center"):
			if(patient_center not in listOfCenter):
				listOfCenter.append(patient_center)

		elif(target == "date"):
			if(patient_date not in listOfDate):
				listOfDate.append(patient_date)

	if(target == "center"):
		return listOfCenter
	elif(target == "date"):
		return listOfDate
"""






'''Exemple Procedure'''
"""
machin = load_exempleData(0)
performAndDisplay_pca(machin, "3d")
clustering_kmean(machin, 2)
"""


'''Parser data patient'''
"""
truc = generate_DataMatrixFromPatientFiles()
quickClustering(truc, 4)
"""




'''General Procedure'''

"""
inputFolder = "DATA/PATIENT"
data = generate_DataMatrixFromPatientFiles(inputFolder)
y = get_targetedY("center", inputFolder)
target_name = get_targetNames("center", inputFolder)

parameters = get_listOfParameters(inputFolder)
display_correlationMatrix(data.transpose(), parameters)
"""

"""
pca = PCA()
C = pca.fit(data).transform(data)
covar = numpy.cov(data.transpose())
"""

"""
plt.plot(pca.explained_variance_ratio_)
plt.show()
plt.boxplot(C[:,0:50])
plt.show()
"""


'''Dummy Data'''


"""
patient1 = [2, 1, 1, 1]
patient2 = [1, 2, 9, 8]
patient3 = [10, 9, 5, 10]
patient4 = [9, 10, 10, 1]
X = numpy.array((patient1, patient2, patient3, patient4))
y = numpy.array((0, 1, 1, 1))
target_name = ["Sain", "Malade"]

pca = PCA()
C = pca.fit(X).transform(X)

print numpy.linalg.eig(numpy.cov(C.transpose()))

plt.plot(pca.explained_variance_ratio_)
plt.show()
plt.boxplot(C[:,0:20])
plt.show()

params = ['mon', 'tue', 'wed', 'stuff']
display_correlationMatrix(X, params)
"""
"""
plt.figure()
for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
	plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
plt.legend()
plt.title("ACP")
plt.show()
"""

"""
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(C[:, 0], C[:, 1], C[:, 2], c=y, cmap=plt.cm.Paired)
ax.set_title("ACP: trois premieres composantes")
ax.set_xlabel("Comp1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("Comp2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("Comp3")
ax.w_zaxis.set_ticklabels([])
plt.show()
"""


"""
est=KMeans(n_clusters=2)
est.fit(machin)
classe=est.labels_

fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(C[:, 0], C[:, 1], C[:, 2], c=classe, cmap=plt.cm.Paired)
ax.set_title("ACP: trois premieres composantes")
ax.set_xlabel("Comp1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("Comp2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("Comp3")
ax.w_zaxis.set_ticklabels([])
plt.show()
"""