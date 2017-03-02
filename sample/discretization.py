"""
Set of functions to perform
discretization
"""


# Brute discretization, according to binary values


"""
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
			variableToPossibleValueToBinaryValue[variable] = {}
			index += 1
data.close()
"""


def create_conversion_dict():
	"""
	-> parse the variable_description.xml file and
	return a dictionnary for the discretization procedure:
	variable_name : Possible_Values : Binary_Values
	-> use for convert posible values of a variable into binary values
	-> return a dictionnary
	"""

	description_file_name = "PARAMETERS/variable_description.xml"
	variableToPossibleValueToBinaryValue = {}
	possible_values_array = []
	binary_values_array = []
	PossibleValueToBinaryValue = {}
	variable_name = ""
	record = 0
	cmpt = 0

	description = open(description_file_name, "r")
	for description_line in description:
		description_line_tronk = description_line.split("\n")
		description_line_tronk = description_line_tronk[0]

		if("\t" not in description_line_tronk and cmpt > 0 and "</" not in description_line_tronk ):
			
			variable_name = description_line_tronk.split("<")
			variable_name = variable_name[1].split(">")
			variable_name = variable_name[0]

			record = 1
			possible_values_array = []
			binary_values_array = []
			variableToPossibleValueToBinaryValue[variable_name] = {}
			PossibleValueToBinaryValue = {}

		elif(record == 1 and "<Possible_Values>" in description_line_tronk):
			description_line_array = description_line_tronk.split("<Possible_Values>")
			description_line_array = description_line_array[1].split("</Possible_Values>")
			description_line_array = description_line_array[0]
			possible_values_array = description_line_array.split(";")

		elif(record == 1 and "<Binary_Values>" in description_line_tronk):
			description_line_array = description_line_tronk.split("<Binary_Values>")
			description_line_array = description_line_array[1].split("</Binary_Values>")
			description_line_array = description_line_array[0]
			binary_values_array = description_line_array.split(";")
			record = 0
		
		if(len(possible_values_array) == len(binary_values_array)):
			possible_value_index = 0
			for possible_value in possible_values_array:
				binary_value = binary_values_array[possible_value_index]
				possible_value_index += 1
				PossibleValueToBinaryValue[possible_value] = binary_value
		
			variableToPossibleValueToBinaryValue[variable_name] = PossibleValueToBinaryValue

		cmpt += 1
	description.close()

	return variableToPossibleValueToBinaryValue



# Algo :

# 1 creation dict de conversion PossibleValueToBinaryValue



# 2 discretization avec le dict

