# R file for statistical analysis
library(tidyr)
library(dplyr)
library(reshape2)
library(data.table)
library(ggplot2)
library(psych)

raw_data <- read.csv("~/raw_data.csv", stringsAsFactors = FALSE)

#high level summary statistics
dimensions <- dim(raw_data) #1422, 72

summary_statistics <- summary(raw_data)

################## Human Expert Data ANOVA  ###################################

# Summary stats on the Master Rating

summary <- summary(raw_data$LM.Master.Rating.Extended)

#summary stats

master_rate <- raw_data$LM.Master.Rating.Extended

descriptive_summary_master_rating = describe(master_rate)

descriptive_summary_raw_data = describe(raw_data)

anova_human_rater <- aov(raw_data$LM.Master.Rating.Extended ~ raw_data$Student.Name, data = raw_data)

anova_human_rater_summary <- summary(anova)

TukeyHSD(anova_human_rater)

summary_stats<- describe(raw_data)
data_frame_summary_stats <- as.data.frame(summary_stats)

summary_stats_saved <- write.csv(data_frame_summary_stats, file = "summary_stats.csv")
