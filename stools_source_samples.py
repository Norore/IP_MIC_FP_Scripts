#!/usr/bin/env python
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description="""Generate stools samples
                                             for FreezerPro from our data Excel
                                             file""")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-d', '--database', required=True,
                    help="""File that contains data from database for all
                         stools data.""")
parser.add_argument('-l', '--location', required=True,
                    help="""File that contains location of each tubes in each
                         box for stools source samples""")
parser.add_argument('-v', '--verbose', required=False,
                    help="""If set, will display text of each kind of step.
                    Accepted values:
                        - True
                        - T
                        - Yes
                        - Y
                        - 1
                    """)
parser.add_argument('-o', '--output', required=True,
                    help="""Output file name of sources vials that will be
                         generate in CSV format for FreezerPro""")
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_database = args['database']
f_location = args['location']
s_samples = args['output']
verbose = args['verbose']

if verbose in ["True", "T", "Yes", "Y", "1"]:
    verbose = True
else:
    verbose = False

try:
    df_freez = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_freezer))
    exit()

try:
    df_database = pd.read_csv(f_database, sep="\t", dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_database))
    exit()

try:
    df_location = pd.read_csv(f_location, dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_database))
    exit()

common_cols = ["Id", "DonorId", "VisitId", "AliquotId", "AliquotingDate", \
                "Comments"]
df_source = df_database[common_cols].copy()
df_source.rename(columns={"Id": "BARCODE",
                          "DonorId": "DonorID",
                          "VisitId": "VisitID",
                          "AliquotId": "AliquotID"},
                 inplace=True)
df_source.loc[:, "CapColor"] = "Green"
df_source.loc[((df_source["AliquotID"] == "1") & (df_source["VisitID"] == "1")),
              "CapColor"] = "Red"
df_source.loc[((df_source["AliquotID"] == "1") & (df_source["VisitID"] == "2")),
              "CapColor"] = "Blue"
df_source.loc[((df_source["AliquotID"] == "2") & (df_source["VisitID"] == "2")),
            "CapColor"] = "White"

df_src_loc = pd.merge(df_source, df_location, on="BARCODE")
del df_src_loc["index"]

df_src_frz_loc = pd.merge(df_src_loc, df_freez, \
                            on=["Level1", "Level3", "Box_Descr"])

df_src_frz_loc.loc[:, "BOX_BARCODE"] = df_src_frz_loc["BOX_BARCODE"].str.\
                                       replace(r"_5mL", r"_5ml")
df_src_frz_loc.loc[:, "Box"] = df_src_frz_loc["BOX_BARCODE"]
df_src_frz_loc.loc[:, "Box_Descr"] = df_src_frz_loc["BOX_BARCODE"].str.\
                                     replace(r"MIC_Feces_(Box)([0-9]{2})_5ml", \
                                             r"\1 \2") + \
                                     " of " + df_src_frz_loc["Level2"]
df_src_frz_loc.loc[:, "Box_Descr"] = "\"" + df_src_frz_loc["Box_Descr"] + \
                                     ", Visit " + df_src_frz_loc["VisitID"] + \
                                     ", Aliquot " + \
                                     df_src_frz_loc["AliquotID"] + "\""
df_src_frz_loc.loc[:, "Box_Descr"] = df_src_frz_loc["Box_Descr"].str.\
                                     replace(r'0([0-9]{1})', r'\1')
df_src_frz_loc.loc[:, "Level3_Descr"] = "\"" + df_src_frz_loc["Level2"] + \
                                        ", " + df_src_frz_loc["Level3"] + "\""
df_src_frz_loc.loc[:, "Sample Type"] = "Stool Source " + \
                                       df_src_frz_loc["CapColor"] + \
                                       " Cap"
df_src_frz_loc.loc[:, "Sample Source"] = df_src_frz_loc["DonorID"]
df_src_frz_loc.loc[:, "Description"] = "\"Donor " + df_src_frz_loc["DonorID"] + \
                                       ", Visit " + \
                                       df_src_frz_loc["VisitID"] + \
                                       ", Aliquot" + \
                                       df_src_frz_loc["AliquotID"] + "\""
df_src_frz_loc.loc[:, "FreezerBarcode"] = df_src_frz_loc["Freezer"]
df_src_frz_loc.loc[:, "ShelfBarcode"] = df_src_frz_loc["Level1"]
df_src_frz_loc.loc[:, "RackBarcode"] = df_src_frz_loc["Level2"]
df_src_frz_loc.loc[:, "DrawerBarcode"] = df_src_frz_loc["Level3"]
del df_src_frz_loc["CapColor"]

print("df_src_frz_loc.head()")
print(df_src_frz_loc.head())
print(df_src_frz_loc.shape)
print("df_src_frz_loc.loc[0]")
print(df_src_frz_loc.loc[0])
# print("df_src_frz_loc.loc[845]")
# print(df_src_frz_loc.loc[845])
# print("df_src_frz_loc.loc[879]")
# print(df_src_frz_loc.loc[879])

# df_source.to_csv(s_samples, header = True, index = False)
