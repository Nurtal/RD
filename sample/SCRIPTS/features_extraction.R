# Features extractions
library(Boruta)

# load data
flow_data <- read.csv("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample\\DATA\\MATRIX\\flowcyto.txt", header = T, stringsAsFactors = F, sep="\t")
diagnosic_table = read.csv("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample\\DATA\\patientIndex.csv", header = F, sep=";")
colnames(diagnosic_table) <- c("OMICID", "diagnostic")

df <- diagnosic_table
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
diagnosic_table <- as.data.frame(m)


rownames(diagnosic_table) <- diagnosic_table$OMICID
rownames(flow_data) <- flow_data$OMICID

flow_data$OMICID <- NULL
diagnosic_table$OMICID <- NULL


flow_data <- merge(diagnosic_table, flow_data, by=0)


# Delete some variables
flow_data$P1_CD14LOWCD16POS_NONCLASSICMONOCYTES <- NULL
flow_data$P2_DRNEGCD123POS_BASOPHILS <- NULL
flow_data$P2_LINNEGDRPOSCD11CNEGCD123POS_PDC <- NULL
flow_data$P2_LINNEGDRPOSCD11CPOSCD123NEGCD1CPOS_MDC1 <-NULL
flow_data$P2_LINNEGDRPOSCD11CPOSCD123NEGCD141POS_MDC2 <- NULL

# Remove patient
flow_data<-flow_data[!(traindata$OMICID=="32151646"),]
flow_data<-flow_data[!(traindata$OMICID=="32151888"),]

# Split into Panel
flow_data_panel_1 <- flow_data[,grep("P1_|OMICID", colnames(flow_data))]
flow_data_panel_2 <- flow_data[,grep("P2_", colnames(flow_data))]
flow_data_panel_3 <- flow_data[,grep("P3_", colnames(flow_data))]
flow_data_panel_4 <- flow_data[,grep("P4_", colnames(flow_data))]
flow_data_panel_5 <- flow_data[,grep("P5_", colnames(flow_data))]
flow_data_panel_6 <- flow_data[,grep("P6_", colnames(flow_data))]


flow_data_panel_2 <- flow_data[,grep("P2_|OMICID", colnames(flow_data))]
flow_data_panel_2 <- merge(flow_data_panel_2, diagnosic_table, by="OMICID")

flow_data_panel_1 <- merge(flow_data_panel_1, diagnosic_table, by="OMICID")
flow_data_panel_1$OMICID <- NULL

# Remove NA or perform Imputation
flow_data_panel_1 <- flow_data_panel_1[complete.cases(flow_data_panel_1),]
flow_data_panel_2 <- flow_data_panel_2[complete.cases(flow_data_panel_2),]
flow_data_panel_3 <- flow_data_panel_3[complete.cases(flow_data_panel_3),]
flow_data_panel_4 <- flow_data_panel_4[complete.cases(flow_data_panel_4),]
flow_data_panel_5 <- flow_data_panel_5[complete.cases(flow_data_panel_5),]
flow_data_panel_6 <- flow_data_panel_6[complete.cases(flow_data_panel_6),]


# Panel to Process:
panel_to_process <- flow_data_panel_1
names(panel_to_process)[12]

# Run Boruta
f <- paste(names(panel_to_process)[1], "~.", sep="")
boruta.train <- Boruta(diagnostic~., data = panel_to_process, doTrace = 2)


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
png("feature_selection_panel_6.png", width=4, height=4, units="in", res=300)
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
write.table(boruta.df, "feature_selection_panel_6.txt", sep=";")

