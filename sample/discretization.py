"""
Set of functions to perform
discretization
"""


# Brute discretization, according to binary values
description_file_name = "PARAMETERS/variable_description.xml"
data_file_name = "DATA/CYTOKINES/discreteMatrix_imputed.csv"


data = open(data_file_name, "r")
cmpt = 0
indexToVariableName = {}
for line in data:
	
	lineWithoutBackN = line.split("\n")
	lineWithoutBackN = lineWithoutBackN[0]
	lineInArray = lineWithoutBackN.split(";")
	
	if(cmpt==0):
		index = 0
		for variable in lineInArray:	
			indexToVariableName[index] = variable
			index += 1
	else:
		index = 0
		for scalar in lineInArray:
			variable_name = indexToVariableName[index]

			description = open(description_file_name, "r")
			record = 0
			for description_line in description:
				description_line_tronk = description_line.split("\n")
				description_line_tronk = description_line_tronk[0]
				if("<"+str(variable_name)+">" in description_line_tronk):
					record = 1
				elif(record == 1 and "<Binary_Values>" in description_line_tronk):
					description_line_array = description_line_tronk.split("<Binary_Values>")
					description_line_array = description_line_array[1].split("</Binary_Values>")
					description_line_array = description_line_array[0]
					print variable_name + " => " + description_line_array
					record = 0



			description.close()


			index += 1

			

	cmpt += 1
data.close()



# Algo :

# 1 creation dict de conversion PossibleValueToBinaryValue



# 2 discretization avec le dict

