#!/usr/bin/env python
import pandas as pd
import argparse
import re
import os
import glob

'''
Initialize arguments
'''

parser = argparse.ArgumentParser(description="""Generate aliquot samples
                    for FreezerPro from original samples file""")
# Freezer file input
parser.add_argument('-i', '--input_file', required=True,
                    help="""Input file with original samples data in CSV format
                    from FreezerPro report""")
# Directory that contains aliquot sample files
parser.add_argument('-d', '--directory', required=True,
                    help="""Directory with aliquot sample files to use""")
# FreezerPro file output
parser.add_argument('-o', '--output_file', required=True,
                    help="""Output file with aliquot samples data in CSV format
                    for FreezerPro import""")
parser.add_argument('-u', '--update_file', required=True,
                    help="""File with original samples data in CSV format
                    for FreezerPro original samples update""")
args = vars(parser.parse_args())

# Freezer file input args
f_input = args['input_file']
# Aliquot sample files directory input args
d_dir = args['directory']
# Output file export args
o_samples = args['output_file']
o_samples_new = re.sub(".csv", "_new.csv", o_samples)
o_samples_upd = re.sub(".csv", "_update.csv", o_samples)
u_samples = args['update_file']

# Read Freezer file input
try:
    df_input = pd.read_csv(f_input, dtype=object)
except IOError:
    print "File '" + f_input + "' does not exist"
    exit()

# Read Aliquot file input
try:
    fic_dir = os.path.join(d_dir, "[0-9]*_TruCSpnttAlqtg_TrackingSheet_[A-Z]*.xlsx")
    l_files = glob.glob(fic_dir.replace('\\', ''))

    fic_dir = os.path.join(d_dir, "[0-9]*_Errors_TruCSpnttAlqtg_TrackingSheet_[A-Z]*.xlsx")
    for f in glob.glob(fic_dir.replace('\\', '')):
        l_files.remove(f)
except IOError:
    print "Directory '" + d_dir + "' does not exist"
    exit()

'''
Defined reusable functions
'''
def df_dtypes_object(dataframe):
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(object)
    return dataframe

def complete_columns(dataframe, list_columns):
    for column in list_columns:
        dataframe[column] = pd.Series([dataframe.loc[0, column]]*len(dataframe))
    return dataframe

# initialize list of dataframes
list_df = []
cols_to_cplt = ["SrcBox_BoxID", "SrcBox_LabExID",
                "Al1Box_BoxID", "Al1Box_LabExID",
                "Al2Box_BoxID", "AliquotingDate"]

print("%d files to read" % len(l_files))

for f_aliquot in l_files:
    print ">>> Works on '"+f_aliquot+"' file <<<"
    try:
        # take all sheets
        dic_aliquots = pd.read_excel(f_aliquot, sheetname = None)
    except IOError:
        print "File '" + f_aliquot + "' does not exist"

    df_aliquot = pd.concat([complete_columns(dic_aliquots[df], cols_to_cplt) \
                            for df in dic_aliquots.keys()])
    df_aliquot["File"] = f_aliquot
    list_df.append(df_aliquot)

try:
    df_aliquot = df_dtypes_object(pd.concat(list_df))
except ValueError:
    print "DataFrame is empty"
    print "Worked on dir " + d_dir

del df_aliquot["Well Expected.2"], df_aliquot["Well Expected.1"], \
    df_aliquot["Al1Box_TubeCtrl"], df_aliquot["Al2Box_TubeCtrl"]
df_aliquot.rename(columns = {"SrcBox_LabExID": "BoxBarcode",
                             "SrcBox_TubeScan": "Name"}, inplace = True)
df_aliquot.loc[:, "Name"] = df_aliquot["Name"].astype(str)
df_aliquot = df_aliquot[df_aliquot.notnull()]
df_aliquot = df_aliquot[df_aliquot["Name"].str.contains("No Read") == False]
df_aliquot = df_aliquot[df_aliquot["Name"].str.contains("No Tube") == False]

df_aliquot = df_aliquot.loc[df_aliquot["Name"] != "(Paste Here output from VisionMate)"]
df_aliquot = df_aliquot.loc[df_aliquot["Name"] != "nan"]

df_aliquot.loc[:, "AliquotingDate"] = df_aliquot["AliquotingDate"].str.replace(r"_[A-Z]*", "")

cols_aliq1 = ["AliquotingDate", "SrcBox_BoxID", "BoxBarcode", \
              "Name", "Al1Box_BoxID", "Al1Box_LabExID", \
              "Al1Box_TubeScan", "Well VisionMate.1"]
df_aliquot1 = df_aliquot[cols_aliq1]
df_aliquot1.rename(columns = {"Well VisionMate.1": "Position"},
                   inplace = True)
df_aliquot1.loc[:, "Name"] = df_aliquot1["Name"].astype(float).astype(int).astype(str)

cols_aliq2 = ["AliquotingDate", "SrcBox_BoxID", "BoxBarcode", \
              "Name", "Al2Box_BoxID", "Al2Box_TubeScan", \
              "Well VisionMate.2"]
df_aliquot2 = df_aliquot[cols_aliq2]
df_aliquot2.rename(columns = {"Well VisionMate.2": "Position"},
                   inplace = True)
df_aliquot2 = df_aliquot2[df_aliquot2["Name"].notnull()]
df_aliquot2 = df_aliquot2[df_aliquot2["Name"].str.contains("[^0-9]") == False]
df_aliquot2.loc[:, "Name"] = df_aliquot2["Name"].astype(float).astype(int).astype(str)

df_input = df_input[["UID", "Name", "Vial Volume", "BoxBarcode"]]

df_al1_fr = pd.merge(df_input, df_aliquot1, on=["Name", "BoxBarcode"])
df_al1_fr.loc[:, "ALIQUOT"] = 1
df_al1_fr.loc[:, "Volume"] = 100.0
del df_al1_fr["Vial Volume"], df_al1_fr["SrcBox_BoxID"], df_al1_fr["Name"], \
    df_al1_fr["BoxBarcode"]
df_al1_fr.rename(columns = {"UID": "ID", "Al1Box_LabExID": "BoxBarcode", \
                            "Al1Box_BoxID": "ThermoBoxBarcode",
                            "Al1Box_TubeScan": "Name"}, \
                 inplace = True)

df_al2_fr = pd.merge(df_input, df_aliquot2, on=["Name", "BoxBarcode"])
df_al2_fr.loc[:, "ALIQUOT"] = 2
df_al2_fr.loc[:, "Volume"] = 100.0
del df_al2_fr["Vial Volume"], df_al2_fr["SrcBox_BoxID"], df_al2_fr["Name"], \
    df_al2_fr["BoxBarcode"]
df_al2_fr.loc[:, "BoxBarcode"] = None
df_al2_fr.rename(columns = {"UID": "ID", \
                            "Al2Box_BoxID": "ThermoBoxBarcode",
                            "Al2Box_TubeScan": "Name"}, \
                 inplace = True)

df_al_fr = pd.concat([df_al1_fr, df_al2_fr])
df_al_fr.loc[:, "Position"] = df_al_fr["Position"].str.replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
df_al_fr.loc[:, "BARCODE"] = df_al_fr["Name"]
df_al_fr.loc[:, "BOX_BARCODE"] = df_al_fr["BoxBarcode"]
df_al_fr.loc[:, "Freezer"] = "MIC_Freezer_1537"
df_al_fr.loc[:, "Freezer_Descr"] = "Freezer 1537"
df_al_fr.loc[df_al_fr["ALIQUOT"] == 2, "BoxBarcode"] = df_al_fr.loc[df_al_fr["ALIQUOT"] == 1, "BoxBarcode"].str.replace("F1", "F2")
df_al_fr.loc[df_al_fr["ALIQUOT"] == 2, "BOX_BARCODE"] = df_al_fr.loc[df_al_fr["ALIQUOT"] == 2, "BoxBarcode"]
df_al_fr.loc[df_al_fr["ALIQUOT"] == 2, "Freezer"] = "Freezer_Outside"
df_al_fr.loc[df_al_fr["ALIQUOT"] == 2, "Freezer_Descr"] = "Freezer Outside of Pasteur Institute"
df_al_fr.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"

keep_cols = ["ALIQUOT", "BoxBarcode", "ID", "Name", \
             "Position", "Volume", "BARCODE", \
             "BOX_BARCODE", "Freezer", "Freezer_Descr", "BoxType"]

df_al_fr[keep_cols].to_csv(o_samples_new, index = False, header = True)

del df_al_fr["BARCODE"]

df_input.rename(columns = {"UID": "ID", "Name": "BARCODE"}, inplace = True)

df_update = pd.merge(df_al_fr, df_input[["ID", "Vial Volume", "BARCODE"]], on="ID")#[["ID", "Vial Volume", "BARCODE", "AliquotingDate", "UpdateDate"]]
# print(df_update.columns)
# exit()
# df_update.loc[:, "BARCODE"] = df_update["Name"]
df_update.loc[:, "Vial Volume"] = df_update["Vial Volume"].astype(float)-(2*100.0)
df_update.loc[:, "UpdateDate"] = df_update["AliquotingDate"].str.replace(r"(\d{4})(\d{2})(\d{2})", r"\3/\2/\1")

df_update[["BARCODE", "Vial Volume", "UpdateDate"]].to_csv(u_samples, index = False, header = True)

df_al_fr.loc[:, "BARCODE"] = df_al_fr["Name"]
df_al_fr.loc[:, "CreationDate"] = df_al_fr["AliquotingDate"].str.replace(r"(\d{4})(\d{2})(\d{2})", r"\3/\2/\1")
df_al_fr.loc[:, "UpdateDate"] = df_al_fr["AliquotingDate"].str.replace(r"(\d{4})(\d{2})(\d{2})", r"\3/\2/\1")

df_al_fr[["BARCODE", "CreationDate", "UpdateDate"]].to_csv(o_samples_upd, index = False, header = True)
