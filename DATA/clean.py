"""
clean data in folder
"""

import glob
import os


listOfPanel = ["PANEL_1", "PANEL_2", "PANEL_3", "PANEL_4", "PANEL_5", "PANEL_6", "PANEL_7", "PANEL_8", "PANEL_9"]
for panel in listOfPanel:
	inputFolder = panel
	listOfPatientFiles = glob.glob(str(inputFolder)+"/*")
	for element in listOfPatientFiles:
		elementInArray = element.split(".")
		extension = elementInArray[-1]
		if(extension != "csv"):
			print "Deleting " + element
			os.remove(element)