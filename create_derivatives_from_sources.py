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
# Remove excluded stimuli
parser.add_argument('-r', '--remove_stimuli', required=False,
                    help="""List of excluded stimuli. Need to be exactly like
                    9,31,40""")
# Remove excluded tubes
parser.add_argument('-e', '--remove_tubes', required=False,
                    help="""File of excluded tubes.""")
# Replace errors tubes
parser.add_argument('-c', '--change_tubes', required=False,
                    help="""File of tubes to replace""")
# Add missing tubes
parser.add_argument('-a', '--add_tubes', required=False,
                    help="""File of tubes to add, need to be in same format as
                    run files from argument --directory""")
# Box location in freezers
parser.add_argument('-f', '--freezers', required=True,
                    help="""File with location of each box of aliquots in
                    freezers""")
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
# Box freezer location file args
f_freez = args['freezers']
# Aliquot sample files directory input args
d_dir = args['directory']
# Output file export args
o_samples = args['output_file']
u_samples = args['update_file']

if args['remove_stimuli']:
    rm_stimuli = args['remove_stimuli'].split(',')
    rm_stimuli = [str(st) for st in rm_stimuli]

if args['remove_tubes']:
    try:
        dic_etubes = pd.read_excel(args['remove_tubes'], sheetname=None)
        df_etubes = pd.concat([dic_etubes[df] for df in dic_etubes.keys()])
    except IOError:
        print "File '" + args['remove_tubes'] + "' does not exist"

if args['change_tubes']:
    try:
        dic_ctubes = pd.read_excel(args['change_tubes'], sheetname=None)
        df_ctubes = pd.concat([dic_ctubes[df] for df in dic_ctubes.keys()])
    except IOError:
        print "File '" + args['change_tubes'] + "' does not exist"

# Read Freezer file input
try:
    df_input = pd.read_csv(f_input, dtype=object)
except IOError:
    print "File '" + f_input + "' does not exist"
    exit()

# Read box location in freezers file input
try:
    df_freez = pd.read_csv(f_freez, dtype=object, sep=";")
except IOError:
    print "File '" + f_freez + "' does not exist"
    exit()

# Read Aliquot file input
try:
    fic_dir = os.path.join(d_dir, \
                "[0-9]*_TruCSpnttAlqtg_TrackingSheet_[A-Z]*.xlsx")
    l_files = glob.glob(fic_dir.replace('\\', ''))

    fic_dir = os.path.join(d_dir, \
                "[0-9]*_Errors_TruCSpnttAlqtg_TrackingSheet_[A-Z]*.xlsx")
    for f in glob.glob(fic_dir.replace('\\', '')):
        l_files.remove(f)
    l_errors = glob.glob(fic_dir.replace('\\', ''))
except IOError:
    print "Directory '" + d_dir + "' does not exist"
    exit()


# Add tubes file input
if args["add_tubes"]:
    add_file = args["add_tubes"]
    l_files.append(add_file)


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

'''
For each file in l_files, generate dataframe of aliquots
'''

# initialize list of dataframes
list_df = []
cols_to_cplt = ["SrcBox_BoxID", "SrcBox_LabExID",
                "Al1Box_BoxID", "Al1Box_LabExID",
                "Al2Box_BoxID", "AliquotingDate"]

print("%d aliquot files to read" % len(l_files))

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

'''
    For each file in l_errors, generate dataframe of corrected tube barcodes
'''

# initialize list of dataframes
list_df = []

print("%d error files to read" % len(l_errors))

for f_error in l_errors:
    print ">>> Works on '"+f_error+"' file <<<"
    try:
        # take all sheets
        dic_errors = pd.read_excel(f_error, sheetname = None, \
                                   converters = {\
                                        "Well VisionMate": lambda x: str(x),
                                        "Well VisionMate.1": lambda x: str(x),
                                        "Well VisionMate.2": lambda x: str(x)
                                   })
    except IOError:
        print "File '" + f_error + "' does not exist"

    df_errors = pd.concat([dic_errors[df] for df in dic_errors.keys()])
    df_errors["File"] = f_error
    list_df.append(df_errors)

try:
    df_errors = df_dtypes_object(pd.concat(list_df))
    df_errors = df_errors.loc[df_errors["Well VisionMate"].notnull()]
except ValueError:
    print "DataFrame is empty"
    print "Worked on dir " + d_dir

# remove control columns that are not representative of data scanned
del df_aliquot["Well Expected.2"], df_aliquot["Well Expected.1"], \
    df_aliquot["Al1Box_TubeCtrl"], df_aliquot["Al2Box_TubeCtrl"]
df_aliquot.rename(columns = {"SrcBox_LabExID": "BoxBarcode",
                             "SrcBox_TubeScan": "Name"}, inplace = True)
df_aliquot.loc[:, "Name"] = df_aliquot["Name"].astype(str)
df_aliquot = df_aliquot[df_aliquot.notnull()]
# remove lines in dataframe of aliquots when Name is not in an expected format
not_name = ["No Read", "No Tube", "(Paste Here output from VisionMate)", \
            "nan"]
df_aliquot = df_aliquot[~df_aliquot["Name"].isin(not_name)]
df_aliquot.loc[:, "Name"] = df_aliquot["Name"].astype(float).\
                             astype(int).astype(str)

# keep date in date format only (YYYY/MM/DD)
df_aliquot.loc[:, "AliquotingDate"] = df_aliquot["AliquotingDate"].str.\
                           replace(r"(\d{4})(\d{2})(\d{2})_[A-Z]*", \
                           r"\3/\2/\1")
df_aliquot.loc[:, "AliquotingDate"] = df_aliquot["AliquotingDate"].str.\
                                        replace(r"\d_[A-Z]+", r"")

"""
Prepare dataframe for Aliquot Fraction 1
"""

# list of columns for aliquot 1 data
cols_aliq1 = ["AliquotingDate", "SrcBox_BoxID", "BoxBarcode", \
              "Name", "Al1Box_BoxID", "Al1Box_LabExID", \
              "Al1Box_TubeScan", "Well VisionMate.1"]
df_aliquot1 = df_aliquot[cols_aliq1]
df_aliquot1.rename(columns = {"Well VisionMate.1": "Position"},
                   inplace = True)
df_aliquot1.loc[:, "Position"] = df_aliquot1["Position"].str.\
                                        replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")

"""
Prepare dataframe for Aliquot Fraction 2
"""

# list of columns for aliquot 2 data
cols_aliq2 = ["AliquotingDate", "SrcBox_BoxID", "BoxBarcode", \
              "Name", "Al2Box_BoxID", "Al1Box_LabExID", \
              "Al2Box_TubeScan", "Well VisionMate.2"]
df_aliquot2 = df_aliquot[cols_aliq2]
df_aliquot2.loc[:, "Al1Box_LabExID"] = df_aliquot2["Al1Box_LabExID"].str.\
                                        replace("F1", "F2")
df_aliquot2.rename(columns = {"Well VisionMate.2": "Position", \
                              "Al1Box_LabExID": "Al2Box_LabExID"},
                   inplace = True)
df_aliquot2.loc[:, "Position"] = df_aliquot2["Position"].str.\
                                        replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
df_aliquot2 = df_aliquot2[df_aliquot2["Name"].notnull()]
df_aliquot2 = df_aliquot2[df_aliquot2["Name"].str.contains("[^0-9]") == False]

"""
Prepare file from FreezerPro for next merges
"""

df_input = df_input[["UID", "Name", "Volume", "BoxBarcode", "BARCODE", \
                     "UpdateDate", "AliquotID", "DonorID", "StimulusID", \
                     "StimulusName", "VisitID", "ThawCycle", \
                     "Sample Source", "Description", "BatchID", \
                     "ShelfBarcode", "RackBarcode", "DrawerBarcode", \
                     "Position"]]
df_input.rename(columns={"Position": "TubeWell"}, inplace=True)

# if user don't want at least one stimulus, don't keep it
if 'rm_stimuli' in locals():
    for st in rm_stimuli:
        """
        Aliquot Fraction 1, remove stimuli
        """
        df_rm_samples1 = df_aliquot1[df_aliquot1["Al1Box_LabExID"].str.\
                            contains(r"S"+st)]
        df_aliquot1 = df_aliquot1[~df_aliquot1["Al1Box_LabExID"].str.\
                        contains(r"S"+st)]
        del df_rm_samples1["BoxBarcode"]
        df_rm_al1_fr = pd.merge(df_input, df_rm_samples1, on="Name")

        df_rm_al1_fr.loc[:, "Sample Type"] = "Fraction1"
        df_rm_al1_fr.loc[:, "Volume"] = 100.0
        del df_rm_al1_fr["SrcBox_BoxID"], df_rm_al1_fr["BoxBarcode"], \
            df_rm_al1_fr["Name"]
        df_rm_al1_fr.rename(columns = {"UID": "ParentID", \
                                      "BARCODE": "SrcTube_Barcode", \
                                      "Al1Box_LabExID": "BoxBarcode", \
                                      "Al1Box_BoxID": "ThermoBoxBarcode", \
                                      "Al1Box_TubeScan": "Name"}, \
                            inplace = True)

        df_rm_al1_fr.loc[:, "Name"] = df_rm_al1_fr["Name"].astype(str)
        del df_rm_al1_fr["SrcTube_Barcode"]

        df_rm_al1_fr.loc[:, "BARCODE"] = df_rm_al1_fr["Name"]
        df_rm_al1_fr.loc[:, "BOX_BARCODE"] = df_rm_al1_fr["BoxBarcode"]
        df_rm_al1_fr.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"
        df_rm_al1_fr.loc[:, "Box"] = df_rm_al1_fr["BOX_BARCODE"]
        df_rm_al1_fr.loc[:, "Box_Descr"] = df_rm_al1_fr["Box"].str.\
                            replace(r"\w+S(\d{1,2})_V(\d)_A(\d)_F(\d)_D(\w+)-(\w+)", \
                            r"""Box of Stimulus \1 for Donors \5 to \6, Visit \2, Aliquot \3, Fraction \4""")
        df_rm_al1_fr.loc[:, "CreationDate"] = df_rm_al1_fr["AliquotingDate"]
        df_rm_al1_fr.loc[:, "UpdateDate"] = df_rm_al1_fr["AliquotingDate"]
        df_rm_al1_fr.loc[:, "Edition comment"] = "Tube sent to RBM. The tube "+df_rm_al1_fr["Name"]+" no longer exists."

        """
        Aliquot 1 Fraction 2, remove stimuli
        """
        df_rm_samples2 = df_aliquot2[df_aliquot2["Al2Box_LabExID"].str.\
                            contains(r"S"+st)]
        df_aliquot2 = df_aliquot2[~df_aliquot2["Al2Box_LabExID"].str.\
                        contains(r"S"+st)]
        del df_rm_samples2["BoxBarcode"]
        df_rm_al2_fr = pd.merge(df_input, df_rm_samples2, on="Name")

        df_rm_al2_fr.loc[:, "Sample Type"] = "Fraction1"
        df_rm_al2_fr.loc[:, "Volume"] = 100.0
        del df_rm_al2_fr["SrcBox_BoxID"], df_rm_al2_fr["BoxBarcode"], \
            df_rm_al2_fr["Name"]
        df_rm_al2_fr.rename(columns = {"UID": "ParentID", \
                                      "BARCODE": "SrcTube_Barcode", \
                                      "Al2Box_LabExID": "BoxBarcode", \
                                      "Al2Box_BoxID": "ThermoBoxBarcode", \
                                      "Al2Box_TubeScan": "Name"}, \
                            inplace = True)

        df_rm_al2_fr.loc[:, "Name"] = df_rm_al2_fr["Name"].astype(str)
        del df_rm_al2_fr["SrcTube_Barcode"]

        df_rm_al2_fr.loc[:, "BARCODE"] = df_rm_al2_fr["Name"]
        df_rm_al2_fr.loc[:, "BOX_BARCODE"] = df_rm_al2_fr["BoxBarcode"]
        df_rm_al2_fr.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"
        df_rm_al2_fr.loc[:, "Box"] = df_rm_al2_fr["BOX_BARCODE"]
        df_rm_al2_fr.loc[:, "Box_Descr"] = df_rm_al2_fr["Box"].str.\
                            replace(r"\w+S(\d{1,2})_V(\d)_A(\d)_F(\d)_D(\w+)-(\w+)", \
                            r"""Box of Stimulus \1 for Donors \5 to \6, Visit \2, Aliquot \3, Fraction \4""")
        df_rm_al2_fr.loc[:, "CreationDate"] = df_rm_al2_fr["AliquotingDate"]
        df_rm_al2_fr.loc[:, "UpdateDate"] = df_rm_al2_fr["AliquotingDate"]
        df_rm_al2_fr.loc[:, "Edition comment"] = "Tube sent to RBM. The tube "+df_rm_al2_fr["Name"]+" no longer exists."

        df_rm_al_fr = pd.concat([df_rm_al1_fr, df_rm_al2_fr])

"""
Merge Aliquot Fraction 1 with Freezer location
"""

print("Nb tubes in Aliquot 1:")
print(len(df_aliquot1))
del df_aliquot1["BoxBarcode"]
df_al1_fr = pd.merge(df_input, df_aliquot1, on="Name")
print("Nb tubes after first merge:")
print(len(df_al1_fr))
df_al1_fr.loc[:, "Sample Type"] = "Fraction1"
df_al1_fr.loc[:, "Volume"] = 100.0
del df_al1_fr["SrcBox_BoxID"], df_al1_fr["BoxBarcode"], df_al1_fr["Name"]
df_al1_fr.rename(columns = {"UID": "ParentID", "BARCODE": "SrcTube_Barcode", \
                            "Al1Box_LabExID": "BoxBarcode", \
                            "Al1Box_BoxID": "ThermoBoxBarcode", \
                            "Al1Box_TubeScan": "Name"}, \
                 inplace = True)

df_al1_fr = pd.merge(df_freez, df_al1_fr, on="BoxBarcode")

"""
Merge Aliquot Fraction 2 with Freezer location
"""

print("Nb tubes in Aliquot 2:")
print(len(df_aliquot2))
del df_aliquot2["BoxBarcode"]
df_al2_fr = pd.merge(df_input, df_aliquot2, on="Name")
print("Nb tubes after first merge:")
print(len(df_al2_fr))
df_al2_fr.loc[:, "Sample Type"] = "Fraction2"
df_al2_fr.loc[:, "Volume"] = 100.0
del df_al2_fr["SrcBox_BoxID"], df_al2_fr["BoxBarcode"], df_al2_fr["Name"]
df_al2_fr.rename(columns = {"UID": "ParentID", "BARCODE": "SrcTube_Barcode", \
                            "Al2Box_LabExID": "BoxBarcode", \
                            "Al2Box_BoxID": "ThermoBoxBarcode", \
                            "Al2Box_TubeScan": "Name"}, \
                 inplace = True)

df_al2_fr = pd.merge(df_freez, df_al2_fr, on="BoxBarcode")

"""
Concat all dataframe
"""
df_al_fr = pd.concat([df_al1_fr, df_al2_fr])
df_al_fr.loc[:, "Name"] = df_al_fr["Name"].astype(str)
del df_al_fr["SrcTube_Barcode"]

df_al_fr.loc[:, "BARCODE"] = df_al_fr["Name"]
df_al_fr.loc[:, "BOX_BARCODE"] = df_al_fr["BoxBarcode"]
df_al_fr.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"
df_al_fr.loc[:, "Box"] = df_al_fr["BOX_BARCODE"]
df_al_fr.loc[:, "Box_Descr"] = df_al_fr["Box"].str.\
                    replace(r"\w+S(\d{1,2})_V(\d)_A(\d)_F(\d)_D(\w+)-(\w+)", \
                    r"""Box of Stimulus \1 for Donors \5 to \6, Visit \2, Aliquot \3, Fraction \4""")
df_al_fr.loc[:, "CreationDate"] = df_al_fr["AliquotingDate"]
df_al_fr.loc[:, "UpdateDate"] = df_al_fr["AliquotingDate"]

# list of columns to keep for import into FreezerPro
keep_cols = ["ParentID", "Name", "BARCODE", "Position", "Volume", \
             "Freezer", "Freezer_Descr", "Level1", "Level1_Descr", \
             "Level2", "Level2_Descr", "Level3", "Level3_Descr", \
             "BoxType", "Box", "Box_Descr", "ThermoBoxBarcode",\
             "BOX_BARCODE", "CreationDate", "UpdateDate", "AliquotID", \
             "DonorID", "StimulusID", "StimulusName", "VisitID", "ThawCycle", \
             "Sample Source", "Description", "BatchID", "Sample Type",\
             "ShelfBarcode", "RackBarcode", "DrawerBarcode"]

# excluded samples
if 'df_etubes' in locals():
    df_etubes = df_dtypes_object(df_etubes)
    df_etubes.rename(columns={"BarcodeId_Source": "Name"}, inplace=True)
    df_etubes = pd.merge(df_etubes, df_input, on="Name")
    df_etubes.rename(columns={"UID": "ParentID"}, inplace=True)
    df_al_fr = pd.merge(df_al_fr, df_etubes[["ParentID"]], on="ParentID", \
                        how="outer")

# tubes in wrong position
'''
Merge df_ctubes with df_input on columns:
    * DonorID
    * StimulusID: create column from SrcBox_Barcode
    * AliquotID: 1
    * VisitID: 1
'''
if 'df_ctubes' in locals():
    df_ctubes = df_dtypes_object(df_ctubes)
    df_ctubes.loc[:, "StimulusID"] = df_ctubes["SrcBox_Barcode"].\
                        str.replace(r"MIC_S(\d+)_V1_A1_D\d{1,3}-\d{2,3}", r"\1")
    df_ctubes.loc[:, "StimulusID"] = df_ctubes["StimulusID"].astype(float).\
                        astype(str)
    df_ctubes.rename(columns={"DonorId": "DonorID"}, inplace=True)
    df_ctubes.loc[:, "DonorID"] = df_ctubes["DonorID"].astype(float).astype(str)
    df_tmp_tubes_origin = pd.merge(df_ctubes, df_input, \
                                   on=["StimulusID", "DonorID"])
    df_tmp_tubes_origin.loc[:, "F2Box_Barcode"] = df_tmp_tubes_origin["F1Box_Barcode"].str.replace("F1", "F2")

    """
    Aliquot Fraction 1, wrong tubes to replace
    """
    df_tmp_tubes_origin1 = df_tmp_tubes_origin[["UID", "Name", "Volume", \
                                               "BoxBarcode", "BARCODE", \
                                               "UpdateDate", "AliquotID", \
                                               "DonorID", "StimulusID", \
                                               "StimulusName", "VisitID", \
                                               "ThawCycle", "BarcodeId_Source",\
                                               "Description", "BatchID", \
                                               "ShelfBarcode", "RackBarcode", \
                                               "Sample Source", "F1TF_Barcode",\
                                               "F1Box_Barcode", \
                                               "DrawerBarcode", "TubeWell"]]
    df_tmp_tubes_origin1.rename(columns={"Name": "NewSrcTube_Barcode", \
                                        "BarcodeId_Source": "SrcTube_Barcode",
                                        "F1TF_Barcode": "ThermoBoxBarcode"},\
                                inplace=True)
    # we have the good source tubes, we need to get the good fractions barcodes
    df_errors1 = df_errors[["Well VisionMate", "Well VisionMate.1"]]
    df_errors1.rename(columns={"Well VisionMate": "NewSrcTube_Barcode", \
                              "Well VisionMate.1": "NewAl1Tube_Barcode"},
                    inplace=True)
    df_ali1 = df_aliquot1.rename(columns={"Name": "SrcTube_Barcode"})
    df_all_bcds1 = pd.merge(df_tmp_tubes_origin1, df_errors1, \
                               on="NewSrcTube_Barcode")
    df_all_bcds1.loc[:, "SrcTube_Barcode"] = df_all_bcds1["SrcTube_Barcode"].\
                                            astype(str)
    df_ali1.loc[:, "SrcTube_Barcode"] = df_ali1["SrcTube_Barcode"].astype(str)
    df_ali1.loc[:, "Position"] = df_ali1["Position"].str.\
                                        replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
    df_ali1_changed = pd.merge(df_all_bcds1, df_ali1, on="SrcTube_Barcode")
    del df_ali1_changed["BoxBarcode"]

    df_ali1_changed.rename(columns={"NewSrcTube_Barcode": "Name", \
                                    "UID": "ParentID", \
                                    "Al1Box_LabExID": "BoxBarcode"}, inplace=True)
    # print("%d lines in df_ali1_changed (before)" % len(df_ali1_changed))
    df_ali1_changed = pd.merge(df_freez, df_ali1_changed, on="BoxBarcode")
    # print("%d lines in df_ali1_changed (after)" % len(df_ali1_changed))

    df_al1_cplt = df_ali1_changed.copy(deep=True)
    # get list of aliquot tube barcode that are wrong and would be changed
    to_remove1 = df_ctubes["BarcodeId_F1"].astype(str).values.tolist()

    df_ali1_changed.rename(columns={"SrcTube_Barcode": "Al1Box_TubeScan"})
    del df_al1_cplt["SrcTube_Barcode"], df_al1_cplt["Al1Box_TubeScan"], \
        df_al1_cplt["Name"]
    df_al1_cplt.rename(columns={"NewAl1Tube_Barcode": "Name"}, inplace=True)
    df_al1_cplt.loc[:, "Sample Type"] = "Fraction1"
    df_al1_cplt.loc[:, "Position"] = df_al1_cplt["Position"].str.\
                replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
    df_al1_cplt.loc[:, "BARCODE"] = df_al1_cplt["Name"]
    df_al1_cplt.loc[:, "BOX_BARCODE"] = df_al1_cplt["F1Box_Barcode"]
    df_al1_cplt.loc[:, "Box"] = df_al1_cplt["BOX_BARCODE"]
    df_al1_cplt.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"
    df_al1_cplt.loc[:, "Box_Descr"] = df_al1_cplt["F1Box_Barcode"].str.\
                replace(r"\w+S(\d{1,2})_V(\d)_A(\d)_F(\d)_D(\w+)-(\w+)", \
                r"""Box of Stimulus \1 for Donors \5 to \6, Visit \2, Aliquot \3, Fraction \4""")
    df_al1_cplt.loc[:, "CreationDate"] = df_al1_cplt["AliquotingDate"]
    df_al1_cplt.loc[:, "UpdateDate"] = df_al1_cplt["AliquotingDate"]

    df_al_fr = pd.concat([df_al_fr, df_al1_cplt])
    df_al_fr = df_al_fr[~(df_al_fr["Name"].isin(to_remove1))]


    """
    Aliquot Fraction 2, wrong tubes to replace
    """
    df_tmp_tubes_origin2 = df_tmp_tubes_origin[["UID", "Name", "Volume", \
                                               "BoxBarcode", "BARCODE", \
                                               "UpdateDate", "AliquotID", \
                                               "DonorID", "StimulusID", \
                                               "StimulusName", "VisitID", \
                                               "ThawCycle", "BarcodeId_Source",\
                                               "Description", "BatchID", \
                                               "ShelfBarcode", "RackBarcode", \
                                               "Sample Source", "F2TF_Barcode",\
                                               "F2Box_Barcode", \
                                               "DrawerBarcode", "TubeWell"]]
    df_tmp_tubes_origin2.rename(columns={"Name": "NewSrcTube_Barcode", \
                                        "BarcodeId_Source": "SrcTube_Barcode",
                                        "F2TF_Barcode": "ThermoBoxBarcode"},\
                                inplace=True)
    # we have the good source tubes, we need to get the good fractions barcodes
    df_errors2 = df_errors[["Well VisionMate", "Well VisionMate.2"]]
    df_errors2.rename(columns={"Well VisionMate": "NewSrcTube_Barcode", \
                              "Well VisionMate.2": "NewAl2Tube_Barcode"},
                    inplace=True)
    df_ali2 = df_aliquot2.rename(columns={"Name": "SrcTube_Barcode"})
    df_all_bcds2 = pd.merge(df_tmp_tubes_origin2, df_errors2, \
                               on="NewSrcTube_Barcode")
    df_all_bcds2.loc[:, "SrcTube_Barcode"] = df_all_bcds2["SrcTube_Barcode"].\
                                            astype(str)
    df_ali2.loc[:, "SrcTube_Barcode"] = df_ali2["SrcTube_Barcode"].astype(str)
    df_ali2.loc[:, "Position"] = df_ali2["Position"].str.\
                                        replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
    df_ali2_changed = pd.merge(df_all_bcds2, df_ali2, on="SrcTube_Barcode")
    del df_ali2_changed["BoxBarcode"]

    df_ali2_changed.rename(columns={"NewSrcTube_Barcode": "Name", \
                                    "UID": "ParentID", \
                                    "Al2Box_LabExID": "BoxBarcode"}, \
                           inplace=True)
    # print("%d lines in df_ali1_changed (before)" % len(df_ali1_changed))
    df_ali2_changed = pd.merge(df_freez, df_ali2_changed, on="BoxBarcode")
    # print("%d lines in df_ali1_changed (after)" % len(df_ali1_changed))

    df_al2_cplt = df_ali2_changed.copy(deep=True)
    # get list of aliquot tube barcode that are wrong and would be changed
    to_remove2 = df_ctubes["BarcodeId_F2"].astype(str).values.tolist()

    df_ali2_changed.rename(columns={"SrcTube_Barcode": "Al2Box_TubeScan"})
    del df_al2_cplt["SrcTube_Barcode"], df_al2_cplt["Al2Box_TubeScan"], \
        df_al2_cplt["Name"]

    df_al2_cplt.rename(columns={"NewAl2Tube_Barcode": "Name"}, inplace=True)
    df_al2_cplt.loc[:, "Sample Type"] = "Fraction2"
    df_al2_cplt.loc[:, "Position"] = df_al2_cplt["Position"].str.\
                replace(r"^([A-Z]+)(\d+)$", r"\1 / \2")
    df_al2_cplt.loc[:, "BARCODE"] = df_al2_cplt["Name"]
    df_al2_cplt.loc[:, "BOX_BARCODE"] = df_al2_cplt["F2Box_Barcode"]
    df_al2_cplt.loc[:, "Box"] = df_al2_cplt["BOX_BARCODE"]
    df_al2_cplt.loc[:, "BoxType"] = "96 (12 x 8) Well Plate"
    df_al2_cplt.loc[:, "Box_Descr"] = df_al2_cplt["F2Box_Barcode"].str.\
                replace(r"\w+S(\d{1,2})_V(\d)_A(\d)_F(\d)_D(\w+)-(\w+)", \
                r"""Box of Stimulus \1 for Donors \5 to \6, Visit \2, Aliquot \3, Fraction \4""")
    df_al2_cplt.loc[:, "CreationDate"] = df_al2_cplt["AliquotingDate"]
    df_al2_cplt.loc[:, "UpdateDate"] = df_al2_cplt["AliquotingDate"]

    df_al_fr = pd.concat([df_al_fr, df_al2_cplt])
    df_al_fr = df_al_fr[~(df_al_fr["Name"].isin(to_remove2))]

    print("Nb tubes after replacing wrong aliquot tubes:")
    print(len(df_al_fr))

    del df_al_fr["Position"]

df_al_fr.rename(columns={"TubeWell": "Position"}, inplace=True)

df_al_fr[keep_cols].to_csv(o_samples, index = False, header = True)
del df_al_fr["Volume"], df_al_fr["BARCODE"]

df_input.rename(columns = {"UID": "ParentID"}, inplace = True)
df_input["Volume"] = df_input["Volume"].astype(float)

df_update = pd.merge(df_al_fr, df_input[["ParentID", "BARCODE", "Volume"]], on="ParentID")

df_update.loc[:, "Volume"] = df_update["Volume"]-(2*100.0)
df_update.loc[:, "UpdateDate"] = df_update["AliquotingDate"].str.replace(r"(\d{4})(\d{2})(\d{2})", r"\3/\2/\1")

if 'df_rm_al_fr' in locals():
    df_update.loc[:, "Edition comment"] = ""
    on_cols = ["BARCODE", "Volume", "UpdateDate", "Edition comment"]
    df_update = pd.concat([df_update[on_cols], df_rm_al_fr[on_cols]])

    print("%d lines in df_update before dropping duplicates" % len(df_update))
    df_update.drop_duplicates(inplace=True)
    print("%d lines in df_update after dropping duplicates" % len(df_update))
    print("%d unique BARCODE in df_update" % len(df_update["BARCODE"].unique()))
    print("%d unique Volume in df_update" % len(df_update["Volume"].unique()))
    print("%d unique UpdateDate in df_update" % len(df_update["UpdateDate"].unique()))
    print("%d unique Edition comment in df_update" % len(df_update["Edition comment"].unique()))
    df_update.to_csv(u_samples, index = False, header = True)

    print("Save %d lines in %s" % (len(df_update), u_samples))

else:
    df_update[["BARCODE", "Volume", "UpdateDate"]].to_csv(u_samples, index = False, header = True)
