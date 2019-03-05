import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook

df = pd.read_csv('./data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
premin = []
premax = []
#remove data of 2-29
df = df[~(df['Date'].str.endswith(r'02-29'))]

#Get temperature in Deg C
#df['Temperature'] = df['Data_Value']/10.0

#set dates
Time = pd.DatetimeIndex(df['Date'])

#find pre-2015 min and max
predf = df[Time.year != 2015]
pretime = pd.DatetimeIndex(predf['Date'])

for j in predf.groupby([pretime.month,pretime.day]):
    premin.append(min(j[1]['Data_Value']))
    premax.append(max(j[1]['Data_Value']))

#find 2015 min and max
df2015 = df[Time.year==2015]
time2015 = pd.DatetimeIndex(df2015['Date'])
min2015 = []
max2015 = []

for j in df2015.groupby([time2015.month,time2015.day]):
    min2015.append(min(j[1]['Data_Value']))
    max2015.append(max(j[1]['Data_Value']))

#find the 2015 break points
mindate = []
maxdate = []
minT = []
maxT = []
for i in range(len(premin)):
    if(premin[i] > min2015[i]):
        mindate.append(i)
        minT.append(min2015[i])
    if(premax[i]<max2015[i]):
        maxdate.append(i)
        maxT.append(max2015[i])

#plot the figures afterwards
plt.figure()

#change unit
for i in range(len(premin)):
    premin[i] = premin[i]/10.0
for i in range(len(premax)):
    premax[i] = premax[i]/10.0
for i in range(len(minT)):
    minT[i] = minT[i]/10.0
for i in range(len(maxT)):
    maxT[i] = maxT[i]/10.0

#plot line for figures
plt.plot(premin, color = 'g',alpha = 0.8, label = 'Minimum Temperature (2005-14)')
plt.plot(premax, color = 'r', alpha = 0.8, label = 'Maximum Temperature (2005-14)')

#plot scatters in figures
plt.scatter(mindate, minT, s = 20, color = 'blue', label = 'Minimum T Record Break (2015)')
plt.scatter(maxdate, maxT, s = 20, color = 'black', label = 'Maximum T Record Break (2015)')

#plot shade area
plt.gca().fill_between(range(len(premin)),premin,premax,facecolor = 'blue',alpha = 0.2)

#remove right and top spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

#plot legend
plt.legend(loc = 8, frameon = False, fontsize = 8)

#plot x axis and labels
plt.xticks( np.linspace(15,15 + 30*11 , num = 12), (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'Jun', r'Jul', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec') )

#plot labels and titles
plt.ylabel('Temperature (Deg C)')
plt.title(r'Extreme Temperature of "Ann Arbor, Michigan" by months')
plt.show()
