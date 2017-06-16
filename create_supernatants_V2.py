#!/usr/bin/env python
"""
# TruCulture Supernatant Visit 2 creation

## Objective

From freezer mapping and knowledge of how the tubes are stored in each box,
will generate an output file for implementation into FreezerPro for the
TruCulture supernatants, in Visit 2.

## Expected file formats read

file with data on donor and visit, provided by our LabKey server,
(../DataToPrepare/list_of_donors_visit2.csv), with fields:
     1. SUBJID: donor ID
     2. donorVisitVisit
     3. VISIT0: did the donor come in Visit 0 (pilot study?)
     4. VISIT1: did the donor come in Visit 1
     5. VISIT2: dit the donor come in Visit 2
     6. SVSTYYV0
     7. SVSTMMV0
     8. SVSTDDV0
     9. SVSTYYV0T1
    10. SVSTYYV1
    11. SVSTMMV1
    12. SVSTDDV1
    13. SVSTYYV1T1
    14. SVSTYYV2
    15. SVSTMMV2
    16. SVSTDDV2
    17. SVSTYYV2T1
    18. v1V0DT
    19. v2V1DT

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

labkey database file have a missing donor for Visit 2, donor 402, need to use
file (../DataToPrepare/Common/LabExMISamples_Donor_402_Visit_2_2012_Week_42.csv),
with fields:
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

Supernatant Visit 2 output to implement in FreezerPro
(../DataToImport/TC_supernatants_samples_V2_all_20161027.csv), with fields:
     1. Name: tube name
     2. DonorID: donor ID
     3. VisitID: visit ID
     4. BatchID: batch ID
     5. StimulusID: stimulus ID
     6. AliquotID: aliquot ID
     7. CreationDate: creation date
     8. UpdateDate: update date
     9. Position: tube position in box
    10. Level2: level 2 name (Rack)
    11. Volume: sample volume
    12. StimulusName: stimulus name
    13. ThawCycle: thaw cycle
    14. BoxType: box type (96 (12 x 8) Well Plate)
    15. Freezer: freezer name
    16. Freezer_Descr: freezer description
    17. Level1: level 1 name (Shelf)
    18. Level1_Descr: level 1 description
    19. Level2_Descr: level 2 description
    20. Level3: level 3 name (Drawer)
    21. Level3_Descr: level 3 description
    22. Sample Type: sample type (PLASMA_1/2/3)
    23. Box_Descr: box description
    24. Box: box name
    25. Sample Source: sample source, donor ID in cohort
    26. Description: tube description
    27. FreezerBarcode: freezer barcode (in user-defined field)
    28. ShelfBarcode: shelf barcode (in user-defined field)
    29. RackBarcode: rack barcode (in user-defined field)
    30. DrawerBarcode: drawer barcode (in user-defined field)
    31. BOX_BARCODE: box barcode (FreezerPro field)
    32. BoxBarcode: box barcode (in user-defined field)
"""
import pandas as pd
df_v2 = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/list_of_donors_visit2.csv")

donors = [d for d in df_v2["SUBJID"]]
df = pd.DataFrame({"DonorID": donors, "RackID": 6, "Group": 0})

df.loc[df["DonorID"]==5096, "DonorID"] = 96
df.loc[df["DonorID"]==5104, "DonorID"] = 104
df.loc[df["DonorID"]==5122, "DonorID"] = 122
df.loc[df["DonorID"]==5167, "DonorID"] = 167
df.loc[df["DonorID"]==5178, "DonorID"] = 178
df.loc[df["DonorID"]==5219, "DonorID"] = 219
df.loc[df["DonorID"]==5268, "DonorID"] = 268
df.loc[df["DonorID"]==5279, "DonorID"] = 279
df.loc[df["DonorID"]==5303, "DonorID"] = 303
df.loc[df["DonorID"]==5308, "DonorID"] = 308
df.loc[df["DonorID"]==5534, "DonorID"] = 534
df.loc[df["DonorID"]==5701, "DonorID"] = 701
df.sort_values(by="DonorID", inplace=True)

df.loc[(df["DonorID"] >= 1) & (df["DonorID"] <= 100), "Group"] = 1
df.loc[(df["DonorID"] >= 101) & (df["DonorID"] <= 200), "Group"] = 2
df.loc[(df["DonorID"] >= 201) & (df["DonorID"] <= 300), "Group"] = 1
df.loc[(df["DonorID"] >= 301) & (df["DonorID"] <= 400), "Group"] = 2
df.loc[(df["DonorID"] >= 401) & (df["DonorID"] <= 500), "Group"] = 1
df.loc[(df["DonorID"] >= 501) & (df["DonorID"] <= 600), "Group"] = 2
df.loc[(df["DonorID"] >= 601) & (df["DonorID"] <= 700), "Group"] = 1
df.loc[(df["DonorID"] >= 701) & (df["DonorID"] <= 800), "Group"] = 2
df.loc[(df["DonorID"] >= 801) & (df["DonorID"] <= 900), "Group"] = 1
df.loc[(df["DonorID"] >= 901) & (df["DonorID"] <= 1000), "Group"] = 2

df.loc[(df["DonorID"] >= 1) & (df["DonorID"] <= 200), "RackID"] = 1
df.loc[(df["DonorID"] >= 201) & (df["DonorID"] <= 400), "RackID"] = 2
df.loc[(df["DonorID"] >= 401) & (df["DonorID"] <= 600), "RackID"] = 3
df.loc[(df["DonorID"] >= 601) & (df["DonorID"] <= 800), "RackID"] = 4
df.loc[(df["DonorID"] >= 801) & (df["DonorID"] <= 1000), "RackID"] = 5

racks = pd.DataFrame({"Level2": ["D001>>096_V2 D101>>195_V2",
                                 "D203>>293_V2 D304>>394_V2",
                                 "D402>>497_V2 D507>>597_V2",
                                 "D604>>695_V2 D701>>793_V2",
                                 "D802>>896_V2 D901>>992_V2",
                                 "DX48>>X50_V2"],
                      "RackID": [1, 2, 3, 4, 5, 6]})

l_aliquots = [1, 2, 3]
l_position = [i+1 for i in range(0, 100)]
l_donors = [d for d in df["DonorID"]]
l_stimuli = [i+1 for i in range(0, 40)]
lines = []
for a in l_aliquots:
    for s in l_stimuli:
        for d in l_donors:
            lines.append([a,s,d])

donors_as = pd.DataFrame(lines, columns=["AliquotID", "StimulusID", "DonorID"])

df1 = df[df["RackID"] == 1]
df2 = df[df["RackID"] == 2]
df3 = df[df["RackID"] == 3]
df4 = df[df["RackID"] == 4]
df5 = df[df["RackID"] == 5]

df1["Position"] = [i+1 for i, v in enumerate(df1["DonorID"])]
df2["Position"] = [i+1 for i, v in enumerate(df2["DonorID"])]
df3["Position"] = [i+1 for i, v in enumerate(df3["DonorID"])]
df4["Position"] = [i+1 for i, v in enumerate(df4["DonorID"])]
df5["Position"] = [i+1 for i, v in enumerate(df5["DonorID"])]

df_pos_tmp = pd.concat([df1, df2, df3, df4, df5])

df6 = df_pos_tmp[(df_pos_tmp["Position"] == 49)]
df6 = pd.concat([df6, df_pos_tmp[(df_pos_tmp["Position"] == 50)]])
df6 = pd.concat([df6, df_pos_tmp[(df_pos_tmp["Position"] > 98)]])
df_pos_tmp = df_pos_tmp[df_pos_tmp["Position"] != 49]
df_pos_tmp = df_pos_tmp[df_pos_tmp["Position"] != 50]
df_pos_tmp.loc[df_pos_tmp["Position"] > 48, "Position"] = df_pos_tmp["Position"] - 2
df6["RackID"] = 6
df_pos_tmp = df_pos_tmp[df_pos_tmp["Position"] <= 96]
df6.sort_values(by=["DonorID", "RackID", "Position"], inplace=True)

import string
string.uppercase
letters = [l for l in string.uppercase]
l_lines = letters[:8]

df6_1 = df6[(df6["DonorID"] >= 1) & (df6["DonorID"] <= 100)]
df6_2 = df6[(df6["DonorID"] >= 101) & (df6["DonorID"] <= 200)]
df6_3 = df6[(df6["DonorID"] >= 201) & (df6["DonorID"] <= 300)]
df6_4 = df6[(df6["DonorID"] >= 301) & (df6["DonorID"] <= 400)]
df6_5 = df6[(df6["DonorID"] >= 401) & (df6["DonorID"] <= 500)]
df6_6 = df6[(df6["DonorID"] >= 501) & (df6["DonorID"] <= 600)]
df6_7 = df6[(df6["DonorID"] >= 601) & (df6["DonorID"] <= 700)]
df6_8 = df6[(df6["DonorID"] >= 701) & (df6["DonorID"] <= 800)]
df6_9 = df6[(df6["DonorID"] >= 801) & (df6["DonorID"] <= 900)]
df6_10 = df6[(df6["DonorID"] > 901) & (df6["DonorID"] <= 1000)]

df6_1["Position"] = [letters[i]+"/1" for i, v in enumerate(df6_1["DonorID"])]
df6_2["Position"] = [letters[i]+"/2" for i, v in enumerate(df6_2["DonorID"])]
df6_3["Position"] = [letters[i]+"/3" for i, v in enumerate(df6_3["DonorID"])]
df6_4["Position"] = [letters[i]+"/4" for i, v in enumerate(df6_4["DonorID"])]
df6_5["Position"] = [letters[i]+"/5" for i, v in enumerate(df6_5["DonorID"])]
df6_6["Position"] = [letters[i]+"/6" for i, v in enumerate(df6_6["DonorID"])]
df6_7["Position"] = [letters[i]+"/7" for i, v in enumerate(df6_7["DonorID"])]
df6_8["Position"] = [letters[i]+"/8" for i, v in enumerate(df6_8["DonorID"])]
df6_9["Position"] = [letters[i]+"/9" for i, v in enumerate(df6_9["DonorID"])]
df6_10["Position"] = [letters[i]+"/10" for i, v in enumerate(df6_10["DonorID"])]

df_pos_extra = pd.concat([df6_1, df6_2, df6_3, df6_4, df6_5, df6_6, df6_7, df6_8, df6_9, df6_10])

df_pos = pd.concat([df_pos_tmp, df_pos_extra])
del df["RackID"]
df_donor_pos = pd.merge(df, df_pos)

df_visit2_tmp = pd.merge(df_donor_pos, donors_as)
df_visit2 = pd.merge(df_visit2_tmp, racks)
df_visit2.sort_values(by=["DonorID", "RackID", "Position"], inplace=True)
del df_visit2["RackID"], df_visit2["Group"]

df_visit2["Volume"] = 400.0

df_stim = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/LabExMI_Stimuli_List.csv")
del df_stim["type"], df_stim["description"], df_stim["sensor"]

df_stim.rename(columns={"stimulusId": "StimulusID", "name": "StimulusName"}, inplace = True)
df_visit2_st = pd.merge(df_visit2, df_stim)
df_visit2 = df_visit2_st

df_visit2["ThawCycle"] = 0

df_visit2["BoxType"] = "96 (12 x 8) Well Plate"

df_visit2["Freezer"] = "MIC_Freezer_1532"

df_visit2.loc[df_visit2["AliquotID"] == 2, "Freezer"] = df_visit2["Freezer"].str.replace("32", "34")
df_visit2.loc[df_visit2["AliquotID"] == 3, "Freezer"] = df_visit2["Freezer"].str.replace("32", "35")

df_visit2["Freezer_Descr"] = df_visit2["Freezer"].str.replace(r"MIC_(Freezer)_(\d{4})", r"\1 \2")

df_visit2["Level1"] = "MIC Freezer1532 Shelf3"

df_visit2.loc[df_visit2["AliquotID"] == 2, "Level1"] = df_visit2["Level1"].str.replace("32", "34")
df_visit2.loc[df_visit2["AliquotID"] == 3, "Level1"] = df_visit2["Level1"].str.replace("32", "35")

df_visit2["Level1_Descr"] = df_visit2["Level1"].str.replace(r"MIC Freezer\d{4} (Shelf)(\d)$", r"\1 \2")

df_visit2["AliquotID"] = df_visit2["AliquotID"].astype(str)

df_visit2["Level2"] = "MIC_Plasma_DX49-X50_S01-40_V2_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 1) & (df_visit2["DonorID"] <= 100), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D001-096_D101-195")
df_visit2.loc[(df_visit2["DonorID"] >= 101) & (df_visit2["DonorID"] <= 200), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D001-096_D101-195")
df_visit2.loc[(df_visit2["DonorID"] >= 201) & (df_visit2["DonorID"] <= 300), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D203-293_D304-394")
df_visit2.loc[(df_visit2["DonorID"] >= 301) & (df_visit2["DonorID"] <= 400), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D203-293_D304-394")
df_visit2.loc[(df_visit2["DonorID"] >= 401) & (df_visit2["DonorID"] <= 500), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D402-497_D507-597")
df_visit2.loc[(df_visit2["DonorID"] >= 501) & (df_visit2["DonorID"] <= 600), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D402-497_D507-597")
df_visit2.loc[(df_visit2["DonorID"] >= 601) & (df_visit2["DonorID"] <= 700), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D604-695_D701-793")
df_visit2.loc[(df_visit2["DonorID"] >= 701) & (df_visit2["DonorID"] <= 800), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D604-695_D701-793")
df_visit2.loc[(df_visit2["DonorID"] >= 801) & (df_visit2["DonorID"] <= 900), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50",  r"D802-896_D901-992")
df_visit2.loc[(df_visit2["DonorID"] >= 901) & (df_visit2["DonorID"] <= 1000), "Level2"] = df_visit2["Level2"].str.replace(r"DX49-X50", r"D802-896_D901-992")
df_visit2.loc[df_visit2["Position"].str.contains(r"[A-Z]", na=False), "Level2"] = "MIC_Plasma_DX48-X50_S01-40_V1_A"+df_visit2["AliquotID"]

df_visit2["Level2_Descr"] = "\"Rack Donors X49 to X50, Stimulus 1 to 40, Visit 2, Aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D001")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"1 to 96 and Donors 101 to 195")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D001")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"1 to 96 and Donors 101 to 195")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D203")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"203 to 293 and Donors 304 to 394")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D203")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"203 to 293 and Donors 304 to 394")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D402")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"402 to 497 and Donors 507 to 597")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D402")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"402 to 497 and Donors 507 to 597")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D604")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"604 to 695 and Donors 701 to 793")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D604")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"604 to 695 and Donors 701 to 793")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D802")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"802 to 896 and Donors 901 to 992")
df_visit2.loc[(df_visit2["Level2"].str.contains(r"D802")), "Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"X49 to X50", r"802 to 896 and Donors 901 to 992")
df_visit2.loc[df_visit2["Position"].str.contains(r"[A-Z]", na=False), "Level2_Descr"] = "\"Rack Donors X49 to X50, Stimulus 1 to 40, Visit 2, Aliquot "+df_visit2["AliquotID"]+"\""

df_visit2["VisitID"] = "2"

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

df_visit2.loc[(df_visit2["DonorID"] >= 1) & (df_visit2["DonorID"] <= 100), "Level3"] = "MIC_Plasma_D001-096_D101-195_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 101) & (df_visit2["DonorID"] <= 200), "Level3"] = "MIC_Plasma_D001-096_D101-195_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 201) & (df_visit2["DonorID"] <= 300), "Level3"] = "MIC_Plasma_D203-293_D304-394_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 301) & (df_visit2["DonorID"] <= 400), "Level3"] = "MIC_Plasma_D203-293_D304-394_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 401) & (df_visit2["DonorID"] <= 500), "Level3"] = "MIC_Plasma_D402-497_D507-597_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 501) & (df_visit2["DonorID"] <= 600), "Level3"] = "MIC_Plasma_D402-497_D507-597_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 601) & (df_visit2["DonorID"] <= 700), "Level3"] = "MIC_Plasma_D604-695_D701-793_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 701) & (df_visit2["DonorID"] <= 800), "Level3"] = "MIC_Plasma_D604-695_D701-793_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 801) & (df_visit2["DonorID"] <= 900), "Level3"] = "MIC_Plasma_D802-896_D901-992_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[(df_visit2["DonorID"] >= 901) & (df_visit2["DonorID"] <= 1000), "Level3"] = "MIC_Plasma_D802-896_D901-992_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]
df_visit2.loc[df_visit2["Position"].str.contains("A|B", na=False), "Level3"] = "MIC_Plasma_DX48-X50_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(int)

df_visit2.loc[(df_visit2["StimulusID"] >= 8) & (df_visit2["StimulusID"] <= 14),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"08-14")
df_visit2.loc[(df_visit2["StimulusID"] >= 15) & (df_visit2["StimulusID"] <= 21),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"15-21")
df_visit2.loc[(df_visit2["StimulusID"] >= 22) & (df_visit2["StimulusID"] <= 28),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"22-28")
df_visit2.loc[(df_visit2["StimulusID"] >= 29) & (df_visit2["StimulusID"] <= 35),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"29-35")
df_visit2.loc[(df_visit2["StimulusID"] >= 36) & (df_visit2["StimulusID"] <= 40),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"36-40")

df_visit2["Level3_Descr"] = "\"Drawer with Plasma for Donors 1 to 96 and Donors 101 to 195, Stimulus 1 to 7, Visit 2, Aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[df_visit2["Level3"].str.contains("08-14"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"8 to 14")
df_visit2.loc[df_visit2["Level3"].str.contains("15-21"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"15 to 21")
df_visit2.loc[df_visit2["Level3"].str.contains("22-28"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"22 to 28")
df_visit2.loc[df_visit2["Level3"].str.contains("29-35"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"29 to 35")
df_visit2.loc[df_visit2["Level3"].str.contains("36-40"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"36 to 40")

df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"203 to 293 and Donors 304 to 394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"402 to 497 and Donors 507 to 597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"604 to 695 and Donors 701 to 793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"802 to 896 and Donors 901 to 992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"X48 to X50")

df_visit2["Sample Type"] = "PLASMA_"+df_visit2["AliquotID"]

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

df_visit2["Box_Descr"] = "\"Box of Stimulus "+df_visit2["StimulusID"]+" for Donors 1 to 96 and Donors 101 to 195, Visit 2, Aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"203 to 293 and Donors 304 to 394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"402 to 497 and Donors 507 to 597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"604 to 695 and Donors 701 to 793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"802 to 896 and Donors 901 to 992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and Donors 101 to 195", r"X48 to X50")

df_visit2["Box"] = "MIC_S"+df_visit2["StimulusID"]+"_V2_A"+df_visit2["AliquotID"]+"_D1-96 MIC_S"+df_visit2["StimulusID"]+"_V2_A"+df_visit2["AliquotID"]+"_D101-195"
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box"] = df_visit2["Box"].str.replace(r"1-96", r"203-293")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box"] = df_visit2["Box"].str.replace(r"1-96", r"402-497")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box"] = df_visit2["Box"].str.replace(r"1-96", r"604-695")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box"] = df_visit2["Box"].str.replace(r"1-96", r"802-896")
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box"] = df_visit2["Box"].str.replace(r"101-195", r"304-394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box"] = df_visit2["Box"].str.replace(r"101-195", r"507-597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box"] = df_visit2["Box"].str.replace(r"101-195", r"701-793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box"] = df_visit2["Box"].str.replace(r"101-195", r"901-992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Box"] = "MIC_S"+df_visit2["StimulusID"]+"_V2_A"+df_visit2["AliquotID"]+"_DX48-X50"

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

# replacement donors
df_visit2.loc[df_visit2["DonorID"] == 96, "DonorID"] = 5096
df_visit2.loc[df_visit2["DonorID"] == 104, "DonorID"] = 5104
df_visit2.loc[df_visit2["DonorID"] == 122, "DonorID"] = 5122
df_visit2.loc[df_visit2["DonorID"] == 167, "DonorID"] = 5167
df_visit2.loc[df_visit2["DonorID"] == 178, "DonorID"] = 5178
df_visit2.loc[df_visit2["DonorID"] == 219, "DonorID"] = 5219
df_visit2.loc[df_visit2["DonorID"] == 268, "DonorID"] = 5268
df_visit2.loc[df_visit2["DonorID"] == 279, "DonorID"] = 5279
df_visit2.loc[df_visit2["DonorID"] == 303, "DonorID"] = 5303
df_visit2.loc[df_visit2["DonorID"] == 308, "DonorID"] = 5308
df_visit2.loc[df_visit2["DonorID"] == 534, "DonorID"] = 5534
df_visit2.loc[df_visit2["DonorID"] == 701, "DonorID"] = 5701

df_visit2["Sample Source"] = df_visit2["DonorID"]

df_visit2["DonorID"] = df_visit2["DonorID"].astype(str)

df_visit2["Description"] = '"Donor '+df_visit2["DonorID"]+', Stimulus '+df_visit2["StimulusID"]+', Visit 2, Aliquot '+df_visit2["AliquotID"]+'"'

df_visit2["FreezerBarcode"] = df_visit2["Freezer"]
df_visit2["ShelfBarcode"] = df_visit2["Level1"]
df_visit2["RackBarcode"] = df_visit2["Level2"]
df_visit2["DrawerBarcode"] = df_visit2["Level3"]
df_visit2["BOX_BARCODE"] = df_visit2["Box"]
df_visit2["BoxBarcode"] = df_visit2["Box"]

df_labkey = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/Common/samples_table_labkey.csv")
df_donor_fix = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/Common/LabExMISamples_Donor_402_Visit_2_2012_Week_42.csv")
del df_donor_fix["Unnamed: 15"]

df_labkey = df_labkey.loc[df_labkey["donorId"] != 402]
df_labkey = pd.concat([df_labkey, df_donor_fix])

df_labkey.rename(columns={"barcodeId": "Name", "donorId": "DonorID",
                          "batchId": "BatchID", "stimulusId": "StimulusID",
                          "aliquotId": "AliquotID", "visitId": "VisitID"},
                 inplace=True)
del df_labkey["volume"], df_labkey["id"], df_labkey["well"]
del df_labkey["rackId"], df_labkey["auditTrail"], df_labkey["deleted"]

df_labkey_plasma = df_labkey[df_labkey["type"].str.contains("PLASMA_")]
df_labkey_plasma = df_labkey_plasma[df_labkey_plasma["VisitID"] == 2]

del df_labkey_plasma["type"]

df_labkey_plasma["StimulusID"] = df_labkey_plasma["StimulusID"].astype(int)
df_labkey_plasma["StimulusID"] = df_labkey_plasma["StimulusID"].astype(str)

df_labkey_plasma["CreationDate"] = df_labkey_plasma["insertDate"].str.replace(r" \d+:\d+:\d+$", r"")
df_labkey_plasma["UpdateDate"] = df_labkey_plasma["updateDate"].str.replace(r" \d+:\d+:\d+$", r"")
del df_labkey_plasma["updateDate"], df_labkey_plasma["insertDate"]

df_labkey_plasma["DonorID"] = df_labkey_plasma["DonorID"].astype(str)
df_labkey_plasma["VisitID"] = df_labkey_plasma["VisitID"].astype(str)
df_labkey_plasma["AliquotID"] = df_labkey_plasma["AliquotID"].astype(str)

df_visit2_final = pd.merge(df_labkey_plasma, df_visit2)

df_visit2_final.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V2_all_20161027.csv", header=True, index=False)
