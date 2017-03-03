"""
main for RD project
"""


#-------------#
# IMPORTATION #######################################################################
#-------------#
from procedure import *
from report import *
from preprocessing import *
from patternMining import *
from cytokines import *
import describe
import sys





#----------------------#
# GET SCRIPT ARGUMENTS ################################################################
#----------------------#
command = sys.argv[1]
listOfCommand = ["program_size",
				 "display_commands",
				 "build_cytokines_data",
				 "show_cytokines_data",
				 "describe_cytokines_eigenVectors",
				 "extract_cytokines_pattern",
				 "generate_cytokines_associationRules",
				 "describe_variableFromCyto",
				 "describe_autoantibodies",
				 "process_associationRules",
				 "describe_discrete_variable",
				 "run_pattern_mining",
				 "remove_data",
				 "build_descriptionFile" ]





#-----------------#
# EXECUTE COMMAND ###########################################################################
#-----------------#
if(command == "program_size"):
	machin = count_line()
	print "[*] program contain "+str(machin)+" lines."

if(command == "display_commands"):
	for element in listOfCommand:
		print "[*] " + element
                                                                                                                                                                                                                                                                                                                                        
if(command == "build_cytokines_data"):
	CreateIndexFile()
	CreateMatrix("DATA/CYTOKINES/clinical_i2b2trans.txt", "DATA/CYTOKINES/matrix.csv")
	format_OMICID("DATA/CYTOKINES/matrix.csv")
	extractBinaryMatrix()
	extractQuantitativeMatrix()

if(command == "show_cytokines_data"):
	PlotProcedure_fittingDisease()

if(command == "describe_cytokines_eigenVectors"):
	numberOfVector = sys.argv[2]
	numberOfVariableToDescribe = sys.argv[3]
	plot_composanteOfEigenVector("DATA/CYTOKINES/quantitativeMatrix.csv", numberOfVariableToDescribe, int(numberOfVector))

if(command == "extract_cytokines_pattern"):
	minsup = sys.argv[2]
	if(minsup == "explore"):
		discretisation_Procedure()
		cohorte = assemble_CohorteFromAllFiles()
		for x in xrange(0, 101):
			extractPatternFromCohorte(cohorte, x, "cytokines")
	else:
		discretisation_Procedure()
		cohorte = assemble_CohorteFromAllFiles()
		extractPatternFromCohorte(cohorte, minsup, "cytokines")

if(command == "generate_cytokines_associationRules"):
	minsup = sys.argv[2]
	confidenceThreshold = sys.argv[3]
	if(minsup == "all"):
		for x in xrange(40, 101): # min set to 40
			minsup = x
			patternFile = "DATA/PATTERN/cytokines_pattern_"+str(minsup)+".csv"
			rulesFile = "DATA/RULES/cytokines_rules_"+str(minsup)+".csv"
			generate_AssociationRulesFromPatternFile(patternFile, rulesFile, confidenceThreshold, 1, "all")	
	else:
		patternFile = "DATA/PATTERN/cytokines_pattern_"+str(minsup)+".csv"
		rulesFile = "DATA/RULES/cytokines_rules_"+str(minsup)+".csv"
		generate_AssociationRulesFromPatternFile(patternFile, rulesFile, confidenceThreshold, 1, "all")

if(command == "describe_variableFromCyto"):
	variableType = sys.argv[2]
	variable = sys.argv[3]
	clean_folders("ALL")
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	#apply_filter("disease", "RA")
	check_patient()
	X = get_OneDimensionnalData("DATA/PATIENT", str(variableType), str(variable))
	show_distribution(X)

if(command == "describe_autoantibodies"):
	diagnostic = sys.argv[2]
	display = sys.argv[3]
	plot_autoantibodiesData(diagnostic, display)

if(command == "process_associationRules"):
	ListOfRulesFile = glob.glob("DATA/RULES/RAW/*.csv")
	for ruleFile in ListOfRulesFile:
		filter_associationRules_paramaterStatus(ruleFile)

	ListOfRulesFile = glob.glob("DATA/RULES/FILTERED/*.csv")
	for ruleFile in ListOfRulesFile:
		reformat_RulesFile(ruleFile)

	ListOfRulesFile = glob.glob("DATA/RULES/FILTERED/*.csv")
	for ruleFile in ListOfRulesFile:
		write_decryptedRulesFiles(ruleFile)

if(command == "describe_discrete_variable"):
	variableName = sys.argv[2]
	splitCohorteAccordingToDiagnostic("DATA/CYTOKINES/discreteMatrix.csv", "DATA/patientIndex.csv")
	cohorte = assemble_CohorteFromDiscreteAllFiles()
	describe_discreteVariable(cohorte, variableName)


if(command == "run_pattern_mining"):
	#---------------------------------#
	# Pattern mining on discrete data #
	# To be continued (Imputation)    #
	# Work on Discrete Data  		  #
	#---------------------------------#

	# Impute Clinical variable for Control patient
	convert_NonAvailableClinicalVariable_forControl("DATA/CYTOKINES/discreteMatrix.csv")

	# Delete variables in the matrix file (i.e delete a column)
	# SAMPLE CODES : all variable are set to "null", not very useful ...
	# \\Clinical\\Consent\\CSPHASE : all patient are PHASE I for now
	# \\Clinical\\Demography\\RACE : almost all patient are white/caucasien.
	# \\Clinical\\Comorbidity\\MHCANCER : almost all patient are set to "No"
	# \\Clinical\\Comorbidity\\MHCOPD : almost all patient are set to "No"
	# \\Clinical\\Comorbidity\\MHHEREDANEMIA : almost all patient are set to "No"
	listOfVariableToDelete = ["\\Clinical\\Medication\\CMATNF",
	 						  "\\Clinical\\Medication\\CMABATACEPT",
	 						  "\\Clinical\\Medication\\CMTOCILIZUMAB",
	 						  "SAMPLECODES",
	 						  "\\Clinical\\Consent\\CSPHASE",
	 						  "\\Clinical\\Demography\\RACE",
	 						  "\\Clinical\\Comorbidity\\MHCANCER",
	 						  "\\Clinical\\Comorbidity\\MHCOPD",
	 						  "\\Clinical\\Comorbidity\\MHHEREDANEMIA"]
	for variableToDelete in listOfVariableToDelete:
		remove_variableFromMatrixFile("DATA/CYTOKINES/discreteMatrix_imputed.csv", variableToDelete)

	# Delete patient with NA values after imputation
	remove_PatientsWithNAValues("DATA/CYTOKINES/discreteMatrix_imputed.csv")

	# Assemble cohorte
	splitCohorteAccordingToDiagnostic("DATA/CYTOKINES/discreteMatrix_imputed.csv", "DATA/patientIndex.csv")
	cohorte = assemble_CohorteFromDiscreteAllFiles()

	# Pattern Mining
	expectedSupport = sys.argv[2]
	extractPatternFromCohorte(cohorte, expectedSupport, "discreteVariables")

	# Generate association rules
	rulesFile = "DATA/RULES/discreteVariables_rules_"+str(expectedSupport)+".csv"
	generate_AssociationRulesFromPatternFile("DATA/PATTERN/discreteVariables_pattern_"+str(expectedSupport)+".csv", rulesFile, 80, 1, "discrete")
	write_decryptedRulesFiles(rulesFile)


if(command == "generate_data_for_NN"):
	####################################
	# Generate Data for the NN Project #
	####################################
	
	generate_binaryDiscretizeData_forNN()

if(command == "remove_data"):
	##################################
	# Remove folders containing data #
	# use it just before commit		 #
	##################################
	remove_data_folders()

if(command == "build_descriptionFile"):
	#################################################
	# Write xml description file from a matrix file #
	# First step for a "clean" discretization       #
	################################################# 
	matrixFileName = "DATA/CYTOKINES/discreteMatrix_imputed.csv"
	print "[+] Write xml description file from "+str(matrixFileName)
	describe.write_xmlDescriptionFile(matrixFileName)
	describe.set_typeValueFrom(matrixFileName)
	describe.set_possibleValuesFrom(matrixFileName)
	describe.set_DiscreteValues()
	describe.set_BinaryValues()
	print "[*] xml description file complete"



#-------#
# TRASH ###########################################################################
#-------#



# a few structure
listOfPanel = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6","PANEL_7","PANEL_8","PANEL_9"]
listOfDisease = ["RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]
listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
listOfGarbageParameterForRA = ["CD45RAnegCD62LhighCD27posCD8pos_Central_MemoryTcells",
							  "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells,"
							  "CD45RAnegCD62LhighCD27posCD4pos_Central_Memory_Tcells",
							  "CD45RAnegCD62LlowCD27negCD8pos_Effector_Memory_Tcells",
							  "CD8pos_CD38pos_Activated_Tcells",
							  "CD45RAposCD62LlowCD27negCD4pos_Effector_T cells",
							  "CD45RAposCD62LlowCD27negCD8pos_Effector_Tcells",
							  "CD45RAposCD62LhighCD27posCD8pos_Naive_Tcells",
							  "CD8pos_CD57pos_Cytotoxic_Tcells",
							  "CD45RAnegCD62LlowCD27negCD4pos_Effector_Memory_Tcells",
							  "CD25pos_activated_CD4pos_Tcells",
							  "gdpos_Tcells",
							  "CD25highCD127lowCD4pos_Regulatory_Tcells",
							  "abpos_Tcells",
							  "CD69pos_activated_CD8pos_Tcells",
							  "CD69pos_activated_CD4pos_Tcells",
							  "CD25pos_activated_CD8pos_Tcells",
							  "CD24highCD38high_Transitional_Bcells",
							  "CD24posCD38negMemory_Bcells",
							  "CD24posCD38pos_Mature_Bcells",
							  "CD27negIgDpos_Naive_Bcells",
							  "CD27posIgDpos_Non-switched_memory_Bcells",
							  "CD27negIgDneg_Bcells",
							  "IgDnegCD27pos",
							  "IgDposCD38neg_Bm1",
							  "IgDposCD38pos_Bm2",
							  "IgDposCD38high_Bm2p",
							  "IgDnegCD38high_Bm3_4",
							  "IgDnegCD38neg_Bm5",
							  "IgDnegCD38pos_eBm5",
							  "CD5pos_Bcells",
							  "CD38highCD27high_Plasmablasts",
							  "CD27pos CD43pos Bcells",
							  "CD5pos CD11bpos Bcells",
							  "CD5neg CD11bneg Bcells",
							  "CD3pos CD20low in Tcells",
							  "CD5pos CD11bneg Bcells",
							  "CD43posCD69negCD27posCD20pos B1 Bcells",
							  "CD5neg CD11bpos Bcells",
							  "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells",
							  "CD45RAnegCD62LhighCD27posCD4pos_Central_Memory_Tcells"]


listOfGarbageParameterForRA2 = ["CD45RAnegCD62LhighCD27posCD8pos_Central_MemoryTcells",
							  "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells,"
							  "CD45RAnegCD62LhighCD27posCD4pos_Central_Memory_Tcells",
							  "CD45RAnegCD62LlowCD27negCD8pos_Effector_Memory_Tcells",
							  "CD8pos_CD38pos_Activated_Tcells",
							  "CD45RAposCD62LlowCD27negCD4pos_Effector_T cells",
							  "CD45RAposCD62LlowCD27negCD8pos_Effector_Tcells",
							  "CD45RAposCD62LhighCD27posCD8pos_Naive_Tcells",
							  "CD8pos_CD57pos_Cytotoxic_Tcells",
							  "CD45RAnegCD62LlowCD27negCD4pos_Effector_Memory_Tcells",
							  "CD25pos_activated_CD4pos_Tcells",
							  "gdpos_Tcells",
							  "CD25highCD127lowCD4pos_Regulatory_Tcells",
							  "abpos_Tcells",
							  "CD69pos_activated_CD8pos_Tcells",
							  "CD69pos_activated_CD4pos_Tcells",
							  "CD25pos_activated_CD8pos_Tcells",
							  "CD24highCD38high_Transitional_Bcells",
							  "CD24posCD38negMemory_Bcells",
							  "CD24posCD38pos_Mature_Bcells",
							  "CD27negIgDpos_Naive_Bcells",
							  "CD27posIgDpos_Non-switched_memory_Bcells",
							  "CD27negIgDneg_Bcells",
							  "IgDnegCD27pos",
							  "IgDposCD38neg_Bm1",
							  "IgDposCD38pos_Bm2",
							  "IgDposCD38high_Bm2p",
							  "IgDnegCD38high_Bm3_4",
							  "IgDnegCD38neg_Bm5",
							  "IgDnegCD38pos_eBm5",
							  "CD5pos_Bcells",
							  "CD38highCD27high_Plasmablasts",
							  "CD27pos CD43pos Bcells",
							  "CD5pos CD11bpos Bcells",
							  "CD5neg CD11bneg Bcells",
							  "CD3pos CD20low in Tcells",
							  "CD5pos CD11bneg Bcells",
							  "CD43posCD69negCD27posCD20pos B1 Bcells"]



#####################
# CLUSTER ON CENTER #
#####################
# Preprocessing




"""
clean_folders("ALL")
checkAndFormat("DATA/"+panel, "DATA/PATIENT")

#remove_typeOfParameter("PROPORTION")
remove_typeOfParameter("ABSOLUTE")
remove_typeOfParameter("RATIO")
remove_typeOfParameter("MFI")

check_patient()
save_data()

# PCA
show_PCA("DATA/PATIENT", "center", "3d", "IMAGES/test.png", "PROPORTION", 1, 1)
#show_PCA("DATA/PATIENT", "disease", "2d", "IMAGES/test.png", "MFI", 1, 1)
#OverviewOnDisease("RA", "MCTD" , "ABSOLUTE", "center", 1)

write_matrixFromPatientFolder()
plot_composanteOfEigenVector("DATA/CYTOKINES/matrixTestFromCyto.csv", "all", 3)

# Reformat file name
#for panel in listOfPanelToConcat:
#add_diagnosticTag("PANEL_9")
"""

"""
listOfVersus = []
for disease1 in listOfDisease:
	for disease2 in listOfDisease:
		if(disease1 != disease2):
			print "=> "+disease1+" VS "+disease2
			versus = [disease1, disease2]
			clean_folders("ALL")
			fusion_panel(listOfPanelToConcat)
			checkAndFormat("DATA/FUSION", "DATA/PATIENT")
			apply_filter("disease", [disease1, disease2])
			remove_parameter("PROPORTION", "mDC1_IN_leukocytes")
			remove_parameter("ABSOLUTE", "Lymphocytes")
			check_patient()
			save_data()
			#print "Perform Outlier Detection"
			#outlierDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
			#print " => Done"
			#print "Perform Novelty Detection"
			#noveltyDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
			#print " => Done"
			print "Perform Overview on "+str(disease1)
			OverviewOnDisease(disease1, disease2, "ABSOLUTE", "disease", 1)
			print " => Done"
			listOfVersus.append(versus)
			#write_OverviewReport(disease1, disease2, "ABSOLUTE", "1 to 6", 2016)
			print "###################"
	
#write_ClassificationReport("ALL", "1 to 6", 2016, listOfVersus)
"""



################################
# Convert matrix to data files #
################################
"""
clean_folders("ALL")
checkAndFormat("DATA/PANEL_1", "DATA/PATIENT")
apply_filter("disease", "Control")
X = get_OneDimensionnalData("DATA/PATIENT", "ABSOLUTE", "Monocytes")
description = stats.describe(X)
mean = description[2]
variance = description[3]
ecartType = sqrt(variance)
print ecartType
"""

#scaleDataInPatientFolder("ALL")



"""

########################
# Distribution analyse #
########################
print "----Distribution Analysis----"
clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
apply_filter("disease", "Control")
threshold = get_ThresholdValue("ABSOLUTE")

"""


"""
##################
# Discretization #
##################

print "----Discretization----"
clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
apply_filter("disease", "RA")
check_patient()
discretization(threshold)


"""

"""
##################
# Pattern Mining #
##################
print "----Pattern Mining----"
cohorte = assemble_Cohorte()

#cohorte = alleviate_cohorte(cohorte, 40)

"""

"""
#####################################
# Explore optimal value of thresold #
# for alleviate function            #
#####################################
import time

minNumberOfParamToRemove = 5
maxTry = 60
machin = get_controledValueOfThreshold(cohorte, maxTry, minNumberOfParamToRemove, 3)
cohorte = alleviate_cohorte(cohorte, machin)
#searchForPattern(cohorte, maxTry, "DATA/PATTERN/test.csv")
"""


"""
for itemset in find_frequent_itemsets(cohorte, 10):
	displayItem = 0
	for variable in itemset:
		variableInArray = variable.split("_")
		if(variableInArray[1] != "normal"):
			displayItem = 1
	if(displayItem):
		print itemset
end = time.time()
print "=> Performed in: " + str(end - start)
"""






####################
# GENERAL Analysis #
####################
#diseaseExplorationProcedure(listOfDisease, listOfPanelToConcat)



#########################
# GLOBAL PATTERN MINING #
#########################

#patternMining_run1()

#patternMining_run2()


#patternMining_run2Reverse()
#patternMining_run3()
#patternMining_run4()
#FrequentItemMining()
"""
listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
for disease1 in listOfDisease:
	x = 0
	while(x < 101):
		FrequentItemMining3(x, disease1, "PROPORTION")
		x = x +5
"""


#x = 0
#while(x < 101):
#	FrequentItemMining2(x)
#	x = x + 5



#visualisation2("RA", "Control", "PROPORTION", 30)
#FrequentItemMining2(15)
#visualisation2("RA", "Control", "PROPORTION", 15)




"""
#############################
# Generate graphic for report
# delta exploration 
#############################


RA_value = []
MCTD_value = []
SjS_value = []
SLE_value = []
SSc_value = []
UCTD_value = []
minSupport_value = []
x = 0
while(x <= 100):
	#FrequentItemMining2(x)
	logFile = open("DATA/PATTERN/FrequentItemMining2_"+str(x)+".log", "r")

	for line in logFile:
		lineInArray = line.split("\n")
		lineInArray = lineInArray[0].split(";")

		# applatir les valeur de delta a 1
		if(float(lineInArray[3]) > 1):
			lineInArray[3] = 1

		if(lineInArray[0] == "RA"):
			RA_value.append(lineInArray[3])
		elif(lineInArray[0] == "MCTD"):
			MCTD_value.append(lineInArray[3])
		elif(lineInArray[0] == "SjS"):
			SjS_value.append(lineInArray[3])
		elif(lineInArray[0] == "SLE"):
			SLE_value.append(lineInArray[3])
		elif(lineInArray[0] == "SSc"):
			SSc_value.append(lineInArray[3])
		elif(lineInArray[0] == "UCTD"):
			UCTD_value.append(lineInArray[3])
	logFile.close()
	x = x + 5


import numpy as np
import matplotlib.pyplot as plt
minSupport_value = np.arange(0, 105, 5)
fig, ax = plt.subplots()
ax.plot(minSupport_value, MCTD_value, label="MCTD")
ax.plot(minSupport_value, RA_value, label="RA")
ax.plot(minSupport_value, SjS_value, label= "SjS")
ax.plot(minSupport_value, SLE_value, label= "SLE")
ax.plot(minSupport_value, SSc_value, label= "SSc")
ax.plot(minSupport_value, UCTD_value, label="UCTD")
ax.set_xlabel("Support (%)")
ax.set_ylabel("Delta")
legend = ax.legend(loc='upper left', shadow=True)
plt.show()
"""


"""
listOfDisease = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
for disease in listOfDisease:
	filter_Pattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold.csv")
	convert_PatternFile("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter.csv")
	parametersOfInterest = extract_parametersFromPattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)
	print disease + " => " + str(len(parametersOfInterest))
#filter_Pattern("DATA/PATTERN/RA_ABSOLUTE_discretisationAlArrache.csv")


#fileName = "DATA/PATTERN/RA_ABSOLUTE_discretisationAlArrache_HeavyFilter_converted.csv"
#parametersOfInterest = extract_parametersFromPattern(fileName, 20)
#listOfAllParameters = get_allParam("ABSOLUTE")
#convert_PatternFile("DATA/PATTERN/RA_ABSOLUTE_discretisationAlArrache_LowFilter.csv")
#remove_parameter("ABSOLUTE", "CD27pos CD43pos Bcells")
#remove_parameter("ABSOLUTE", "CD45RAnegCD62LhighCD27posCD8pos_Central_MemoryTcells")
"""


"""
clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
apply_filter("disease", "RA")
check_patient()

filter_Pattern("DATA/PATTERN/"+"RA"+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold.csv")
convert_PatternFile("DATA/PATTERN/"+"RA"+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter.csv")
parametersOfInterest = extract_parametersFromPattern("DATA/PATTERN/"+"RA"+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)

filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
filter_ArtefactValue("ABSOLUTE", "Monocytes", 1200)
filter_ArtefactValue("ABSOLUTE", "CD14highCD16neg_classicalMonocytes", 1000)
filter_ArtefactValue("ABSOLUTE", "CD15highCD16neg_Eosinophils", 800)
filter_ArtefactValue("ABSOLUTE", "CD15lowCD16high_Neutrophils", 1100)
filter_ArtefactValue("ABSOLUTE", "CD69pos_activated_CD4pos_Tcells", 600)
filter_ArtefactValue("ABSOLUTE", "CD8pos_CD57pos_Cytotoxic_Tcells", 500)
filter_ArtefactValue("ABSOLUTE", "CD14pos_monocytes", 1200)


for parameter in parametersOfInterest:
	print "=> Checking parameter "+str(parameter)

	#filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "CD8pos_CD38pos_Activated_Tcells", 1000000)
	#filter_ArtefactValue("ABSOLUTE", "IgDnegCD27pos", 60000)
	#filter_ArtefactValue("ABSOLUTE", "CD45RAnegCD62LhighCD27posCD4pos_Central_MemoryTcells", 1500000)
	#filter_ArtefactValue("ABSOLUTE", "CD45RAposCD62LhighCD27posCD4pos_Naive_Tcells", 1400000)
	#filter_ArtefactValue("ABSOLUTE", "CD27posIgDpos_Non-switched_memory_Bcells", 15000)

	X = get_OneDimensionnalData("DATA/PATIENT", "ABSOLUTE", parameter)
	show_distribution(X)
"""






def visualisation(disease):
	"""
	IN PROGRESS
	"""

	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", [disease, "Control"])
	check_patient()

	filter_Pattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold.csv")
	convert_PatternFile("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter.csv")
	parametersOfInterest = extract_parametersFromPattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 0)
	listOfAllParameters = get_allParam("ABSOLUTE")

	listOfAllParameters = get_allParam("ABSOLUTE")
	for parameter in listOfAllParameters:
		if(parameter not in parametersOfInterest):
			remove_parameter("ABSOLUTE", parameter)

	filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)

	#filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "Monocytes", 1200)
	#filter_ArtefactValue("ABSOLUTE", "CD14highCD16neg_classicalMonocytes", 1000)
	#filter_ArtefactValue("ABSOLUTE", "CD15highCD16neg_Eosinophils", 800)
	#filter_ArtefactValue("ABSOLUTE", "CD15lowCD16high_Neutrophils", 1100)
	#filter_ArtefactValue("ABSOLUTE", "CD69pos_activated_CD4pos_Tcells", 600)
	#filter_ArtefactValue("ABSOLUTE", "CD8pos_CD57pos_Cytotoxic_Tcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "CD14pos_monocytes", 1200)

	check_patient()
	save_data()

	saveName1 = "IMAGES/"+disease+"_vs_"+"Control"+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+disease+"_vs_"+"Control"+"_PCA2D.jpg"
	show_correlationMatrix("DATA/PATIENT", saveName1, "ABSOLUTE", 1)
	show_PCA("DATA/PATIENT", "disease", "2d", saveName2, "ABSOLUTE", 1, 1)


"""
clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
apply_filter("disease", "RA")
check_patient()

X = get_OneDimensionnalData("DATA/PATIENT", "ABSOLUTE", "CD15lowCD16high_Neutrophils")
show_distribution(X)
"""


#visualisation("MCTD")
#visualisation2("SLE", "MCTD")





"""
listOfDisease2 = ["RA", "MCTD", "SjS", "SLE", "SSc", "UCTD"]
for disease in listOfDisease2:
	visualisation(disease)
"""
"""
import itertools

disease = 'RA'

clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
apply_filter("disease", [disease, "Control"])
check_patient()

filter_Pattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold.csv")
convert_PatternFile("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter.csv")
parametersOfInterest = extract_parametersFromPattern("DATA/PATTERN/"+disease+"_FrequentItem_ABSOLUTE_meanGeneratedThreshold_HeavyFilter_converted.csv", 15)


for subset in itertools.combinations(parametersOfInterest, 3):
	testParameters = []
	for item in subset:
		testParameters.append(item)

	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", [disease, "Control"])
	check_patient()
	
	listOfAllParameters = get_allParam("ABSOLUTE")
	for parameter in listOfAllParameters:
		if(parameter not in testParameters):
			remove_parameter("ABSOLUTE", parameter)

	filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)

	filter_ArtefactValue("ABSOLUTE", "CD27pos CD43pos Bcells", 500)
	filter_ArtefactValue("ABSOLUTE", "Monocytes", 1200)
	filter_ArtefactValue("ABSOLUTE", "CD14highCD16neg_classicalMonocytes", 1000)
	filter_ArtefactValue("ABSOLUTE", "CD15highCD16neg_Eosinophils", 800)
	#filter_ArtefactValue("ABSOLUTE", "CD15lowCD16high_Neutrophils", 1100)
	filter_ArtefactValue("ABSOLUTE", "CD69pos_activated_CD4pos_Tcells", 600)
	#filter_ArtefactValue("ABSOLUTE", "CD8pos_CD57pos_Cytotoxic_Tcells", 500)
	#filter_ArtefactValue("ABSOLUTE", "CD14pos_monocytes", 1200)

	check_patient()
	save_data()

	saveName1 = "IMAGES/"+disease+"_vs_"+"Control"+"_matrixCorrelation.jpg"
	saveName2 = "IMAGES/"+disease+"_vs_"+"Control"+"_PCA2D.jpg"
	show_correlationMatrix("DATA/PATIENT", saveName1, "ABSOLUTE", 1)
	show_PCA("DATA/PATIENT", "disease", "2d", saveName2, "ABSOLUTE", 1, 1)
"""



#print "Perform Outlier Detection"
#outlierDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
#print " => Done"
#print "Perform Novelty Detection"
#noveltyDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
#print " => Done"
#print "Perform Overview on "+str(disease1)
#OverviewOnDisease(disease1, disease2, "ABSOLUTE", "disease", 1)
#print " => Done"
#listOfVersus.append(versus)
#write_OverviewReport(disease1, disease2, "ABSOLUTE", "1 to 6", 2016)
#print "###################"
	
#write_ClassificationReport("ALL", "1 to 6", 2016, listOfVersus)
#compile_report()





"""
for itemset in find_frequent_itemsets(cohorte, 30):
	for element in itemset:
		print itemset
"""

"""
	X = get_OneDimensionnalData("DATA/PATIENT", "ABSOLUTE", param)
	try:
		show_distribution(X)
	except:
		print "can't show "+param
"""
"""

###############
# RA Analysis #
###############

listOfVersus = []
disease1 = "RA"
clean_report()
clean_image()
for disease2 in listOfDisease:
	if(disease1 != disease2):
		print "=> "+disease1+" VS "+disease2
		versus = [disease1, disease2]
		clean_folders("ALL")
		fusion_panel(listOfPanelToConcat)
		checkAndFormat("DATA/FUSION", "DATA/PATIENT")
		apply_filter("disease", [disease1, disease2])
		remove_parameter("PROPORTION", "mDC1_IN_leukocytes")
		remove_parameter("ABSOLUTE", "Lymphocytes")
		
		for parameter in listOfNormalParameters:
			remove_parameter("ABSOLUTE", parameter)

		check_patient()
		save_data()
		print "Perform Outlier Detection"
		#outlierDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
		print " => Done"
		print "Perform Novelty Detection"
		#noveltyDetection("disease", disease1, "disease", disease2, "ABSOLUTE", 0)
		print " => Done"
		print "Perform Overview on "+str(disease1)
		OverviewOnDisease(disease1, disease2, "ABSOLUTE", "disease", 1)
		print " => Done"
		listOfVersus.append(versus)
		#write_OverviewReport(disease1, disease2, "ABSOLUTE", "1 to 6", 2016)
		print "###################"
	
#write_ClassificationReport("ALL", "1 to 6", 2016, listOfVersus)
compile_report()

"""


"""TEST SPACE"""

"""
# training set
restore_Data()
check_patient()
apply_filter("disease", "Control")
X = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "PROPORTION")
X = scale_Data(X)
X = PCA(n_components=2).fit_transform(X)
#print X

# new observation
restore_Data()
apply_filter("disease", "SLE")
X_test = generate_DataMatrixFromPatientFiles2("DATA/PATIENT", "PROPORTION")
X_test = scale_Data(X_test)
X_test = PCA(n_components=2).fit_transform(X_test)
oneClassSvm(X, X_test, "control", "sle")
"""

#use_SupportVectorMachine("PANEL_1", "PROPORTION", "disease", "RA", "Test.pkl")

#checkAndFormat("DATA/PANEL_1", "DATA/PATIENT")
#show_PCA("DATA/PATIENT", "disease", "2d", "test4.png", "PROPORTION", 1)
#show_cluster("DATA/PATIENT", 2, "testCluster.png")

#checkAndFormat("DATA/PANEL_6", "DATA/PATIENT")
#show_PCA("DATA/PATIENT", "center", "3d", "test4.png")
#show_cluster("DATA/PATIENT", 30, "testCluster.png")
#show_correlationMatrix("DATA/PATIENT", "correlationMatrix_Pan0el1.jpg")
#RunOnFullData()



"""
for panel in listOfPanel:
	for disease in listOfDisease:
		saveName = str(panel)+"_"+str(disease)+"_ABSOLUTE.pkl"
		use_SupportVectorMachine(panel, "ABSOLUTE", "disease", disease, saveName, "linear")
		use_SupportVectorMachine(panel, "ABSOLUTE", "disease", disease, saveName, "poly")
		use_SupportVectorMachine(panel, "ABSOLUTE", "disease", disease, saveName, "rbf")
		
"""

#for panel in listOfPanel : 
#	OverviewOnPanel(panel, "PROPORTION", "disease")


"""
listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
clean_folders("ALL")
fusion_panel(listOfPanelToConcat)
checkAndFormat("DATA/FUSION", "DATA/PATIENT")
"""
"""
check_patient()
save_data()
outlierDetection("disease", "Control", "disease", "SLE", "PROPORTION")
"""


