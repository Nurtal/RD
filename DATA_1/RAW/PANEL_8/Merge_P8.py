#!/usr/bin/python
# Lucas Le Lann
# 25/01/2016

from collections import defaultdict
import os.path
import glob, os

print "test"

i=0

for file in glob.glob("*.csv"):
	print os.path.basename(file)
	patient_tmp=os.path.basename(file)
	center=patient_tmp.split("_")[2]
	patient=patient_tmp.split("_")[1]
	case=patient_tmp.split("_")[0]
	por_file=open(case+"_PROPORTION.txt","a")
	abs_file=open(case+"_ABSOLUTE.txt","a")
	esl_file=open(case+"_ELSE.txt","a")
	
	header = "center"
	
	count=0
	with open(file, "r") as myfile:
		for line in myfile:
			line=line.replace("\t",";")
			line=line.split(";")
			if count == 0 :
				new_line=case+"_"+center+"_"+patient+";"
				por_file.write(new_line)
				abs_file.write(new_line)
				esl_file.write(new_line)
			
			
			else:
				line[4]=line[4].replace("\n","")
				new_line=line[4]+";"
				if line[2] == "PROPORTION":
					por_file.write(new_line)
				elif line[2] == "ABSOLUTE":
					abs_file.write(new_line)
				else:
					esl_file.write(new_line)
			count+=1
	por_file.write("\n")
	abs_file.write("\n")
	esl_file.write("\n")
