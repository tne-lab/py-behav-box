import numpy as np

def trial_number(row):
    trial1 = [54, 86, 117, 148, 179, 210, 241, 297]
    trial2 = [61, 92, 123, 154, 185, 216, 247, 303]
    trial3 = [67, 98, 129, 160, 191, 222, 253, 309]
    trial4 = [73, 104, 135, 166, 197, 228, 259, 315]
    trial5 = [79 , 110, 141, 172, 203, 234, 265, 321]
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

def trial_perse(row):
    np_regressive = [79, 110, 141, 172, 203, 234, 265, 321]
    np_perseverative = [54, 61, 67, 73, 86, 92, 98, 104, 117, 123, 129, 135, 148, 154, 160, 166, 179, 185, 191, 197, 210, 216, 222, 228, 241, 247, 253, 259, 297, 303, 309, 315]

    ID = row[8]

    if ID in np_regressive:
     return 1000
    elif ID in np_perseverative:
     return 1
    else:
     return 0

def trial(row):
    #Definir os estates
    npchoice = [54, 61, 67, 73, 79, 86, 92, 98, 104, 110, 117, 123, 129, 135, 141, 148, 154, 160, 166, 172, 179, 185, 191, 197, 203, 210, 216, 222, 228, 234, 241, 247, 253, 259, 265, 297, 303, 309, 315, 321]
    right_choice = [55, 62, 68, 74, 80, 87, 93, 99, 105, 111, 118, 124, 130, 136, 142, 149, 155, 161, 167, 173, 180, 186, 192, 198, 204, 211, 217, 223, 229, 235, 242, 248, 254, 260, 266, 298, 304, 310, 316, 322]
    error = [57, 64, 70, 76, 82, 89, 95, 101, 107, 113, 120, 126, 132, 138, 144, 151, 157, 163, 169, 175, 182, 188, 194, 200, 206, 213, 219, 225, 231, 237, 244, 250, 256, 262, 268, 300, 306, 312, 318, 324]
    omission = [52, 84, 115, 146, 177, 208, 239, 295]

    random1_npchoice = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
    random1_response = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]
    random2_npchoice = [271, 276, 281, 286, 291]
    random2_response = [272, 277, 282, 287, 292]

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

def conf(row, SS):
    ProtocolN = SS["Protocol"].iloc[0] # define that the first value on the Protocol column will be the variable ProtocolN
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

    random1_npchoice = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
    random2_npchoice = [271, 276, 281, 286, 291]
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

def createDataFrame(data, SS):
    data["Conf"] = data.apply(conf, axis = "columns", args = (SS,))
    data.apply(conf, axis = "columns", args = (SS,))
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
    print(dataRT)
    return data, dataRT

def perse(row):
    random = row[26]
    taskorder = row[27]
    correctness = row[30]
    cumsum = row[34]
    print('randomtype: ', random, '\ntaskorder type: ', taskorder)
    print('correcttype: ', correctness, '\ncumsum type: ', cumsum)
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

def determineConditionsNormal(SS):
    return [
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

def determineConditions45Task_Order(SS):
    return [
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

def determineConditions46Task_Order(SS):
    return [
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
