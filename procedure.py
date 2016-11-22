"""
A few procedures
ready to use
"""
import os
from trashlib import *
from trashlib2 import *
from machineLearning import *



def show_PCA(inputFolder, target, projection, saveFile, dataType, details):
	"""
	Perform and display PCA
	-> inputFolder is a string, indicate the folder where are patients files
	-> target is a string, currently only "center" and "date" are availabe
	-> projection can be set to "3d" or "2d"
	-> saveFile is a string, filename where graphical output is saved
	"""
	data = generate_DataMatrixFromPatientFiles2(inputFolder, dataType)
	y = get_targetedY(target, inputFolder)
	target_name = get_targetNames(target, inputFolder)
	quickPCA(data, y, target_name, projection, saveFile, details)


def show_cluster(inputFolder, numberOfCluster, saveFile):
	"""
	Perform kmean clustering
	-> inputFolder is a string, name of the folder containing data
	-> numberOfCluster is an int, number of cluster to generate
	-> saveFile is a string, filename where graphical output is saved
	"""
	data = generate_DataMatrixFromPatientFiles(inputFolder)
	quickClustering(data, numberOfCluster, saveFile)


def show_correlationMatrix(inputFolder, saveName, dataType):
	"""
	IN ROGRESS
	"""
	data = generate_DataMatrixFromPatientFiles2(inputFolder, dataType)
	listOfParametres = get_listOfParameters2(inputFolder, dataType)
	display_correlationMatrix(data.transpose(), listOfParametres, saveName)


def checkAndFormat(inputFolder, outputFolder):
	"""
	IN PROGRESS
	"""
	
	listOfFilesToDelete = glob.glob(outputFolder+"/*.csv")
	for fileName in listOfFilesToDelete:
		os.remove(fileName)
	listOfFilesToDelete = glob.glob("DATA/VECTOR/*.csv")
	for fileName in listOfFilesToDelete:
		os.remove(fileName)
	convert_tabSepratedFile(inputFolder, outputFolder)


def RunOnFullData():
	"""
	IN PROGRESS
	"""
	listOfElements = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6","PANEL_7","PANEL_8","PANEL_9"]
	for panel in listOfElements:
		folder = "DATA/"+str(panel)
		saveName = str(panel)+"_matrixCorrelation.jpg"
		print folder
		checkAndFormat(folder, "DATA/PATIENT")
		show_correlationMatrix("DATA/PATIENT", saveName)



def OverviewOnPanel(panel, dataType, target):
	"""
	IN PROGRESS
	"""
	folder = "DATA/"+str(panel)
	saveName1 = "IMAGES/"+str(panel)+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+str(panel)+"_PCA2D.jpg"
	saveName3 = "IMAGES/"+str(panel)+"_PCA3D.jpg"
	checkAndFormat(folder, "DATA/PATIENT")
	show_correlationMatrix("DATA/PATIENT", saveName1, dataType)
	show_PCA("DATA/PATIENT", target, "2d", saveName2, dataType, 0)
	show_PCA("DATA/PATIENT", target, "3d", saveName3, dataType, 1)	



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

