#Open the data (I directly drag the data from the internet)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook

#upload data
osu_womenbasketball = pd.read_csv('data_womenbasketball.csv')
osu_basketball = pd.read_csv('data_basketball.csv')
osu_football = pd.read_csv('data_football.csv')
osu_icehockey = pd.read_csv('data_icehockey.csv')

#Calculate the winning percentage in % form
osu_basketball['Win percentage']=osu_basketball.Win/(osu_basketball.Win+osu_basketball.Lose)*100
osu_football['Win percentage']=osu_football.Win/(osu_football.Win+osu_football.Lose+osu_football.Tie)*100
osu_icehockey['Win percentage']=osu_icehockey.Win/(osu_icehockey.Win+osu_icehockey.Lose+osu_icehockey.Tie)*100
osu_womenbasketball['Win percentage']=osu_womenbasketball.Win/(osu_womenbasketball.Win+osu_womenbasketball.Lose)*100

#Plot the figure
fig,ax = plt.subplots(1,1,figsize=(10,5))
#remove all the spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
# Avoid unnecessary whitespace.
ax.set_xlim(1950, 2020)
ax.set_ylim(-0.25, 105)

# Make sure your axis ticks are large enough to be easily read.
# You don't want your viewers squinting to read your plot.
plt.xticks(range(1950, 2020, 10), fontsize=10)
plt.yticks(range(0, 125, 25), fontsize=10)
ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.2)

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)

#plot line for figures
plt.plot(osu_basketball['Year'],osu_basketball['Win percentage'].rolling(window = 5).mean(),linewidth = 2, color = 'orange',alpha = 0.8, label = r"Men's Basketball" )
plt.plot(osu_womenbasketball['Year'],osu_womenbasketball['Win percentage'].rolling(window = 5).mean(),'--',linewidth = 2, color = 'orange',alpha = 0.8, label = r"Women's Basketball" )
plt.plot(osu_football['Year'],osu_football['Win percentage'].rolling(window = 5).mean(),linewidth = 2, color = 'red',alpha = 0.8, label = r"Men's Football" )
plt.plot(osu_icehockey['Year'],osu_icehockey['Win percentage'].rolling(window = 5).mean(),linewidth = 2, color = 'blue',alpha = 0.8, label = r"Men's Ice_hockey" )

#plot legend
plt.legend(loc = 3, frameon = False, fontsize = 14)

# level set equations
plt.text(2010, 10, r"Win(%) = (Game Won)/(Game Won + Game Lost + Game Tied) * 100%", {'color': 'green', 'fontsize': 8}, va="top", ha="right")

#plot labels and titles
plt.xlabel(r'Season (Year)',fontsize = 14)
plt.ylabel(r'5 Year Moving Average Win (%)',fontsize = 14)
plt.title(r'The Ohio State University Sports Teams Win(%) (5 Year Moving Average)',fontsize = 16)
plt.show()
