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


def clustering_kmean(data, numberOfClusters):
	"""
	Perform a pca on data
	perform clusterring (kmean) with numberOfClusters
	display in 3d
	"""

	X=data.data
	pca = PCA()
	C = pca.fit(X).transform(X)
	est=KMeans(n_clusters=numberOfClusters)
	est.fit(X)
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


def performAndDisplay_pca(data, representation):
	"""
	Perform and display a pca
	data are DataFrame object
	representation have to be set on "2d" or "3d"
	"""

	X=data.data
	y=data.target
	target_name=[0,1,2,3,4,5,6,7,8,9]
	pca = PCA()
	C = pca.fit(X).transform(X)

	# Additional Graphics
	# -> Decroissance de la variance explique
	# ->Diagramme des premieres composante principales
	#-------------------------------------------------

	#plt.plot(pca.explained_variance_ratio_)
	#plt.show()
	#plt.boxplot(C[:,0:20])
	#plt.show()

	if(representation=="2d"):
		plt.figure()
		for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
			plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
		plt.legend()
		plt.title("ACP")
		plt.show()
	elif(representation=="3d"):
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
	else:
		print "Bad parameter for reprsentation, please choose between 2d or 3d"



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
	Use all patients files present in
	DATA folder.
	return a numpy.array (data matrice)
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfVectorFiles = []

	for patientFile in listOfPatientFiles:
		patientFilesInArray = patientFile.split(".")
		vectorFileName = patientFilesInArray[0]+"_VECTOR.csv"
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
				parameterValue = int(parameterValue[:-1])
				listOfvalue.append(parameterValue)
		vectorData.close()
		listOfVector.append(listOfvalue)

	data = numpy.array(tuple(listOfVector))
	return data

def quickClustering(matrice, numberOfClusters):
	"""
	perform and display a kmean clusterring
	-> matrice is a numpy.array
	-> numberOfClusters is a int
	"""
	pca = PCA()
	C = pca.fit(matrice).transform(matrice)

	est=KMeans(n_clusters=numberOfClusters)
	est.fit(matrice)
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


def get_targetNames(target, inputFolder):
	"""
	-> return the list of center or the list of date
	occuring in patient file present in data folder
	"""	
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfCenter = []
	listOfDate = []
	for patientFile in listOfPatientFiles:
		patientFileInArray = patientFile.split("/")
		patientFileInArray = patientFileInArray[-1]
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



def get_targetedY(target, inputFolder):
	"""
	-> get an numpy.array containing date or center value
	-> used to display 2 dimensional pca
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfCenter = []
	listOfDate = []

	for patientFile in listOfPatientFiles:
		patientFileInArray = patientFile.split("/")
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")

		
		if(len(patientFileInArray) < 6):
			patient_id = patientFileInArray[0]
			patient_center = patientFileInArray[1]
			patient_date = patientFileInArray[2]

			target_names = get_targetNames(target, inputFolder)
			
			cmpt_color = 0
			for element in target_names:
				if(target == "center" and patient_center == element):	
					listOfCenter.append(cmpt_color)
				if(target == "date" and patient_date == element):
					listOfDate.append(cmpt_color)
				cmpt_color = cmpt_color + 1	

	if(target == "center"):
		target_center = numpy.array(tuple(listOfCenter))
		return target_center
	elif(target == "date"):
		target_date = numpy.array(tuple(listOfDate))
		return target_date


def quickPCA(data, y, target_name, projection):
	"""
	-> perform and display pca
	-> data is a numpy.array object
	-> y is a numpy.array object (contient aaprtenance data, i.e centre, maladie ...)
		Encoder en int
	-> target_name : le nom des parametre en y
	-> projection: 2d ou 3d
	"""

	pca = PCA()
	C = pca.fit(data).transform(data)

	if(projection == "2d"):
		plt.figure()
		for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
			plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
		plt.legend()
		plt.title("ACP")
		plt.show()
	elif(projection =="3d"):
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



"""Test Space"""

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

inputFolder = "DATA"
data = generate_DataMatrixFromPatientFiles(inputFolder)
y = get_targetedY("center", inputFolder)
target_name = get_targetNames("center", inputFolder)
quickPCA(data, y, target_name, "3d")

'''Dummy Data'''
"""
patient1 = [1, 1, 1, 1]
patient2 = [9, 9, 9, 9]
patient3 = [10, 10, 10, 10]
patient4 = [10, 9, 10, 9]
X = numpy.array((patient1, patient2, patient3, patient4))
y = numpy.array((0, 1, 1, 1))
print y
target_name = ["Sain", "Malade"]

pca = PCA()
C = pca.fit(X).transform(X)
print C



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