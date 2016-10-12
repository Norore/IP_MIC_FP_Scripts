#!/usr/bin/env python
import pandas as pd
import json

df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/freezers_supernatants.csv")
df["VisitID"] = df["Level3"].str.replace(r"MIC_Plasma_S\d{2}-\d{2}_V(\d{1})_A\d{1}", r"\1")
df["AliquotID"] = df["Level3"].str.replace(r"MIC_Plasma_S\d{2}-\d{2}_V\d{1}_A(\d{1})", r"\1")
df["StimulusID"] = df["Box"].str.replace(r"MIC_S(\d{1,2})_V\d{1}_A\d{1}_D\d{1,3}-\d{1,3}", r"\1")
df["StimulusID"] = df["StimulusID"].str.replace(r"(\d{1,2}) \d{1,2}", r"\1")

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
dff = pd.merge(df, dp, on=["VisitID", "AliquotID", "StimulusID"])
dfd = dff.loc[dff["VisitID"] == '1']
dfd["Position"] = dfd["Position"].astype(str)
dfd["DonorID"] = dfd["Level2"].str.replace(r"D(\d)\d{2}>>\d{3}_V\d", r"\1")+"00"
dfd["DonorID"] = dfd["DonorID"].astype(int)
dfd["Position"] = dfd["Position"].astype(int)
dfd["DonorID"] = dfd["DonorID"]+dfd["Position"]

with open("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/donors_X97_X00.json", "r") as infile:
    donors = json.load(infile)

lines=[]
for col in donors:
    for num, val in enumerate(donors[col]):
        lines.append([col+"/"+str(num+1), val])

dd = pd.DataFrame(lines, columns=["Position","DonorID"], dtype=object)
dp = pd.DataFrame([str(col)+"/"+str(line+1) for col in ['A', 'B', 'C', 'D', 'E',
                                        'F', 'G', 'H'] for line in range(0, 12)],
                   columns=["Position"])
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

del df_tokeep["Position"]
df_tokeep.rename(columns={"PositionNum": "Position"}, inplace=True)

dfd["StimulusID"] = dfd["StimulusID"].astype(int)
dfd = pd.merge(dfd, dfs, on=["StimulusID"])

df_final = pd.concat([dfd, pd.merge(df_tokeep, dfs, on="StimulusID")])
df_final.reset_index(inplace=True)
del(df_final["index"])

df_final["Volume"] = 400.0
df_final["Sample Type"] = "PLASMA"
df_final["ThawCycle"] = 0
df_final["CreationDate"] = "05/10/2016"
df_final["BatchID"] = "A"
df_final["Name"] = [334090000+i for i in range(0, len(df_final))]
df_final["Sample Source"] = df_final["DonorID"]


df_final["VisitID"] = df_final["VisitID"].astype(str)
df_final["AliquotID"] = df_final["AliquotID"].astype(int)
df_final["Freezer"] = "MIC_Freezer_1532"
df_final.loc[df_final["AliquotID"] == 2, "Freezer"] = df_final["Freezer"].str.replace("32", "34")
df_final.loc[df_final["AliquotID"] == 3, "Freezer"] = df_final["Freezer"].str.replace("32", "35")
df_final["Freezer_Descr"] = "Freezer 1532"
df_final.loc[df_final["AliquotID"] == 2, "Freezer_Descr"] = df_final["Freezer_Descr"].str.replace("32", "34")
df_final.loc[df_final["AliquotID"] == 3, "Freezer_Descr"] = df_final["Freezer_Descr"].str.replace("32", "35")
df_final["Level1"] = "MIC Freezer1532 Shelf1"
df_final.loc[df_final["AliquotID"] == 2, "Level1"] = df_final["Level1"].str.replace("32", "34")
df_final.loc[df_final["AliquotID"] == 3, "Level1"] = df_final["Level1"].str.replace("32", "35")
df_final["Level1_Descr"] = "Shelf 1"
df_final["Level2"] = "DX97>>X00_V1"
df_final.loc[(df_final["DonorID"] >= 1) & (df_final["DonorID"] <= 96), "Level2"] = "D001>>096_V1"
df_final.loc[(df_final["DonorID"] >= 101) & (df_final["DonorID"] <= 196), "Level2"] = "D101>>196_V1"
df_final.loc[(df_final["DonorID"] >= 201) & (df_final["DonorID"] <= 296), "Level2"] = "D201>>296_V1"
df_final.loc[(df_final["DonorID"] >= 301) & (df_final["DonorID"] <= 396), "Level2"] = "D301>>396_V1"
df_final.loc[(df_final["DonorID"] >= 401) & (df_final["DonorID"] <= 496), "Level2"] = "D401>>496_V1"
df_final.loc[(df_final["DonorID"] >= 501) & (df_final["DonorID"] <= 596), "Level2"] = "D501>>596_V1"
df_final.loc[(df_final["DonorID"] >= 601) & (df_final["DonorID"] <= 696), "Level2"] = "D601>>696_V1"
df_final.loc[(df_final["DonorID"] >= 701) & (df_final["DonorID"] <= 796), "Level2"] = "D701>>796_V1"
df_final.loc[(df_final["DonorID"] >= 801) & (df_final["DonorID"] <= 896), "Level2"] = "D801>>896_V1"
df_final.loc[(df_final["DonorID"] >= 901) & (df_final["DonorID"] <= 996), "Level2"] = "D901>>996_V1"
df_final["Level2_Descr"] = "\"Rack donors X97 to X00, Visit "+df_final["VisitID"]+"\""
df_final.loc[(df_final["DonorID"] >= 1) & (df_final["DonorID"] <= 96), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"1 to 96")
df_final.loc[(df_final["DonorID"] >= 101) & (df_final["DonorID"] <= 196), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"101 to 196")
df_final.loc[(df_final["DonorID"] >= 201) & (df_final["DonorID"] <= 296), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"201 to 296")
df_final.loc[(df_final["DonorID"] >= 301) & (df_final["DonorID"] <= 396), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"301 to 396")
df_final.loc[(df_final["DonorID"] >= 401) & (df_final["DonorID"] <= 496), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"401 to 496")
df_final.loc[(df_final["DonorID"] >= 501) & (df_final["DonorID"] <= 596), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"501 to 596")
df_final.loc[(df_final["DonorID"] >= 601) & (df_final["DonorID"] <= 696), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"601 to 696")
df_final.loc[(df_final["DonorID"] >= 701) & (df_final["DonorID"] <= 796), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"701 to 796")
df_final.loc[(df_final["DonorID"] >= 801) & (df_final["DonorID"] <= 896), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"801 to 896")
df_final.loc[(df_final["DonorID"] >= 901) & (df_final["DonorID"] <= 996), "Level2_Descr"] = df_final["Level2_Descr"].str.replace(r"X97 to X00", r"901 to 996")
df_final["AliquotID"] = df_final["AliquotID"].astype(str)
df_final["Level3"] = "MIC_Plasma_"+df_final["Level2"]+"_S01-07_V"+df_final["VisitID"]+"_A"+df_final["AliquotID"]
df_final.loc[df_final["StimulusID"] > 7, "Level3"] = df_final["Level3"].str.replace("S01-07", "S08-14")
df_final.loc[df_final["StimulusID"] > 14, "Level3"] = df_final["Level3"].str.replace("S08-14", "S15-21")
df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S15-21", "S22-28")
df_final.loc[df_final["StimulusID"] > 28, "Level3"] = df_final["Level3"].str.replace("S22-28", "S29-35")
df_final.loc[df_final["StimulusID"] > 35, "Level3"] = df_final["Level3"].str.replace("S29-35", "S36-40")
df_tmp = df_final["Level2_Descr"].str.extract(r"(X?\d+) to (X?\d+)")
df_tmp.rename(columns={0: "from", 1: "to"}, inplace=True)
df_final["Level3_Descr"] = "\"Drawer with Plasma for donors "+df_tmp["from"]+\
                            " to "+df_tmp["to"]+", stimulus 1 to 7, visit "+\
                            df_final["VisitID"]+", aliquot "+df_final["AliquotID"]+"\""
df_final.loc[df_final["StimulusID"] > 7, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("1 to 7", "8 to 14")
df_final.loc[df_final["StimulusID"] > 14, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("8 to 14", "15 to 21")
df_final.loc[df_final["StimulusID"] > 21, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("15 to 21", "22 to 28")
df_final.loc[df_final["StimulusID"] > 28, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("22 to 28", "29 to 35")
df_final.loc[df_final["StimulusID"] > 35, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("29 to 35", "36 to 40")

df_final["StimulusID"] = df_final["StimulusID"].astype(str)
df_final["Box"] = "MIC_S"+df_final["StimulusID"]+"_V"+df_final["VisitID"]+"_A"+\
                    df_final["AliquotID"]+"_D"+df_tmp["from"]+"-"+df_tmp["to"]
df_final["Box_Descr"] = "\"Box of stimulus "+df_final["StimulusID"]+\
                        ", for donors "+df_tmp["from"]+" to "+df_tmp["to"]+\
                        ", visit "+df_final["VisitID"]+", aliquot "+\
                        df_final["AliquotID"]+"\""
df_final["BoxType"] = "96 (12 x 8) Well Plate"
df_final["DonorID"] = df_final["DonorID"].astype(str)
df_final["Description"] = "\"Donor "+df_final["DonorID"]+", stimulus "+df_final["StimulusID"]+", visit 1, aliquot "+df_final["AliquotID"]+"\""

# df_final.loc[df_final["StimulusID"] > 14, "Level3"] = df_final["Level3"].str.replace("S08-14", "S15-21")
# df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S15-21", "S22-29")
# df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S22-29", "S22-28")
# df_final.loc[df_final["StimulusID"] > 28, "Level3"] = df_final["Level3"].str.replace("S22-28", "S29-35")
# df_final.loc[df_final["StimulusID"] > 35, "Level3"] = df_final["Level3"].str.replace("S29-35", "S36-40")
# df_final["Level3_Descr"] = "\"Drawer with Plasma for donors X97 to X00, stimulus 1 to 7, visit 1, aliquot "+df_final["AliquotID"]+"\""
# df_final.loc[df_final["StimulusID"] > 7, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("1 to 7", "8 to 14")
# df_final.loc[df_final["StimulusID"] > 14, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("8 to 14", "15 to 21")
# df_final.loc[df_final["StimulusID"] > 21, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("15 to 21", "22 to 28")
# df_final.loc[df_final["StimulusID"] > 28, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("22 to 28", "29 to 35")
# df_final.loc[df_final["StimulusID"] > 35, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("29 to 35", "36 to 40")
# df_final["StimulusID"] = df_final["StimulusID"].astype(str)
# df_final["Box"] = "MIC_S"+df_final["StimulusID"]+"_V1_A"+df_final["AliquotID"]+"_DX97-X00"
# df_final["Box_Descr"] = "\"Box of stimulus "+df_final["StimulusID"]+", for donors X97 to X00, visit 1, aliquot "+df_final["AliquotID"]+"\""
# df_final["DonorID"] = df_final["DonorID"].astype(str)
# df_final["Description"] = "\"Donor "+df_final["DonorID"]+", stimulus "+df_final["StimulusID"]+", visit 1, aliquot "+df_final["AliquotID"]+"\""

df_labkey = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/Common/samples_table_labkey.csv")
del df_labkey["id"], df_labkey["auditTrail"]

df_lk_plasma = df_labkey.loc[df_labkey["type"].str.contains("PLASMA_")]
df_lk_plasma.rename(columns={"barcodeId": "BarcodeID", "donorId": "DonorID", "visitId": "VisitID", "stimulusId": "StimulusID", "aliquotId": "AliquotID"}, inplace=True)

df_lk_tomerge = df_lk_plasma[["BarcodeID", "DonorID", "VisitID", "AliquotID", "StimulusID", "batchId", "insertDate", "updateDate"]]
df_lk_tomerge = df_lk_tomerge.loc[df_lk_tomerge["VisitID"]==1]
df_lk_tomerge["StimulusID"] = df_lk_tomerge["StimulusID"].astype(int)

df_final["DonorID"] = df_final["DonorID"].astype(int)
df_final["StimulusID"] = df_final["StimulusID"].astype(int)
df_final["AliquotID"] = df_final["AliquotID"].astype(int)
df_final["VisitID"] = df_final["VisitID"].astype(int)

from_labkey = sorted(list(set(df_lk_tomerge["DonorID"].unique())-set(df_final["DonorID"].unique())))
print("\n".join([str(i+1)+": "+ str(d) for i,d in enumerate(from_labkey)]))
print "nb DonorID only from labkey:",len(from_labkey)

df_merged = pd.merge(df_final, df_lk_tomerge, on=["DonorID", "VisitID", "AliquotID", "StimulusID"])
del df_merged["BatchID"], df_merged["Name"], df_merged["CreationDate"]
df_merged.rename(columns={"batchId": "BatchID", "BarcodeID": "Name", "insertDate": "CreationDate", "updateDate": "UpdateDate"}, inplace=True)

df_merged.to_csv("/Users/nlaviell/TC_supernatants_samples_V1_all.csv", header=True, index=False)
