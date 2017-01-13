=========================
# REDUCE DIMENSIONALITY #
=========================

## Overview

## Directories
DATA  
DATA/CYTOKINES  
DATA/DATABASES  
DATA/FUSION  
DATA/PANEL_1  
DATA/PANEL_2  
DATA/PANEL_3  
DATA/PANEL_4  
DATA/PANEL_5  
DATA/PANEL_6  
DATA/PANEL_7  
DATA/PANEL_8  
DATA/PANEL_9  
DATA/PATIENT  
DATA/PATIENT_SAVE  
DATA/PATIENT_VIRTUAL  
DATA/PATTERN  
DATA/REJECTED  
DATA/RULES  
DATA/VECTOR  
IMAGES  
PARAMETERS  
REPORT  
REPORT/IMAGES  
REPORT/template  
RESULTATS  

## Files  
main.py  
analysis.py  
cytokines.py  
exemple.py  
fcsAnalysis.py  
machineLearning.py  
patternMining.py  
preprocessing.py  
procedure.py  
README.md  
reorder.py  
report.py  
test.py  
trashlib.py  



## Command list

1. program_size  
   print the number of lines in the program

2. build_cytokines_data  
   run a few functions in order to prepare the cytokines data for analysis  
   1. Create the patient index file
   2. Create the matrix from cytokines data
   3. format the matrix (drop the OMICID)
   4. split matrix into quantitative and others values 

3. describe_autoantibodies <diagnostic> <display> 
   run a procedure to plot the actual number of patient postive and negative  
   for the autoantibodies.  
   diagnostic could be pick among the list:  
   1. Control  
   2. RA
   3. MCTD  
   4. PAPs  
   5. SjS 
   6. SLE  
   7. SSc  
   8. UCTD  
Could be a combinaison (list) of the terms, could be set to "all" (i.e a list of all terms)  
Could be set to "overview" and display % values instead of raw count.
 
Display is a boolean, 1 to see the negative count AND the positive count, 0 for  only the positive count  

3. process_associationRules  
Filter, format (clp format) and translate association rules.  

4. describe_discrete_variable <variable_name>  
plot the proportion of NA data for this variable, and enumerate the possible values.  
variable_name can be in the form pX or can be the real name of the variable (e.g \\Clinical\\Symptom\\ABNORMINFLAM)
