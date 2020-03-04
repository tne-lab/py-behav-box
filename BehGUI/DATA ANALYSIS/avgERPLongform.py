"""
###############################################################################################################

NOTE:  Run ERPs_RAW_to_percent_change.Py first to convert daily raw data with absolute ERPs into % change over baseline.

################################################################################################################
"""
import pandas as pd
import matplotlib.pyplot as plt
def createPlot(df,  ax, label):
    # Get mean
    tempy = tempdf.groupby(['ERP Time']).mean()
    #print(tempy)
    #print("\n")
    # Add pre and sort
    tempy = tempy.reset_index()
    predf = pd.DataFrame([['Pre',0]], columns=['ERP Time', 'ERPs'])
    tempy = tempy.append(predf)
    #print(tempy)
    #print("\n")
    tempy = tempy.iloc[::-1] # Reverse order
    
    # Plot if data
    # Note: tup[0] = uAmps, tup[1] = ms Lag
    if tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 0 :
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = 'SHAM',style='k^-') #Style ' col shape line', col=b-blue, g-green, r-red,c-cyan,m-magenta,y-yellow,k-black,w-white
                                                                                                                           #shape: v triangle, ^ triangle, s square, o circle, d diamond

    elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='rv-') #
    elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='ro-')
    elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 200: # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='rs-')
        
    elif tempy.Lag_ms[1] == 20 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='gv-') #
    elif tempy.Lag_ms[1] == 20 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='go-')
    elif tempy.Lag_ms[1] == 200 and tempy.uAmps[1] == 200: # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='gs-')
        
    elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='bv-') #
    elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='bo-')
    elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 200: # && tup[1] = 0:
        tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = label,style='bs-')


    plt.legend()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_visible(True)
    ax.set_ylim(-50,360)

def createSubPlot(title):
    fig, ax = plt.subplots(1, 1)
    ax.set_title(title)
    ax.set_ylabel('% Change in ERPs')
    ax.set_xlabel('ERP Time')
    return ax

def getDirectionERP(df, dir):
    # create list of options
    list = ['POST_5-' + str(dir), 'POST_30-' + str(dir), 'POST24HR-' + str(dir)]
    # pick out directions
    tempdf = df.loc[df['ERP Time'].isin(list)]
    # remove extra chars ('-2/-1')
    tempdf['ERP Time'] = tempdf['ERP Time'].map(lambda x: x[:-2])
    return tempdf

"""
MAIN PROG STARTS HERE


Plotting ERPS IL->BLA
"""
df = pd.read_csv(r'E:\py-behav-box\BehGUI\DATA\SUMMARY_ERPs_PERC_CHG_Long_Form.csv', skiprows = 0)
#df = pd.read_csv(r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPs_PERC_CHG_Long_Form.csv', skiprows = 0)


permutation_list = df[['uAmps','Lag_ms']].drop_duplicates()
#permutation_list = df[['Lag_ms','uAmps']].drop_duplicates()
print(permutation_list)
#permutation_list = permutation_list.sort_values(by = ['uAmps'])
permutation_list = permutation_list.sort_values(by = ['Lag_ms'])
dfdir = getDirectionERP(df, 1)
print (dfdir)
print("...............")

### Treatmenet IL->BLA
df1 = dfdir.loc[(dfdir['Treatment'] == 1)]
ax1 = createSubPlot('Treatment: IL->BLA\nERPs IL->BLA')
permutation_list = permutation_list.sort_values(by = ['Lag_ms'])
for tup in permutation_list.itertuples(index=False):
        # Get data for permutation
    tempdf = df1.loc[(df1.uAmps == tup[0]) & (df1.Lag_ms == tup[1])]
    if not tempdf.empty:
        createPlot(tempdf, ax1, str(tup[0]) + ' uA-' + str(tup[1]) + ' ms')


### Treatment BLA->IL
df1 = dfdir.loc[(dfdir['Treatment'] == 2)]
ax2 = createSubPlot('Treatment: BLA->IL\nERPs IL->BLA')
permutation_list = permutation_list.sort_values(by = ['Lag_ms'])
for tup in permutation_list.itertuples(index=False):
        # Get data for permutation
    tempdf = df1.loc[(df1.uAmps == tup[0]) & (df1.Lag_ms == tup[1])]
    if not tempdf.empty:
        createPlot(tempdf, ax2, str(tup[0]) + ' uA-' + str(tup[1]) + ' ms')


"""
Plotting BLA->IL
"""
dfdir = getDirectionERP(df, 2)

### Treatment IL->BLA
df1 = dfdir.loc[(dfdir['Treatment'] == 1)]
ax3 = createSubPlot('Treatment: IL->BLA\nERPs BLA->IL')
permutation_list = permutation_list.sort_values(by = ['Lag_ms'])
for tup in permutation_list.itertuples(index=False):
        # Get data for permutation
    tempdf = df1.loc[(df1.uAmps == tup[0]) & (df1.Lag_ms == tup[1])]
    if not tempdf.empty:
        createPlot(tempdf, ax3, str(tup[0]) + ' uA-' + str(tup[1]) + ' ms')


### Treatment BLA->IL
df1 = dfdir.loc[(dfdir['Treatment'] == 2)]
ax4 = createSubPlot('Treatment: BLA->IL\nERPs BLA->IL')
permutation_list = permutation_list.sort_values(by = ['Lag_ms'])
for tup in permutation_list.itertuples(index=False):
        # Get data for permutation
    tempdf = df1.loc[(df1.uAmps == tup[0]) & (df1.Lag_ms == tup[1])]
    if not tempdf.empty:
        createPlot(tempdf, ax4, str(tup[0]) + ' uA-' + str(tup[1]) + ' ms')


plt.show()


