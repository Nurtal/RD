"""
write tex report
"""



def write_OverviewReport(target, dataType, panelRange, date):
	"""
	IN PROGRESS

	-> TODO :
		- write doc
	"""

	# write overview header
	report_file = open("REPORT/"+str(target)+".tex", "w")
	header_template = open("REPORT/Overview_header.tex", "r")
	for line in header_template:
		report_file.write(line)
	header_template.close()
	

	# write overview content
	# Write title
	report_file.write("\\title{REPORT on "+str(target)+"}\n")
	report_file.write("\\author{Analysis performed on "+str(dataType)+" data, panel "+str(panelRange)+"}\n")
	report_file.write("\\date{"+str(date)+"}\n")
	report_file.write("\\begin{document}\n")
	report_file.write("\\maketitle\n\n")

	# write Overview PCA section
	report_file.write("\\section{Overview PCA}\n")
	report_file.write("\\begin{center}\n")
	report_file.write("\\begin{tabular}{c c}\n")
	report_file.write("\\includegraphics[scale=0.30]{\"IMAGES/"+str(target)+"_PCA2D\"} & \\includegraphics[scale=0.30]{\"IMAGES/"+str(target)+"_PCA3D\"} \\\\ \n")
	report_file.write("ACP, projection biparametrique & ACP, projection en trois dimensions \n")
	report_file.write("\\end{tabular}\n")
	report_file.write("\\end{center}\n\n")

	# Write Correlation section
	report_file.write("\\section{Correlation}\n")
	report_file.write("\\begin{center}\n")
	report_file.write("\\begin{tabular}{c}\n")
	report_file.write("\\includegraphics[scale=0.15]{\"IMAGES/"+str(target)+"_matrixCorrelation\"} \\\\ \n")
	report_file.write("Matrice des correlations")
	report_file.write("\\end{tabular}\n")
	report_file.write("\\end{center}\n\n")

	# write Variance Details section
	report_file.write("\\section{Variance Details}\n")
	report_file.write("\\begin{center}\n")
	report_file.write("\\begin{tabular}{c c}\n")
	report_file.write("\\includegraphics[scale=0.20]{\"IMAGES/"+str(target)+"_PCA3D_variance1\"} & \\includegraphics[scale=0.20]{\"IMAGES/"+str(target)+"_PCA3D_variance2\"} \\\\ \n")
	report_file.write("Decroissance de la variance expliquee & Diagramme des premieres composantes principales\n")
	report_file.write("\\end{tabular}\n")
	report_file.write("\\end{center}\n")

	# write overview footer
	report_file.write("\\end{document}")
	report_file.close()


def write_ClassificationReport(dataType, panelRange, date, listOfAssociation):
	"""
	IN PROGRESS

	TODO:
		- write doc
	"""

	# write overview header
	report_file = open("REPORT/Classification.tex", "w")
	header_template = open("REPORT/Classification_header.tex", "r")
	for line in header_template:
		report_file.write(line)
	header_template.close()

	# write overview content
	# Write title
	report_file.write("\\title{Classification}\n")
	report_file.write("\\author{Analysis performed on "+str(dataType)+" data, panel "+str(panelRange)+"}\n")
	report_file.write("\\date{"+str(date)+"}\n")
	report_file.write("\\begin{document}\n")
	report_file.write("\\maketitle\n\n")


	# write section
	for association in listOfAssociation:
		report_file.write("\\section{"+str(association[0])+" versus "+str(association[1])+"}\n")
		report_file.write("\\begin{center}\n")
		report_file.write("\\begin{tabular}{c c}\n")
		report_file.write("\\includegraphics[scale=0.20]{\"IMAGES/"+str(association[0])+"_vs_"+str(association[1])+"_outlierDetection\"} & \\includegraphics[scale=0.20]{\"IMAGES/"+str(association[0])+"_vs_"+str(association[1])+"_noveltyDetection\"} \\\\ \n")
		report_file.write("Robust covariance estimation and Mahalanobis distances relevance & novelty detection with one class Support Vector Machine\n")
		report_file.write("\\end{tabular}")
		report_file.write("\\end{center}")


	# write overview footer
	report_file.write("\\end{document}")
	report_file.close()


"""TEST SPACE"""
#write_report("MCTD", "ABSOLUTE", "1 to 6", 2016)
listOfAssociation = [["Control", "RA"], ["Control", "SLE"]]
write_ClassificationReport("PROPORTION", "1 to 6", 2016, listOfAssociation)