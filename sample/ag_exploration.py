"""
"""

import dichotomization
import numpy
import random
import os



def create_random_individual(variable_to_position, intervals_min, intervals_max):
	"""
	-> Create an individual (a dict structure)
	where variable match to number of intervals for discretization
	(init randomly between intervals_min and intervals_max)
	-> intervals_min is always >= 2
	-> variable_to_position is a dict, obtain from the dichotomization.extract_matrix_from
	   function
	"""
	individual = {}
	for variable_name in variable_to_position.values():
		intervals = random.randint(2, intervals_max)
		individual[variable_name] = intervals
	return individual


def create_disjonctTable_for_matrix(data, variable_to_position, individual):
	"""
	-> create all disjonctif table for the variables in data
	-> variable_to_position is a dict, obtain from the dichotomization.extract_matrix_from
	   function
	-> individual is a dict, get by create_random_individual function

	"""
	variable_index_to_table = {}
	index = 0
	variables_names = variable_to_position.values()

	for variable in data.transpose():
		variable_name = variables_names[index]
		number_of_interval = individual[variable_name]
		table = dichotomization.create_disjonct_table(variable, "quantiles", number_of_interval)
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
		variable_index = 0
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



def save_dichotomized_matrix_in_file(index_to_variable, row_to_patient, data, individual, data_save_name):
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
		number_of_steps = individual[variables]
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


def evaluate_individual(individual, data_file_name):
	"""
	-> Evaluate the individual using NN project
	-> individual is a dict, get by create_random_individual function
	-> data_file_name is the matrix file name
	-> use the evaluation.py script in NN project
	"""

	# Generate matrix from data file
	pack = dichotomization.extract_matrix_from(data_file_name)
	data = pack[0]
	variable_to_position = pack[1]

	# Create disjonct Table for Matrix
	disjonctif_tables = create_disjonctTable_for_matrix(data, variable_to_position, individual)

	# use disjonct table for dichotomization
	#	- use matrix and table as input
	#	- return a new matrix
	data_dichotomized = dichotomize(data, disjonctif_tables)
	save_file_name = "DATA\\MATRIX\\data_dichotomized_pattern_individual_to_evaluate.csv"
	save_dichotomized_matrix_in_file(pack[1], pack[2], data_dichotomized, individual, save_file_name)

	# Run the NN and clean the data
	os.chdir("..\\..\\NN")
	os.system("python evaluation.py")
	os.chdir("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample")
	os.remove(save_file_name)

	# Get the score
	score = -1
	score_file = open("..\\..\\NN\\evaluation_score.log", "r")
	for line in score_file:
		line = line.split("\n")
		line = line[0]
		score = line
	score_file.close()
	return score


def create_population(number_of_individual, data_file_name):
	"""
	-> Create a population of random initialized individuals
	"""
	pack = dichotomization.extract_matrix_from(data_file_name)
	variable_to_position = pack[1]

	population = []
	intervals_min = 2
	intervals_max = 100
	for x in range(0, number_of_individual):
		individual = create_random_individual(variable_to_position, intervals_min, intervals_max)
		population.append(individual)

	return population



def grade_population(population, data_file_name):
	"""
	-> Compute score for the population 
	(i.e average of individuals score in population)
	-> return also the dict individual : score

	=> Problem there, have to resolve identification
	   of individuals
	"""

	score_list = []
	score_to_individuals = {}
	for individual in population:
		score = evaluate_individual(machin, data_file_name)
		score_list.append(float(score))
		score_to_individuals[individual] = score
	# compute final score
	final_score = numpy.average(score_list)

	return (final_score, score_to_individuals)


"""TEST SPACE"""



#--------------------#
# Prepare Population #
#--------------------#

# Generate matrix from data file
pack = dichotomization.extract_matrix_from("DATA/MATRIX/panel_1_filtered_processed.txt")
data = pack[0]
variable_to_position = pack[1]

# init population
pop = create_population(3, "DATA/MATRIX/panel_1_filtered_processed.txt")

# create individual
machin = create_random_individual(variable_to_position, 2, 75)


#-------------------------#
# Evaluate the individual #
#-------------------------#

"""
# get score
score = evaluate_individual(machin, "DATA/MATRIX/panel_1_filtered_processed.txt")

# evaluate population
g = grade_population(pop, "DATA/MATRIX/panel_1_filtered_processed.txt")
"""


#--------#
# Evolve #
#--------#

# => Get the Bests in population
grades = grade_population(pop, "DATA/MATRIX/panel_1_filtered_processed.txt")
individual_to_score = grades[1]

print individual_to_score






# => Randomly select bad individuals

# => Breed together parent to repopulate

# => Merge parent and child to constitute the next population

# => Mutate a small random portion of the population
