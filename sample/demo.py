#-------------#
# IMPORTATION #######################################################################
#-------------#
import procedure
import describe
import discretization
import reorder
import cytokines
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
	reorder.clean_folders("ALL")
	procedure.checkAndFormat("DATA/"+panel, "DATA/PATIENT")
	#remove_typeOfParameter("PROPORTION")
	reorder.remove_typeOfParameter("ABSOLUTE")
	reorder.remove_typeOfParameter("RATIO")
	reorder.remove_typeOfParameter("MFI")
	reorder.check_patient()
	reorder.save_data()
	procedure.show_PCA("DATA/PATIENT", "center", "3d", "IMAGES/test.png", "PROPORTION", 0, 1)


###################################
# CLUSTER ON CENTER FOR ALL PANEL #
###################################
if(command == "case_2"):
	# Preprocessing
	reorder.clean_folders("ALL")
	listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3", "PANEL_4", "PANEL_5", "PANEL_6"]
	reorder.convert_DRFZ_to_CHARITE()
	reorder.fusion_panel(listOfPanelToConcat)
	procedure.checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	#remove_typeOfParameter("PROPORTION")
	reorder.remove_typeOfParameter("ABSOLUTE")
	reorder.remove_typeOfParameter("RATIO")
	reorder.remove_typeOfParameter("MFI")
	reorder.check_patient()
	reorder.save_data()
	
	procedure.show_PCA("DATA/PATIENT", "center", "3d", "IMAGES/test.png", "PROPORTION", 0, 1)

	# Analyse eigenVector
	reorder.write_matrixFromPatientFolder()
	cytokines.plot_composanteOfEigenVector("DATA/CYTOKINES/matrixTestFromCyto.csv", 7, 3)


#######################################
# PREPARATION DATA FOR NEURAL NETWORK #
#######################################
if(command == "prepare_data"):

	raw_data_file = "DATA/MATRIX/clinical_i2b2trans.txt"
	matrixFileName = "DATA/MATRIX/matrix.csv"

	print "[+] Format data from "+str(raw_data_file)
	cytokines.CreateMatrix(raw_data_file, matrixFileName)
	cytokines.format_OMICID(matrixFileName)
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





