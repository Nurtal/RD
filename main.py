"""
main for RD project
"""

from procedure import *

listOfPanel = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6","PANEL_7","PANEL_8","PANEL_9"]
listOfDisease = ["Control", "RA", "MCTD", "PAPs", "SjS", "SLE", "SSc", "UCTD"]

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
check_patient()
save_data()
outlierDetection("disease", "Control", "disease", "SLE", "PROPORTION")
"""



listOfPanelToConcat = ["PANEL_1","PANEL_2","PANEL_3","PANEL_4","PANEL_5","PANEL_6"]
for disease in listOfDisease:
	print "=> Control VS "+disease
	clean_folders("ALL")
	fusion_panel(listOfPanelToConcat)
	checkAndFormat("DATA/FUSION", "DATA/PATIENT")
	apply_filter("disease", ["Control", disease])
	remove_parameter("PROPORTION", "mDC1_IN_leukocytes")
	check_patient()
	save_data()
	OverviewOnDisease(disease, "PROPORTION", "disease", 0)
	




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