import pandas as pd
import matplotlib.pyplot as plt

def createPlot(df, tup, ax):
    # Get data for permutation
    tempdf = df.loc[(df.uAmps == tup[0]) & (df.Lag_ms == tup[1])]
    # Get mean
    tempy = tempdf.groupby(['ERP Time']).mean()
    # Add pre and sort
    tempy = tempy.reset_index()
    print(tempy)
    predf = pd.DataFrame([['Pre',0]], columns=['ERP Time', 'ERPs'])
    tempy = tempy.append(predf)
    tempy = tempy.iloc[::-1] # Reverse order
    
    # Plot if data
    # Note: tup[0] = uAmps, tup[1] = ms Lag
    if len(tempy.index) > 1:
        if tup[0] == 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = 'SHAM',style='k^-')
##        else:
##            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='o-')
        elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label =str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='rv-') #
##        elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
##            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='ro-')
        elif tempy.Lag_ms[1] == 0 and tempy.uAmps[1] == 200: # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='rs-')
            
        elif tempy.Lag_ms[1] == 20 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='gv-') #
        elif tempy.Lag_ms[1] == 20 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='go-')
        elif tempy.Lag_ms[1] == 200 and tempy.uAmps[1] == 200: # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='gs-')
            
        elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 50 : # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='bv-') #
        elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 100 : # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='bo-')
        elif tempy.Lag_ms[1] == 100 and tempy.uAmps[1] == 200: # && tup[1] = 0:
            tempy.plot(x = 'ERP Time', y= 'ERPs', ax=ax, label = str(tup[0]) + ' uA-' + str(tup[1]) + ' ms',style='bs-')
        plt.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_visible(True)
    ax.set_ylim(-100,250)

def createSubPlot(title):
    fig, ax = plt.subplots(1, 1)
    ax.set_title(title)
    ax.set_ylabel('% Change in ERP from baseline')
    ax.set_xlabel('ERP Time Post Treatment')
    return ax

def getDirectionERP(df, dir):
    # create list of options
    erptimlist = ['POST_5-' + str(dir), 'POST_30-' + str(dir), 'POST24HR-' + str(dir)]
    # pick out directions
    tempdf = df.loc[df['ERP Time'].isin(erptimlist)]
    # remove extra chars ('-2/-1')
    tempdf['ERP Time'] = tempdf['ERP Time'].map(lambda x: x[:-2])
    print("tempdf: ",tempdf)
    return tempdf

"""
Plotting ERPS IL->BLA
"""
#df = pd.read_csv(r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPS_CALC_LONG_FORM-50 and 100.csv', skiprows = 2)
#df = pd.read_csv(r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPS_CALC_LONG_FORM.csv', skiprows = 2)
#df = pd.read_csv(r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPs_PERC_CHG_Long_Form.csv', skiprows = 0)
df = pd.read_csv(r'E:\py-behav-box\BehGUI\DATA\SUMMARY_ERPs_PERC_CHG_Long_Form.csv', skiprows = 0)

perm_list = df[['uAmps','Lag_ms']].drop_duplicates()

df1dir = getDirectionERP(df, 1)
df2dir = getDirectionERP(df, 2)

################### Same direction vs Opposite direction ###################
ax1 = createSubPlot('Treatment and ERPs in same direction')
dfSame = df1dir.loc[(df1dir['Treatment'] == 1)] #'IL->BLA'
dfSame = dfSame.append(df2dir.loc[(df2dir['Treatment'] == 1)])
print("dfSame: ")
print(dfSame)
for tup in perm_list.itertuples(index= False): #leave out index
    createPlot(dfSame, tup, ax1)

print('----------------')
ax2 = createSubPlot('Treatment and ERPs in oposite directions')
dfAnti = df1dir.loc[(df1dir['Treatment'] == 2)] #'BLA-IL'
dfAnti = dfAnti.append(df2dir.loc[(df2dir['Treatment'] == 2)])
print("dfOpposite: ")
print(dfAnti)
for tup in perm_list.itertuples(index= False):
    createPlot(dfAnti, tup, ax2)



'''
################### Four Sep Plots ###################
### Treatmenet IL->BLA
df1 = dfdir.loc[(dfdir['Treatment'] == 1)]
ax1 = createSubPlot('Treatment: IL->BLA\nERPs IL->BLA')
for tup in perm_list.itertuples(index=False):
    createPlot(df1, tup, ax1)


### Treatment BLA->IL
df1 = dfdir.loc[(dfdir['Treatment'] == 2)]
ax2 = createSubPlot('Treatment: BLA->IL\nERPs IL->BLA')
for tup in perm_list.itertuples(index=False):
    createPlot(df1, tup, ax2)


"""
Plotting BLA->IL
"""
dfdir = getDirectionERP(df, 2)

### Treatment IL->BLA
df1 = dfdir.loc[(dfdir['Treatment'] == 1)]
ax3 = createSubPlot('Treatment: IL->BLA\nERPs BLA->IL')
for tup in perm_list.itertuples(index=False):
    createPlot(df1, tup, ax3)


### Treatment BLA->IL
df1 = dfdir.loc[(dfdir['Treatment'] == 2)]
ax4 = createSubPlot('Treatment: BLA->IL\nERPs BLA->IL')
for tup in perm_list.itertuples(index=False):
    createPlot(df1, tup, ax4)
'''

plt.show()


