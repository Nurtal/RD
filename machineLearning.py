"""
Machine learning methods
for RD project.
"""

from trashlib import *
from trashlib2 import *

from sklearn import svm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.model_selection import KFold, cross_val_score
from sklearn.externals import joblib

import matplotlib.pyplot as plt



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

	X = data
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
		# WIth different values of parameter C
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
		
		# have to work on this
		x_min = -3
		x_max = 3
		y_min = -3
		y_max = 3

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

		plt.show()

	return validation











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


iris = datasets.load_iris()
X = iris.data
X = PCA(n_components=2).fit_transform(iris.data)
y = [0] * 100 + [1] * 50
"""

scores = svmClassification(X, y, "poly", "filename.pkl", 0, 1, 0)


