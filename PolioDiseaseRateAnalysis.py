# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:31:55 2015

@author: JD Davis

A visual analysis of polio disease rates
from 1888-2013

Most of the data in this set are preventable with vaccination.

website for data: https://www.healthdata.gov
Data set : ProjectTyco_Level1

Analysis done in Python 3.4

"""
import pandas as pd
import csv

#first order of business is taking a peak at the dataset

data_file = "/Users/Work/Desktop/disease.hx.csv"
with open(data_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)
    
#take a peak at the data set

len(data) # get an idea of number of observations

print ('number of columns', len(reader.fieldnames))

#write a function so you can read in data in smaller chunks
#useful for larger data sets, and it also memorizes the path for you!
def dataset(path):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

#find out which diseases are represented
print (set([row ["disease"] for row in dataset(data_file)]))

#look at range of years

print ('first year of observations', min(set([int(row['epi_week']) for row in dataset (data_file)])))

#looks like starts in epi_week 1916, week 1

#now let's look at the latest date
print ('last year of observations', max(set(int(row["epi_week"]) for row in dataset(data_file))))

{row ["disease"] for row in dataset(data_file)}
(['RUBELLA', 'POLIO', 'MEASLES', 'HEPATITIS A', 'DIPHTHERIA', 'PERTUSSIS',
  'SMALLPOX', 'MUMPS'])

#now let's do some simple statistical analysis and visualization
       
import csv
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/Work/Desktop/disease.hx.csv', index_col='id')                      

#let's look at some summary statistics and do a regression
df.dtypes #see what the variables are and their data type
df.describe() #descriptive stats

#make a new object that has only the POLIO cases
df2 = df.copy()
df2
df3=df2[df2['disease'].isin(['POLIO'])]
df3

#lastly we'll look at quantiles
from scipy.stats.mstats import mquantiles
print ('quantiles:', mquantiles(df.inc))

import seaborn as sns

sns.set(style="white", palette="muted")
f, axes = plt.subplots(2,2, figsize=(7,7), sharex=True)
sns.despine(left=True)
b, g, r, p = sns.color_palette("muted", 4)
sns.distplot(df3.inc, kde=False, color=b, ax=axes[0,0])
sns.distplot(df3.inc, hist=False, rug=True, color=r, ax=axes[0,1])
sns.distplot(df3.inc, hist=False, color=g, kde_kws={"shade": True}, ax=axes[1,0])
sns.distplot(df3.inc, color=p, ax=axes[1,1])

plt.setp(axes, yticks=[])
plt.tight_layout()

#histogramming the data for Polio
s = pd.Series(df3.inc)
pd.value_counts(s) #the data on the frequency of values

df3.describe()

"""We see that first year for Polio monitoring was 1928 and the last year with
a significant count was 1968. For Polio subset 81531 records exist in the data set
The maximum incidence ratio during this time period was 33 and minimum
was zero. """

import numpy as np
import statsmodels.api as sm

x = df3.epi_week
y = df3.inc
results = sm.OLS(y, x).fit()
print (results.summary()) 

"""You will see that time, i.e. epi_week is strongly associated with incidence, 
but there is a fairly high skew rate (9.447) and Kurtosis is very high (209.747).
Thus its inappropriate to use a linear regression with the data in this format"""

#let's look at the data in a probability plot to see what might be the problem
import statsmodels.api as sm
from matplotlib import pyplot as plt
mod_fit = sm.OLS(df3.epi_week, df3.inc).fit()
res = mod_fit.resid # residuals
fig = sm.qqplot(res)
plt.show()

#the problem with a linear regression model may be that at about -1 quantiles
#the samples flatten out...again this is due to the advent of vaccination most likely

pp_x = sm.ProbPlot(x, fit=True)
x = df3.epi_week
y = df3.inc
pp_x = sm.ProbPlot(x, fit=True)
pp_y = sm.ProbPlot(y, fit=True)
fig2 = pp_x.probplot(exceed=True)

#fig 2 above suggests we should select dates between 1925 and 1970
#if we want to perform a linear regression, however for this analysis
#probably not a meaningful assessment

"""Let's do one last visualization to look at the incidence over time by, 
state, week and population"""

sns.pairplot(df3, hue="state", vars=('epi_week', 'population', 'inc'),
             size=7.5)
             
"""The new visual assessment shows that incidence of polio grew before it was
virtually eliminated by 1968.  Since we do see some variability by state we 
might want to subset again by region of the country.  However that's another
lesson!  For this lesson we will compare Texas (south) to California (west)
to Massachusetts(east), to Illinois(north) """


df3 = df.copy()
df3
df.south=df3[df3['state'].isin(['TX'])]
df.south

df.north = df3[df3['state'].isin(['IL'])]
df.west = df3[df3['state'].isin(['CA'])]
df.east = df3[df3['state'].isin(['MA'])]
df.east

df.east.describe()
df.west.describe() #highest incidence
df.north.describe()
df.south.describe() #lowest incidence

#now let's look at variables from before
sns.pairplot(df.east, hue="state", vars=('epi_week', 'inc'),
             size=5) #MA high incidence 1940-late 1960s
             
sns.pairplot(df.west, hue="state", vars=('epi_week', 'inc'),
             size=5) #CA incidence peaks in the 1940s and declines thereafter
             
sns.pairplot(df.north, hue="state", vars=('epi_week', 'inc'),
             size=5) #IL incidence peaks in the 1940s and declines thereafter

sns.pairplot(df.south, hue="state", vars=('epi_week', 'inc'),
             size=5) #TX you can see the incidence peaked in the 1960s
             
"""Our final visual assessment shows something quite interesting.  It looks
as though a peak in polio incidence occurred in MA, CA and IL in the 1940s, 
but TX peaked in the 1960s.  It would be interesting to explore the data
further to determine if this is a real effect and if so to explore history
to determine why there was a lag in decline of polio in TX""" 
             
             





