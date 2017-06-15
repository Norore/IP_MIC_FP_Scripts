#!/usr/bin/env python
"""
## Objective

## Expected file formats put in arguments

--frezer, file with freezer data in CSV format for FreezerPro, with fields:
    1. Box: box name in freezer
    2. Freezer: freezer name
    3. Freezer_Descr: freezer description
    4. Level1: level 1 name (Shelf)
    5. Level1_Descr: level 1 description
    6. Level2: level 2 name (Rack)
    7. Level2_Descr: level 2 description
    8. Level3: level 3 name (Drawer)
    9. Level3_Descr: level 3 description

--database, file that contains data from database for all stools data, with
fields:
     1. Id: stool source tube barcode
     2. DonorId: donor ID
     3. VisitId: visit ID
     4. AliquotId: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool sample
     7. Aliquot_1_BC: stool aliquot L tube barcode
     8. Aliquot_1_Weight: stool aliquot L weight sample
     9. Aliquot_1_Plate_Location: stool aliquot L tube position in box
    10. Aliquot_1_Plate_Number: stool aliquot L box barcode
    11. Aliquot_1_DNA_BC: stool DNA tube barcode
    12. Aliquot_1_DNA_Location: stool DNA tube position in box
    13. Aliquot_1_DNA_Box: stool DNA box barcode
    14. Aliquot_1_DNA_Date: stool DNA sample aliquoting date
    15. Aliquot_2_BC: stool aliquot R1 tube barcode
    16. Aliquot_2_Weight: stool aliquot R1 weight sample
    17. Aliquot_2_Plate_Location: stool aliquot R1 tube position in box
    18. Aliquot_2_Plate_Number: stool aliquot R1 box barcode
    19. Aliquot_3_BC: stool aliquot R2 tube barcode
    20. Aliquot_3_Weight: stool aliquot R2 weight sample
    21. Aliquot_3_Plate_Location: stool aliquot R2 tube position in box
    22. Aliquot_3_Plate_Number: stool aliquot R2 box barcode
    23. Aliquot_4_BC: stool aliquot R3 tube barcode
    24. Aliquot_4_Weight: stool aliquot R3 weight sample
    25. Aliquot_4_Plate_Location: stool aliquot R3 tube position in box
    26. Aliquot_4_Plate_Number: stool aliquot R3 box barcode

--location, file that contains location of each tubes in each box for stools
source samples, with fields:
    1. Level1: level 1 name (Shelf)
    2. Level3: level 3 name (Rack)
    3. Box_Descr: box description (Box number)
    4. Position: tube position in box
    5. BARCODE: tube barcode
    6. BOX_BARCODE: box barcode

## Expected file formats output in arguments

--output, output file name of sources vials that will be generate in CSV
format for FreezerPro, with fields:
     1. BARCODE: tube barcode
     2. DonorID: donor ID
     3. VisitID: visit ID
     4. AliquotID: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool sample
     7. Level1: level 1 name (Shelf)
     8. Box_Descr: box description
     9. Position: tube position in box
    10. BOX_BARCODE: box barcode (FreezerPro field?)
    11. Freezer: freezer name
    12. Freezer_Descr: freezer description
    13. Level1_Descr: level 1 description
    14. Level2: level 2 name (Rack)
    15. Level2_Descr: level 2 description
    16. Box: box name
    17. BoxType: box type (48 (12 x 8) Stool Well Plate)
    18. Sample Type: sample type (Stool Source White/Green Cap)
    19. Sample Source: sample source
    20. Description: tube description
    21. FreezerBarcode: freezer barcode (in user-defined fields for the sample type)
    22. ShelfBarcode: shelf barcode (in user-defined fields for the sample type)
    23. RackBarcode: rack barcode (in user-defined fields for the sample type)
    24. BoxBarcode: rack barcode (in user-defined fields for the sample type)

"""

import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description=print(__doc__))
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
# Some barcode were added by hand, so they may have "mL" instead of "ml"
# df_src_frz_loc.loc[:, "BOX_BARCODE"] = df_src_frz_loc["BOX_BARCODE"].str.\
#                                        replace(r"_5mL", r"_5ml")
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
df_src_frz_loc.loc[:, "BoxBarcode"] = df_src_frz_loc["BOX_BARCODE"]

df_src_frz_loc.to_csv(s_samples, header = True, index = False)
if verbose:
    print("> Final output contains {} lines for {} columns.".format(df_src_frz_loc.shape[0], \
                                                                      df_src_frz_loc.shape[1]))
