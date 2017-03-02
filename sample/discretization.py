"""
Set of functions to perform
discretization
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





def binarization(data_file_name, conversion_dict):
	"""
	-> Perform a "binarization" of the value present in data_file_name,
	   with the dictionnary conversion_dict (create from the create_conversion_dict function)
	-> create a discreteMatrix_imputed_binary file in CYTOKINES folder

	-> TODO:
		- clean code
	"""

	data = open(data_file_name, "r")
	cmpt = 0
	indexToVariableName = {}
	indexOfVariableToDelete = []
	identifiant_index = "undef"
	variables_keep_index = []

	# Select Column to Write
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")
		if(cmpt==0):
			index = 0
			for variable in lineInArray:

				PossibleValueToBinaryValue = conversion_dict[variable]

				# catch the identifiant variable
				if(variable == "\Clinical\Sampling\OMICID"):
					identifiant_index = index
					variables_keep_index.append(identifiant_index)

				# catch the variable with binary values in description file
				if(len(PossibleValueToBinaryValue.values()) > 0):
					# scan the binary values for ERROR entry
					if("ERROR" not in PossibleValueToBinaryValue.values()):
						variables_keep_index.append(index)

				indexToVariableName[index] = variable			
				index += 1
		cmpt += 1
	data.close()
		

	# Perform the conversion
	data = open(data_file_name, "r")
	data_converted = open("DATA/CYTOKINES/discreteMatrix_imputed_binary.csv", "w")
	cmpt =0
	header_new = ""
	for line in data:
		lineWithoutBackN = line.split("\n")
		lineWithoutBackN = lineWithoutBackN[0]
		lineInArray = lineWithoutBackN.split(";")

		line_new = ""

		if(cmpt == 0):
			index = 0
			for variable in lineInArray:
				if(index in variables_keep_index):
					header_new += variable +";" 
				index += 1
			header_new = header_new[:-1]
			data_converted.write(header_new+"\n")


		else:
			index = 0
			for scalar in lineInArray:
				variable_name = indexToVariableName[index]
				if(index in variables_keep_index):
					PossibleValueToBinaryValue = conversion_dict[variable_name]
					if(index != identifiant_index):
						scalar_new = PossibleValueToBinaryValue[scalar]
					else:
						scalar_new = scalar

					line_new += scalar_new +";"

				index += 1
			line_new = line_new[:-1]
			data_converted.write(line_new+"\n")
		cmpt += 1
	data_converted.close()
	data.close()



# TEST SPACE
#machin = create_conversion_dict()
#binarization("DATA/CYTOKINES/discreteMatrix_imputed.csv", machin)