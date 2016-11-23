import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA

# import some data to play with
iris = datasets.load_iris()
#X = iris.data[:, :2]  # we only take the first two features.
X = iris.data
Y = iris.target


"""
x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

plt.figure(2, figsize=(8, 6))
plt.clf()


# Plot the training points
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
"""



"""

# To getter a better understanding of interaction of the dimensions
# plot the first three PCA dimensions
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = PCA(n_components=3).fit_transform(iris.data)
ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=Y,
           cmap=plt.cm.Paired)
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])

plt.show()



X_reduced = PCA(n_components=3).fit_transform(iris.data)
x_min, x_max = X_reduced[:, 0].min() - .5, X_reduced[:, 0].max() + .5
y_min, y_max = X_reduced[:, 1].min() - .5, X_reduced[:, 1].max() + .5

plt.figure(2, figsize=(8, 6))
plt.clf()

# Plot the training points
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=Y, cmap=plt.cm.Paired)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())

plt.show()

"""

#####################################################################################

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


# Our dataset and targets
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


Y = [0] * 8 + [1] * 8

X = PCA(n_components=2).fit_transform(iris.data)
#Y = iris.target
Y = [0] * 100 + [1] * 50

print Y


# figure number
fignum = 1

# fit the model
for kernel in ('linear', 'poly', 'rbf'):
    clf = svm.SVC(kernel=kernel, gamma=2)
    clf.fit(X, Y)

    # plot the line, the points, and the nearest vectors to the plane
    plt.figure(fignum, figsize=(8, 8))
    plt.clf()


    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80, facecolors='none', zorder=10)
    plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)

    plt.axis('tight')
    x_min = -3
    x_max = 3
    y_min = -3
    y_max = 3

    clf.decision_function_shape='ovo'


    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    print Z.shape
    print XX.shape
    print YY.shape

    # Put the result into a color plot
    Z = Z.reshape(XX.shape)
    plt.figure(fignum, figsize=(4, 3))
    plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
    plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],
                levels=[-.5, 0, .5])

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.xticks(())
    plt.yticks(())
    fignum = fignum + 1

plt.show()


"""

############################################################

"""
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import datasets, svm

digits = datasets.load_digits()
X = digits.data
y = digits.target

svc = svm.SVC(kernel='linear')
C_s = np.logspace(-10, 0, 10)

scores = list()
scores_std = list()
for C in C_s:
    svc.C = C
    this_scores = cross_val_score(svc, X, y, n_jobs=1)
    scores.append(np.mean(this_scores))
    scores_std.append(np.std(this_scores))

# Do the plotting
import matplotlib.pyplot as plt
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
"""


#############################################################################

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


def plot_decision_function(classifier, sample_weight, axis, title):
    # plot the decision function
    xx, yy = np.meshgrid(np.linspace(-4, 5, 500), np.linspace(-4, 5, 500))

    Z = classifier.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # plot the line, the points, and the nearest vectors to the plane
    axis.contourf(xx, yy, Z, alpha=0.75, cmap=plt.cm.bone)
    axis.scatter(X[:, 0], X[:, 1], c=y, s=100 * sample_weight, alpha=0.9,
                 cmap=plt.cm.bone)

    axis.axis('off')
    axis.set_title(title)


# we create 20 points
np.random.seed(0)
X = np.r_[np.random.randn(10, 2) + [1, 1], np.random.randn(10, 2)]
y = [1] * 10 + [-1] * 10


# test
X = PCA(n_components=2).fit_transform(iris.data)
y = iris.target

print y


sample_weight_last_ten = abs(np.random.randn(len(X)))
sample_weight_constant = np.ones(len(X))
# and bigger weights to some outliers
sample_weight_last_ten[15:] *= 5
sample_weight_last_ten[9] *= 15

# for reference, first fit without class weights

# fit the model
clf_weights = svm.SVC()
clf_weights.fit(X, y, sample_weight=sample_weight_last_ten)

clf_no_weights = svm.SVC()
clf_no_weights.fit(X, y)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
plot_decision_function(clf_no_weights, sample_weight_constant, axes[0],
                       "Constant weights")
plot_decision_function(clf_weights, sample_weight_last_ten, axes[1],
                       "Modified weights")

plt.show()

"""


################################################################################

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
from sklearn.externals import joblib
from sklearn import preprocessing

xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))


# Generate train data
X = 0.3 * np.random.randn(100, 2)
X = PCA(n_components=2).fit_transform(iris.data) # test
X_train = np.r_[X + 2, X - 2]



# Generate some regular novel observations
X = 0.3 * np.random.randn(20, 2)
X_test = np.r_[X + 2, X - 2]
# Generate some abnormal novel observations
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))


# fit the model
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(X_train)

joblib.dump(clf, "test.pkl")


clf = joblib.load('test.pkl') 

y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
#y_pred_outliers = clf.predict(X_outliers)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
#n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size


# plot the line, the points, and the nearest vectors to the plane
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)


plt.title("Novelty Detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

s = 40
b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=s)
b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=s)
#c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=s)
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend([a.collections[0], b1, b2],
           ["learned frontier", "training observations",
            "new observations"],
           loc="upper left",
           prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlabel(
    "error train: %d/200 ; errors novel observations: %d/40 ; "
    % (n_error_train, n_error_test))
plt.show()



def show_inlierDetection(modelFileName, trainingData, testData):
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



show_inlierDetection("test.pkl", X_train, X_test)

"""

####################################################################################


"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.covariance import EmpiricalCovariance, MinCovDet

#n_samples = 150
#n_outliers = 25
#n_features = 2

# generate data
#gen_cov = np.eye(n_features)
#gen_cov[0, 0] = 2.
#X = np.dot(np.random.randn(n_samples, n_features), gen_cov)
X = PCA(n_components=2).fit_transform(iris.data) # test


# add some outliers
#outliers_cov = np.eye(n_features)
#outliers_cov[np.arange(1, n_features), np.arange(1, n_features)] = 7.
#X[-n_outliers:] = np.dot(np.random.randn(n_outliers, n_features), outliers_cov)


X_outliers = np.random.uniform(low=3, high=4, size=(20, 2))


def show_outlierDetection(X, X_outliers):

	n_outliers = len(X_outliers)
	n_samples = len(X)
	X[-n_outliers:] = X_outliers

	# fit a Minimum Covariance Determinant (MCD) robust estimator to data
	robust_cov = MinCovDet().fit(X)

	# compare estimators learnt from the full data set with true parameters
	emp_cov = EmpiricalCovariance().fit(X)


	fig = plt.figure()
	plt.subplots_adjust(hspace=-.1, wspace=.4, top=.95, bottom=.05)

	# Show data set
	subfig1 = plt.subplot(3, 1, 1)
	inlier_plot = subfig1.scatter(X[:, 0], X[:, 1], color='black', label='inliers')
	outlier_plot = subfig1.scatter(X_outliers[:, 0], X_outliers[:, 1], color='red', label='outliers')
	subfig1.set_xlim(subfig1.get_xlim()[0], 11.)
	subfig1.set_title("Mahalanobis distances of a contaminated data set:")

	# Show contours of the distance functions
	xx, yy = np.meshgrid(np.linspace(plt.xlim()[0], plt.xlim()[1], 100),
	                     np.linspace(plt.ylim()[0], plt.ylim()[1], 100))
	zz = np.c_[xx.ravel(), yy.ravel()]

	mahal_emp_cov = emp_cov.mahalanobis(zz)
	mahal_emp_cov = mahal_emp_cov.reshape(xx.shape)
	emp_cov_contour = subfig1.contour(xx, yy, np.sqrt(mahal_emp_cov),
	                                  cmap=plt.cm.PuBu_r,
	                                  linestyles='dashed')

	mahal_robust_cov = robust_cov.mahalanobis(zz)
	mahal_robust_cov = mahal_robust_cov.reshape(xx.shape)
	robust_contour = subfig1.contour(xx, yy, np.sqrt(mahal_robust_cov),
	                                 cmap=plt.cm.YlOrBr_r, linestyles='dotted')

	subfig1.legend([emp_cov_contour.collections[1], robust_contour.collections[1],
	                inlier_plot, outlier_plot],
	               ['MLE dist', 'robust dist', 'inliers', 'outliers'],
	               loc="upper right", borderaxespad=0)
	plt.xticks(())
	plt.yticks(())

	# Plot the scores for each point
	emp_mahal = emp_cov.mahalanobis(X - np.mean(X, 0)) ** (0.33)
	subfig2 = plt.subplot(2, 2, 3)
	subfig2.boxplot([emp_mahal[:-n_outliers], emp_mahal[-n_outliers:]], widths=.25)
	subfig2.plot(1.26 * np.ones(n_samples - n_outliers), emp_mahal[:-n_outliers], '+k', markeredgewidth=1)
	subfig2.plot(2.26 * np.ones(n_outliers), emp_mahal[-n_outliers:], '+k', markeredgewidth=1)
	subfig2.axes.set_xticklabels(('inliers', 'outliers'), size=15)
	subfig2.set_ylabel(r"$\sqrt[3]{\rm{(Mahal. dist.)}}$", size=16)
	subfig2.set_title("1. from non-robust estimates\n(Maximum Likelihood)")
	plt.yticks(())

	robust_mahal = robust_cov.mahalanobis(X - robust_cov.location_) ** (0.33)
	subfig3 = plt.subplot(2, 2, 4)
	subfig3.boxplot([robust_mahal[:-n_outliers], robust_mahal[-n_outliers:]],
	                widths=.25)
	subfig3.plot(1.26 * np.ones(n_samples - n_outliers),
	             robust_mahal[:-n_outliers], '+k', markeredgewidth=1)
	subfig3.plot(2.26 * np.ones(n_outliers),
	             robust_mahal[-n_outliers:], '+k', markeredgewidth=1)
	subfig3.axes.set_xticklabels(('inliers', 'outliers'), size=15)
	subfig3.set_ylabel(r"$\sqrt[3]{\rm{(Mahal. dist.)}}$", size=16)
	subfig3.set_title("2. from robust estimates\n(Minimum Covariance Determinant)")
	plt.yticks(())

	plt.show()

show_outlierDetection(X, X_outliers)


"""

####################################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm




xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))

# Generate train data
#X = 0.3 * np.random.randn(100, 2)
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
X_train = np.r_[X + 2, X - 2]


# Generate some regular novel observations
X = 0.3 * np.random.randn(20, 2)
X_test = np.r_[X + 2, X - 2]


# Generate some abnormal novel observations
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

def oneClassSvm(X_train, X_outliers):

	# fit the model
	clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
	clf.fit(X_train)
	y_pred_train = clf.predict(X_train)
	#y_pred_test = clf.predict(X_test)
	y_pred_outliers = clf.predict(X_outliers)
	n_error_train = y_pred_train[y_pred_train == -1].size
	#n_error_test = y_pred_test[y_pred_test == -1].size
	n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

	# plot the line, the points, and the nearest vectors to the plane
	Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)

	plt.title("Novelty Detection")
	plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
	a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
	plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

	s = 40
	b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=s)
	#b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=s)
	c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=s)
	plt.axis('tight')
	plt.xlim((-5, 5))
	plt.ylim((-5, 5))
	plt.legend([a.collections[0], b1, c],
	           ["learned frontier", "training observations",
	            "new regular observations", "new abnormal observations"],
	           loc="upper left",
	           prop=matplotlib.font_manager.FontProperties(size=11))
	plt.xlabel(
	    "error train: %d/200 ; errors novel regular: ; "
	    "errors novel abnormal: %d/40"
	    % (n_error_train, n_error_outliers))
	plt.show()

#oneClassSvm(X_train, X_outliers)