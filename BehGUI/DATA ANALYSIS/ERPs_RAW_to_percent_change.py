import pandas as pd
#### Go down to bottom to change paths

# IL->BLA = 1
# BLA->IL = 2
def rawToLongForm(path, outPath):
    # Load file
    df = pd.read_csv(path, skiprows=1)
    #df = df.dropna() # Drops row with NaN  # Note: most notes colums do not have any entries

    row_list = []
    treatment = 0
    curPre1 = 0
    curPre2 = 0
    for index, row in df.iterrows():
        #print(row)
        if 'PRE_ERP' in row['ERP_TIMING']:
            curPre1 = row['ERP_IL-BLA']
            curPre2 = row['ERP_BLA-IL']
            if "IL->BLA" in row['Treatment']: #IL->BLA = 1
                treatment = 1
            elif "BLA->IL" in row['Treatment']: #BLA->IL = 2
                treatment = 2
            else:
                print("No treatment!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print (row)
        elif 'POST__5' in row['ERP_TIMING']:
            percentChange1 = (row['ERP_IL-BLA'] - curPre1 ) / curPre1 * 100
            percentChange2 = (row['ERP_BLA-IL'] - curPre2 ) / curPre2 * 100
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST_5-1', 'ERPs' : percentChange1})
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST_5-2', 'ERPs' : percentChange2})
            
        elif 'POST_30' in row['ERP_TIMING']:
            percentChange1 = (row['ERP_IL-BLA'] - curPre1 ) / curPre1 * 100
            percentChange2 = (row['ERP_BLA-IL'] - curPre2 ) / curPre2 * 100
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST_30-1', 'ERPs' : percentChange1})
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST_30-2', 'ERPs' : percentChange2})
            
        elif 'POST24H' in row['ERP_TIMING']:
            percentChange1 = (row['ERP_IL-BLA'] - curPre1 ) / curPre1 * 100
            percentChange2 = (row['ERP_BLA-IL'] - curPre2 ) / curPre2 * 100
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST24HR-1', 'ERPs' : percentChange1})
            row_list.append({'Date' : row['Date'], 'Time' : row[' Time'], 'RAT' : row[' RAT'], 'uAmps' : row['uAmps'], 'Lag_ms' : row['Lag_ms'], 'Treatment' : treatment, 'ERP Time' : 'POST24HR-2', 'ERPs' : percentChange2})  
    
    dfOut = pd.DataFrame(row_list)
    dfOut.to_csv(outPath)
    print("DONE!")
    print("New long-form file with % change in ERPs is: ",outPath)

if __name__ == "__main__":
    ## Change me! ##
    #path = r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPs_RAW.csv'
    #outPath = r'G:\Shared drives\TNEL - UMN\Project related material\PLASTICITY\Plasticity\DATA ANALYSIS\SUMMARY_ERPs_PERC_CHG_Long_Form.csv'
    path = r'E:\py-behav-box\BehGUI\DATA\SUMMARY_ERPs_RAW.csv'
    outPath = r'E:\py-behav-box\BehGUI\DATA\SUMMARY_ERPs_PERC_CHG_Long_Form.csv'

    ################
    rawToLongForm(path, outPath)
