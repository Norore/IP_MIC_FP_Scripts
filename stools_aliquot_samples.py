#!/usr/bin/env python
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description="""Generate stools aliquot samples
                                             for FreezerPro from our data Excel
                                              file""")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-d', '--directory', required=True,
                    help="""Directory with files that contains informations
                         about the tubes aliquoted.""")
parser.add_argument('-r', '--repository', required=True,
                    help="""Directory with files that contains informations
                         about the tubes location.""")
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
                    help="""Output file name that will be generate in CSV
                         format for FreezerPro""")
args = vars(parser.parse_args())

f_freezer = args['freezer']
d_dir = args['directory']
r_dir = args['repository']
o_samples = args['output']
verbose = args['verbose']

if verbose in ["True", "T", "Yes", "Y", "1"]:
    verbose = True
else:
    verbose = False

if d_dir[-1] != "/":
    d_dir += "/*.csv"
else:
    d_dir += "*.csv"
if r_dir[-1] != "/":
    r_dir += "/*.csv"
else:
    r_dir += "*.csv"

try:
    df_freez = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_freezer))
    exit()

try:
    ld_files = glob.glob(d_dir.replace('\\', ''))
except IOError:
    print("Directory '{}' does not exist".format(d_dir))
    exit()

try:
    lr_files = glob.glob(r_dir.replace('\\', ''))
except IOError:
    print("Directory '{}' does not exist".format(r_dir))
    exit()

# create dataframe for stools metadata
# initialize list of dataframes
if verbose: print("Get files for aliquot of stools metadata:")

list_df = []
for f_stool_md in ld_files:

    if verbose: print(">>> Works on '{}' file <<<".format(f_stool_md))

    try:
        df_stool_md = pd.read_csv(f_stool_md, sep=",", dtype=object)
    except IOError:
        print("File '{}' does not exist".format(f_stool_md))

    try:
        del df_stool_md["Unnamed: 12"]
    except KeyError:
        print("Error of column in file '{}'.".format(f_stool_md))
        print(df_stool_md.columns)
        del df_stool_md["Unnamed: 15"]
    list_df.append(df_stool_md.copy())

df_stools_md = pd.concat(list_df)

# create dataframe for stools location
# initialize list of dataframes
if verbose: print("Get files for aliquot of stools location:")

list_df = []
for f_stool_loc in lr_files:

    if verbose: print(">>> Works on '{}' file <<<".format(f_stool_loc))

    try:
        df_stool_loc = pd.read_csv(f_stool_loc, sep=";", dtype=object)
    except IOError:
        print("File '{}' does not exist".format(f_stool_loc))

    try:
        del df_stool_loc["Unnamed: 1"], df_stool_loc["Unnamed: 2"]
    except KeyError:
        print("Error of column in file '{}'.".format(f_stool_loc))
        print(df_stool_loc.columns)

    col_to_remove = df_stool_loc.iloc[:, [0]].columns.tolist().pop()
    new_df_test = pd.DataFrame(df_stool_loc[col_to_remove].str.split(',').\
                                                               tolist(), \
                               columns=["Position", "Box", \
                               "BarcodeID"]).copy()

    df_stool_loc.loc[:, "Position"] = new_df_test["Position"].copy()
    df_stool_loc.loc[:, "Box"] = new_df_test["Box"].copy()
    df_stool_loc.loc[:, "barcodeId"] = new_df_test["BarcodeID"].copy()
    df_stool_loc = df_stool_loc.loc[~(df_stool_loc["barcodeId"].\
                                      isin(["No Tube", "No Read"]))].copy()
    list_df.append(df_stool_loc[["Box", "barcodeId"]].copy())

df_stools_loc = pd.concat(list_df)

print("Nb of unique donorId:")
print(df_stools_md["donorId"].nunique())

exit()

if verbose: print("Merge all files.")

df_stools = pd.merge(df_stools_md, df_stools_loc, on=["barcodeId"])
df_final = pd.merge(df_stools, df_freez, on=["Box"])
del df_final["rackId"], df_final["deleted"], df_final["id"], \
    df_final["auditTrail"], df_final["well"], df_final["stimulusId"]
df_final.rename(columns={"aliquotId": "AliquotID",
                        "batchId": "BatchID",
                        "donorId": "DonorID",
                        "visitId": "VisitID",
                        "barcodeId": "Name",
                        "insertDate": "InsertDate",
                        "updateDate": "UpdateDate",
                        "type": "Sample Type",
                        "comments": "Comments",
                        "volume": "Volume",
                        "weight": "Weight"},
                inplace = True)

# write final result in CSV file format
if verbose: print("Write results in file '{}'".format(o_samples))
df_final.to_csv(o_samples, index=False, header=True)
