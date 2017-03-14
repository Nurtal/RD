# Features extractions
library(Boruta)

# load data
flow_data <- read.csv("/home/foulquier/Bureau/SpellCraft/WorkSpace/FeatureSelection/flowcyto.txt", header = T, stringsAsFactors = F, sep="\t")
diagnosic_table = read.csv("/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/RD/sample/DATA/patientIndex.csv", header = F, sep=";")
colnames(diagnosic_table) <- c("OMICID", "diagnostic")

rownames(diagnosic_table) <- diagnosic_table$OMICID
rownames(flow_data) <- flow_data$OMICID
diagnosic_table$OMICID <- NULL
flow_data <- merge(diagnosic_table, flow_data, by=0)


# convert disease to 1, control to 0
df <- flow_data
m <- as.matrix(df)
m[m=="Control"] <- 0
m[m=="SLE"] <- 1
m[m=="RA"] <- 1
m[m=="UCTD"] <- 1
m[m=="undef"] <- 1
m[m=="SSc"] <- 1
m[m=="SjS"] <- 1
m[m=="PAPs"] <- 1
m[m=="MCTD"] <- 1
flow_data <- as.data.frame(m)

# Delete some variables
flow_data$Row.names <- NULL
flow_data$P1_CD14LOWCD16POS_NONCLASSICMONOCYTES <- NULL
flow_data$P2_DRNEGCD123POS_BASOPHILS <- NULL
flow_data$P2_LINNEGDRPOSCD11CNEGCD123POS_PDC <- NULL
flow_data$P2_LINNEGDRPOSCD11CPOSCD123NEGCD1CPOS_MDC1 <-NULL
flow_data$P2_LINNEGDRPOSCD11CPOSCD123NEGCD141POS_MDC2 <- NULL

# Remove patient
flow_data<-flow_data[!(traindata$OMICID=="32151646"),]
flow_data<-flow_data[!(traindata$OMICID=="32151888"),]

# Split into Panel
flow_data_panel_1 <- flow_data[,grep("P1_|diagnostic|OMICID", colnames(flow_data))]
flow_data_panel_2 <- flow_data[,grep("P2_|diagnostic|OMICID", colnames(flow_data))]
flow_data_panel_3 <- flow_data[,grep("P3_|diagnostic|OMICID", colnames(flow_data))]
flow_data_panel_4 <- flow_data[,grep("P4_|diagnostic|OMICID", colnames(flow_data))]
flow_data_panel_5 <- flow_data[,grep("P5_|diagnostic|OMICID", colnames(flow_data))]
flow_data_panel_6 <- flow_data[,grep("P6_|diagnostic|OMICID", colnames(flow_data))]


# Remove NA or perform Imputation
flow_data_panel_1 <- flow_data_panel_1[complete.cases(flow_data_panel_1),]
flow_data_panel_2 <- flow_data_panel_2[complete.cases(flow_data_panel_2),]
flow_data_panel_3 <- flow_data_panel_3[complete.cases(flow_data_panel_3),]
flow_data_panel_4 <- flow_data_panel_4[complete.cases(flow_data_panel_4),]
flow_data_panel_5 <- flow_data_panel_5[complete.cases(flow_data_panel_5),]
flow_data_panel_6 <- flow_data_panel_6[complete.cases(flow_data_panel_6),]


# Panel to Process:
panel_to_process <- flow_data_panel_6

# Run Boruta
boruta.train <- Boruta(diagnostic~.-OMICID, data = panel_to_process, doTrace = 2)


# Display results
plot(boruta.train, xlab = "", xaxt = "n")
lz<-lapply(1:ncol(boruta.train$ImpHistory),function(i)
  boruta.train$ImpHistory[is.finite(boruta.train$ImpHistory[,i]),i])

names(lz) <- colnames(boruta.train$ImpHistory)
Labels <- sort(sapply(lz,median))
axis(side = 1,las=2,labels = names(Labels),
     at = 1:ncol(boruta.train$ImpHistory), cex.axis = 0.7)


# Supplemental Results
final.boruta <- TentativeRoughFix(boruta.train)

# Display supplemental results
png("/home/foulquier/Bureau/SpellCraft/WorkSpace/FeatureSelection/feature_selection_panel_1.png", width=4, height=4, units="in", res=300)
plot(final.boruta, xlab = "", xaxt = "n")
lz<-lapply(1:ncol(boruta.train$ImpHistory),function(i)
  boruta.train$ImpHistory[is.finite(boruta.train$ImpHistory[,i]),i])

names(lz) <- colnames(boruta.train$ImpHistory)
Labels <- sort(sapply(lz,median))
axis(side = 1,las=2,labels = names(Labels),
     at = 1:ncol(boruta.train$ImpHistory), cex.axis = 0.7)
dev.off()

# Final steps
getSelectedAttributes(final.boruta, withTentative = F)
boruta.df <- attStats(final.boruta)
write.table(boruta.df, "/home/foulquier/Bureau/SpellCraft/WorkSpace/FeatureSelection/feature_selection_panel_1.txt", sep=";")

# Write new tables
selected_variables <- getSelectedAttributes(final.boruta, withTentative = F)
f <- paste(selected_variables, collapse='|')
f <- paste(c(f, "diagnostic|OMICID"), collapse = '|')
panel_to_process <- panel_to_process[,grep(f, colnames(panel_to_process))]

write.table(panel_to_process, "/home/foulquier/Bureau/SpellCraft/WorkSpace/FeatureSelection/panel_6_filtered.txt", sep=";")
