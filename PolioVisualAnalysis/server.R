library(shiny)
library(curl)

getPolioData <- function(){
        fileUrl <- "https://docs.google.com/spreadsheets/d/1sAs4NPoG-oKpC8D2T9VsOgfc7uXLaCHPHUVcm_msxIk/pub?gid=965821679&single=true&output=csv"
        download.file(url = fileUrl, destfile = "~/data.csv", mode="w", method = "curl")
        }
getPolioData()
polioData <- read.csv("~/data.csv")

shinyServer(function(input, output){
                output$table <- renderDataTable({polioData})
                output$newHist <- renderPlot({
                        hist((as.numeric(polioData$number)), 
                             xlab = 'Polio Incidence', col = 'lightblue', 
                             main = 'Calculated Frequency Distribution of Polio Occurences 1928-1968')})
                output$barPlot <- renderPlot({
                        data <- table((polioData[,input$region]), (polioData[,input$region2]))
                        barplot(data, main = "Polio Data from 1928-1968", ylab=input$region, xlab=input$region2, col = 'lightblue')})
})
                
