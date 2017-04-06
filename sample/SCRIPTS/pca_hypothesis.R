#Test PCA hypothesis


data <- read.csv("/home/nurtal/Spellcraft/test/cohorte.csv")

#nuages de points
pairs(data)

#partition des données (var. actives et illustratives)
data.actifs <- data[,1:4]
data.illus <- data[,5:5]
#nombre d'observations
n <- nrow(data.actifs)
print(n)


#centrage et réduction des données --> cor = T
#calcul des coordonnées factorielles --> scores = T
acp.data <- princomp(data.actifs, cor = T, scores = T)
#print
print(acp.data)
#summary
print(summary(acp.data))
#quelles les propriétés associées à l'objet ?
print(attributes(acp.data))


#obtenir les variances associées aux axes c.-à-d. les valeurs propres
val.propres <- acp.data$sdev^2
print(val.propres)
#scree plot (graphique des éboulis des valeurs propres)
plot(1:4,val.propres,type="b",ylab="Valeurs 
propres",xlab="Composante",main="Scree plot")
#intervalle de confiance des val.propres à 95% (cf.Saporta, page 172)
val.basse <- val.propres * exp(-1.96 * sqrt(2.0/(n-1)))
val.haute <- val.propres * exp(+1.96 * sqrt(2.0/(n-1)))
#affichage sous forme de tableau
tableau <- cbind(val.basse,val.propres,val.haute)
colnames(tableau) <- c("B.Inf.","Val.","B.Sup")
print(tableau,digits=3)
