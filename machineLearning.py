"""
Machine learning methods
for RD project.
"""

from trashlib import *
from trashlib2 import *
#from procedure import *

from sklearn import svm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import neighbors, datasets

from sklearn import *

#from sklearn.model_selection import KFold, cross_val_score
from sklearn.externals import joblib
#from sklearn import preprocessing


import matplotlib.pyplot as plt
from sklearn.covariance import EmpiricalCovariance, MinCovDet


def svmClassification(data, label, kernel, modelSaveFile, exploreCParameter, displayResult, returnValidation):
	"""
	IN PROGRESS

	# BUG REPORT :
		ValueError: X.shape[1] = 2 should be equal to 43, 
		the number of features at training time

	-> data is a numpy Array
	-> label is a numpy Array
	-> kernel is a string, could be:
		- linear
		- poly
		- rbf
	-> modelSaveFile is a string, should be ".pkl",
	   name of the file where the model is saved
	-> exploreCParameter is a boolean, 1 for enable
	   exploration, else 0
	-> displayResult is a boolean, work only if label
	   contain only 2 class
	-> returnValidation is a boolean, seems to have
	   trouble when low number of class
	"""

	X = preprocessing.scale(data)
	y = label

	validation = "undef"

	svc = svm.SVC(kernel=kernel)
	svc.fit(X, y)
	joblib.dump(svc, modelSaveFile) 
   	
   	# Validation 
	# cross-validated scores
	if(returnValidation):
		k_fold = KFold(n_splits=3)
		validation = cross_val_score(svc, X, y, cv=k_fold, n_jobs=1)


	if(exploreCParameter):
		# Compare The score of the model
		# With different values of parameter C
		# ( Penalty parameter of the error term )
		# a small value for C means the margin is calculated
		# using many or all of the observations around the
		# separating line (more regularization); a large value
		# for C means the margin is calculated on observations
		# close to the separating line (less regularization).
		C_s = np.logspace(-10, 0, 10)
		scores = list()
		scores_std = list()
		for C in C_s:
		    svc.C = C
		    this_scores = cross_val_score(svc, X, y, n_jobs=1)
		    scores.append(np.mean(this_scores))
		    scores_std.append(np.std(this_scores))

		# Plot the result
		plt.figure(1, figsize=(4, 3))
		plt.clf()
		plt.semilogx(C_s, scores)
		plt.semilogx(C_s, np.array(scores) + np.array(scores_std), 'b--')
		plt.semilogx(C_s, np.array(scores) - np.array(scores_std), 'b--')
		locs, labels = plt.yticks()
		plt.yticks(locs, list(map(lambda x: "%g" % x, locs)))
		plt.ylabel('CV score')
		plt.xlabel('Parameter C')
		plt.ylim(0, 1.1)
		plt.show()

	if(displayResult):
		# Graphical output of the classification
		# for now work only with bivalue labels
		# ( i.e looking for only 2 groups)
		fignum = 1
		clf = svm.SVC(kernel=kernel, gamma=2)
		clf.fit(X, y)

		plt.figure(fignum, figsize=(8, 8))
		plt.clf()
		plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80, facecolors='none', zorder=10)
		plt.scatter(X[:, 0], X[:, 1], c=y, zorder=10, cmap=plt.cm.Paired)
		plt.axis('tight')
		
		# grahpe scale
		x_min = np.amin(X)
		x_max = np.amax(X)
		y_min = np.amin(X)
		y_max = np.amax(X)

		clf.decision_function_shape='ovo'
		XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
		Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

		# Put the result into a color plot
		Z = Z.reshape(XX.shape)
		plt.figure(fignum, figsize=(4, 3))
		plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
		plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])

		plt.xlim(x_min, x_max)
		plt.ylim(y_min, y_max)

		plt.xticks(())
		plt.yticks(())
		fignum = fignum + 1

		#plt.show()
		figsaveName = modelSaveFile.split(".")
		figsaveName = "IMAGES/"+figsaveName[0]+".jpg"
		plt.savefig(figsaveName)
		plt.close()

	return validation




def get_targetAgainstTheRest(targetType, target, inputFolder):
	"""
	-> targetType is a string, could be:
		- center
		- date
		- disease
	-> target is a string, the name of a specific target
	-> inputFolder is a string, name of the folder where
	   patient files are stored.
	-> return a numpy array containing 1 for element that belong to target,
	else 0.
	-> used to get boolean y value (labels of data)
	"""
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
	listOfCenter = []
	listOfDate = []
	listOfDisease = []

	for patientFile in listOfPatientFiles:
		patientFileInArray = patientFile.split("\\") # change on Linux / Windows
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")

		patient_disease = patientFileInArray[0]
		patient_id = patientFileInArray[1]
		patient_center = patientFileInArray[2]
		patient_date = patientFileInArray[3]
			
		if(targetType == "center"):
			if(patient_center == target):
				listOfCenter.append(1)
			else:
				listOfCenter.append(0)

		elif(targetType == "date"):
			if(patient_date == target):
				listOfDate.append(1)
			else:
				listOfDate.append(0)

		elif(targetType == "disease"):
			if(patient_disease == target):
				listOfDisease.append(1)
			else:
				listOfDisease.append(0)


	if(targetType == "center"):
		target_center = numpy.array(tuple(listOfCenter))
		return target_center
	elif(targetType == "date"):
		target_date = numpy.array(tuple(listOfDate))
		return target_date
	elif(targetType == "disease"):
		target_disease = numpy.array(tuple(listOfDisease))
		return target_disease


def show_inlierDetection(modelFileName, trainingData, testData):
	"""
	-> modelFileName is a string, name of the pkl file 
	   containing the model.
	-> trainingData is a Numpy Array
	-> testData is a Numpy Array
	"""
	xx, yy = np.meshgrid(np.linspace(np.amin(trainingData), np.amax(trainingData), 500), np.linspace(np.amin(trainingData), np.amax(trainingData), 500))

	clf = joblib.load(modelFileName) 

	# standardization
	trainingData = preprocessing.scale(trainingData)
	testData = preprocessing.scale(testData)

	y_pred_train = clf.predict(trainingData)
	y_pred_test = clf.predict(testData)
	n_error_train = y_pred_train[y_pred_train == -1].size
	n_error_test = y_pred_test[y_pred_test == -1].size

	# plot the line, the points, and the nearest vectors to the plane
	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)

	plt.title("Novelty Detection")
	plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
	a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
	plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

	s = 40
	b1 = plt.scatter(trainingData[:, 0], trainingData[:, 1], c='white', s=s)
	b2 = plt.scatter(testData[:, 0], testData[:, 1], c='blueviolet', s=s)
	plt.axis('tight')
	plt.xlim((np.amin(trainingData), np.amax(trainingData)))
	plt.ylim((np.amin(trainingData), np.amax(trainingData)))
	plt.legend([a.collections[0], b1, b2],
	           ["learned frontier", "training observations",
	            "new observations"],
	           loc="upper left",
	           prop=matplotlib.font_manager.FontProperties(size=11))
	plt.xlabel("Density Estimation with One class SVM ")
	    
	plt.show()




def show_outlierDetection(X, X_outliers):
	"""
	-> X is a numpy array containing tje training data
	-> X_outliers is the data to test

	=> seems to have problem when X is small
	"""

	n_outliers = len(X_outliers)
	n_samples = len(X)
	X[-n_outliers:] = X_outliers

	# fit a Minimum Covariance Determinant (MCD) robust estimator to data
	# compare estimators learnt from the full data set with true parameters
	robust_cov = MinCovDet().fit(X)
	emp_cov = EmpiricalCovariance().fit(X)

	fig = plt.figure(facecolor = "white")
	plt.subplots_adjust(hspace=-.1, wspace=.4, top=.95, bottom=.05)

	# Show data set
	subfig1 = plt.subplot(3, 1, 1)
	inlier_plot = subfig1.scatter(X[:, 0], X[:, 1], color='black', label='inliers')
	outlier_plot = subfig1.scatter(X_outliers[:, 0], X_outliers[:, 1], color='red', label='outliers')
	subfig1.set_xlim(subfig1.get_xlim()[0], 11.)
	subfig1.set_title("Mahalanobis distances")

	# Show contours of the distance functions
	xx, yy = np.meshgrid(np.linspace(plt.xlim()[0], plt.xlim()[1], 100), np.linspace(plt.ylim()[0], plt.ylim()[1], 100))
	zz = np.c_[xx.ravel(), yy.ravel()]
	mahal_emp_cov = emp_cov.mahalanobis(zz)
	mahal_emp_cov = mahal_emp_cov.reshape(xx.shape)
	emp_cov_contour = subfig1.contour(xx, yy, np.sqrt(mahal_emp_cov), cmap=plt.cm.PuBu_r, linestyles='dashed')
	mahal_robust_cov = robust_cov.mahalanobis(zz)
	mahal_robust_cov = mahal_robust_cov.reshape(xx.shape)
	robust_contour = subfig1.contour(xx, yy, np.sqrt(mahal_robust_cov), cmap=plt.cm.YlOrBr_r, linestyles='dotted')
	subfig1.legend([emp_cov_contour.collections[1], robust_contour.collections[1], inlier_plot, outlier_plot], ['MLE dist', 'robust dist', 'inliers', 'test data'], loc="upper right", borderaxespad=0)
	plt.xticks(())
	plt.yticks(())

	# SubPLot 1
	emp_mahal = emp_cov.mahalanobis(X - np.mean(X, 0)) ** (0.33)
	subfig2 = plt.subplot(2, 2, 3)
	subfig2.boxplot([emp_mahal[:-n_outliers], emp_mahal[-n_outliers:]], widths=.25)
	subfig2.plot(1.26 * np.ones(n_samples - n_outliers), emp_mahal[:-n_outliers], '+k', markeredgewidth=1)
	subfig2.plot(2.26 * np.ones(n_outliers), emp_mahal[-n_outliers:], '+k', markeredgewidth=1)
	subfig2.axes.set_xticklabels(('inliers', 'test data'), size=15)
	subfig2.set_ylabel(r"$\sqrt[3]{\rm{(Mahal. dist.)}}$", size=16)
	subfig2.set_title("1. from non-robust estimates\n(Maximum Likelihood)")
	plt.yticks(())

	# SubPLot 2
	robust_mahal = robust_cov.mahalanobis(X - robust_cov.location_) ** (0.33)
	subfig3 = plt.subplot(2, 2, 4)
	subfig3.boxplot([robust_mahal[:-n_outliers], robust_mahal[-n_outliers:]], widths=.25)
	subfig3.plot(1.26 * np.ones(n_samples - n_outliers), robust_mahal[:-n_outliers], '+k', markeredgewidth=1)
	subfig3.plot(2.26 * np.ones(n_outliers), robust_mahal[-n_outliers:], '+k', markeredgewidth=1)
	subfig3.axes.set_xticklabels(('inliers', 'test data'), size=15)
	subfig3.set_ylabel(r"$\sqrt[3]{\rm{(Mahal. dist.)}}$", size=16)
	subfig3.set_title("2. from robust estimates\n(Minimum Covariance Determinant)")
	plt.yticks(())

	plt.show()




"""Test Space"""

"""
X = np.c_[(.4, -.7),
          (-1.5, -1),
          (-1.4, -.9),
          (-1.3, -1.2),
          (-1.1, -.2),
          (-1.2, -.4),
          (-.5, 1.2),
          (-1.5, 2.1),
          (1, 1),
          # --
          (1.3, .8),
          (1.2, .5),
          (.2, -2),
          (.5, -2.4),
          (.2, -2.3),
          (0, -2.7),
          (1.3, 2.1)].T

y = [0] * 8 + [1] * 8

"""


	
#iris = datasets.load_iris()
#X = iris.data
#X = PCA(n_components=2).fit_transform(iris.data)
#y = [0] * 100 + [1] * 50

"""
checkAndFormat("DATA/PANEL_3", "DATA/PATIENT")
X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "PROPORTION")
X = PCA(n_components=2).fit_transform(X)
y = get_targetAgainstTheRest("disease", "RA", "DATA/PATIENT")
scores = svmClassification(X, y, "poly", "filename.pkl", 0, 1, 0)
print scores
"""
"""
restore_Data()
apply_filter("disease", "Control")
X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "PROPORTION")
X = PCA(n_components=2).fit_transform(X)

restore_Data()
apply_filter("disease", "RA")
X_test = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "PROPORTION")
X_test = PCA(n_components=2).fit_transform(X_test)

show_outlierDetection(X, X_test)
#show_inlierDetection("filename.pkl", X, X_test)
"""
#X_test = np.random.uniform(low=3, high=4, size=(5, 2))

#print str(len(y)) + " || " +str(len(X)) 
#scores = svmClassification(X, y, "linear", "filename.pkl", 0, 1, 0)


#iris = datasets.load_iris()
#X = iris.data
#X = PCA(n_components=2).fit_transform(iris.data)
#X_test = np.random.uniform(low=3, high=4, size=(5, 2))
#show_outlierDetection(X, X_test)
#show_inlierDetection("filename.pkl", X, X_test)

#print scores

#show_outlierDetection(X, X_test)


