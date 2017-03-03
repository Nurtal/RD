#-------------#
# IMPORTATION #######################################################################
#-------------#
from procedure import *
from report import *
from preprocessing import *
from patternMining import *
from cytokines import *
import describe
import discretization
import sys



#----------------------#
# GET SCRIPT ARGUMENTS ################################################################
#----------------------#
command = sys.argv[1]


#####################
# CLUSTER ON CENTER #
#####################

if(command == "case_1"):
	# Preprocessing
	panel = "PANEL_9"
	print "=> " +str(panel)
	clean_folders("ALL")
	checkAndFormat("DATA/"+panel, "DATA/PATIENT")
	#remove_typeOfParameter("PROPORTION")
	remove_typeOfParameter("ABSOLUTE")
	remove_typeOfParameter("RATIO")
	remove_typeOfParameter("MFI")
	check_patient()
	save_data()
	show_PCA("DATA/PATIENT", "center", "3d", "IMAGES/test.png", "PROPORTION", 0, 1)


###################################
# CLUSTER ON CENTER FOR ALL PANEL #
###################################
if(command == "case_2"):
	# Preprocessing
	clean_folders("ALL")
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3", "PANEL_4", "PANEL_5", "PANEL_6"]
	convert_DRFZ_to_CHARITE()
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	#remove_typeOfParameter("PROPORTION")
	remove_typeOfParameter("ABSOLUTE")
	remove_typeOfParameter("RATIO")
	remove_typeOfParameter("MFI")
	check_patient()
	save_data()
	
	show_PCA("DATA/PATIENT", "center", "3d", "IMAGES/test.png", "PROPORTION", 0, 1)

	# Analyse eigenVector
	write_matrixFromPatientFolder()
	plot_composanteOfEigenVector("DATA/CYTOKINES/matrixTestFromCyto.csv", 7, 3)


#######################################
# PREPARATION DATA FOR NEURAL NETWORK #
#######################################
if(command == "prepare_data"):

	raw_data_file = "DATA/MATRIX/clinical_i2b2trans.txt"
	matrixFileName = "DATA/MATRIX/matrix.csv"

	print "[+] Format data from "+str(raw_data_file)
	CreateMatrix(raw_data_file, matrixFileName)
	format_OMICID(matrixFileName)
	print "[*] New file "+str(matrixFileName)+" created"

	print "[+] Write xml description file from "+str(matrixFileName)
	describe.write_xmlDescriptionFile(matrixFileName)
	describe.set_typeValueFrom(matrixFileName)
	describe.set_possibleValuesFrom(matrixFileName)
	describe.set_DiscreteValues()
	describe.set_BinaryValues()
	print "[*] Xml description file complete"

	print "[+] Initiate binarization for "+str(matrixFileName)
	conversion_dict = discretization.create_conversion_dict()
	discretization.binarization(matrixFileName, conversion_dict)
	print "[*] Binarization complete"





