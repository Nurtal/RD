

index_to_keep = []
medication_index = []

data = open("data/clinical_i2b2trans_1.txt", "r")
output = open("data/clinical_i2b2trans_1.csv", "w")
output_clinical = open("data/clinical_data_phase_1.csv", "w")


cmpt = 0
for line in data:
	line = line.split("\n")
	line = line[0]
	line_in_array = line.split("\t")

	if(cmpt == 0):
		index = 0
		header_in_string = ""
		clinical_header_in_string = ""
		for element in line_in_array:
			header_in_string += str(element)+","
			element_in_array = element.split("\\")
			if("Clinical" in element_in_array):
				index_to_keep.append(index)
				clinical_header_in_string += str(element)+","
			index += 1

		header_in_string = header_in_string[:-1]
		header_in_string = header_in_string.replace(" ", "")
		output.write(header_in_string+"\n")

		clinical_header_in_string = clinical_header_in_string[:-1]
		clinical_header_in_string = clinical_header_in_string.replace(" ", "")
		output_clinical.write(clinical_header_in_string+"\n")



	else:
		index = 0
		line_in_string = ""
		clinical_line_in_string = ""
		for element in line_in_array:
			line_in_string += str(element)+","
			if(index in index_to_keep):
				clinical_line_in_string += str(element)+","
			index += 1

		line_in_string = line_in_string[:-1]
		line_in_string = line_in_string.replace(" ", "")
		output.write(line_in_string+"\n")

		clinical_line_in_string = clinical_line_in_string[:-1]
		clinical_line_in_string = clinical_line_in_string.replace(" ", "")
		output_clinical.write(clinical_line_in_string+"\n")

	cmpt += 1

output_clinical.close()
output.close()
data.close()