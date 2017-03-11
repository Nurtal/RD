"""
dichotomization test
for RD
"""
import scipy.stats
import numpy
import math

# data test
data = numpy.array([[45, 10, 23], [21,12,87],[87,2,56]])

# Algo
# -> Pour chaque variable calculer:
# 		- medianne
#		- ecart type
# 		-> Creation tableau disjonctif
#			-> Nombre de "case" dans le tableau



for variable in data.transpose():
	description = scipy.stats.describe(variable)
	mean = description[2]
	variance = description[3]
	ecart_type = math.sqrt(variance)

	# Creation du tableau