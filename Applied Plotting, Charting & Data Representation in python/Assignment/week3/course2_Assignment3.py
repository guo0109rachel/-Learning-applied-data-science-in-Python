# Use the following data for this assignment:
%matplotlib notebook
import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])
df
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as ss
import matplotlib.colors as col
import matplotlib.cm as cm
import mpl_toolkits.axes_grid1.inset_locator as mpl

%matplotlib notebook

#get the stat data for four samples
dfT = df.T
dfStats = dfT.describe()
dfStatsT=dfStats.T
dfStatsT['yerr'] = dfStatsT['std']/np.sqrt(dfStatsT['count'])*ss.norm.ppf(1-0.05/2)
dfStats = dfStatsT.T
dfStats

#get x and y axis and errbar list
xMList = list(dfStats)
yMList = list(dfStats.loc['mean'])
errList = list(dfStats.loc['yerr'])

#compute the probablity of the mean > y for each column
conf_ints = [ss.norm.interval(0.95,loc=mu,scale=se) for mu,se in zip(dfStats.loc['mean'],dfStats.loc['std']/np.sqrt(dfStatsT['count']))]
def compute_probs(y,conf_int):
    if y < np.min(conf_int):
        result = 1.0
    elif y > np.max(conf_int):
        result = 0.0
    else:
        result = (np.max(conf_int)-y)/(np.max(conf_int)-np.min(conf_int))
    return result

# Setup the colormap
cml = col.LinearSegmentedColormap.from_list('MyCmapName',['darkblue','white','darkred'])
cpick = cm.ScalarMappable(cmap=cml, norm=col.Normalize(vmin=0,vmax=1.0))
cpick.set_array([])

#Click the threshold value


threshold = 43000
#Compute the probabilities
probs = [compute_probs(threshold,ci) for ci in conf_ints]
# Setup the plot
pfigure = plt.bar(range(len(df.T.columns)),yMList, yerr=errList,color=cpick.to_rgba(probs),edgecolor='black')

# Add the horizontal line and add its value as a y-tick
x1, x2 = plt.xlim()
line, = plt.plot([x1, x2], [threshold, threshold], 'k-', color='grey', lw=1, label="_not in legend")

# Set the x-axis tick marks to be the years
plt.xticks(range(len(df.T.columns)),df.T.columns)

plt.gca().set_title('Distribution comparison for chosen mean of (y-axis value): {}'.format(threshold))
# Add the colorbar
cbar = plt.colorbar(cpick,orientation='horizontal')

# Turn off some plot rectangle spines
[plt.gca().spines[loc].set_visible(False) for loc in ['top', 'right']]

plt.show()

def onclick(event):
    threshold = event.ydata
    #Compute the probabilities
    probs = [compute_probs(threshold,ci) for ci in conf_ints]
    # Setup the plot
    pfigure = plt.bar(range(len(df.T.columns)),yMList, yerr=errList,color=cpick.to_rgba(probs),edgecolor='black')

    # Add the horizontal line and add its value as a y-tick
    line.set_ydata([event.ydata,event.ydata])

    # Set the x-axis tick marks to be the years
    plt.xticks(range(len(df.T.columns)),df.T.columns)

    plt.gca().set_title('Distribution comparison for chosen mean of (y-axis value): {}'.format(threshold))

    # Turn off some plot rectangle spines
    [plt.gca().spines[loc].set_visible(False) for loc in ['top', 'right']]

    plt.show()

# tell mpl_connect we want to pass a 'button_press_event' into onclick when the event is detected
plt.gcf().canvas.mpl_connect('button_press_event', onclick)
