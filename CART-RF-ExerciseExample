##Background

#The goal of this project's analysis is to predict classes of exercises based upon self-quantified movement.  In this study the author's took a group of health enthuasists who normally take measurements of their exercise regularly to improve their health using devices such as Jawbone Up, Nike FuelBand and Fitbit. The data from the current study was quantified to determine how well participants performed barbell lifts.  They were asked to perform the barbell ifts both correctly and incorrectly in 5 different ways.  These methods were then quantified using 160 features batherd from acclerometers on the belt, forearm, and dumbell of 6 participants. More information 
##Raw Data Assessment

#The full training data set contains 19622 observations and 160 features. It is unlikely that all these features are necessary to make accurate predictions.  To address this a practical approach is taken to reducing data dimensionality. We will do this with a bit of pre-processing of the data before splitting the "training" data into a training set and a validation set.


library(gridExtra)
library(caret)
library(rpart)
library(RColorBrewer)
library(rattle)
library(ggplot2)
library(randomForest) 
library(rpart.plot)
library(AppliedPredictiveModeling)
library(parallel)
library(doParallel)

#load the training and testing data for pre-processing

TrainingData <- read.csv("/Users/Work/Desktop/PracticalML/pml-training.csv", header=TRUE, stringsAsFactors=FALSE)

#dimensions of training data
dim(TrainingData)

isMissing <- sapply(TrainingData, function(x) any(is.na(x) | x== ""))
isPredictor <- !isMissing & grepl("belt|[^(fore) ] arm |dumbell | forearm", names(isMissing))
featureCandidates <- names(isMissing)[isPredictor]

dataInclude <- c("classe", featureCandidates)
featureData <- TrainingData[dataInclude] #now all data is selected for 13 features
dim(featureData) #14 columns, 19622 observations
str(featureData) #make sure "classe" is still present

#confirm numerically that none of selected features have near-zero variances

nzv <- nearZeroVar(featureData, saveMetrics=TRUE)
summary(nzv) 

featureData2 <- TrainingData[featureCandidates]
descrCor <- cor(featureData2)
perfectCorFeatures <- sum(abs(descrCor[upper.tri(descrCor)]) > 0.999) 
perfectCorFeatures

highCorFeatures <- findCorrelation(descrCor, cutoff = 0.75)
highCorFeatures 

classe <- featureData$classe
filteredFeatures <- cbind(classe, (featureData[,-(findCorrelation(descrCor, cutoff=0.75))])) 

#creation of Training and Validation data using 5 resamples
set.seed(1234)

trainIndex <- createDataPartition(filteredFeatures$classe, p=0.6, list=FALSE, times=5) #here we created a 60/40% split with 5 resamplings

dataTrain <- filteredFeatures[trainIndex,]
dataValidate <- filteredFeatures[-trainIndex,]

plt1 <- ggplot(dataTrain, aes(factor(classe), dataTrain$roll_belt)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt1 <- plt1 + labs(x="Classe", y="Roll Belt") 

plt2 <- ggplot(dataTrain, aes(factor(classe), dataTrain$total_accel_belt)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt2 <- plt2 + labs(x="Classe", y="Total Acceleration Belt")

plt3 <- ggplot(dataTrain, aes(factor(classe), dataTrain$gyros_belt_x)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt3 <- plt3 + labs(x="Classe", y="Gyros Belt X")

plt4 <- ggplot(dataTrain, aes(factor(classe), dataTrain$gyros_belt_y)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt4 <- plt4 + labs(x="Classe", y="Gryos Belt Y")

plt5 <- ggplot(dataTrain, aes(factor(classe), dataTrain$magnet_belt_z)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt5 <- plt5 + labs(x="Classe", y="Gyros Belt Z")

plt6 <- ggplot(dataTrain, aes(factor(classe), dataTrain$accel_belt_x)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt6 <- plt6 + labs(x="Classe", y="Acceleration Belt X")

plt7 <- ggplot(dataTrain, aes(factor(classe), dataTrain$magnet_belt_y)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none")
plt7 <- plt7 + labs(x="Classe", y="Magnet Belt Y")

plt8 <- ggplot(dataTrain, aes(factor(classe), dataTrain$magnet_belt_z)) + geom_violin(aes(fill=classe)) + theme_bw() + theme(legend.position="none") + labs(x = "Classe", y ="Magnet Belt Z")

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
    library(grid)
    
    # Make a list from the ... arguments and plotlist
    plots <- c(list(...), plotlist)
    
    numPlots = length(plots)
    
    # If layout is NULL, then use 'cols' to determine layout
    if (is.null(layout)) {
        # Make the panel
        # ncol: Number of columns of plots
        # nrow: Number of rows needed, calculated from # of cols
        layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                         ncol = cols, nrow = ceiling(numPlots/cols))
    }
    
    if (numPlots==1) {
        print(plots[[1]])
        
    } else {
        # Set up the page
        grid.newpage()
        pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
        
        # Make each plot, in the correct location
        for (i in 1:numPlots) {
            # Get the i,j matrix positions of the regions that contain this subplot
            matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
            
            print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                            layout.pos.col = matchidx$col))
        }
    }
}

multiplot(plt1, plt2, cols=2)
multiplot(plt3, plt4, cols=2)
multiplot(plt5, plt6, cols=2)
multiplot(plt6, plt7, cols=2)
multiplot(plt8, cols=2)

clusters <- makeCluster(detectCores() -1)
registerDoParallel(clusters)

ctrl <- trainControl(classProbs = TRUE, savePredictions = TRUE, allowParallel = TRUE)

method <- "rpart"

system.time(ModelClassTree <- train(classe ~., preProcess=c("center", "scale"), data=dataTrain, method="rpart"))

ModelClassTree

predictedClassTree <- predict(ModelClassTree, dataValidate)

cmCT <- confusionMatrix(predictedClassTree, dataValidate$classe)
cmCT

stopCluster(clusters)

varImp(ModelClassTree)
ModelClassTree$finalModel

#estimated error rate : 

save(ModelClassTree, file="ModelClassTree.RData")


#########Train the Prediction Model Random Forest##############

clusters <- makeCluster(detectCores() -1)
registerDoParallel(clusters)

ctrl <- trainControl(classProbs = TRUE, savePredictions = TRUE, allowParallel = TRUE)

method <- "rf"

system.time(ModelRF <- train(classe ~., preProcess=c("center", "scale"), data=dataTrain, method="rf"))

ModelRF

predictedRF <- predict(ModelRF, dataValidate)

cmRF <- confusionMatrix(predictedRF, dataValidate$classe)
cmRF

varImp(ModelRF)
ModelClassTree$finalModel

stopCluster(clusters)

#estimated error rate : 

save(ModelRF, file="ModelRF.RData")

###Final Algorithm Choice

########Predict with chosen model on test data############

TestingData <- read.csv("/Users/Work/Desktop/PracticalML/pml-testing.csv", header=TRUE, stringsAsFactors=FALSE)

load(file="ModelRF.RData", verbose=FALSE)

predictFinal <- predict(ModelRF, TestingData)
predictCT <- predict(ModelClassTree, TestingData)

#Write files for submission
pml_write_files = function(x){
    n=length(x)
    for (i in 1:n){
        filename=paste("problem_id_", i, ".txt")
        write.table(x[i], file=filename, quote=FALSE, row.names=FALSE, col.names=FALSE)
    }
}

pml_write_files(predictFinal)
pml_write_files(predictCT)
