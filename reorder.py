"""
convert, save, filter 
operation on data files
"""

from trashlib import *
from trashlib2 import *

import glob
import shutil
import os


def convert_tabSepratedFile(inputFolder, outputFolder):
	"""
	convert all tab separated files present in
	inputfolder to ";" separated file in outputFolder
	-> inputFolder is a string
	-> outputFolder is a string
	-> return nothing
	"""

	listOfPatientFiles = glob.glob(str(inputFolder)+"/*.csv")
		
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFileName = patientFileInArray[-1]
		newPatientFileName = outputFolder+"/"+str(patientFileName)

		dataInPatientFile = open(patientFile, "r")
		newPatientFile = open(newPatientFileName, "w")
		for originalLine in dataInPatientFile:
			originalLineInArray = originalLine.split("\t")
			cmpt = 0
			for element in originalLineInArray:
				if(cmpt < len(originalLineInArray)-1):
					newPatientFile.write(str(element)+";")
				else:
					newPatientFile.write(str(element))
				cmpt = cmpt + 1

		dataInPatientFile.close()
		newPatientFile.close()

		print "=> "+patientFileName+" Done"



def apply_filter(targetType, target):
	"""
	-> Delete all files in DATA/PATIENT not passing the apply_filter
	   (i.e all files with a targetType not matching target)
	   (e.g : aplly_filter(center, ubo) will delete all non-ubo files)

	-> targetType is a string, could be:
		- center
		- date
		- disease
	"""

	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
			patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		patientFileInArray = patientFileInArray[-1]
		patientFileInArray = patientFileInArray.split("_")
			
		patient_disease = patientFileInArray[0]
		patient_id = patientFileInArray[1]
		patient_center = patientFileInArray[2]
		patient_date = patientFileInArray[3]
				
		if(targetType == "center" and patient_center != target):	
			os.remove(patientFile)
			print patientFile + " => Deleted"
		elif(targetType == "date" and patient_date != target):
			os.remove(patientFile)
			print patientFile + " => Deleted"
		elif(targetType == "disease" and patient_disease != target):
			os.remove(patientFile)
			print patientFile + " => Deleted"



def restore_Data():
	"""
	-> Delete all files in DATA/PATIENT
	-> Copy all files from DATA/PATIENT_SAVE to DATA/PATIENT
	"""
	
	# clean destination
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")
	for patientFile in listOfPatientFiles:
		os.remove(patientFile)

	# copy from backup to destination
	listOfPatientSaved = glob.glob("DATA/PATIENT_SAVE/*.csv")
	for patientSaved in listOfPatientSaved:
		shutil.copy(patientSaved, "DATA/PATIENT/")



def fusion_panel(listOfPanels):
	"""
	IN PROGRESS

	-> concat patient files, use all panel present in listOfPanels
	-> listOfPanels is a list of string

	TODO:
		-> test on real data
	"""


	# initialiser les files
	listOfPatientFiles = glob.glob("DATA/"+str(listOfPanels[0])+"/*.csv")
	for patientFile in listOfPatientFiles:
		if(platform.system() == "Linux"):
				patientFileInArray = patientFile.split("/")
		elif(platform.system() == "Windows"):
			patientFileInArray = patientFile.split("\\")
		
		patientFileName = patientFileInArray[-1]
		newPatientFileName = "DATA/PATIENT/"+str(patientFileName)
		newFile = open(newPatientFileName, "w")
		newFile.close()

	# remplir le fichier
	for panel in listOfPanels:
		listOfPatientFiles = glob.glob("DATA/"+str(panel)+"/*.csv")
		for patientFile in listOfPatientFiles:
			if(platform.system() == "Linux"):
				patientFileInArray = patientFile.split("/")
			elif(platform.system() == "Windows"):
				patientFileInArray = patientFile.split("\\")
		patientFileName = patientFileInArray[-1]
		newPatientFileName = "DATA/PATIENT/"+str(patientFileName)
		sourceFile = open("DATA/"+str(panel)+"/"+patientFileName, "r")
		dataToCopy = []
		for line in sourceFile:
			dataToCopy.append(line)
		sourceFile.close()

		destinationFile = open(newPatientFileName, "a")
		for line in dataToCopy:
			destinationFile.write(line)
		destinationFile.close()




def save_data():
	"""
	IN PROGRESS
	"""

	# clean destination
	listOfPatientFiles = glob.glob("DATA/PATIENT_SAVE/*.csv")
	for patientFile in listOfPatientFiles:
		os.remove(patientFile)

	# copy to destination
	listOfPatientFiles = glob.glob("DATA/PATIENT/*.csv")	
	for patientFile in listOfPatientFiles:
		shutil.copy(patientFile, "DATA/PATIENT_SAVE/")





