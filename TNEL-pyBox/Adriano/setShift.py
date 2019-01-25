import numpy as np
import pandas as pd
import os
import setShiftFunc as SSF

#os.chdir("D:/UMN rats GS4")
SS = pd.read_csv("test1_umn2019.csv")

SS["Time_in_sec"] = SS["Time"] # new column transforming graphicstate unities in seconds
SS["RTmask"] = SS["Time_in_sec"].diff() # new column which subtract rows values from previous row

SS["Protocol"] = SS["Protocol"].astype("category")
SS["Session"] = SS["Session"].astype("category")
SS["Station"] = SS["Station"].astype("category")
SS["Run"] = SS["Run"].astype("category")
SS["Project"] = SS["Project"].astype("category")
SS["UserID"] = SS["UserID"].astype("category")
SS["Subject"] = SS["Subject"].astype("category")
SS["A[1] Rear"] = SS["Rear"].astype("category")
SS["A[2] Front"] = SS["Front"].astype("category")
SS["A[3] Middle NP"] = SS["Middle"].astype("category")
SS["A[4] "] = SS["Manual Switch"].astype("category")

SS["Trial_ID"] = SS.apply(SSF.trial_number, axis = "columns")
SS.apply(SSF.trial_number, axis = "columns")

SS["perseverative_or_regressive"] = SS.apply(SSF.trial_perse, axis = "columns")
SS.apply(SSF.trial_perse, axis = "columns")

ProtocolN = SS["Protocol"].iloc[0] # define that the first value on the Protocol column will be the variable ProtocolN
if ProtocolN == 44:
    conditions = SSF.determineConditionsNormal(SS)
    choices = ["Rand1", "Side1", "Light1", "Side2", "Light2", "Side3", "Light3", "Side4", "Light4", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    conditions = SSF.determineConditionsNormal(SS)
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    npchoice_conflict = [86, 98, 104, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [92, 110, 123, 135, 154, 160, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [54, 61, 67, 73, 79]
elif ProtocolN == 45:
    conditions = SSF.determineConditionsNormal(SS)
    choices = ["Rand1", "Side3", "Light4", "Side4", "Light1", "Side1", "Light2", "Side2", "Light3", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    conditions = SSF.determineConditions45Task_Order(SS)
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    npchoice_conflict = [54, 67, 86, 98, 104, 117, 129, 141, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 92, 110, 123, 135, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [148, 154, 160, 166, 172]
elif ProtocolN == 46:
    conditions = SSF.determineConditionsNormal(SS)
    choices = ["Rand1", "Side2", "Light2", "Side3", "Light3", "Side4", "Light4", "Side1", "Light1", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    conditions = SSF.determineConditions46Task_Order(SS)
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    npchoice_conflict = [54, 67, 86, 98, 104, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 92, 110, 123, 135, 154, 160, 191, 197, 222, 234, 303, 309]
    npchoice_set = [241, 247, 253, 259, 265]
elif ProtocolN == 47:
    conditions = SSF.determineConditionsNormal(SS)
    choices = ["Rand1", "Side4", "Light1", "Side1", "Light2", "Side2", "Light3", "Side3", "Light4", "Rand2"]
    SS["TaskID"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    conditions = SSF.determineConditionsNormal(SS)
    choices = [1, 9, 2, 3, 4, 5, 6, 7, 8, 10]
    SS["Task_Order"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating
    npchoice_conflict = [54, 67, 117, 129, 141, 148, 166, 172, 179, 185, 203, 210, 216, 228, 241, 253, 297, 315, 321]
    npchoice_NONconflict = [61, 73, 79, 123, 135, 154, 160, 191, 197, 222, 234, 247, 259, 265, 303, 309]
    npchoice_set = [86, 92, 98, 104, 110]

conditions = SSF.determineConditionsNormal(SS)
choices = ["Random", "Side", "Light", "Side", "Light", "Side", "Light", "Side", "Light", "Random"]
SS["Task_Type"] = np.select(conditions, choices, default = "black") # the np.,select function allows conditional formating

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

if "S17" in SS["Subject"].values:
        S17 = SS[SS["Subject"] == "S17"]
        S17.iat[0,20] = 0
        Subject_S17 = SS["Subject"] == "S17"
        S17["Trial"] = S17.apply(SSF.trial, axis = "columns")
        S17.apply(SSF.trial, axis = "columns")
        S17, S17RT = SSF.createDataFrame(S17, SS)
