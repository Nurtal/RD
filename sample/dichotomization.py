"""
dichotomization test
for RD
"""
import scipy.stats
import numpy
import math




def extract_matrix_from(file_name):
	"""
	-> extract a matrix (numpy.array object)
	   from the file file_name
	-> Used to create matrix for the dichotomization process
	-> All parameters except for OMICID
	   and diagnostic are present in the matrix
	-> return a tuple (matrix, index_to_variable, row_to_patient)
	   where:
	   		-index_to_variable is a dict, position in a vector to
	         the name of the corresponding variable.
	        -row_to_patient is a dict, postion in matrix (row, i.e vector index)
	         to the OMICID of the corresponding patient.
	"""

	index_to_variable = {}
	row_to_patient = {}
	OMICID_index = "undef"
	exclude_list = ["OMICID", "diagnostic"]
	matrix = []

	# initialise index to variable dictionnary
	# create matrix without OMICID and diagnostic
	file_data = open(file_name, "r")
	cmpt_line = 0
	for line in file_data:
		line = line.split("\n")
		line = line[0]
		line_array = line.split(";")
		if(cmpt_line == 0):
			cmpt_index = 0
			for scalar in line_array:
				if(scalar not in exclude_list):
					index_to_variable[cmpt_index] = scalar
				if(scalar == "OMICID"):
					OMICID_index = cmpt_index
				cmpt_index += 1
		else:
			cmpt_index = 0
			vector = []
			for scalar in line_array:
				if(cmpt_index in index_to_variable.keys()):
					vector.append(float(scalar))
				cmpt_index += 1
			matrix.append(vector)
		cmpt_line += 1
	file_data.close()

	matrix = numpy.array(matrix)

	# initialise row to patient dictionnary
	file_data = open(file_name, "r")
	cmpt_line = 0
	for line in file_data:
		line = line.split("\n")
		line = line[0]
		line_array = line.split(";")
		if(cmpt_line > 0):
			patient_omicid = line_array[OMICID_index]
			row_to_patient[cmpt_line] = patient_omicid
		cmpt_line += 1
	file_data.close()

	return (matrix, index_to_variable, row_to_patient)





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


def dichotomize(data, tables):
	"""
	-> perform dichotomization on data, using tables.
	-> data is a matrix
	-> tables is a listof disjonctif table (i.e 2D array)
	-> return a new dichotomized matrix
	"""
	data_new = []
	for vector in data:
		variable_index = 1
		vector_new = []
		for scalar in vector:
			scalar_new = []
			interval_list = tables[variable_index]
			for interval in interval_list:
				interval_min = interval[0]
				interval_max = interval[1]
				if(scalar >= interval_min and scalar <= interval_max):
					scalar_new.append(1)
				else:
					scalar_new.append(0)
			vector_new.append(scalar_new)
			variable_index += 1
		vector_new_1D = []
		for elt in vector_new:
			vector_new_1D += elt
		data_new.append(vector_new_1D)

	return data_new




def save_dichotomized_matrix_in_file(index_to_variable, row_to_patient, data, number_of_steps, data_save_name):
	"""
	-> save dichotomized matrix in file data_save_name
	-> index_to_variable is a dict, generated with the extract_matrix_from function
	-> row_to_patient is a dict, generated with the extract_matrix_from function
	-> data is the dichotomized matrix
	-> number_of_steps is the number of interval used for the dichotomization
	-> Used to prepare a file for the NN module
	"""
	
	header = ""
	data_save = open(data_save_name, "w")

	for variables in index_to_variable.values():
		for iteration in xrange(0, number_of_steps):
			header += variables+"_ITERATION_"+str(iteration)+";"
	header = header + "OMICID"

	data_save.write(header+"\n")
	cmpt_row = 1
	for vector in data:
		line_new = ""
		cmpt_index = 0
		for scalar in vector:
			line_new += str(scalar) +";"
			cmpt_index += 1

		line_new += str(row_to_patient[cmpt_row])
		data_save.write(line_new+"\n")
		cmpt_row += 1 
	data_save.close()



"""TEST SPACE"""
data = numpy.array([[45, 10, 23,0], [21,12,56,5],[87,2,87,10]])
variable = numpy.array([0,1,5,6,4,10])

tables = create_disjonctTable_for_matrix(data, 3)
truc = dichotomize(data, tables)


cmpt_vector = 0
for vector in truc:
	print data[cmpt_vector]
	print vector
	cmpt_vector += 1



# Generate matrix from data file
pack = extract_matrix_from("DATA/MATRIX/panel_1_filtered_processed.txt")
data = pack[0]

# create disjonct table for all variable in a matrix
#	-> input : a matrix
#	-> output : dict of table {variableIndex : disjonctTable}
#tables_test = create_disjonctTable_for_matrix(data, 5)

# use disjonct table for dichotomization
#	- use matrix and table as input
#	- return a new matrix
#truc = dichotomize(data, tables_test)


# save dichotomized matrix in a file to be processed by NN
#save_dichotomized_matrix_in_file(pack[1], pack[2], truc, 5, "DATA/MATRIX/data_dichotomized_test.csv")

	



