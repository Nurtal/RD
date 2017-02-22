"""
analysis lib for RD
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




def quickClustering(matrice, numberOfClusters, saveFile):
	"""
	perform and display a kmean clusterring
	-> matrice is a numpy.array
	-> numberOfClusters is a int
	-> saveFile is a string
	"""
	pca = PCA()
	C = pca.fit(matrice).transform(matrice)

	est=KMeans(n_clusters=numberOfClusters)
	est.fit(matrice)
	classe=est.labels_

	print classe

	fig = plt.figure(1, figsize=(8, 6))
	ax = Axes3D(fig, elev=-150, azim=110)
	ax.scatter(C[:, 0], C[:, 1], C[:, 2], c=classe, cmap=plt.cm.Paired)
	ax.set_title("kmean : "+str(numberOfClusters)+" clusters")
	ax.set_xlabel("Comp1")
	ax.w_xaxis.set_ticklabels([])
	ax.set_ylabel("Comp2")
	ax.w_yaxis.set_ticklabels([])
	ax.set_zlabel("Comp3")
	ax.w_zaxis.set_ticklabels([])
	plt.savefig(saveFile)
	plt.show()


def get_targetNames(target, inputFolder):
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
	listOfId = []
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
		elif(target == "id"):
			if(patient_disease not in listOfId):
				listOfId.append(patient_id)

	if(target == "center"):
		return listOfCenter
	elif(target == "date"):
		return listOfDate
	elif(target == "disease"):
		return listOfDisease
	elif(target == "id"):
		return listOfId


def get_targetedY(target, inputFolder):
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
	listOfId = []

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

		target_names = get_targetNames(target, inputFolder)
			
		cmpt_color = 0
		for element in target_names:
			if(target == "center" and patient_center == element):	
				listOfCenter.append(cmpt_color)
			elif(target == "date" and patient_date == element):
				listOfDate.append(cmpt_color)
			elif(target == "disease" and patient_disease == element):
				listOfDisease.append(cmpt_color)
			elif(target == "id" and patient_id == element):
				listOfId.append(cmpt_color)
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
	elif(target == "id"):
		target_id = numpy.array(tuple(listOfId))
		return target_id


def quickPCA(data, y, target_name, projection, saveName, details, show):
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
		plt.figure()
		for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
			plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
		plt.legend()
		plt.title("ACP")
		plt.savefig(saveName)
		if(show):
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
			plt.show()
		plt.close()



def display_correlationMatrix(data, listOfParameters, saveName, show):
	"""
	display a graphe representation of the correlation matrix of
	data.
	-> data is numpy.Array object
	-> listOfParameters is the list of parameters in data.
	-> may have to transpose data (data.transpose())
	-> show is a boolean, if 1: display graphe
	"""
	matrixCorr = numpy.corrcoef(data)
	listOfIndex = range(0, len(listOfParameters))
	fig = plt.figure(1, figsize=(24, 12))
	plt.imshow(matrixCorr, cmap=cm.jet, interpolation='nearest')
	plt.colorbar()
	plt.xticks(listOfIndex, listOfParameters, rotation=90)
	plt.yticks(listOfIndex, listOfParameters)
	plt.savefig(saveName)
	if(show):
		plt.show()
	plt.close()


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

		#print "=> " +str(patientFile)

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
	TODO:
		- marche mal pour "ALL", doublons dans les noms de 
		parametres
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
	for 2d or 3d visualisation.
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfVectorFiles = []

	for patientFile in listOfPatientFiles:

		patientFilesInArray = patientFile.split(".")
		patientFilesInArray = patientFilesInArray[0]
		if(platform.system() == "Linux"):
			patientFilesInArray = patientFilesInArray.split("/")
		elif(platform.system() == "Windows"):
			patientFilesInArray = patientFilesInArray.split("\\")
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



