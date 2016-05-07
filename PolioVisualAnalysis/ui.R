library(shiny)
library(RCurl)
library(curl)

getPolioData <- function(){
        fileUrl <- "https://docs.google.com/spreadsheets/d/1sAs4NPoG-oKpC8D2T9VsOgfc7uXLaCHPHUVcm_msxIk/pub?gid=965821679&single=true&output=csv"
        download.file(url = fileUrl, destfile = "~/data.csv", mode="w", method = "curl")
}
getPolioData()
polioData <- read.csv("~/data.csv")

shinyUI(fluidPage(
        h4("Polio Vaccine Efficacy in the US: Visual Assessment"),
        sidebarLayout(
                sidebarPanel(
                        helpText("Select the information you wish to display in the Reactive Visualization:"),
                        selectInput("region", "X-Axis", 
                                    choices = colnames(polioData)),
                        selectInput("region2", "Y-Axis", 
                                    choices = colnames(polioData))),
                mainPanel(
                        p('Polio vaccine was first administered in the 1950s, yet the United States was not declared Polio-free until 1979. At the time of administration, the vaccine was not fully proven to be effective in clinical trials.  Dr. Jonas Salk wrote, "Risks, I like to say, always pay off.  You learn what to do, or what not to do." Dr. Salk was the inventor of the first polio vaccine and is directly responsible for contributions to eradicating Polio.  Explore the data to see for yourself whether vaccination was a cure, or a preventative measure.'),
                        tabsetPanel(
                                tabPanel("Histogram of Polio Incidences 1928-1968", 
                                         plotOutput("newHist")),
                                tabPanel("Reactive Visualization", plotOutput("barPlot")),
                                tabPanel("Table of Data", dataTableOutput("table"))
                  ))
)))
