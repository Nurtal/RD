# Features extractions
library(Boruta)

# load data
flow_data <- read.csv("C:\\Users\\PC_immuno\\Desktop\\Nathan\\SpellCraft\\RD\\sample\\DATA\\MATRIX\\flowcyto.txt", header = T, stringsAsFactors = F, sep="\t")

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
flow_data_panel_1 <- flow_data[,grep("P1_", colnames(flow_data))]
flow_data_panel_2 <- flow_data[,grep("P2_", colnames(flow_data))]
flow_data_panel_3 <- flow_data[,grep("P3_", colnames(flow_data))]
flow_data_panel_4 <- flow_data[,grep("P4_", colnames(flow_data))]
flow_data_panel_5 <- flow_data[,grep("P5_", colnames(flow_data))]
flow_data_panel_6 <- flow_data[,grep("P6_", colnames(flow_data))]

# Remove NA or perform Imputation
flow_data_panel_1 <- flow_data_panel_1[complete.cases(flow_data_panel_1),]
flow_data_panel_2 <- flow_data_panel_2[complete.cases(flow_data_panel_2),]
flow_data_panel_3 <- flow_data_panel_3[complete.cases(flow_data_panel_3),]
flow_data_panel_4 <- flow_data_panel_4[complete.cases(flow_data_panel_4),]
flow_data_panel_5 <- flow_data_panel_5[complete.cases(flow_data_panel_5),]
flow_data_panel_6 <- flow_data_panel_6[complete.cases(flow_data_panel_6),]


# Panel to Process:
panel_to_process <- flow_data_panel_6
names(panel_to_process)[1]

# Run Boruta
f <- paste(names(panel_to_process)[1], "~.", sep="")
boruta.train <- Boruta(P6_CD27POS_CD43POS_BCELLS~., data = panel_to_process, doTrace = 2)


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

