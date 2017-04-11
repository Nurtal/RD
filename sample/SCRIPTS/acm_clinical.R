library(FactoMineR)
library(factoextra)
library(corrplot)

#-----------------#
# DATA PROCESSING #
#-----------------#

#load data
data <- read.csv("/home/foulquier/Bureau/SpellCraft/WorkSpace/SCRIPTS/data/clinical_data_phase_1.csv", stringsAsFactors=TRUE)

# drop medication (lots of NA)
medication_col_names = grep("Medication", names(data), value=TRUE)
drops <- medication_col_names
data = data[ , !(names(data) %in% drops)]

# drop a few  variable
drops_2 = c("X.Clinical.Diagnosis.ONSETDTC", "X.Clinical.Sampling.LBDTC", "X.Clinical.Sampling.USUBJID", "X.Clinical.Sampling.OMICID", "X.Clinical.Demography.BRTHYR", "X.Clinical.Sampling.DURATIONYR")
data = data[ , !(names(data) %in% drops_2)]

# drop a few other variables
drops_3 = c("X.Clinical.Symptom.PEGLOBAL", "X.Clinical.Demography.AGE", "X.Clinical.Consent.CSPHASE", "X.Clinical.Demography.RACE")
data = data[ , !(names(data) %in% drops_3)]


# get only the control (a dataframe full of NA ...)
control_data = data[data$X.Clinical.Diagnosis.DISEASE == "Control", ] 

# use only patient without NA ( drop control in the process ...)
data = data[complete.cases(data),]
data <- data.frame(lapply(data, as.factor))

# Create sub data
lung_data = data[,grep("Lung", names(data), value=TRUE)]
lung_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
lung_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
lung_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

kidney_data = data[,grep("Kidney", names(data), value=TRUE)]
kidney_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
kidney_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
kidney_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

nerveSystem_data = data[,grep("NerveSystem", names(data), value=TRUE)]
nerveSystem_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
nerveSystem_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
nerveSystem_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

skin_data = data[,grep("Skin", names(data), value=TRUE)]
skin_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
skin_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
skin_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

muscleAndSkeletal_data = data[,grep("MuscleandSkeletal", names(data), value=TRUE)]
muscleAndSkeletal_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
muscleAndSkeletal_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
muscleAndSkeletal_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

comorbidity_data = data[,grep("Comorbirdity", names(data), value=TRUE)]
comorbidity_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
comorbidity_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
comorbidity_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

vascular_data = data[,grep("Vascular", names(data), value=TRUE)]
vascular_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
vascular_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
vascular_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

gastro_data = data[,grep("Gastro", names(data), value=TRUE)]
gastro_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
gastro_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
gastro_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

heart_data = data[,grep("Heart", names(data), value=TRUE)]
heart_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
heart_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
heart_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

diagnosis_data = data[,grep("Diagnosis", names(data), value=TRUE)]
diagnosis_data$X.Clinical.Diagnosis.DISEASE = as.factor(data$X.Clinical.Diagnosis.DISEASE)
diagnosis_data$X.Clinical.Demography.SEX = as.factor(data$X.Clinical.Demography.SEX)
diagnosis_data$X.Clinical.Sampling.CENTER = as.factor(data$X.Clinical.Sampling.CENTER)

sub_data_list = list(lung_data, kidney_data, nerveSystem_data, skin_data, muscleAndSkeletal_data, comorbidity_data, vascular_data, gastro_data, heart_data, diagnosis_data)


for(val in 1:length(sub_data_list)){
  
  # Get data
  data = sub_data_list[[val]]
  
  # Perfrom ACM
  mca1 = MCA(data, graph = FALSE)
  
  # Extract variable and individuals
  var <- get_mca_var(mca1)
  ind <- get_mca_ind(mca1)
  
  # Extract "labels" for future coloration
  sick <- as.factor(data$X.Clinical.Diagnosis.DISEASE)
  sex <- as.factor(data$X.Clinical.Demography.SEX)
  center <- as.factor(data$X.Clinical.Sampling.CENTER)
  
  #--------------#
  # PLot Section #
  #--------------#
  
  # Plot individual, colored by sickness, add ellipse
  fviz_mca_ind(mca1, label="none", habillage = sick,
               addEllipses = TRUE, ellipse.level = 0.95)
  
  
}







#------------#
# TEST SPACE #
#------------#


#-----#
# ACM #
#-----#

mca1 = MCA(heart_data, graph = TRUE)
fviz_screeplot(mca1)

plot(mca1)
fviz_mca_biplot(mca1)

# Correlation between variables and principal dimensions
plot(mca1, choix = "var")


var <- get_mca_var(mca1)
corrplot(var$contrib, is.corr = FALSE)


# work on individual
ind <- get_mca_ind(mca1)
fviz_mca_ind(mca1)

# contribution of individual to dimensions
fviz_contrib(mca1, choice = "ind", axes = 1:2, top = 20)

# Control the transparency of individuals using their contribution
# Possible values for the argument alpha.ind are :
# "cos2", "contrib", "coord", "x", "y"
fviz_mca_ind(mca1, alpha.ind="contrib")

# represent individual, colored by diagnostic
sick <- as.factor(data$X.Clinical.Diagnosis.DISEASE)
sex <- as.factor(data$X.Clinical.Demography.SEX)
center <- as.factor(data$X.Clinical.Sampling.CENTER)
fviz_mca_ind(mca1, label = "none", habillage=sick)

# add ellipse
fviz_mca_ind(mca1, label="none", habillage = sick,
             addEllipses = TRUE, ellipse.level = 0.95)


