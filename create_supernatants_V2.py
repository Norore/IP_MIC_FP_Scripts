#!/usr/bin/env python

import pandas as pd
df_v2 = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/list_of_donors_visit2.csv")

donors = [d for d in df_v2["SUBJID"]]
df = pd.DataFrame({"DonorID": donors, "RackID": 6})
df.sort_values(by="DonorID", inplace=True)

df.loc[(df["DonorID"] >= 1) & (df["DonorID"] <= 96), "RackID"] = 1
df.loc[(df["DonorID"] >= 101) & (df["DonorID"] <= 195), "RackID"] = 1
df.loc[(df["DonorID"] >= 203) & (df["DonorID"] <= 293), "RackID"] = 2
df.loc[(df["DonorID"] >= 304) & (df["DonorID"] <= 394), "RackID"] = 2
df.loc[(df["DonorID"] >= 402) & (df["DonorID"] <= 497), "RackID"] = 3
df.loc[(df["DonorID"] >= 507) & (df["DonorID"] <= 597), "RackID"] = 3
df.loc[(df["DonorID"] >= 604) & (df["DonorID"] <= 695), "RackID"] = 4
df.loc[(df["DonorID"] >= 701) & (df["DonorID"] <= 793), "RackID"] = 4
df.loc[(df["DonorID"] >= 802) & (df["DonorID"] <= 896), "RackID"] = 5
df.loc[(df["DonorID"] >= 901) & (df["DonorID"] <= 992), "RackID"] = 5

racks = pd.DataFrame({"Level2": ["D001>>096_V2 D101>>195_V2",
                                 "D203>>293_V2 D304>>394_V2",
                                 "D402>>497_V2 D507>>597_V2",
                                 "D604>>695_V2 D701>>793_V2",
                                 "D802>>896_V2 D901>>992_V2",
                                 "DX48>>X50_V2"],
                      "RackID": [1, 2, 3, 4, 5, 6]})

l_aliquots = [1, 2, 3]
l_position = [i+1 for i in range(0, 96)]
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

df6 = df[df["RackID"] == 6]

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
df6_11 = df6[(df6["DonorID"] > 1000)]

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
df6_11["Position"] = [letters[i]+"/11" for i, v in enumerate(df6_11["DonorID"])]

df_pos_extra = pd.concat([df6_1, df6_2, df6_3, df6_4, df6_5, df6_6, df6_7, df6_8, df6_9, df6_10, df6_11])

df_pos = pd.concat([df_pos_tmp, df_pos_extra])

df_donor_pos = pd.merge(df, df_pos)

df_visit2 = pd.merge(df_donor_pos, donors_as)
del df_visit2["RackID"]

df_visit2["Volume"] = 400.0

df_stim = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/LabExMI_Stimuli_List.csv")
del df_stim["type"], df_stim["description"], df_stim["sensor"]

df_stim.rename(columns={"stimulusId": "StimulusID", "name": "StimulusName"}, inplace = True)
df_visit2_st = pd.merge(df_visit2, df_stim)
df_visit2 = df_visit2_st

df_visit2["ThawCycle"] = 0

df_visit2["Sample Source"] = df_visit2["DonorID"]

df_visit2["BoxType"] = "96 (12 x 8) Well Plate"

df_visit2["Freezer"] = "MIC_Freezer_1532"

df_visit2.loc[df_visit2["AliquotID"] == 2, "Freezer"] = df_visit2["Freezer"].str.replace("32", "34")
df_visit2.loc[df_visit2["AliquotID"] == 3, "Freezer"] = df_visit2["Freezer"].str.replace("32", "35")

df_visit2["Freezer_Descr"] = df_visit2["Freezer"].str.replace(r"MIC_(Freezer)_(\d{4})", r"\1 \2")

df_visit2["Level1"] = "MIC Freezer1532 Shelf3"

df_visit2.loc[df_visit2["AliquotID"] == 2, "Level1"] = df_visit2["Level1"].str.replace("32", "34")
df_visit2.loc[df_visit2["AliquotID"] == 3, "Level1"] = df_visit2["Level1"].str.replace("32", "35")

df_visit2["Level1_Descr"] = df_visit2["Level1"].str.replace(r"MIC Freezer\d{4} (Shelf)(\d)$", r"\1 \2")

# df_visit2["Level2"] = "DX48>>X50_V2"
df_visit2["Level2"] = "DX48>>X50_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 1) & (df_visit2["DonorID"] <= 98), "Level2"] = "D001>>096_V2 D101>>195_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 101) & (df_visit2["DonorID"] <= 195), "Level2"] = "D001>>096_V2 D101>>195_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 203) & (df_visit2["DonorID"] <= 293), "Level2"] = "D203>>293_V2 D304>>394_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 304) & (df_visit2["DonorID"] <= 394), "Level2"] = "D203>>293_V2 D304>>394_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 402) & (df_visit2["DonorID"] <= 497), "Level2"] = "D402>>497_V2 D507>>597_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 507) & (df_visit2["DonorID"] <= 597), "Level2"] = "D402>>497_V2 D507>>597_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 604) & (df_visit2["DonorID"] <= 695), "Level2"] = "D604>>695_V2 D701>>793_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 701) & (df_visit2["DonorID"] <= 793), "Level2"] = "D604>>695_V2 D701>>793_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 802) & (df_visit2["DonorID"] <= 896), "Level2"] = "D802>>896_V2 D901>>992_V2"
df_visit2.loc[(df_visit2["DonorID"] >= 901) & (df_visit2["DonorID"] <= 992), "Level2"] = "D802>>896_V2 D901>>992_V2"
df_visit2["Level2_Descr"] = df_visit2["Level2"].str.replace(r"D(\d+)>>(\d+)_V2 D(\d+)>>(\d+)_V(2)", r'"Rack donors \1 to \2 and donors \3 to \4, visit \5"')
df_visit2["Level2_Descr"] = df_visit2["Level2"].str.replace(r"DX(\d+)>>X(\d+)_V(2)", r'"Rack donors X\1 to X\2, visit \3"')
df_visit2["Level2_Descr"] = df_visit2["Level2_Descr"].str.replace(r"001 to 096", r"1 to 96")

df_visit2["VisitID"] = "2"
# df_visit2["VisitID"].astype(str)

df_visit2["AliquotID"] = df_visit2["AliquotID"].astype(str)
df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

df_visit2["Level3"] = "MIC_Plasma_S01-07_V"+df_visit2["VisitID"]+"_A"+df_visit2["AliquotID"]

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(int)

df_visit2.loc[(df_visit2["StimulusID"] >= 8) & (df_visit2["StimulusID"] <= 14),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"08-14")
df_visit2.loc[(df_visit2["StimulusID"] >= 15) & (df_visit2["StimulusID"] <= 21),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"15-21")
df_visit2.loc[(df_visit2["StimulusID"] >= 22) & (df_visit2["StimulusID"] <= 28),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"22-28")
df_visit2.loc[(df_visit2["StimulusID"] >= 29) & (df_visit2["StimulusID"] <= 35),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"29-35")
df_visit2.loc[(df_visit2["StimulusID"] >= 36) & (df_visit2["StimulusID"] <= 40),"Level3"] = df_visit2["Level3"].str.replace(r"01-07", r"36-40")

df_visit2["Level3_Descr"] = "\"Drawer with plasma for donors 1 to 96 and donors 101 to 195, stimulus 1 to 7, visit 2, aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[df_visit2["Level3"].str.contains("08-14"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"8 to 14")
df_visit2.loc[df_visit2["Level3"].str.contains("15-21"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"15 to 21")
df_visit2.loc[df_visit2["Level3"].str.contains("22-28"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"22 to 28")
df_visit2.loc[df_visit2["Level3"].str.contains("29-35"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"29 to 35")
df_visit2.loc[df_visit2["Level3"].str.contains("36-40"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 7", r"36 to 40")

df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"203 to 293 and donors 304 to 394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"402 to 497 and donors 507 to 597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"604 to 695 and donors 701 to 793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"802 to 896 and donors 901 to 992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Level3_Descr"] = df_visit2["Level3_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"X48 to X50")

df_visit2["Sample Type"] = "PLASMA"

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

df_visit2["Box_Descr"] = "\"Box of stimulus "+df_visit2["StimulusID"]+" for donors 1 to 96 and donors 101 to 195, visit 2, aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"203 to 293 and donors 304 to 394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"402 to 497 and donors 507 to 597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"604 to 695 and donors 701 to 793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"802 to 896 and donors 901 to 992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96 and donors 101 to 195", r"X48 to X50")

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

df_visit2["Level3_Descr"].unique()

df_visit2["Box_Descr"] = "\"Box of stimulus "+df_visit2["StimulusID"]+" for donors 1 to 96 and donors 101 to 195, visit 2, aliquot "+df_visit2["AliquotID"]+"\""
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96", r"203 to 293")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96", r"402 to 497")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96", r"604 to 695")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"1 to 96", r"802 to 896")
df_visit2.loc[df_visit2["Level2"].str.contains("D203"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"101 to 195", r"304 to 394")
df_visit2.loc[df_visit2["Level2"].str.contains("D402"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"101 to 195", r"507 to 597")
df_visit2.loc[df_visit2["Level2"].str.contains("D604"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"101 to 195", r"701 to 793")
df_visit2.loc[df_visit2["Level2"].str.contains("D802"), "Box_Descr"] = df_visit2["Box_Descr"].str.replace(r"101 to 195", r"901 to 992")
df_visit2.loc[df_visit2["Level2"].str.contains("DX"), "Box_Descr"] = "\"Box of stimulus "+df_visit2["StimulusID"]+" for donors X48 to X50, visit 2, aliquot "+df_visit2["AliquotID"]+"\""

df_visit2["StimulusID"] = df_visit2["StimulusID"].astype(str)

df_visit2["Box_Descr"] = "\"Box of stimulus "+df_visit2["StimulusID"]+" for donors 1 to 96 and donors 101 to 195, visit 2, aliquot "+df_visit2["AliquotID"]+"\""

df_visit2["Box"] = "MIC_S"+df_visit2["StimulusID"]+"_V2_A"+df_visit2["AliquotID"]+"_D1-96 MIC_S"+df_visit2["StimulusID"]+"_V2_A"+df_visit2["AliquotID"]+"_D101-195"

df_visit2["DonorID"] = df_visit2["DonorID"].astype(str)

df_visit2["Description"] = '"Donor '+df_visit2["DonorID"]+', stimulus '+df_visit2["StimulusID"]+', visit 2, aliquot '+df_visit2["AliquotID"]+'"'

df_labkey = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/Common/samples_table_labkey.csv")
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
df_visit2_final.to_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/TC_supernatants_samples_V2_all_20161010.csv", header=True, index=False)
