"""
"""

import dichotomization
import numpy
import random
import os
import platform
import operator
import math
import sys






class Individual(object):
	
	def __init__(self):
		self._id=-1
		self._intervals_to_variables = {}







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


def evaluate_individual(individual, data_file_name, method, filter_strat):
	"""
	-> Evaluate the individual using NN project
	-> individual is a Individual object
	-> data_file_name is the matrix file name
	-> method is a string, the method to use to compute the score,
	   could be:
	   		- nn (for neural network)
	   		- svm (for support vector machine)
	   		- tree (decision tree)
	-> filter_strat is a string, name of the filter aplly n cohorte,
	   could be:
	   			- random
	   			- any disesae (SLE, SjS ...)
	-> run evaluation script in the NN folder
	"""

	# Generate matrix from data file
	pack = dichotomization.extract_matrix_from(data_file_name)
	data = pack[0]
	variable_to_position = pack[1]

	# Create disjonct Table for Matrix
	disjonctif_tables = create_disjonctTable_for_matrix(data, variable_to_position, individual._intervals_to_variables)

	# use disjonct table for dichotomization
	#	- use matrix and table as input
	#	- return a new matrix
	data_dichotomized = dichotomize(data, disjonctif_tables)
	if(platform.system() == "Windows"):
		save_file_name = "DATA\\MATRIX\\data_dichotomized_pattern_individual_to_evaluate.csv"
	elif(platform.system() == "Linux"):
		save_file_name = "DATA/MATRIX/data_dichotomized_pattern_individual_to_evaluate.csv"
	save_dichotomized_matrix_in_file(pack[1], pack[2], data_dichotomized, individual._intervals_to_variables, save_file_name)

	# compute the score
	if(method == "nn"):
		# Run the NN and clean the data
		if(platform.system() == "Windows"):
			os.chdir("..\\..\\NN")
			os.system("python evaluation.py "+str(filter_strat))
			os.chdir("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample")
		elif(platform.system() == "Linux"):
			os.chdir("../../NN")
			os.system("python evaluation.py "+str(filter_strat))
			os.chdir("/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/RD/sample")
	
	elif(method == "svm"):
		# Run SVM evaluation in NN folder
		if(platform.system() == "Windows"):
			os.chdir("..\\..\\NN")
			os.system("python svm_evaluation.py "+str(filter_strat))
			os.chdir("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample")
		elif(platform.system() == "Linux"):
			os.chdir("../../NN")
			os.system("python svm_evaluation.py "+str(filter_strat))
			os.chdir("/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/RD/sample")
	
	elif(method == "tree"):
		# Run decision tree evaluation in NN folder
		if(platform.system() == "Windows"):
			os.chdir("..\\..\\NN")
			os.system("python svm_evaluation.py "+str(filter_strat))
			os.chdir("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample")
		elif(platform.system() == "Linux"):
			os.chdir("../../NN")
			os.system("python tree_evaluation.py "+str(filter_strat))
			os.chdir("/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/RD/sample")
	


	else:
		print "[ERROR] method: "+str(method)+" is not recognized"

	#os.remove(save_file_name)

	# Get the score
	score = -1
	if(platform.system() == "Windows"):
		score_file = open("..\\..\\NN\\evaluation_score.log", "r")
	elif(platform.system() == "Linux"):
		score_file = open("../../NN/evaluation_score.log", "r")
	for line in score_file:
		line = line.split("\n")
		line = line[0]
		score = line
	score_file.close()
	return score


def create_population(number_of_individual, data_file_name, intervals_min, intervals_max):
	"""
	-> Create a population of random initialized individuals
	"""
	pack = dichotomization.extract_matrix_from(data_file_name)
	variable_to_position = pack[1]

	population = []
	for x in range(0, number_of_individual):
		individual = Individual()
		individual._id = x
		individual._intervals_to_variables = create_random_individual(variable_to_position, intervals_min, intervals_max)
		population.append(individual)

	return population



def grade_population(population, data_file_name, score_method, filter_strat):
	"""
	-> Compute score for the population 
	(i.e average of individuals score in population)
	-> score_method is a string, the method to use for scoring, could be:
		- nn (neural network)
		- svm (support vector machine)
	-> filter_strat is a string, name of the filter aplly n cohorte,
	   could be:
	   			- random
	   			- any disesae (SLE, SjS ...)
	-> return also the dict individual : score

	"""

	score_list = []
	score_to_individuals = {}
	for individual in population:
		score = evaluate_individual(individual, data_file_name, score_method, filter_strat)
		score_list.append(float(score))
		score_to_individuals[individual._id] = score
	
	# compute final score
	final_score = numpy.average(score_list)

	return (final_score, score_to_individuals)



def get_best_individual_in_population(number_of_individual_to_keep, grades, population):
	"""
	-> return the bests individual in populations
	-> number_of_individual_to_keep is the number of bests candidate to retrieve
	-> grades is a tuple, generated by grade_population() function
	-> population is a list of individual
	"""
	individual_keep_number = number_of_individual_to_keep
	individual_keep_list = []
	best_individual = []
	
	x = grades[1]
	sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
	
	cmpt = 0
	for t in sorted_x:
		if(cmpt < individual_keep_number):
			individual_keep_list.append(t[0])
		cmpt += 1

	for individual in population:
		if(individual._id in individual_keep_list):
			best_individual.append(individual)

	return best_individual



def random_selection_of_bad_candidates(bests_candidates, population, number_of_bad_individual_to_keep):
	"""
	-> Randomly select bad individuals,
	-> best bests_candidates are obtain with the get_best_individual_in_population() function
	-> population is a list of individual
	-> number_of_bad_individual_to_keep is an int
	"""

	bad_individuals = []
	bad_individuals_selected = []
	bests_id = []

	for individual in bests_candidates:
		bests_id.append(individual._id)

	for individual in population:
		if(individual._id not in bests_id):
			bad_individuals.append(individual)

	for x in range(0, number_of_bad_individual_to_keep):
		random_id = random.randint(0, len(bad_individuals)-1)
		bad_individuals_selected.append(bad_individuals[random_id])

	return bad_individuals_selected



def mutation(mutation_rate, min_mutation_value, max_mutation_value, parents):
	"""
	-> random mutation for parents
	-> mutation rate is an int between 0 and 100
	-> min and max mutation value should be set to min and max init value
	   for the creation of individual
	"""
	for individual in parents:
		if(random.randint(0,100) <= mutation_rate):
			possible_parameter_to_mutate = individual._intervals_to_variables.keys()
			parameter_to_mutate = possible_parameter_to_mutate[random.randint(0, len(possible_parameter_to_mutate)-1)]
			individual._intervals_to_variables[parameter_to_mutate] = random.randint(min_mutation_value, max_mutation_value)




def get_youngest_id_in_population(population):
	"""
	-> return the id of the youngest member
	   in the population
	"""

	individual_id_list = []
	for individual in population:
		individual_id_list.append(individual._id)
	individual_id_list.sort()

	return individual_id_list[-1]


def create_children(parents, population):
	"""
	-> crossover between parents
	to create children
	-> parents are a list of individuals
	-> population is a list of Individuals (include parents)
	-> return a list of individuals
	"""
	parents_length = len(parents)
	desired_length = len(population) - parents_length
	children = []
	child_id = get_youngest_id_in_population(population) + 1
	while len(children) < desired_length:
		male = random.randint(0, parents_length-1)
		female = random.randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]

			parameters = male._intervals_to_variables.keys()
			half = len(parameters) / 2

			# child creation
			child = Individual()
			child._id = child_id

			# legacy from father
			for param in parameters[half:]:
				child._intervals_to_variables[param] = male._intervals_to_variables[param]
			
			# legacy from mother
			for param in parameters[:half]:
				child._intervals_to_variables[param] = female._intervals_to_variables[param]

			children.append(child)

		child_id += 1

		return children



"""The Big One"""


def run_ag_exploration(data_file, number_of_individual_per_generation, max_iteration, score_method, filter_strat):
	"""
	-> Run the genetic algorithm
	-> data_file used in the evaluation process
	-> number_of_individual_per_generation is an int
	-> max_iteration is an int
	-> score_method is a string, the method to use for scoring, could be:
		- nn (neural network)
		- svm (support vector machine)
		- tree (decision tree)
	-> filter_strat is a string, name of the filter aplly n cohorte,
	   could be:
	   			- random
	   			- any disesae (SLE, SjS ...)
	-> return nothing but write a few results file in DATA/EXPLORATION
	"""

	#--------------------#
	# General parameters #
	#--------------------#
	
	progress = 0
	mutation_rate = 10
	intervals_min = 2
	intervals_max = 10
	number_of_good_parents = 8
	number_of_bad_parents = 2
	score_threshold = 80


	result_file_name = "undef"
	solution_file_name = "undef"
	filter_name = "control_vs_"+str(filter_strat)

	if(platform.system() == "Linux"):
		result_file_name = data_file.split("/")
		result_file_name = result_file_name[-1]
		result_file_name = result_file_name.split(".")
		max_result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_max.csv"
		min_result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_min.csv"
		result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+".csv"
		result_file_name = "DATA/EXPLORATION/"+result_file_name
		max_result_file_name = "DATA/EXPLORATION/"+max_result_file_name
		min_result_file_name = "DATA/EXPLORATION/"+min_result_file_name

		solution_file_name = data_file.split("/")
		solution_file_name = solution_file_name[-1]
		solution_file_name = solution_file_name.split(".")
		solution_file_name = solution_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_FixeStep.log"
		solution_file_name = "DATA/EXPLORATION/"+solution_file_name	

	elif(platform.system() == "Windows"):
		result_file_name = data_file.split("\\")
		result_file_name = result_file_name[-1]
		result_file_name = result_file_name.split(".")
		max_result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_max.csv"
		min_result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_min.csv"
		result_file_name = result_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+".csv"
		result_file_name = "DATA\\EXPLORATION\\"+result_file_name
		max_result_file_name = "DATA\\EXPLORATION\\"+max_result_file_name
		min_result_file_name = "DATA\\EXPLORATION\\"+min_result_file_name

		solution_file_name = data_file.split("\\")
		solution_file_name = solution_file_name[-1]
		solution_file_name = solution_file_name.split(".")
		solution_file_name = solution_file_name[0]+"_"+str(filter_name)+"_"+str(score_method)+"_FixeStep.log"
		solution_file_name = "DATA\\EXPLORATION\\"+solution_file_name

	#--------------------#
	# Prepare Population #
	#--------------------#

	# Generate matrix from data file
	pack = dichotomization.extract_matrix_from(data_file)
	data = pack[0]
	variable_to_position = pack[1]

	# init population
	pop = create_population(number_of_individual_per_generation, data_file, intervals_min, intervals_max)

	# init results files
	result_file = open(result_file_name, "w")
	result_file.close()

	max_result_file = open(max_result_file_name, "w")
	max_result_file.close()

	min_result_file = open(min_result_file_name, "w")
	min_result_file.close()

	for x in range(0, max_iteration):

		#-------------------------#
		# Evaluate the individual #
		#-------------------------#

		# evaluate population
		g = grade_population(pop, data_file, score_method, filter_strat)

		# write result in file
		result_file = open(result_file_name, "a")
		result_file.write(str(x)+","+str(g[0])+"\n")
		result_file.close()

		# write solution in file if one of the individual in
		# population looks like a good solution (i.e score >= threshold)
		save_pop = False
		score_list = []
		for individual in pop:
			individual_score = g[1][individual._id]
			score_list.append(individual_score)
			if(float(individual_score) >= float(score_threshold)):
				save_pop = True

		if(save_pop):
			solution_file_name_processed = solution_file_name.replace("FixeStep", str(progress))
			solution_file = open(solution_file_name_processed, "w")
			for individual in pop:
				solution_file.write(">"+str(individual._id)+","+str(g[1][individual._id])+"\n")
				for key in individual._intervals_to_variables.keys():
					solution_file.write(str(key) +","+str(individual._intervals_to_variables[key])+"\n")
			solution_file.close()

		# Get the best score in population and write 
		# the result in a file
		best_score = max(score_list)
		max_score_file = open(max_result_file_name, "a")
		max_score_file.write(str(progress)+","+str(best_score)+"\n")
		max_score_file.close()

		# Get the worst score in population and write 
		# the result in a file
		worst_score = min(score_list)
		min_score_file = open(min_result_file_name, "a")
		min_score_file.write(str(progress)+","+str(worst_score)+"\n")
		min_score_file.close()



		#--------#
		# Evolve #
		#--------#

		# => Get the Bests in population
		bests = get_best_individual_in_population(number_of_good_parents, g, pop)

		# => Randomly select bad individuals
		bads = random_selection_of_bad_candidates(bests, pop, number_of_bad_parents)

		# => Mutate a small random portion of the population
		parents = bests + bads
		mutation(mutation_rate, intervals_min, intervals_max, parents)

		# => crossover parents to create children
		children = create_children(parents, pop)

		# => Merge parent and child to constitute the next population
		parents.extend(children)

		# progress bar
		step = float((100/max_iteration))
		progress += 1
		progress_perc = progress*step
		factor = math.ceil((progress_perc/2))
		progress_bar = "#" * int(factor)
		progress_bar += "-" * int(50 - factor)
		display_line = "["+str(score_method)+"]|"+progress_bar+"|"+str(progress)+"|"+str(g[0])
		sys.stdout.write("\r%d%%" % progress_perc)
		sys.stdout.write(display_line)
		sys.stdout.flush()



"""TEST SPACE"""
 

classifier_list = ["svm", "tree", "nn"]
filter_list = ["SLE", "SSc", "SjS", "random"]

for x in range(1,2):
	print "\n => Processing Panel "+str(x)+"\n"
	data_file = "DATA/MATRIX/panel_"+str(x)+"_filtered_processed.txt"
	
	for classifier in classifier_list:
		for cohorte_filter in filter_list:
			max_iteration = 10
			number_of_individual_per_generation = 16
			run_ag_exploration(data_file, number_of_individual_per_generation, max_iteration, classifier, cohorte_filter)






