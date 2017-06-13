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
parser.add_argument('-o', '--output', required=True,
                    help="""Output file name of sources vials that will be
                         generate in CSV format for FreezerPro""")
parser.add_argument('-v', '--verbose', required=False,
                    help="""If set, will display text of each kind of step.
                    Accepted values:
                        - True
                        - T
                        - Yes
                        - Y
                        - 1
                    """)
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_database = args['database']
f_location = args['location']
s_samples = args['output']
verbose = args['verbose']

if verbose in ["True", "T", "Yes", "Y", 1]:
    verbose = True
else:
    verbose = False

try:
    df_freez = pd.read_csv(f_freezer, dtype=object)
    if verbose:
        print("Read file {} of Freezer hierarchy:".format(f_freezer))
        print("> Extracted {} lines and {} columns.".format(df_freez.shape[0], \
                                                            df_freez.shape[1]))
except IOError:
    print("File '{}' does not exist".format(f_freezer))
    exit()

try:
    df_database = pd.read_csv(f_database, sep="\t", dtype=object)
    if verbose:
        print("Read data file {} with info about source tubes and aliquots".format(f_database))
        print("> Extracted {} lines and {} columns.".format(df_database.shape[0], \
                                                          df_database.shape[1]))
except IOError:
    print("File '{}' does not exist".format(f_database))
    exit()

try:
    df_location = pd.read_csv(f_location, dtype=object)
    if verbose:
        print("Read file {} with tubes location:".format(f_location))
        print("> Extracted {} lines and {} columns.".format(df_location.shape[0], \
                                                          df_location.shape[1]))
except IOError:
    print("File '{}' does not exist".format(f_location))
    exit()

if verbose:
    print("...")
    print("Process sources...")

common_cols = ["Id", "DonorId", "VisitId", "AliquotId", "AliquotingDate", \
                "Comments"]
df_source = df_database[common_cols].copy()
if verbose:
    print("Extracted {} columns from {}:".format(len(common_cols), f_database))
    print("\n".join(["+ {}".format(c) for c in common_cols]))
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

if verbose:
    print("...")
    print("Process sources location...")

df_src_loc = pd.merge(df_source, df_location, on="BARCODE")

if verbose:
    print("> Merged files {} and {}, using column BARCODE.".format(f_database, \
                                                                 f_location))
    print("> Result of merge contains {} lines for {} columns.".format(df_src_loc.shape[0], \
                                                                     df_src_loc.shape[1]))
del df_src_loc["index"]

if verbose:
    print("...")
    print("Process FreezerPro formating...")

df_src_frz_loc = pd.merge(df_src_loc, df_freez, \
                            on=["Level1", "Level3", "Box_Descr"])
if verbose:
    print("> Merged sources data and file {}, using columns Level1, Level2 and Level3.".format(f_freezer))
    print("> Result of merge contains {} lines for {} columns.".format(df_src_frz_loc.shape[0], \
                                                                     df_src_frz_loc.shape[1]))
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
                                       ", Aliquot " + \
                                       df_src_frz_loc["AliquotID"] + "\""
df_src_frz_loc.loc[:, "Level2"] = df_src_frz_loc["Level3"]
df_src_frz_loc.loc[:, "Level2_Descr"] = df_src_frz_loc["Level3_Descr"]
del df_src_frz_loc["Level3"], df_src_frz_loc["Level3_Descr"], \
    df_src_frz_loc["CapColor"]
df_src_frz_loc.loc[:, "FreezerBarcode"] = df_src_frz_loc["Freezer"]
df_src_frz_loc.loc[:, "ShelfBarcode"] = df_src_frz_loc["Level1"]
df_src_frz_loc.loc[:, "RackBarcode"] = df_src_frz_loc["Level2"]

df_src_frz_loc.to_csv(s_samples, header = True, index = False)
if verbose:
    print("> Final output contains {} lines for {} columns.".format(df_src_frz_loc.shape[0], \
                                                                      df_src_frz_loc.shape[1]))
