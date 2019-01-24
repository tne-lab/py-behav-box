# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:21:44 2018

@author: aerei
"""
import numpy as np
import pandas as pd
import os
os.chdir("D:/UMN rats GS4")
SS = pd.read_csv("test1_umn2019.csv")#1
#SS = pd.read_csv("05222018_P45_S10-S15.csv")#2
#SS = pd.read_csv("05232018_P46_S10-S15.csv")#3
#SS = pd.read_csv("05242018_P47_S10-S15.csv")#4
#SS = pd.read_csv("05302018_P45_S10-S15.csv")#5
#SS = pd.read_csv("05312018_P46_S10-S15.csv")#6
#SS = pd.read_csv("06012018_P47_S10-S15.csv")#7
#SS = pd.read_csv("06302018_P46_S10-S15.csv")#8
#SS = pd.read_csv("07012018_P47_S10-S15.csv")#9
#SS = pd.read_csv("07032018_P44_S10-S15.csv")#10
#SS = pd.read_csv("07042018_P45_S10-S15.csv")#11
#SS = pd.read_csv("07052018_P46_S10-S15.csv")#12
#SS = pd.read_csv("07082018_P47_S10-S15.csv")#13
#SS = pd.read_csv("07092018_P44_S10-S15.csv")#14
#SS = pd.read_csv("07102018_P45_S10-S15.csv")#15
#SS = pd.read_csv("07122018_P46_S10-S15.csv")#16
#SS = pd.read_csv("07132018_P47_S10-S15.csv")#17
#SS = pd.read_csv("18.csv")

SS["Time_in_sec"] = SS["Time"] # new column transforming graphicstate unities in seconds
SS["RTmask"] = SS["Time_in_sec"].diff() # new column which subtract rows values from previous row

SS["Protocol"] = SS["Protocol"].astype("category")
SS["Session"] = SS["Session"].astype("category")
SS["Station"] = SS["Station"].astype("category")
SS["Run"] = SS["Run"].astype("category")
SS["Project"] = SS["Project"].astype("category")
SS["UserID"] = SS["UserID"].astype("category")
SS["Subject"] = SS["Subject"].astype("category")
# SS["Current State"] = SS["Current State"].astype("category")
# SS["A1 - Rear NP"] = SS["A1 - Rear NP"].astype("category") # IF going to sum, average, etc, do not change to category
# SS["A2 - Front NP"] = SS["A2 - Front NP"].astype("category")
# SS["A3 - MIddle NP"] = SS["A3 - MIddle NP"].astype("category")
# SS["A4 - "] = SS["A4 - "].astype("category")
SS["A[1] Rear"] = SS["Rear"].astype("category")
SS["A[2] Front"] = SS["Front"].astype("category")
SS["A[3] Middle NP"] = SS["Middle"].astype("category")
SS["A[4] "] = SS["Manual Switch"].astype("category")

ProtocolN = SS["Protocol"].iloc[0] # define that the first value on the Protocol column will be the variable ProtocolN
if ProtocolN == 44: #check if the protocol number is 82 or 83 and classify the tasks accordinly
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)),
        (SS["Current State"].between(83, 113)),
        (SS["Current State"].between(114, 144)),
        (SS["Current State"].between(145, 175)),
        (SS["Current State"].between(176, 206)),
        (SS["Current State"].between(207, 237)),
        (SS["Current State"].between(238, 268)),
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = ["Rand1", "Side1", "Light1", "Side2", "Light2", "Side3", "Light3", "Side4", "Light4", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
elif ProtocolN == 45:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)), #Side3
        (SS["Current State"].between(83, 113)), #Light4
        (SS["Current State"].between(114, 144)), #Side4
        (SS["Current State"].between(145, 175)),#Light
        (SS["Current State"].between(176, 206)), #Side1
        (SS["Current State"].between(207, 237)), #Light2
        (SS["Current State"].between(238, 268)), #Side2
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = ["Rand1", "Side3", "Light4", "Side4", "Light1", "Side1", "Light2", "Side2", "Light3", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
elif ProtocolN == 46:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)), #Side2
        (SS["Current State"].between(83, 113)), #Light2
        (SS["Current State"].between(114, 144)), #Side3
        (SS["Current State"].between(145, 175)), #Light3
        (SS["Current State"].between(176, 206)), #Side4
        (SS["Current State"].between(207, 237)), #Light4
        (SS["Current State"].between(238, 268)), #Side1
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = ["Rand1", "Side2", "Light2", "Side3", "Light3", "Side4", "Light4", "Side1", "Light1", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
else:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)), #Side4
        (SS["Current State"].between(83, 113)), #Light1
        (SS["Current State"].between(114, 144)), #Side1
        (SS["Current State"].between(145, 175)), #Light2
        (SS["Current State"].between(176, 206)), #Side2
        (SS["Current State"].between(207, 237)), #Light3
        (SS["Current State"].between(238, 268)), #Side3
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = ["Rand1", "Side4", "Light1", "Side1", "Light2", "Side2", "Light3", "Side3", "Light4", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    
conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)),
        (SS["Current State"].between(83, 113)),
        (SS["Current State"].between(114, 144)),
        (SS["Current State"].between(145, 175)),
        (SS["Current State"].between(176, 206)),
        (SS["Current State"].between(207, 237)),
        (SS["Current State"].between(238, 268)),
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
choices = ["Random", "Side", "Light", "Side", "Light", "Side", "Light", "Side", "Light", "Random"]
SS["Task_Type"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
 
    
if ProtocolN == 44: #check if the protocol number is 82 or 83 and classify the tasks accordinly
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)),
        (SS["Current State"].between(83, 113)),
        (SS["Current State"].between(114, 144)),
        (SS["Current State"].between(145, 175)),
        (SS["Current State"].between(176, 206)),
        (SS["Current State"].between(207, 237)),
        (SS["Current State"].between(238, 268)),
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
elif ProtocolN == 45:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(145, 175)),#Light
        (SS["Current State"].between(176, 206)), #Side1
        (SS["Current State"].between(207, 237)), #Light2
        (SS["Current State"].between(238, 268)), #Side2
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(51, 82)), #Side3
        (SS["Current State"].between(83, 113)), #Light4
        (SS["Current State"].between(114, 144)), #Side4
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
elif ProtocolN == 46:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(238, 268)), #Side1
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(51, 82)), #Side2
        (SS["Current State"].between(83, 113)), #Light2
        (SS["Current State"].between(114, 144)), #Side3
        (SS["Current State"].between(145, 175)), #Light3
        (SS["Current State"].between(176, 206)), #Side4
        (SS["Current State"].between(207, 237)), #Light4
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
else:
    conditions = [
        (SS["Current State"] < 51),
        (SS["Current State"].between(51, 82)), #Side4
        (SS["Current State"].between(83, 113)), #Light1
        (SS["Current State"].between(114, 144)), #Side1
        (SS["Current State"].between(145, 175)), #Light2
        (SS["Current State"].between(176, 206)), #Side2
        (SS["Current State"].between(207, 237)), #Light3
        (SS["Current State"].between(238, 268)), #Side3
        (SS["Current State"].between(295, 324)) | (SS["Current State"] == 269),
        (SS["Current State"].between(270, 295)) | (SS["Current State"] == 325)]
    choices = [1, 9, 2, 3, 4, 5, 6, 7, 8, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
  
    
trial1 = [54, 86, 117, 148, 179, 210, 241, 297]
trial2 = [61, 92, 123, 154, 185, 216, 247, 303]
trial3 = [67, 98, 129, 160, 191, 222, 253, 309]
trial4 = [73, 104, 135, 166, 197, 228, 259, 315]
trial5 = [79 , 110, 141, 172, 203, 234, 265, 321]

def trial_number(row):
    ID = row[8]
    
    if ID in trial1:
        return 1
    elif ID in trial2:
        return 2
    elif ID in trial3:
        return 3
    elif ID in trial4:
        return 4
    elif ID in trial5:
        return 5
    else:
        return 0
    
SS["Trial_ID"] = SS.apply(trial_number, axis = "columns")
SS.apply(trial_number, axis = "columns")

np_regressive = [79, 110, 141, 172, 203, 234, 265, 321]
np_perseverative = [54, 61, 67, 73, 86, 92, 98, 104, 117, 123, 129, 135, 148, 154, 160, 166, 179, 185, 191, 197, 210, 216, 222, 228, 241, 247, 253, 259, 297, 303, 309, 315]
 
def trial_perse(row):
     ID = row[8]
     
     if ID in np_regressive:
         return 1000
     elif ID in np_perseverative:
         return 1
     else:
         return 0
    
SS["perseverative_or_regressive"] = SS.apply(trial_perse, axis = "columns")
SS.apply(trial_perse, axis = "columns")

#SS2 = SS[SS["Subject"] == "SS2___"] # filters to select only "SS2" cells
#SS3 = SS[SS["Subject"] == "SS3___"] 
#SS4 = SS[SS["Subject"] == "SS4___"]
#S1 = SS[SS["Subject"] == "S1____"]
#S2 = SS[SS["Subject"] == "S2____"]
#S3 = SS[SS["Subject"] == "S3____"]
#S7 = SS[SS["Subject"] == "S7____"]

#SS2.iat[0,20] = 0 # overwrites the first value of RT column (which is NAN or a wrong number
#SS3.iat[0,20] = 0
#SS4.iat[0,20] = 0
#S1.iat[0,20] = 0
#S2.iat[0,20] = 0
#S3.iat[0,20] = 0
#S7.iat[0,20] = 0

#Subject_SS2 = SS["Subject"] == "SS2___"
#Subject_SS3 = SS["Subject"] == "SS3___"
#Subject_SS4 = SS["Subject"] == "SS4___"
#Subject_S1 = SS["Subject"] == "S1____"
#Subject_S2 = SS["Subject"] == "S2____"
#Subject_S3 = SS["Subject"] == "S3____"
#Subject_S7 = SS["Subject"] == "S7____"

if "S10___" in SS["Subject"].values:
    S10 = SS[SS["Subject"] == "S10___"]
    S10.iat[0,20] = 0
    Subject_S10 = SS["Subject"] == "S10___"
    
if "S12___" in SS["Subject"].values:
    S12 = SS[SS["Subject"] == "S12___"]
    S12.iat[0,20] = 0
#    S12.iat[0,21] = 0
    Subject_S12 = SS["Subject"] == "S12___"
    
if "S13___" in SS["Subject"].values:
    S13 = SS[SS["Subject"] == "S13___"]
    S13.iat[0,20] = 0
    Subject_S13 = SS["Subject"] == "S13___"

if "S14___" in SS["Subject"].values:
    S14 = SS[SS["Subject"] == "S14___"]
    S14.iat[0,20] = 0
    Subject_S14 = SS["Subject"] == "S14___"
    
if "S15___" in SS["Subject"].values:
    S15 = SS[SS["Subject"] == "S15___"]
    S15.iat[0,20] = 0
    Subject_S15 = SS["Subject"] == "S15___"

if "REV5__" in SS["Subject"].values:
    REV5 = SS[SS["Subject"] == "REV5__"]
    REV5.iat[0,20] = 0
    Subject_REV5 = SS["Subject"] == "REV5__"
    
if "REV6__" in SS["Subject"].values:
    REV6 = SS[SS["Subject"] == "REV6__"]
    REV6.iat[0,20] = 0
    Subject_REV6 = SS["Subject"] == "REV6__"

if "REV7__" in SS["Subject"].values:
    REV7 = SS[SS["Subject"] == "REV7__"]
    REV7.iat[0,20] = 0
    Subject_REV7 = SS["Subject"] == "REV7__"
    
if "S16" in SS["Subject"].values:
    S16 = SS[SS["Subject"] == "S16"]
    S16.iat[0,20] = 0
    Subject_S16 = SS["Subject"] == "S16"

if "S17" in SS["Subject"].values:
    S17 = SS[SS["Subject"] == "S17"]
    S17.iat[0,20] = 0
    Subject_S17 = SS["Subject"] == "S17"
    
if "S18" in SS["Subject"].values:
    S18 = SS[SS["Subject"] == "S18"]
    S18.iat[0,20] = 0
    Subject_S18 = SS["Subject"] == "S18"

if "S19" in SS["Subject"].values:
    S19 = SS[SS["Subject"] == "S19"]
    S19.iat[0,20] = 0
    Subject_S19 = SS["Subject"] == "S16"

if "S20" in SS["Subject"].values:
    S20 = SS[SS["Subject"] == "S20"]
    S20.iat[0,20] = 0
    Subject_S20 = SS["Subject"] == "S20"
    
if ProtocolN == 44:
    Task1 = SS["Current State"] < 51
    Task2 = SS["Current State"].between(51, 82)
    Task3 = SS["Current State"].between(83, 113)
    Task4 = SS["Current State"].between(114, 144)
    Task5 = SS["Current State"].between(145, 175)
    Task6 = SS["Current State"].between(176, 206)
    Task7 = SS["Current State"].between(207, 237)
    Task8 = SS["Current State"].between(238, 268) 
    Task9 = SS["Current State"].between(295, 324) & (SS["Current State"] == 269)
    Task10 = SS["Current State"].between(270, 295) & (SS["Current State"] == 270)
elif ProtocolN == 45:
    Task1 = SS["Current State"] < 51
    Task5 = SS["Current State"].between(51, 82)
    Task6 = SS["Current State"].between(83, 113)
    Task7 = SS["Current State"].between(114, 144)
    Task8 = SS["Current State"].between(145, 175)
    Task9 = SS["Current State"].between(176, 206)
    Task2 = SS["Current State"].between(207, 237)
    Task3 = SS["Current State"].between(238, 268) 
    Task4 = SS["Current State"].between(295, 324) & (SS["Current State"] == 269)
    Task10 = SS["Current State"].between(270, 295) & (SS["Current State"] == 270)
elif ProtocolN == 46:
    Task1 = SS["Current State"] < 51
    Task8 = SS["Current State"].between(51, 82)
    Task9 = SS["Current State"].between(83, 113)
    Task2 = SS["Current State"].between(114, 144)
    Task3 = SS["Current State"].between(145, 175)
    Task4 = SS["Current State"].between(176, 206)
    Task5 = SS["Current State"].between(207, 237)
    Task6 = SS["Current State"].between(238, 268) 
    Task7 = SS["Current State"].between(295, 324) & (SS["Current State"] == 269)
    Task10 = SS["Current State"].between(270, 295) & (SS["Current State"] == 270)
elif ProtocolN == 47:
    Task1 = SS["Current State"] < 51
    Task3 = SS["Current State"].between(51, 82)
    Task4 = SS["Current State"].between(83, 113)
    Task5 = SS["Current State"].between(114, 144)
    Task6 = SS["Current State"].between(145, 175)
    Task7 = SS["Current State"].between(176, 206)
    Task8 = SS["Current State"].between(207, 237)
    Task9 = SS["Current State"].between(238, 268) 
    Task2 = SS["Current State"].between(295, 324) & (SS["Current State"] == 269)
    Task10 = SS["Current State"].between(270, 295) & (SS["Current State"] == 270)
    

    




    
#SS2 = SS.query("Subject == 'SS2___'")
#SS3 = SS.query("Subject == 'SS3___'")
#SS4 = SS.query("Subject == 'SS4___'")
#S1 = SS.query("Subject == 'S1____'")
#S2 = SS.query("Subject == 'S2____'")
#S3 = SS.query("Subject == 'S3____'")
#S7 = SS.query("Subject == 'S7____'")
#S10 = SS.query("Subject == 'S10___'")

#Definir os estates
npchoice = [54, 61, 67, 73, 79, 86, 92, 98, 104, 110, 117, 123, 129, 135, 141, 148, 154, 160, 166, 172, 179, 185, 191, 197, 203, 210, 216, 222, 228, 234, 241, 247, 253, 259, 265, 297, 303, 309, 315, 321]
right_choice = [55, 62, 68, 74, 80, 87, 93, 99, 105, 111, 118, 124, 130, 136, 142, 149, 155, 161, 167, 173, 180, 186, 192, 198, 204, 211, 217, 223, 229, 235, 242, 248, 254, 260, 266, 298, 304, 310, 316, 322]
error = [57, 64, 70, 76, 82, 89, 95, 101, 107, 113, 120, 126, 132, 138, 144, 151, 157, 163, 169, 175, 182, 188, 194, 200, 206, 213, 219, 225, 231, 237, 244, 250, 256, 262, 268, 300, 306, 312, 318, 324]
omission = [52, 84, 115, 146, 177, 208, 239, 295]

random1_npchoice = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
random1_response = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]
random2_npchoice = [271, 276, 281, 286, 291]
random2_response = [272, 277, 282, 287, 292]

if ProtocolN == 44:
    npchoice_conflict = [86, 98, 104, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [92, 110, 123, 135, 154, 160, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [54, 61, 67, 73, 79]
elif ProtocolN == 45:
    npchoice_conflict = [54, 67, 86, 98, 104, 117, 129, 141, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 92, 110, 123, 135, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [148, 154, 160, 166, 172]
elif ProtocolN == 46:
    npchoice_conflict = [54, 67, 86, 98, 104, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 92, 110, 123, 135, 154, 160, 191, 197, 222, 234, 303, 309]
    npchoice_set = [241, 247, 253, 259, 265]
elif ProtocolN == 47:
    npchoice_conflict = [54, 67, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 123, 135, 154, 160, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [86, 92, 98, 104, 110]

def trial(row):
    ID = row[9]
    ID_for_omission = row[8]
    
    if ID in npchoice:
        return "trial_start"
    elif ID in right_choice:
        return "correct"
    elif ID in error:
        return "incorrect"
    elif ID in omission and ID_for_omission in npchoice:
        return "omission"
    elif ID in random1_npchoice:
        return "trial_start"
    elif ID in random1_response:
        return "correct_random1"
    elif ID in random2_npchoice:
        return "trial_start"
    elif ID in random2_response:
        return "correct_random2"
    else:
        return ""


#SS2["Trial"] = SS2.apply(trial, axis = "columns")    
#SS2.apply(trial, axis = "columns")
#SS3["Trial"] = SS3.apply(trial, axis = "columns")    
#SS3.apply(trial, axis = "columns")
#SS4["Trial"] = SS4.apply(trial, axis = "columns")    
# SS4.apply(trial, axis = "columns")
# S1["Trial"] = S1.apply(trial, axis = "columns")    
# S1.apply(trial, axis = "columns")
# S2["Trial"] = S2.apply(trial, axis = "columns")    
# S2.apply(trial, axis = "columns")
# S3["Trial"] = S3.apply(trial, axis = "columns")    
# S3.apply(trial, axis = "columns")
# S7["Trial"] = S7.apply(trial, axis = "columns")    
# S7.apply(trial, axis = "columns")
if "S10___" in SS["Subject"].values:
    S10["Trial"] = S10.apply(trial, axis = "columns")    
    S10.apply(trial, axis = "columns")

if "S12___" in SS["Subject"].values:   
    S12["Trial"] = S12.apply(trial, axis = "columns")    
    S12.apply(trial, axis = "columns")

if "S13___" in SS["Subject"].values:
    S13["Trial"] = S13.apply(trial, axis = "columns")    
    S13.apply(trial, axis = "columns")
    
if "S14___" in SS["Subject"].values:
    S14["Trial"] = S14.apply(trial, axis = "columns")    
    S14.apply(trial, axis = "columns")
    
if "S15___" in SS["Subject"].values:
    S15["Trial"] = S15.apply(trial, axis = "columns")    
    S15.apply(trial, axis = "columns")
    
if "REV5__" in SS["Subject"].values:
    REV5["Trial"] = REV5.apply(trial, axis = "columns")    
    REV5.apply(trial, axis = "columns")

if "REV6__" in SS["Subject"].values:
    REV6["Trial"] = REV6.apply(trial, axis = "columns")    
    REV6.apply(trial, axis = "columns")
    
if "REV7__" in SS["Subject"].values:
    REV7["Trial"] = REV7.apply(trial, axis = "columns")    
    REV7.apply(trial, axis = "columns")
    
if "S16" in SS["Subject"].values:
    S16["Trial"] = S16.apply(trial, axis = "columns")    
    S16.apply(trial, axis = "columns")

if "S17" in SS["Subject"].values:
    S17["Trial"] = S17.apply(trial, axis = "columns")    
    S17.apply(trial, axis = "columns")

if "S18" in SS["Subject"].values:
    S18["Trial"] = S18.apply(trial, axis = "columns")    
    S18.apply(trial, axis = "columns")

if "S19" in SS["Subject"].values:
    S19["Trial"] = S19.apply(trial, axis = "columns")    
    S19.apply(trial, axis = "columns")

if "S20" in SS["Subject"].values:
    S20["Trial"] = S20.apply(trial, axis = "columns")    
    S20.apply(trial, axis = "columns")

# OLD NOT FUNCTIONING =============================================================================
def conf(row):
    ID = row[8]
     
    if ID in npchoice_conflict:
         return "conf"
    elif ID in npchoice_NONconflict:
         return "non_conf"
    elif ID in npchoice_set:
         return "set"
    elif ID in random1_npchoice:
         return "random1"
    elif ID in random2_npchoice:
         return "random2"
    else:
         return ""


# NEW =============================================================================
#def conf(row):
#    ID = row[8]
#    Task_number= row [23]
#     
#    if ID in npchoice_conflict:
#        return "conf"
#    elif ID in npchoice_NONconflict:
#        return "non_conf"
#    elif ID in npchoice_set and Task_number == 1:
#        return "set"
#    elif ID in random1_npchoice:
#        return "random1"
#    elif ID in random2_npchoice:
#        return "random2"
#    else:
#         return ""
# =============================================================================

# SS2["Conf"] = SS2.apply(conf, axis = "columns")
# SS2.apply(conf, axis = "columns")
# SS3["Conf"] = SS3.apply(conf, axis = "columns")
# SS3.apply(conf, axis = "columns")
# SS4["Conf"] = SS4.apply(conf, axis = "columns")
# SS4.apply(conf, axis = "columns")
# S1["Conf"] = S1.apply(conf, axis = "columns")
# S1.apply(conf, axis = "columns")
# S2["Conf"] = S2.apply(conf, axis = "columns")
# S2.apply(conf, axis = "columns")
# S3["Conf"] = S3.apply(conf, axis = "columns")
# S3.apply(conf, axis = "columns")
# S7["Conf"] = S7.apply(conf, axis = "columns")
# S7.apply(conf, axis = "columns")
         
     
if "S10___" in SS["Subject"].values:
    S10["Conf"] = S10.apply(conf, axis = "columns")
    S10.apply(conf, axis = "columns")
    S10["Trial"].replace("", np.nan, inplace = True)
    S10.dropna(subset = ["Trial"], inplace = True)
    S10 = S10.reset_index(drop=True)
    S10["RT"] = S10["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S10RT = S10[S10["Trial"] != "trial_start"]
    S10RT = S10RT.reset_index(drop=True)
    S10RT["Trial_Number"]= range(1, len(S10RT) +1)
    S10RT["cumsum"] = S10RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S10RT["Task_Order"] = S10RT["Task_Order"].astype("int")
    S10RT["cumsum"] = S10RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S10RT["Error_Type"] = S10RT.apply(perse, axis = "columns")
    S10RT.apply(perse, axis = "columns")
    
    
if "S12___" in SS["Subject"].values:
    S12["Conf"] = S12.apply(conf, axis = "columns")
    S12.apply(conf, axis = "columns")
    S12["Trial"].replace("", np.nan, inplace = True)
    S12.dropna(subset = ["Trial"], inplace = True)
    S12 = S12.reset_index(drop=True)
    S12["RT"] = S12["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S12RT = S12[S12["Trial"] != "trial_start"]
    S12RT = S12RT.reset_index(drop=True)
    S12RT["Trial_Number"]= range(1, len(S12RT) +1)
#    S12RT["new"] = S12RT["mask_perseverative_or_regressive"].cumsum()
    S12RT["cumsum"] = S12RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S12RT["Task_Order"] = S12RT["Task_Order"].astype("int")
    S12RT["cumsum"] = S12RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S12RT["Error_Type"] = S12RT.apply(perse, axis = "columns")
    S12RT.apply(perse, axis = "columns")
#    def newconf(row):
#        askorder = row[23]
#        correctness = row[26]
#        cumsum = row[30]
#        oldconf
        
    
if "S13___" in SS["Subject"].values:
    S13["Conf"] = S13.apply(conf, axis = "columns")
    S13.apply(conf, axis = "columns")
    S13["Trial"].replace("", np.nan, inplace = True)
    S13.dropna(subset = ["Trial"], inplace = True)
    S13 = S13.reset_index(drop=True)
    S13["RT"] = S13["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S13RT = S13[S13["Trial"] != "trial_start"]
    S13RT = S13RT.reset_index(drop=True)
    S13RT["Trial_Number"]= range(1, len(S13RT) +1)
    S13RT["cumsum"] = S13RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S13RT["Task_Order"] = S13RT["Task_Order"].astype("int")
    S13RT["cumsum"] = S13RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S13RT["Error_Type"] = S13RT.apply(perse, axis = "columns")
    S13RT.apply(perse, axis = "columns")

if "S14___" in SS["Subject"].values:
    S14["Conf"] = S14.apply(conf, axis = "columns")
    S14.apply(conf, axis = "columns")
    S14["Trial"].replace("", np.nan, inplace = True)
    S14.dropna(subset = ["Trial"], inplace = True)
    S14 = S14.reset_index(drop=True)
    S14["RT"] = S14["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S14RT = S14[S14["Trial"] != "trial_start"]
    S14RT = S14RT.reset_index(drop=True)
    S14RT["Trial_Number"]= range(1, len(S14RT) +1)
    S14RT["cumsum"] = S14RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S14RT["Task_Order"] = S14RT["Task_Order"].astype("int")
    S14RT["cumsum"] = S14RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S14RT["Error_Type"] = S14RT.apply(perse, axis = "columns")
    S14RT.apply(perse, axis = "columns")
    
if "S15___" in SS["Subject"].values:
    S15["Conf"] = S15.apply(conf, axis = "columns")
    S15.apply(conf, axis = "columns")
    S15["Trial"].replace("", np.nan, inplace = True)
    S15.dropna(subset = ["Trial"], inplace = True)
    S15 = S15.reset_index(drop=True)
    S15["RT"] = S15["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S15RT = S15[S15["Trial"] != "trial_start"]
    S15RT = S15RT.reset_index(drop=True)
    S15RT["Trial_Number"]= range(1, len(S15RT) +1)
    S15RT["cumsum"] = S15RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S15RT["Task_Order"] = S15RT["Task_Order"].astype("int")
    S15RT["cumsum"] = S15RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S15RT["Error_Type"] = S15RT.apply(perse, axis = "columns")
    S15RT.apply(perse, axis = "columns")

if "REV5__" in SS["Subject"].values:
    REV5["Conf"] = REV5.apply(conf, axis = "columns")
    REV5.apply(conf, axis = "columns")
    REV5["Trial"].replace("", np.nan, inplace = True)
    REV5.dropna(subset = ["Trial"], inplace = True)
    REV5 = REV5.reset_index(drop=True)
    REV5["RT"] = REV5["Time_in_sec"].diff() # new column which subtract rows values from previous row
    REV5RT = REV5[REV5["Trial"] != "trial_start"]
    REV5RT = REV5RT.reset_index(drop=True)
    REV5RT["Trial_Number"]= range(1, len(REV5RT) +1)
    REV5RT["cumsum"] = REV5RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    REV5RT["Task_Order"] = REV5RT["Task_Order"].astype("int")
    REV5RT["cumsum"] = REV5RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    REV5RT["Error_Type"] = REV5RT.apply(perse, axis = "columns")
    REV5RT.apply(perse, axis = "columns")

if "REV6__" in SS["Subject"].values:
    REV6["Conf"] = REV6.apply(conf, axis = "columns")
    REV6.apply(conf, axis = "columns")
    REV6["Trial"].replace("", np.nan, inplace = True)
    REV6.dropna(subset = ["Trial"], inplace = True)
    REV6 = REV6.reset_index(drop=True)
    REV6["RT"] = REV6["Time_in_sec"].diff() # new column which subtract rows values from previous row
    REV6RT = REV6[REV6["Trial"] != "trial_start"]
    REV6RT = REV6RT.reset_index(drop=True)
    REV6RT["Trial_Number"]= range(1, len(REV6RT) +1)
    REV6RT["cumsum"] = REV6RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    REV6RT["Task_Order"] = REV6RT["Task_Order"].astype("int")
    REV6RT["cumsum"] = REV6RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    REV6RT["Error_Type"] = REV6RT.apply(perse, axis = "columns")
    REV6RT.apply(perse, axis = "columns")

if "REV7__" in SS["Subject"].values:
    REV7["Conf"] = REV7.apply(conf, axis = "columns")
    REV7.apply(conf, axis = "columns")
    REV7["Trial"].replace("", np.nan, inplace = True)
    REV7.dropna(subset = ["Trial"], inplace = True)
    REV7 = REV7.reset_index(drop=True)
    REV7["RT"] = REV7["Time_in_sec"].diff() # new column which subtract rows values from previous row
    REV7RT = REV7[REV7["Trial"] != "trial_start"]
    REV7RT = REV7RT.reset_index(drop=True)
    REV7RT["Trial_Number"]= range(1, len(REV7RT) +1)
    REV7RT["cumsum"] = REV7RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    REV7RT["Task_Order"] = REV7RT["Task_Order"].astype("int")
    REV7RT["cumsum"] = REV7RT["cumsum"].astype("int")
    def perse(row):
        random = row[22]
        taskorder = row[23]
        correctness = row[26]
        cumsum = row[30]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    REV7RT["Error_Type"] = REV7RT.apply(perse, axis = "columns")
    REV7RT.apply(perse, axis = "columns")
'''
if "S16" in SS["Subject"].values:
    S16["Conf"] = S16.apply(conf, axis = "columns")
    S16.apply(conf, axis = "columns")
    S16["Trial"].replace("", np.nan, inplace = True)
    S16.dropna(subset = ["Trial"], inplace = True)
    S16 = S16.reset_index(drop=True)
    S16["RT"] = S16["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S16RT = S16[S16["Trial"] != "trial_start"]
    S16RT = S16.reset_index(drop=True)
    S16RT["Trial_Number"]= range(1, len(S16RT) +1)
    S16RT["cumsum"] = S16RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S16RT["Task_Order"] = S16RT["Task_Order"].astype("int")
    S16RT["cumsum"] = S16RT["cumsum"].astype("int")
    def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S16RT["Error_Type"] = S16RT.apply(perse, axis = "columns")
    S16RT.apply(perse, axis = "columns")
'''
#for i in range(0,20):
   # subjectNumber = "S"+Str(ï)
    #if subjectNumber in SS["Subject"].values:
        
    

        
        
def createDataFrame(data):
    data["Conf"] = data.apply(conf, axis = "columns")
    data.apply(conf, axis = "columns")
    data["Trial"].replace("", np.nan, inplace = True)
    data.dropna(subset = ["Trial"], inplace = True)
    data = data.reset_index(drop=True)
    data["RT"] = data["Time_in_sec"].diff() # new column which subtract rows values from previous row
    
    dataRT = data[data["Trial"] != "trial_start"]
    dataRT = dataRT.reset_index(drop=True)
    dataRT["Trial_Number"]= range(1, len(dataRT) +1)
    dataRT["cumsum"] = dataRT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    dataRT["Task_Order"] = dataRT["Task_Order"].astype("int")
    dataRT["cumsum"] = dataRT["cumsum"].astype("int")
    dataRT["Error_Type"] = dataRT.apply(perse, axis = "columns")
    dataRT.apply(perse, axis = "columns")
    return data, dataRT

def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""

if "S17" in SS["Subject"].values:
    S17, S17RT = createDataFrame(S17)

 
'''
    ####################################################
#Repeat this if statement for all subjects!    
if "S17" in SS["Subject"].values:
    S17, S17RT = createDataFrame(S17)

def createDataFrame(data):
    data["Conf"] = data.apply(conf, axis = "columns")
    data.apply(conf, axis = "columns")
    data["Trial"].replace("", np.nan, inplace = True)
    data.dropna(subset = ["Trial"], inplace = True)
    data = data.reset_index(drop=True)
    data["RT"] = data["Time_in_sec"].diff() # new column which subtract rows values from previous row
    
    dataRT = data[data["Trial"] != "trial_start"]
    dataRT = dataRT.reset_index(drop=True)
    dataRT["Trial_Number"]= range(1, len(dataRT) +1)
    dataRT["cumsum"] = dataRT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    dataRT["Task_Order"] = dataRT["Task_Order"].astype("int")
    dataRT["cumsum"] = dataRT["cumsum"].astype("int")
    dataRT["Error_Type"] = dataRT.apply(perse, axis = "columns")
    dataRT.apply(perse, axis = "columns")
    return data, dataRT

def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
       ######################################## 
    
if "S17" in SS["Subject"].values:
    S17["Conf"] = S17.apply(conf, axis = "columns")
    S17.apply(conf, axis = "columns")
    S17["Trial"].replace("", np.nan, inplace = True)
    S17.dropna(subset = ["Trial"], inplace = True)
    S17 = S17.reset_index(drop=True)
    S17["RT"] = S17["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S17RT = S17[S17["Trial"] != "trial_start"]
    S17RT = S17RT.reset_index(drop=True)
    S17RT["Trial_Number"]= range(1, len(S17RT) +1)
    S17RT["cumsum"] = S17RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S17RT["Task_Order"] = S17RT["Task_Order"].astype("int")
    S17RT["cumsum"] = S17RT["cumsum"].astype("int")
    def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S17RT["Error_Type"] = S17RT.apply(perse, axis = "columns")
    S17RT.apply(perse, axis = "columns")

if "S18" in SS["Subject"].values:
    S18["Conf"] = S18.apply(conf, axis = "columns")
    S18.apply(conf, axis = "columns")
    S18["Trial"].replace("", np.nan, inplace = True)
    S18.dropna(subset = ["Trial"], inplace = True)
    S18 = S18.reset_index(drop=True)
    S18["RT"] = S18["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S18RT = S18[S18["Trial"] != "trial_start"]
    S18RT = S18RT.reset_index(drop=True)
    S18RT["Trial_Number"]= range(1, len(S18RT) +1)
    S18RT["cumsum"] = S18RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S18RT["Task_Order"] = S18RT["Task_Order"].astype("int")
    S18RT["cumsum"] = S18RT["cumsum"].astype("int")
    def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S18RT["Error_Type"] = S18RT.apply(perse, axis = "columns")
    S18RT.apply(perse, axis = "columns")

if "S19" in SS["Subject"].values:
    S19["Conf"] = S19.apply(conf, axis = "columns")
    S19.apply(conf, axis = "columns")
    S19["Trial"].replace("", np.nan, inplace = True)
    S19.dropna(subset = ["Trial"], inplace = True)
    S19 = S19.reset_index(drop=True)
    S19["RT"] = S19["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S19RT = S19[S19["Trial"] != "trial_start"]
    S19RT = S19RT.reset_index(drop=True)
    S19RT["Trial_Number"]= range(1, len(S19RT) +1)
    S19RT["cumsum"] = S19RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S19RT["Task_Order"] = S19RT["Task_Order"].astype("int")
    S19RT["cumsum"] = S19RT["cumsum"].astype("int")
    def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S19RT["Error_Type"] = S19RT.apply(perse, axis = "columns")
    S19RT.apply(perse, axis = "columns")

if "S20" in SS["Subject"].values:
    S20["Conf"] = S20.apply(conf, axis = "columns")
    S20.apply(conf, axis = "columns")
    S20["Trial"].replace("", np.nan, inplace = True)
    S20.dropna(subset = ["Trial"], inplace = True)
    S20 = S20.reset_index(drop=True)
    S20["RT"] = S20["Time_in_sec"].diff() # new column which subtract rows values from previous row
    S20RT = S20[S20["Trial"] != "trial_start"]
    S20RT = S20RT.reset_index(drop=True)
    S20RT["Trial_Number"]= range(1, len(S20RT) +1)
    S20RT["cumsum"] = S20RT.groupby("TaskID")["perseverative_or_regressive"].cumsum()
    S20RT["Task_Order"] = S20RT["Task_Order"].astype("int")
    S20RT["cumsum"] = S20RT["cumsum"].astype("int")
    def perse(row):
        random = row[26]
        taskorder = row[27]
        correctness = row[30]
        cumsum = row[34]
               
        if (taskorder > 1 and correctness == "incorrect" and cumsum == 1):
            return "1st"
        elif (taskorder > 1 and correctness == "incorrect" and cumsum < 1000 and cumsum > 1):
            return "perseverative"
        elif (taskorder > 1 and correctness == "incorrect"and cumsum > 1000):
            return "regressive"
        elif (taskorder > 1 and correctness == "correct"):
            return "correct"
        elif (taskorder > 1 and correctness == "omission"):
            return "omission"
        elif random == "Random":
            return "random"
        else:
            return ""
    S20RT["Error_Type"] = S20RT.apply(perse, axis = "columns")
    S20RT.apply(perse, axis = "columns")
'''
#if "S10___" in SS["Subject"].values:
#    S10["Trial"].replace("", np.nan, inplace = True)
 #   S10.dropna(subset = ["Trial"], inplace = True)
  #  S10 = S10.reset_index(drop=True)
   # S10["RT"] = S10["Time_in_sec"].diff() # new column which subtract rows values from previous row
   # S10RT = S10[S10["Trial"] != "trial_start"]
    # S10RT = S10RT.reset_index(drop=True)
    

# writerSS2temp = pd.ExcelWriter("SS2temp.xlsx", engine="xlsxwriter")
# SS2.to_excel(writerSS2temp, sheet_name="SS2", index = False)
# writerSS2temp.save()    

# SS2["Trial"].replace("", np.nan, inplace = True)
# SS2.dropna(subset = ["Trial"], inplace = True)
# SS2 = SS2.reset_index(drop=True)
# SS2["RT"] = SS2["Time_in_sec"].diff() # new column which subtract rows values from previous row
# SS2RT = SS2[SS2["Trial"] != "trial_start"]
# SS2RT = SS2RT.reset_index(drop=True)

# SS3["Trial"].replace("", np.nan, inplace = True)
# SS3.dropna(subset = ["Trial"], inplace = True)
# SS3 = SS3.reset_index(drop=True)
# SS3["RT"] = SS3["Time_in_sec"].diff() # new column which subtract rows values from previous row
# SS3RT = SS3[SS3["Trial"] != "trial_start"]
# SS3RT = SS3RT.reset_index(drop=True)

# SS4["Trial"].replace("", np.nan, inplace = True)
# SS4.dropna(subset = ["Trial"], inplace = True)
# SS4 = SS4.reset_index(drop=True)
# SS4["RT"] = SS4["Time_in_sec"].diff() # new column which subtract rows values from previous row
# SS4RT = SS4[SS4["Trial"] != "trial_start"]
# SS4RT = SS4RT.reset_index(drop=True)

# S1["Trial"].replace("", np.nan, inplace = True)
# S1.dropna(subset = ["Trial"], inplace = True)
# S1 = S1.reset_index(drop=True)
# S1["RT"] = S1["Time_in_sec"].diff() # new column which subtract rows values from previous row
# S1RT = S1[S1["Trial"] != "trial_start"]
# S1RT = S1RT.reset_index(drop=True)

# S2["Trial"].replace("", np.nan, inplace = True)
# S2.dropna(subset = ["Trial"], inplace = True)
# S2 = S2.reset_index(drop=True)
# S2["RT"] = S2["Time_in_sec"].diff() # new column which subtract rows values from previous row
# S2RT = S2[S2["Trial"] != "trial_start"]
# S2RT = S2RT.reset_index(drop=True)

# S3["Trial"].replace("", np.nan, inplace = True)
# S3.dropna(subset = ["Trial"], inplace = True)
# S3 = S3.reset_index(drop=True)
# S3["RT"] = S3["Time_in_sec"].diff() # new column which subtract rows values from previous row
# S3RT = S3[S3["Trial"] != "trial_start"]
# S3RT = S3RT.reset_index(drop=True)

# S7["Trial"].replace("", np.nan, inplace = True)
# S7.dropna(subset = ["Trial"], inplace = True)
# S7 = S7.reset_index(drop=True)
# S7["RT"] = S7["Time_in_sec"].diff() # new column which subtract rows values from previous row
# S7RT = S7[S7["Trial"] != "trial_start"]
# S7RT = S7RT.reset_index(drop=True)

#S10["Trial"].replace("", np.nan, inplace = True)
#S10.dropna(subset = ["Trial"], inplace = True)
#S10 = S10.reset_index(drop=True)
#S10["RT"] = S10["Time_in_sec"].diff() # new column which subtract rows values from previous row
#S10RT = S10[S10["Trial"] != "trial_start"]
#S10RT = S10RT.reset_index(drop=True)

#########################>>>>>>>>>>>>>>>>>>>> S* rats!!!!
#ReactionTime = S10RT.append([S12RT, S13RT, S14RT, S15RT], ignore_index= True)
#ReactionTime = S12RT.append([S13RT, S14RT, S15RT], ignore_index= True)
ReactionTime = S16RT.append([S17RT, S18RT, S19RT, S20RT], ignore_index= True)
ReactionTimeClean = ReactionTime.drop(["Project", 
                                       "UserID", 
                                       "A1 - Rear NP",
                                       "A2 - Front NP", 
                                       "A3 - MIddle NP",
                                       "A[1] Rear",
                                       "A[2] Front",
                                       "A[3] MIddle NP",
                                       "Station", "Run",
                                       "Current State", 
                                       "RTmask",
                                       "Time",
                                       "Transition State",
                                       "Transition Event", 
                                       "A4 - ", 
                                       "A[4] ",
                                       "perseverative_or_regressive",
                                       "cumsum"], axis = 1)

male = ["S1____", "S2____", "S3____", "S7____", "S10___", "S12___", "S13___", "S14___", "S15___", "REV5__", "REV6__", "REV7__", "S16", "S17", "S18", "S19", "S20"]
female = ["SS2___", "SS3___", "SS4___"]
          
def sex(row):
    ID = row[2]
        
    if ID in male:
        return "Male"
    elif ID in female:
        return "Female"
    else:
        return ""
    
ReactionTimeClean["Sex"] = ReactionTimeClean.apply(sex, axis = "columns")    
ReactionTimeClean.apply(sex, axis = "columns")


# =============================================================================
# All_rats = ["SS2___", "SS3___", "SS4___", "S1____", "S2____", "S3____", "S7____", "S10___" ]
# Session1 = [23, 24]
# Session2 = [25, 26]
# Session3 = [27, 28]
# Session4 = [29, 30]
# Session5 = [31, 32]
# Session6 = [33, 34]
# Session7 = [35]
# Session8 = [36]
# Session9 = [38]
# Session10 = [39]
# Session11 = [40]
# Session12 = [41]
# Session13 = [43]
# Session14 = [44]
# Session15 = [45]
# Session16 = [46]
# Session17 = [47]
# Session18 = [48]
# Session19 = [49]
# Session20 = [50]
# Session1_12 = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41]
# Session13_20 = [43, 44, 45, 46, 47, 48, 49, 50]
# =============================================================================

# =============================================================================
# All_rats = ["SS2___", "SS3___", "SS4___", "S1____", "S2____", "S3____", "S7____", "S10___", "S12___", "S13___", "S14___", "S15___" ]
# Session1 = [1]
# Session2 = [2]
# Session3 = [3]
# Session4 = [4]
# Session5 = [5]
# Session6 = [6]
# Session7 = [7]
# Session8 = [8]
# Session9 = [9]
# Session10 = [10]
# Session11 = [11]
# Session12 = [12]
# Session13 = [13]
# Session14 = [14]
# Session15 = [15]
# Session16 = [16]
# Session17 = [17]
# Session18 = [18]
# Session19 = [19]
# Session20 = [20]
# Session21 = [21]
# Session1_12 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
# 
# def drug(row):
#     subject = row[2]
#     session = row[1]
#          
#     if subject in All_rats and session in Session1_12: 
#          return "no"
# #     elif subject == "SS2___" and (session in Session14 or
# #                                   session in Session16 or
# #                                   session in Session17 or
# #                                   session in Session19):
# #         return "mcpp2"
# #     elif subject == "SS3___" and (session in Session13 or
# #                                   session in Session15 or
# #                                   session in Session18 or
# #                                   session in Session20):
# #         return "mcpp2"
# #     elif subject == "SS4___" and (session in Session14 or
# #                                   session in Session16 or
# #                                   session in Session17 or
# #                                   session in Session19):
# #         return "mcpp2"
# #     elif subject == "S1____" and (session in Session13 or
# #                                   session in Session15 or
# #                                   session in Session18 or
# #                                   session in Session20):
# #         return "mcpp2"
# #     elif subject == "S2____" and (session in Session14 or
# #                                   session in Session16 or
# #                                   session in Session17 or
# #                                   session in Session19):
# #         return "mcpp2"
# #     elif subject == "S3____" and (session in Session13 or
# #                                   session in Session15 or
# #                                   session in Session18 or
# #                                   session in Session20):
# #         return "mcpp2"
# #     elif subject == "S7____" and (session in Session14 or
# #                                   session in Session16 or
# #                                   session in Session17 or
# #                                   session in Session19):
# #         return "mcpp2"
# #     else:
# #         return ""
# #           
# ReactionTimeClean["Drug"] = ReactionTimeClean.apply(drug, axis = "columns")    
# ReactionTimeClean.apply(drug, axis = "columns")
# 
# 
# def stim(row):
#     subject = row[2]
#     session = row[1]
#         
#     if subject == "S10___" and (session in Session1 or
#                                   session in Session3 or
#                                   session in Session5 or
#                                   session in Session7 or
#                                   session in Session9 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17):
#         return "ON"
#     elif subject == "S12___" and (session in Session2 or
#                                   session in Session3 or
#                                   session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "ON"
#     elif subject == "S13___" and (session in Session1 or
#                                   session in Session3 or
#                                   session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "ON"
#     elif subject == "S14___" and (session in Session1 or
#                                   session in Session2 or
#                                   session in Session5 or
#                                   session in Session7 or
#                                   session in Session9 or
#                                   session in Session11 or
#                                   session in Session13 or
#                                   session in Session14 or
#                                   session in Session16 or
#                                   session in Session19 or
#                                   session in Session21):
#         return "ON"
#     elif subject == "S15___" and (session in Session1 or
#                                   session in Session2 or
#                                   session in Session3 or
#                                   session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session13 or
#                                   session in Session14 or
#                                   session in Session16 or
#                                   session in Session19 or
#                                   session in Session21):
#         return "ON"
#     else:
#         return "OFF"
#     
# ReactionTimeClean["Stim"] = ReactionTimeClean.apply(stim, axis = "columns")    
# ReactionTimeClean.apply(stim, axis = "columns")
# 
# def stim_int(row):
#     subject = row[2]
#     session = row[1]
#     stim_on_off = row[15]
#         
#     if stim_on_off == "OFF":
#         return "0"
#     elif subject == "S10___" and (session in Session1 or
#                                   session in Session3 or
#                                   session in Session5 or
#                                   session in Session7 or
#                                   session in Session9 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17):
#         return "300"
#     elif subject == "S12___" and (session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "300"
#     elif subject == "S13___" and (session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session12 or
#                                   session in Session15 or
#                                   session in Session17 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "300"
#     elif subject == "S14___" and (session in Session2 or
#                                   session in Session5 or
#                                   session in Session7 or
#                                   session in Session9 or
#                                   session in Session11 or
#                                   session in Session13 or
#                                   session in Session14 or
#                                   session in Session16 or
#                                   session in Session19 or
#                                   session in Session21):
#         return "300"
#     elif subject == "S15___" and (session in Session1 or
#                                   session in Session4 or
#                                   session in Session6 or
#                                   session in Session8 or
#                                   session in Session10 or
#                                   session in Session13 or
#                                   session in Session14 or
#                                   session in Session16 or
#                                   session in Session19 or
#                                   session in Session21):
#         return "300"
#     elif subject == "S12___" and (session in Session2):
#         return "200"
#     elif subject == "S12___" and (session in Session3):
#         return "100"
#     elif subject == "S13___" and (session in Session3):
#         return "200"
#     elif subject == "S13___" and (session in Session1):
#         return "100"
#     elif subject == "S14___" and (session in Session1):
#         return "200"
#     elif subject == "S15___" and (session in Session3):
#         return "200"
#     elif subject == "S15___" and (session in Session2):
#         return "100"
# 
# 
# ReactionTimeClean["Stim_Int"] = ReactionTimeClean.apply(stim_int, axis = "columns")    
# ReactionTimeClean.apply(stim_int, axis = "columns")
# =============================================================================

All_rats = ["SS2___", "SS3___", "SS4___", "S1____", "S2____", "S3____", "S7____", "S10___", "S12___", "S13___", "S14___", "S15___", "REV5__", "REV6__", "REV7__", "S15___", "S16", "S17", "S18", "S19", "S20"]
# ============================================================================= FOR RATS S. do not use for REVS
# Session1 = [160,162]
# Session2 = [163,165]
# Session3 = [166,168]
# Session4 = [169,171]
# Session5 = [172]
# Session6 = [173]
# Session7 = [174]
# Session8 = [212]
# Session9 = [215]
# Session10 = [219]
# Session11 = [223]
# Session12 = [227]
# Session13 = [237]
# Session14 = [240]
# Session15 = [247]
# Session16 = [255]
# Session17 = [258]
# #Session18 = [18]
# #Session19 = [19]
# #Session20 = [20]
# #Session21 = [21]
# Session1_17 = [160,162,163,165,166,168,169,171,172,173,174,212,215,219,223,227,237,240,247,255,258]
# =============================================================================

Session1 = [1]
Session2 = [2]
Session3 = [3]
Session4 = [4]
Session5 = [5]
Session6 = [6]
Session7 = [7]
Session8 = [8]
Session9 = [9]
Session10 = [10]
Session11 = [11]
Session12 = [12]
Session13 = [13]
Session14 = [14]
Session15 = [15]
Session16 = [16]
Session17 = [17]
#Session18 = [18]
#Session19 = [19]
#Session20 = [20]
#Session21 = [21]
Session1_17 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

def drug(row):
    subject = row[2]
    session = row[1]
         
    if subject in All_rats and session in Session1_17: 
         return "no"
#     elif subject == "SS2___" and (session in Session14 or
#                                   session in Session16 or
#                                   session in Session17 or
#                                   session in Session19):
#         return "mcpp2"
#     elif subject == "SS3___" and (session in Session13 or
#                                   session in Session15 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "mcpp2"
#     elif subject == "SS4___" and (session in Session14 or
#                                   session in Session16 or
#                                   session in Session17 or
#                                   session in Session19):
#         return "mcpp2"
#     elif subject == "S1____" and (session in Session13 or
#                                   session in Session15 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "mcpp2"
#     elif subject == "S2____" and (session in Session14 or
#                                   session in Session16 or
#                                   session in Session17 or
#                                   session in Session19):
#         return "mcpp2"
#     elif subject == "S3____" and (session in Session13 or
#                                   session in Session15 or
#                                   session in Session18 or
#                                   session in Session20):
#         return "mcpp2"
#     elif subject == "S7____" and (session in Session14 or
#                                   session in Session16 or
#                                   session in Session17 or
#                                   session in Session19):
#         return "mcpp2"
#     else:
#         return ""
#           
ReactionTimeClean["Drug"] = ReactionTimeClean.apply(drug, axis = "columns")    
ReactionTimeClean.apply(drug, axis = "columns")


def stim(row):
    subject = row[2]
    session = row[1]
        
    if subject == "S10___" and (session in Session1 or
                                  session in Session3 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "ON"
    elif subject == "S12___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session8 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session14 or
                                  session in Session16):
        return "ON"
    elif subject == "S13___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session6 or
                                  session in Session8 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session14 or
                                  session in Session16):
        return "ON"
    elif subject == "S14___" and (session in Session1 or
                                  session in Session3 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "ON"
    elif subject == "S15___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session6 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "ON"
    elif subject == "REV5__" and (session in Session2 or
                                  session in Session4 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session15 or
                                  session in Session17):
        return "ON"    
    elif subject == "REV6__" and (session in Session2 or
                                  session in Session4 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session15 or
                                  session in Session17):
        return "ON"    
    elif subject == "REV7__" and (session in Session1 or
                                  session in Session3 or
                                  session in Session6 or
                                  session in Session8 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session14 or
                                  session in Session16):
        return "ON"    

    else:
        return "OFF"
    
ReactionTimeClean["Stim"] = ReactionTimeClean.apply(stim, axis = "columns")    
ReactionTimeClean.apply(stim, axis = "columns")

def stim_int(row):
    subject = row[2]
    session = row[1]
    stim_on_off = row[15]
        
    if stim_on_off == "OFF":
        return "0"
    elif subject == "S10___" and (session in Session1 or
                                  session in Session3 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "300"
    elif subject == "S12___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session8 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session14 or
                                  session in Session16):
        return "300"
    elif subject == "S13___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session6 or
                                  session in Session8 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session14 or
                                  session in Session16):
        return "300"
    elif subject == "S14___" and (session in Session1 or
                                  session in Session3 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "300"
    elif subject == "S15___" and (session in Session2 or
                                  session in Session4 or
                                  session in Session6 or
                                  session in Session9 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session15 or
                                  session in Session17):
        return "300"
    elif subject == "REV5__" and (session in Session2 or
                                  session in Session4 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session15 or
                                  session in Session17):
        return "300"    
    elif subject == "REV6__" and (session in Session2 or
                                  session in Session4 or
                                  session in Session5 or
                                  session in Session7 or
                                  session in Session9 or
                                  session in Session11 or
                                  session in Session13 or
                                  session in Session15 or
                                  session in Session17):
        return "300"    
    elif subject == "REV7__" and (session in Session1 or
                                  session in Session3 or
                                  session in Session6 or
                                  session in Session8 or
                                  session in Session10 or
                                  session in Session12 or
                                  session in Session14 or
                                  session in Session16):
        return "300"
    else:
        return "0"
  
ReactionTimeClean["Stim_Int"] = ReactionTimeClean.apply(stim_int, axis = "columns")    
ReactionTimeClean.apply(stim_int, axis = "columns")

def stim_period(row):
    session = row[1]
    stim_on_off = row[15]
        
    if stim_on_off == "ON" and session in Session1_17:
        return "60"
    else:
        return "0"

ReactionTimeClean["Stim_Period"] = ReactionTimeClean.apply(stim_period, axis = "columns")    
ReactionTimeClean.apply(stim_period, axis = "columns")

# =============================================================================
# if 1 == 1 :
#     conditions = [
#         (ReactionTimeClean["Session"] == 160) | (ReactionTimeClean["Session"] == 162),
#         (ReactionTimeClean["Session"] == 163) | (ReactionTimeClean["Session"] == 165),
#         (ReactionTimeClean["Session"] == 166) | (ReactionTimeClean["Session"] == 168),
#         (ReactionTimeClean["Session"] == 169) | (ReactionTimeClean["Session"] == 171),
#         (ReactionTimeClean["Session"] == 172),
#         (ReactionTimeClean["Session"] == 173),
#         (ReactionTimeClean["Session"] == 174),
#         (ReactionTimeClean["Session"] == 212),
#         (ReactionTimeClean["Session"] == 215),
#         (ReactionTimeClean["Session"] == 219),
#         (ReactionTimeClean["Session"] == 223),
#         (ReactionTimeClean["Session"] == 227),
#         (ReactionTimeClean["Session"] == 237),
#         (ReactionTimeClean["Session"] == 240),
#         (ReactionTimeClean["Session"] == 247),
#         (ReactionTimeClean["Session"] == 255),
#         (ReactionTimeClean["Session"] == 258)]
#     choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
#     ReactionTimeClean["Session"] = np.select(conditions, choices)
# else:
#     print("ERROR")
# =============================================================================


if 1 == 1 :
    conditions = [
        (ReactionTimeClean["Session"] == 1),
        (ReactionTimeClean["Session"] == 2),
        (ReactionTimeClean["Session"] == 3),
        (ReactionTimeClean["Session"] == 4),
        (ReactionTimeClean["Session"] == 5),
        (ReactionTimeClean["Session"] == 6),
        (ReactionTimeClean["Session"] == 7),
        (ReactionTimeClean["Session"] == 8),
        (ReactionTimeClean["Session"] == 9),
        (ReactionTimeClean["Session"] == 10),
        (ReactionTimeClean["Session"] == 11),
        (ReactionTimeClean["Session"] == 12),
        (ReactionTimeClean["Session"] == 13),
        (ReactionTimeClean["Session"] == 14),
        (ReactionTimeClean["Session"] == 15),
        (ReactionTimeClean["Session"] == 16),
        (ReactionTimeClean["Session"] == 17)]
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    ReactionTimeClean["Session"] = np.select(conditions, choices)
else:
    print("ERROR")
ReactionTime_ok = ReactionTimeClean[["Subject","Sex","Drug", "Stim", "Stim_Int", "Stim_Period", "Session", "Protocol", "Task_Order", "Task_Type", "TaskID", "Trial_ID","Trial_Number", "Trial","Error_Type", "Conf", "Time_in_sec", "RT"]]




ReactionTime_ok.to_csv('SS2018_revs_session17.csv', index = False)

def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]
if __name__ == "__main__":
    clear_all()

# =============================================================================
# S1 = pd.read_csv("SS2018_session1.csv")
# S2 = pd.read_csv("SS2018_session2.csv")
# S3 = pd.read_csv("SS2018_session3.csv")
# S4 = pd.read_csv("SS2018_session4.csv")
# S5 = pd.read_csv("SS2018_session5.csv")
# S6 = pd.read_csv("SS2018_session6.csv")
# S7 = pd.read_csv("SS2018_session7.csv")
# S8 = pd.read_csv("SS2018_session8.csv")
# S9 = pd.read_csv("SS2018_session9.csv")
# S10 = pd.read_csv("SS2018_session10.csv")
# S11 = pd.read_csv("SS2018_session11.csv")
# S12 = pd.read_csv("SS2018_session12.csv")
# S13 = pd.read_csv("SS2018_session13.csv")
# S14 = pd.read_csv("SS2018_session14.csv")
# S15 = pd.read_csv("SS2018_session15.csv")
# S16 = pd.read_csv("SS2018_session16.csv")
# S17 = pd.read_csv("SS2018_session17.csv")
# 
# SS2018 = S1.append([S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,S16,S17], ignore_index= True)
# SS2018.to_csv('SS2018.csv', index = False)
# =============================================================================
# writerSS2RT = pd.ExcelWriter("SS2RT.xlsx", engine="xlsxwriter")
# SS2RT.to_excel(writerSS2RT, sheet_name="SS2", index = False)
# writerSS2RT.save()
    
    
# =============================================================================
S1 = pd.read_csv("SS2018_revs_session1.csv")
S2 = pd.read_csv("SS2018_revs_session2.csv")
S3 = pd.read_csv("SS2018_revs_session3.csv")
S4 = pd.read_csv("SS2018_revs_session4.csv")
S5 = pd.read_csv("SS2018_revs_session5.csv")
S6 = pd.read_csv("SS2018_revs_session6.csv")
S7 = pd.read_csv("SS2018_revs_session7.csv")
S8 = pd.read_csv("SS2018_revs_session8.csv")
S9 = pd.read_csv("SS2018_revs_session9.csv")
S10 = pd.read_csv("SS2018_revs_session10.csv")
S11 = pd.read_csv("SS2018_revs_session11.csv")
S12 = pd.read_csv("SS2018_revs_session12.csv")
S13 = pd.read_csv("SS2018_revs_session13.csv")
S14 = pd.read_csv("SS2018_revs_session14.csv")
S15 = pd.read_csv("SS2018_revs_session15.csv")
S16 = pd.read_csv("SS2018_revs_session16.csv")
S17 = pd.read_csv("SS2018_revs_session17.csv")

SS2018_rev = S1.append([S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,S16,S17], ignore_index= True)
SS2018_rev.to_csv('SS2018_revs.csv', index = False)