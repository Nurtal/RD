"""
A few procedures
ready to use
"""

from trashlib import *



def show_PCA(inputFolder, target, projection, saveFile):
	"""
	Perform and display PCA
	-> inputFolder is a string, indicate the folder where are patients files
	-> target is a string, currently only "center" and "date" are availabe
	-> projection can be set to "3d" or "2d"
	-> saveFile is a string, filename where graphical output is saved
	"""
	data = generate_DataMatrixFromPatientFiles(inputFolder)
	y = get_targetedY(target, inputFolder)
	target_name = get_targetNames(target, inputFolder)
	quickPCA(data, y, target_name, projection, saveFile)


def show_cluster(inputFolder, numberOfCluster, saveFile):
	"""
	Perform kmean clustering
	-> inputFolder is a string, name of the folder containing data
	-> numberOfCluster is an int, number of cluster to generate
	-> saveFile is a string, filename where graphical output is saved
	"""
	data = generate_DataMatrixFromPatientFiles(inputFolder)
	quickClustering(data, numberOfCluster, saveFile)


