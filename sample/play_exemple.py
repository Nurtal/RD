"""
Math project
"""



# => create cohorte

p_1 = [12, 5, -2, -15, "control"]
p_2 = [8, 4, -1, -12, "control"]
p_3 = [10, 6, -3, -8, "control"]
p_4 = [-5, 5, -2, 16, "patient"]
p_5 = [-1, 4, -1, 13, "patient"]

cohorte = [p_1, p_2, p_3, p_4, p_5]

data_file = open("SCRIPTS/cohorte.csv", "w")
for patient in cohorte:

	patient_in_line = ""
	for scalar in patient:
		patient_in_line += str(scalar)+";"

	patient_in_line = patient_in_line[:-1]
	data_file.write(patient_in_line+"\n")

data_file.close()


# => perform PCA
# - probably gone a use a R script


# cohorte modified



# perform PCA
