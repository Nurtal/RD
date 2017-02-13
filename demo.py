#-------------#
# IMPORTATION #######################################################################
#-------------#
from procedure import *
from report import *
from preprocessing import *
from patternMining import *
from cytokines import *
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
	panel = "PANEL_4"
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
