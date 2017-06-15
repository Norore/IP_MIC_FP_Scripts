#!/usr/bin/env python
"""
# Supernatant Visit 1 creation

## Objective

From freezer mapping and knowledge of how the tubes are stored in each box,
will generate an output file for implementation into FreezerPro for the
TruCulture supernatants, in Visit 1.

## Expected file formats read

freezer mapping (../DataToImport/freezers_supernatants.csv), with fields:
     1. Freezer: freezer name
     2. Freezer_Descr: freezer description
     3. Level1: level 1 name (Shelf)
     4. Level1_Descr: level 1 description
     5. Level2: level 2 name (Rack)
     6. Level2_Descr: level 2 description
     7. Level3: level 3 name (Drawer)
     8. Level3_Descr: level 3 description
     9. Box: box name
    10. Box_Descr: box description
    11. BoxType: box type (96 (12 x 8) Well Plate)

specific donors mapping (../DataToPrepare/donors_X97_X00.json), will look like:
{
  "A": [97, 197, 297, 397, 497, 597, 697, 797, 897, 997],
  "B": [98, 198, 298, 398, 498, 598, 698, 798, 898, 998],
  "C": [99, 199, 299, 399, 499, 599, 699, 799, 899, 999],
  "D": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
}
where key "A" is the line value in box, and value in list form is the DonorID
in each well of current line.

stimulus informations (../DataToPrepare/LabExMI_Stimuli_List.csv), with fields:
    1. stimulusId: stimulus ID
    2. name: stimulus name
    3. type: stimulus type
    4. description: stimulus description
    5. sensor: stimulus sensor

labkey database file (../DataToPrepare/Common/samples_table_labkey.csv), with
fields:
    1. id: line number
    2. barcodeId: tube barcode
    3. donorId: donor ID
    4. visitId: visit ID
    5. batchId: batch ID
    6. type: type of sample
    7. stimulusId: stimulus ID
    8. volume: sample volume
    9. aliquotId: aliquot ID
    10. rackId: rack ID
    11. well: tube position in box
    12. auditTrail: ?
    13. deleted: ?
    14. insertDate: insertion date
    15. updateDate: update date

## Expected file formats writted
Supernatant Visit 1 output to implement in FreezerPro
(../DataToImport/TC_supernatants_samples_V1_all_20161027.csv), with fields:
     1. AliquotID: aliquot ID
     2. Box: box name
     3. BoxType: box type (96 (12 x 8) Well Plate)
     4. Box_Descr: box description
     5. DonorID: donor ID
     6. Freezer: freezer name
     7. Freezer_Descr: freezer description
     8. Level1: level 1 name (Shelf)
     9. Level1_Descr: level 1 description
    10. Level2: level 2 name (Rack)
    11. Level2_Descr: level 2 description
    12. Level3: level 3 name (Drawer)
    13. Level3_Descr: level 3 description
    14. Position: tube position in box
    15. StimulusID: stimulus ID
    16. StimulusName: stimulus name
    17. VisitID: visit ID
    18. Volume: sample volume
    19. ThawCycle: sample thaw cycle
    20. Sample Source: sample source, donor ID in cohort
    21. Description: tube description
    22. Sample Type: sample type (PLASMA_1/2/3)
    23. Name: tube name
    24. BatchID: batch ID
    25. CreationDate: sample creation date
    26. UpdateDate: sample update date
    27. FreezerBarcode: freezer barcode (in user-defined field)
    28. ShelfBarcode: shelf barcode (in user-defined field)
    29. RackBarcode: rack barcode (in user-defined field)
    30. DrawerBarcode: drawer barcode (in user-defined field)
    31. BOX_BARCODE: box barcode (FreezerPro field?)
    32. BoxBarcode: box barcode (in user-defined field)
"""

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
df_final.loc[(df_final["DonorID"] >= 101) & (df_final["DonorID"] <= 196), "Level1"] = df_final["Level1"].str.replace("Shelf1", "Shelf2")
df_final.loc[(df_final["DonorID"] >= 301) & (df_final["DonorID"] <= 396), "Level1"] = df_final["Level1"].str.replace("Shelf1", "Shelf2")
df_final.loc[(df_final["DonorID"] >= 501) & (df_final["DonorID"] <= 596), "Level1"] = df_final["Level1"].str.replace("Shelf1", "Shelf2")
df_final.loc[(df_final["DonorID"] >= 701) & (df_final["DonorID"] <= 796), "Level1"] = df_final["Level1"].str.replace("Shelf1", "Shelf2")
df_final.loc[(df_final["DonorID"] >= 901) & (df_final["DonorID"] <= 996), "Level1"] = df_final["Level1"].str.replace("Shelf1", "Shelf2")

df_final["Level1_Descr"] = "Shelf 1"
df_final.loc[(df_final["DonorID"] >= 101) & (df_final["DonorID"] <= 196), "Level1_Descr"] = df_final["Level1_Descr"].str.replace("1", "2")
df_final.loc[(df_final["DonorID"] >= 301) & (df_final["DonorID"] <= 396), "Level1_Descr"] = df_final["Level1_Descr"].str.replace("1", "2")
df_final.loc[(df_final["DonorID"] >= 501) & (df_final["DonorID"] <= 596), "Level1_Descr"] = df_final["Level1_Descr"].str.replace("1", "2")
df_final.loc[(df_final["DonorID"] >= 701) & (df_final["DonorID"] <= 796), "Level1_Descr"] = df_final["Level1_Descr"].str.replace("1", "2")
df_final.loc[(df_final["DonorID"] >= 901) & (df_final["DonorID"] <= 996), "Level1_Descr"] = df_final["Level1_Descr"].str.replace("1", "2")

df_final["AliquotID"] = df_final["AliquotID"].astype(str)

df_final["Level2"] = "MIC_Plasma_DX97-X00_S01-40_V1_A"+df_final["AliquotID"]
df_final.loc[(df_final["DonorID"] >= 1) & (df_final["DonorID"] <= 96), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D001-096")
df_final.loc[(df_final["DonorID"] >= 101) & (df_final["DonorID"] <= 196), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D101-196")
df_final.loc[(df_final["DonorID"] >= 201) & (df_final["DonorID"] <= 296), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D201-296")
df_final.loc[(df_final["DonorID"] >= 301) & (df_final["DonorID"] <= 396), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D301-396")
df_final.loc[(df_final["DonorID"] >= 401) & (df_final["DonorID"] <= 496), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D401-496")
df_final.loc[(df_final["DonorID"] >= 501) & (df_final["DonorID"] <= 596), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D501-596")
df_final.loc[(df_final["DonorID"] >= 601) & (df_final["DonorID"] <= 696), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D601-696")
df_final.loc[(df_final["DonorID"] >= 701) & (df_final["DonorID"] <= 796), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D701-796")
df_final.loc[(df_final["DonorID"] >= 801) & (df_final["DonorID"] <= 896), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D801-896")
df_final.loc[(df_final["DonorID"] >= 901) & (df_final["DonorID"] <= 996), "Level2"] = df_final["Level2"].str.replace(r"DX97-X00", r"D901-996")

df_final["Level2_Descr"] = "\"Rack Donors X97 to X00, Stimulus 1 to 40, Visit "+df_final["VisitID"]+", Aliquot "+df_final["AliquotID"]+"\""
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

df_tmp = df_final["Level2"].str.extract(r"D(X?\d+)-(X?\d+)")
df_tmp.rename(columns={0: "from", 1: "to"}, inplace=True)
df_final["Level3"] = "MIC_Plasma_D"+df_tmp["from"]+"-"+df_tmp["to"]+"_S01-07_V"+df_final["VisitID"]+"_A"+df_final["AliquotID"]
df_final.loc[df_final["Level3"].str.contains("D001-096"), "Level3"] = df_final["Level3"].str.replace(r"D001-096", r"D1-96")
df_final.loc[df_final["StimulusID"] > 7, "Level3"] = df_final["Level3"].str.replace("S01-07", "S08-14")
df_final.loc[df_final["StimulusID"] > 14, "Level3"] = df_final["Level3"].str.replace("S08-14", "S15-21")
df_final.loc[df_final["StimulusID"] > 21, "Level3"] = df_final["Level3"].str.replace("S15-21", "S22-28")
df_final.loc[df_final["StimulusID"] > 28, "Level3"] = df_final["Level3"].str.replace("S22-28", "S29-35")
df_final.loc[df_final["StimulusID"] > 35, "Level3"] = df_final["Level3"].str.replace("S29-35", "S36-40")
df_tmp = df_final["Level2_Descr"].str.extract(r"(X?\d+) to (X?\d+)")
df_tmp.rename(columns={0: "from", 1: "to"}, inplace=True)
df_final["Level3_Descr"] = "\"Drawer with Plasma for Donors "+df_tmp["from"]+\
                            " to "+df_tmp["to"]+", Stimulus 1 to 7, Visit "+\
                            df_final["VisitID"]+", Aliquot "+df_final["AliquotID"]+"\""
df_final.loc[df_final["StimulusID"] > 7, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("1 to 7", "8 to 14")
df_final.loc[df_final["StimulusID"] > 14, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("8 to 14", "15 to 21")
df_final.loc[df_final["StimulusID"] > 21, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("15 to 21", "22 to 28")
df_final.loc[df_final["StimulusID"] > 28, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("22 to 28", "29 to 35")
df_final.loc[df_final["StimulusID"] > 35, "Level3_Descr"] = df_final["Level3_Descr"].str.replace("29 to 35", "36 to 40")

df_final["StimulusID"] = df_final["StimulusID"].astype(str)
df_final["Box"] = "MIC_S"+df_final["StimulusID"]+"_V"+df_final["VisitID"]+"_A"+\
                    df_final["AliquotID"]+"_D"+df_tmp["from"]+"-"+df_tmp["to"]
df_final["Box_Descr"] = "\"Box of Stimulus "+df_final["StimulusID"]+\
                        ", for Donors "+df_tmp["from"]+" to "+df_tmp["to"]+\
                        ", Visit "+df_final["VisitID"]+", Aliquot "+\
                        df_final["AliquotID"]+"\""
df_final["BoxType"] = "96 (12 x 8) Well Plate"

# replacement donors
df_final.loc[df_final["DonorID"] == 96, "DonorID"] = 5096
df_final.loc[df_final["DonorID"] == 104, "DonorID"] = 5104
df_final.loc[df_final["DonorID"] == 122, "DonorID"] = 5122
df_final.loc[df_final["DonorID"] == 167, "DonorID"] = 5167
df_final.loc[df_final["DonorID"] == 178, "DonorID"] = 5178
df_final.loc[df_final["DonorID"] == 219, "DonorID"] = 5219
df_final.loc[df_final["DonorID"] == 268, "DonorID"] = 5268
df_final.loc[df_final["DonorID"] == 279, "DonorID"] = 5279
df_final.loc[df_final["DonorID"] == 303, "DonorID"] = 5303
df_final.loc[df_final["DonorID"] == 308, "DonorID"] = 5308
df_final.loc[df_final["DonorID"] == 534, "DonorID"] = 5534
df_final.loc[df_final["DonorID"] == 701, "DonorID"] = 5701

df_final.loc[df_final["Sample Source"] == 96, "Sample Source"] = 5096
df_final.loc[df_final["Sample Source"] == 104, "Sample Source"] = 5104
df_final.loc[df_final["Sample Source"] == 122, "Sample Source"] = 5122
df_final.loc[df_final["Sample Source"] == 167, "Sample Source"] = 5167
df_final.loc[df_final["Sample Source"] == 178, "Sample Source"] = 5178
df_final.loc[df_final["Sample Source"] == 219, "Sample Source"] = 5219
df_final.loc[df_final["Sample Source"] == 268, "Sample Source"] = 5268
df_final.loc[df_final["Sample Source"] == 279, "Sample Source"] = 5279
df_final.loc[df_final["Sample Source"] == 303, "Sample Source"] = 5303
df_final.loc[df_final["Sample Source"] == 308, "Sample Source"] = 5308
df_final.loc[df_final["Sample Source"] == 534, "Sample Source"] = 5534
df_final.loc[df_final["Sample Source"] == 701, "Sample Source"] = 5701

df_final["DonorID"] = df_final["DonorID"].astype(str)
df_final["Description"] = "\"Donor "+df_final["DonorID"]+", Stimulus "+df_final["StimulusID"]+", Visit 1, Aliquot "+df_final["AliquotID"]+"\""

df_final["Sample Type"] = "PLASMA_"+df_final["AliquotID"]

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

df_merged = pd.merge(df_final, df_lk_tomerge, on=["DonorID", "VisitID", "AliquotID", "StimulusID"])
del df_merged["BatchID"], df_merged["Name"], df_merged["CreationDate"]
df_merged.rename(columns={"batchId": "BatchID", "BarcodeID": "Name", "insertDate": "CreationDate", "updateDate": "UpdateDate"}, inplace=True)

df_merged["CreationDate"] = df_merged["CreationDate"].str.replace(" \d+:\d+:\d+$", "")
df_merged["UpdateDate"] = df_merged["UpdateDate"].str.replace(" \d+:\d+:\d+$", "")

df_merged["FreezerBarcode"] = df_merged["Freezer"]
df_merged["ShelfBarcode"] = df_merged["Level1"]
df_merged["RackBarcode"] = df_merged["Level2"]
df_merged["DrawerBarcode"] = df_merged["Level3"]
df_merged["BOX_BARCODE"] = df_merged["Box"]
df_merged["BoxBarcode"] = df_merged["Box"]

df_merged.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V1_all_20161027.csv", header=True, index=False)
