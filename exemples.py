"""
a few exemple data & procedure
for the RD project
"""
import numpy
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_exempleData(display):
	"""
	-> Load exemple data from the
	web for specific usage
	-> display is an integer,
		- 1 to display download data
		- 0 to display nothing
	"""
	digits = datasets.load_digits()

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


def exempleProcedure1():
	"""
	just compute 3
	exemple functions
	"""
	machin = load_exempleData(0)
	performAndDisplay_pca(machin, "3d")
	clustering_kmean(machin, 2)


def dummyDataTest():
	"""
	perform and display a pca
	on dummy variables
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
	fig = plt.figure()
	for c, i, target_name in zip("rgbcmykrgb", [0,1,2,3,4,5,6,7,8,9], target_name):
		plt.scatter(C[y == i,0], C[y == i,1], c=c, label=target_name)
	plt.legend()
	plt.title("ACP")
	plt.savefig("test.png")
	plt.close(fig)



dummyDataTest()