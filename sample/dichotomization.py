"""
dichotomization test
for RD
"""
import scipy.stats
import numpy
import math



def create_disjonct_table(variable, method, number_of_interval):
	"""
	-> build disjonctif table for a specific variable
	-> variable is a numpy.array
	-> method is a string, could be:
		- ecart_type (not workingfor now)
		- standard : create parse variable from min to max
		  and create interval of the same size
	-> number_of_interval is an int, the number of interval
	   you want for your table.

	TODO:
		- implement new methods
		- correct ecart_type implementation 
	"""
	description = scipy.stats.describe(variable)
	minmax = description[1]
	minimum = minmax[0]
	maximum = minmax[1]
	mean = description[2]
	variance = description[3]
	ecart_type = math.sqrt(variance)
	tableau = []

	# Creation du tableau
	if(method == "ecart_type"):

		#!!!!!!!!!!!!!!!!!!!!!!!!!#
		# NOT FONCTIONNAL FOR NOW #
		#!!!!!!!!!!!!!!!!!!!!!!!!!#

		# 1 => using ecart type
		# -> Determine le pas en se basant sur
		# le nombre interval souhaite.
		step = 1/float(number_of_interval)
		
		# Construction des interval
		interval_max = minimum
		for number in range(0,number_of_interval):
			interval_min = interval_max
			interval_max = interval_min + (number*step*ecart_type)

			#print str(interval_min) + " || " +str(interval_max)

		#print "-------------------"

	elif(method == "standard"):

		# 2 => using only min and max
		amplitude = maximum - minimum
		step = float(amplitude) / float(number_of_interval)
		interval_min = minimum
		interval_max = interval_min + step
		for number in range(0, number_of_interval):
			
			interval = []

			if(number == 0):
				interval_min = minimum
				interval_max = interval_min + step
			else:
				interval_min = interval_max
				interval_max = interval_min + step

			interval.append(interval_min)
			interval.append(interval_max)
			tableau.append(interval)

		return tableau


def create_disjonctTable_for_matrix(data, number_of_interval):
	"""
	-> create all disjonctif table for the matrix
	-> matrix is the input data
	-> number_of_interval is an int, the number of interval
	   to set for each variable.

	TODO:
		- select number_of_interval according to the description.xml
		  file
		- give a vector of number_of_interval

	"""
	variable_index_to_table = {}
	index = 1
	for variable in data.transpose():
		table = create_disjonct_table(variable, "standard", number_of_interval)
		variable_index_to_table[index] = table
		index += 1

	return variable_index_to_table

"""TEST SPACE"""
data = numpy.array([[45, 10, 23,0], [21,12,87,5],[87,2,56,10]])
variable = numpy.array([0,1,5,6,4,10])

# Create disjonct table => OK
table_test = create_disjonct_table(variable, "standard", 5)

# create disjonct table for all variable in a matrix
#	-> input : a matrix
#	-> output : dict of table {variableIndex : disjonctTable}
tables_test = create_disjonctTable_for_matrix(data, 5)

# use disjonct table for dichotomization