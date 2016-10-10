import pandas as pd
df = pd.read_csv("/Volumes/Nebula/LabExMI/freezer0004.csv")
df.head()
df = pd.read_csv("/Volumes/Nebula/LabExMI/freezer0004.csv", sep=";", dtype=object)
df.head()
df["Position"] = 64
df.loc[df["AliquotID"] == 2, "Freezer"] = df["Freezer"].str.replace("0004", "0014")
df["Freezer"].unique()
df["Freezer"] = df.loc[df["AliquotID"] == 2, "Freezer"].str.replace("0004", "0014")
df["Freezer"].unique()
df = pd.read_csv("/Volumes/Nebula/LabExMI/freezer0004.csv", sep=";", dtype=object)
df["Position"] = 64
df.loc[df["AliquotID"] == 2, "Freezer"]
df.loc[df["AliquotID"] == "2", "Freezer"]
df.loc[df["AliquotID"] == "2", "Freezer"] = df["Freezer"].str.replace("0004", "0014")
df["Freezer"].unique()
df.loc[df["AliquotID"] == "3", "Freezer"] = df["Freezer"].str.replace("0004", "0024")
df.loc[df["AliquotID"] == "2", "Freezer_Descr"] = df["Freezer_Descr"].str.replace("0004", "0014")
df.loc[df["AliquotID"] == "3", "Freezer_Descr"] = df["Freezer_Descr"].str.replace("0004", "0024")
df["Freezer_Descr"].unique()
df["Level1"].uniques()
df["Level1"].unique()
df["Level1_Descr"].unique()
df.loc[df["AliquotID"] == "2", "Level1_Descr"] = df["Level1_Descr"].str.replace("0004", "0014")
df.loc[df["AliquotID"] == "3", "Level1_Descr"] = df["Level1_Descr"].str.replace("0004", "0024")
df.head()
df["Level2"] = df["Level2"].str.replace("801-896", "401-496")
df.loc[df["VisitID"], "Level2"] = df["Level2"].str.replace("401-496", "402-497")
df.loc[df["VisitID"] == "2", "Level2"] = df["Level2"].str.replace("401-496", "402-497")
df["Level2"].unique()
df.columns
df = pd.read_csv("/Volumes/Nebula/LabExMI/freezer0003.csv", sep=";", dtype=object)
df.head()
df.loc[df["AliquotID"] == "1", "Freezer"] = df["Freezer"].str.replace("0003", "0005")
df.loc[df["AliquotID"] == "1", "Freezer_Descr"] = df["Freezer_Descr"].str.replace("0003", "0005")
df["Freezer"].unique()
df["Freezer_Descr"].unique()
df.loc[df["AliquotID"] == "2", "Freezer"] = df["Freezer"].str.replace("0003", "0015")
df.loc[df["AliquotID"] == "2", "Freezer_Descr"] = df["Freezer_Descr"].str.replace("0003", "0015")
df.loc[df["AliquotID"] == "3", "Freezer"] = df["Freezer"].str.replace("0003", "0025")
df.loc[df["AliquotID"] == "3", "Freezer_Descr"] = df["Freezer_Descr"].str.replace("0003", "0025")
df["Freezer"].unique()
df["Freezer_Descr"].unique()
df["DonorID"].unique()
df["DonorID"] = 464
df.columns
df["Level1"].unique()
df["Level1_Descr"].unique()
df.loc[df["AliquotID"] == "1", "Level1_Descr"] = df["Level1_Descr"].str.replace("0003", "0005")
df.loc[df["AliquotID"] == "2", "Level1_Descr"] = df["Level1_Descr"].str.replace("0003", "0015")
df.loc[df["AliquotID"] == "3", "Level1_Descr"] = df["Level1_Descr"].str.replace("0003", "0025")
df["Level2"].unique()
df.loc[df["VisitID"] == "2", "Level2"] = df["Level2"].str.replace("801-896", "402-497")
df.loc[df["VisitID"] == "1", "Level2"] = df["Level2"].str.replace("801-896", "401-496")
df["Level2"].unique()
df["Level2_Descr"]
df["Level2_Descr"].unique()
df.loc[df["VisitID"] == "2", "Level2_Descr"] = df["Level2_Descr"].str.replace("081 to 896", "402 to 497")
df.loc[df["VisitID"] == "1", "Level2_Descr"] = df["Level2_Descr"].str.replace("081 to 896", "401 to 496")
df["Level2_Descr"].unique()
df["Level3"].unique()
df.columns()
df.columns
df.rename(columns={"Level2": "Level3", "Level2_Descr": "Level3_Descr"})
df.rename(columns={"Level2": "Level3", "Level2_Descr": "Level3_Descr"}, inplace=True)
df.columns
df["Level2"] = "D401-496_V1"
df["Level2_Descr"] = "Rack donors 401 to 496, visit "+df["VisitID"]
df["Level2"] = "D401-496_V"+df["VisitID"]
df.loc[df["VisitID"] == "2", "Level2"] = df["Level2"].str.replace("401-496", "402-497")
df.loc[df["VisitID"] == "2", "Level2_Descr"] = df["Level2_Descr"].str.replace("401 to 496", "402 to 497")
df["Level2"].unique()
df["Level2_Descr"].unique()
df.columns
df["Position"].unique()
df["Sample Source"] = df["DonorID"]
df["Level3_Descr"].unique()
df["Box_Descr"].unique()
df["Box"].unique()
df.loc[df["VisitID"] == "2", "Box_Descr"] = df["Box_Descr"].str.replace("801 to 896", "402 to 497")
df.loc[df["VisitID"] == "1", "Box_Descr"] = df["Box_Descr"].str.replace("801 to 896", "401 to 496")
df.loc[df["VisitID"] == "1", "Box"] = df["Box"].str.replace("801-896", "401-496")
df.loc[df["VisitID"] == "2", "Box"] = df["Box"].str.replace("801-896", "402-497")
df["Box"].unique()
df["Box_Descr"].unique()
df["Description"].unique()
df["Description"] = df["Description"].str.replace("845", "464")
df.columns
df["Sample Source"].unique()
df["Gender"] = "Female"
df["Age"] = "40-49"
df.to_csv("/Volumes/Nebula/LabExMI/freezers_D464.csv", header=True, index=False)
df["Name"].unique()
donors = [ i+1 for i in range(301, 399)]
donors
donors = [ i+1 for i in range(300, 399)]
len(donors)
donors[:5]
donors[5:]
donors[-5:]
donors[5:]
donors[:5]
donors[-5:]
dd = pd.DataFrame(donors, columns = "Name")
dd = pd.DataFrame(donors, columns = ["Name"])
dd.head()
dd = pd.DataFrame(donors, columns = ["Name"], dtype=object)
dd = pd.DataFrame(donors, columns = ["Source Name"], dtype=object)
dd["Description"] = "Donor "+dd["Source Name"]
dd["Description"] = "Donor "+str(dd["Source Name"])
dd.head()
dd["Source Name"] = dd["Source Name"].astype(str)
dd["Description"] = "Donor "+str(dd["Source Name"])
dd["Description"] = "Donor "+dd["Source Name"]
dd.head()
dd["Source Type"] = "Donor"
dd["DonorID"] = dd["Source Name"]
dd["Age"] = "30-39"
dd["Gender"] = "Male"
dd.head()
dd.to_csv("/Volumes/Nebula/LabExMI/cohort_test.csv", index=False, header=True)
dd.rename(columns = {"Source Name": "Name"}, inplace=True)
del dd["Source Type"]
dd.head()
dd.to_csv("/Volumes/Nebula/LabExMI/cohort_test.csv", index=False, header=True)

df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/freezers_supernatants.csv")
df["VisitID"] = df["Level3"].str.replace(r"MIC_Plasma_S\d{2}-\d{2}_V(\d{1})_A\d{1}", r"\1")
df["AliquotID"] = df["Level3"].str.replace(r"MIC_Plasma_S\d{2}-\d{2}_V\d{1}_A(\d{1})", r"\1")
df["StimulusID"] = df["StimulusID"].str.replace(r"(\d{1,2}) \d{1,2}", r"\1")
df.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_test.csv", header=True, index=False)
l_pos = [ i+1 for i in range(0, 96) ]
l_stim = [str(i+1) for i in range(0, 40)]
l_aliq = [str(i+1) for i in range(0, 3)]
l_visit = [str(i+1) for i in range(0, 2)]
lines = []
for s in l_stim:
    for p in l_pos:
        for a in l_aliq:
            for v in l_visit:
                lines.append([a,s,v,p])

dp = pd.DataFrame(lines, columns=["AliquotID", "StimulusID", "VisitID", "Position"], dtype=object)
merge(df, dp, on=["VisitID", "AliquotID", "StimulusID"])
pd.merge(df, dp, on=["VisitID", "AliquotID", "StimulusID"])
dff = pd.merge(df, dp, on=["VisitID", "AliquotID", "StimulusID"])
dff.loc[dff.Position == 1,"Level2"].str.replace(r"D(\d)\d\d>>\d{3}_V\d", r"\1")
dff.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_test.csv", header=True, index=False)
dfd = dff.loc[dff.VisitID == '1']
dfd.Level2.str.replace(r"D(\d)\d{2}>>\d{3}_V\d", r"\1")

'''
Miss few columns, need to create them
'''

with open("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/donors_X97_X00.json", "r") as infile:
    donors = json.load(infile)

lines=[]
for col in donors:
    for num, val in enumerate(donors[col]):
        lines.append([col+"/"+str(num+1), val])

dd = pd.DataFrame(lines, columns=["Position","DonorID"], dtype=object)
dp = pd.DataFrame([str(col)+"/"+str(line+1) for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for line in range(0, 12)], columns=["Position"])
dp["PositionNum"] = dp.index+1
l_pos = [i+1 for i in range(0, 96)]
l_aliquot = [i+1 for i in range(0, 3)]
l_stim = [i+1 for i in range(0, 40)]
lines = []
for p in l_pos:
    for a in l_aliquot:
        for s in l_stim:
            lines.append([p,a,s,1])

dataframe = pd.DataFrame(lines, columns=["PositionNum", "AliquotID", "StimulusID","VisitID"], dtype=object)
ddp = pd.merge(dp, dd, on=["Position"])

dfs = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/LabExMI_Stimuli_List.csv", dtype=object)
del dfs["type"], dfs["description"], dfs["sensor"]
dfs.rename(columns={"stimulusId": "StimulusID", "name": "StimulusName"}, inplace=True)

df_tokeep = pd.merge(ddp, dataframe, on=["PositionNum"])
dfs["StimulusID"] = dfs["StimulusID"].astype(int)
df_tokeep["StimulusID"] = df_tokeep["StimulusID"].astype(int)

df_final = pd.merge(df_tokeep, dfs, on="StimulusID")
df_final["Volume"] = 400.0
df_final["Sample Type"] = "PLASMA"
df_final["ThawCycle"] = 0
df_final["CreationDate"] = "05/10/2016"
df_final["BatchID"] = "A"
df_final["Name"] = [334090000+i for i in range(0, len(df_final))]
df_final["Sample Source"] = df_final["DonorID"]


df_final["VisitID"] = df_final["VisitID"].astype(str)

df_final["Freezer"] = "MIC_Freezer_1532"
df_final.loc[df_final["AliquotID"] == 2, "Freezer"] = df_final["Freezer"].str.replace("1532", "1534")
df_final.loc[df_final["AliquotID"] == 3, "Freezer"] = df_final["Freezer"].str.replace("1532", "1535")
df_final["Freezer_Descr"] = "Freezer 1532"
df_final.loc[df_final["AliquotID"] == 2, "Freezer_Descr"] = df_final["Freezer_Descr"].str.replace("1532", "1534")
df_final.loc[df_final["AliquotID"] == 3, "Freezer_Descr"] = df_final["Freezer_Descr"].str.replace("1532", "1535")
df_final["Level1"] = "MIC Freezer1532 Shelf1"
df_final.loc[df_final["AliquotID"] == 2, "Level1"] = df_final["Level1"].str.replace("1532", "1534")
df_final.loc[df_final["AliquotID"] == 3, "Level1"] = df_final["Level1"].str.replace("1532", "1535")
df_final["Level1_Descr"] = "Shelf 1"
df_final["Level2"] = "DX97>>X00"
df_final["Level2_Descr"] = "\"Rack donors X97 to X00, Visit "+df_final["VisitID"]+"\""
df_final["AliquotID"] = df_final["AliquotID"].astype(str)
df_final["Level3"] = "MIC_Plasma_"+df_final["Level2"]+"_S01-07_V"+df_final["VisitID"]+"_A"+df_final["AliquotID"]
df_final.loc[df_final["StimulusID"] > 7, "Level3"] = df_final["Level3"].str.replace("S01-07", "S08-14")
df_final.loc[df_final["StimulusID"] > 14, "Level3"] = df_final["Level3"].str.replace("S08-14", "S15-21")
df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S15-21", "S22-28")
df_final.loc[df_final["StimulusID"] > 28, "Level3"] = df_final["Level3"].str.replace("S22-28", "S29-35")
df_final.loc[df_final["StimulusID"] > 35, "Level3"] = df_final["Level3"].str.replace("S29-35", "S36-40")
df_final["Level3_Descr"] = "\"Drawer with Plasma for donors X97 to X00, stimulus 1 to 7, visit "+df_final["VisitID"]+", aliquot "+df_final["AliquotID"]+"\""
df_final.loc[df_final["StimulusID"] > 7, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("1 to 7", "8 to 14")
df_final.loc[df_final["StimulusID"] > 14, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("8 to 14", "15 to 21")
df_final.loc[df_final["StimulusID"] > 21, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("15 to 21", "22 to 28")
df_final.loc[df_final["StimulusID"] > 28, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("22 to 28", "29 to 35")
df_final.loc[df_final["StimulusID"] > 35, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("29 to 35", "36 to 40")
df_final["StimulusID"] = df_final["StimulusID"].astype(str)
df_final["Box"] = "MIC_S"+df_final["StimulusID"]+"_V"+df_final["VisitID"]+"_A"+df_final["AliquotID"]+"_DX97-X00"
df_final["Box_Descr"] = "\"Box of stimulus "+df_final["StimulusID"]+", for donors X97 to X00, visit "+df_final["VisitID"]+", aliquot "+df_final["AliquotID"]+"\""
df_final["BoxType"] = "96 (12 x 8) Well Plate"
df_final["DonorID"] = df_final["DonorID"].astype(str)
df_final["Description"] = "\"Donor "+df_final["DonorID"]+", stimulus "+df_final["StimulusID"]+", visit 1, aliquot "+df_final["AliquotID"]+"\""

del df_final["Position"]
df_final.rename(columns={"PositionNum": "Position"}, inplace=True)

df_final.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1_X97-X00.csv", header=True, index=False)

df_final.loc[df_final["StimulusID"] > 14, "Level3"] = df_final["Level3"].str.replace("S08-14", "S15-21")
df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S15-21", "S22-29")
df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S22-29", "S22-28")
df_final.loc[df_final["StimulusID"] > 28, "Level3"] = df_final["Level3"].str.replace("S22-28", "S29-35")
df_final.loc[df_final["StimulusID"] > 35, "Level3"] = df_final["Level3"].str.replace("S29-35", "S36-40")
df_final["Level3_Descr"] = "\"Drawer with Plasma for donors X97 to X00, stimulus 1 to 7, visit 1, aliquot "+df_final["AliquotID"]+"\""
df_final.loc[df_final["StimulusID"] > 7, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("1 to 7", "8 to 14")
df_final.loc[df_final["StimulusID"] > 14, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("8 to 14", "15 to 21")
df_final.loc[df_final["StimulusID"] > 21, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("15 to 21", "22 to 28")
df_final.loc[df_final["StimulusID"] > 28, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("22 to 28", "29 to 35")
df_final.loc[df_final["StimulusID"] > 35, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("29 to 35", "36 to 40")
df_final["StimulusID"] = df_final["StimulusID"].astype(str)
df_final["Box"] = "MIC_S"+df_final["StimulusID"]+"_V1_A"+df_final["AliquotID"]+"_DX97-X00"
df_final["Box_Descr"] = "\"Box of stimulus "+df_final["StimulusID"]+", for donors X97 to X00, visit 1, aliquot "+df_final["AliquotID"]+"\""
df_final["DonorID"] = df_final["DonorID"].astype(str)
df_final["Description"] = "\"Donor "+df_final["DonorID"]+", stimulus "+df_final["StimulusID"]+", visit 1, aliquot "+df_final["AliquotID"]+"\""
df_final.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1_X97-X00.csv", header=True, index=False)

import pandas as pd
df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1.csv")
df_labkey = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/Common/samples_table_labkey.csv")
del df_labkey["id"], df_labkey["auditTrail"]
df_40d = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1_X97-X00.csv")

df_lk_plasma = df_labkey.loc[df_labkey["type"].str.contains("PLASMA_")]
df_lk_plasma.rename(columns={"barcodeId": "BarcodeID", "donorId": "DonorID", "visitId": "VisitID", "stimulusId": "StimulusID", "aliquotId": "AliquotID"}, inplace=True)

df_lk_tomerge = df_lk_plasma[["BarcodeID", "DonorID", "VisitID", "AliquotID", "StimulusID", "batchId", "insertDate", "updateDate"]]
df_lk_tomerge = df_lk_tomerge.loc[df_lk_tomerge["VisitID"]==1]

df_all = pd.concat([df, df_40d])

df_merged = pd.merge(df_all, df_lk_tomerge, on=["DonorID", "VisitID", "AliquotID", "StimulusID"])
del df_merged["BatchID"], df_merged["Name"], df_merged["CreationDate"]
df_merged.rename(columns={"batchId": "BatchID", "BarcodeID": "Name", "insertDate": "CreationDate", "updateDate": "UpdateDate"}, inplace=True)
df_merged.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1_all.csv", header=True, index=False)
