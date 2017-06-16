#!/usr/bin/env python
"""
# Nasal Swab creation

## About

This script is a draft, it will probably be withdraw later

"""
import pandas as pd
import numpy as np
import argparse
import sys
import re

'''
Initialize arguments
'''

parser = argparse.ArgumentParser(description="""Generate Nasal Swabs
                    samples for FreezerPro from our data Excel & CSV files""")
# Freezer file import
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
# Trizol pellet file import
parser.add_argument('-t', '--nasalm', required=True,
                    help="""File with Nasal Swab mapping data in XLSX format
                    for merge with freezer data""")
parser.add_argument('-s', '--nasalms', required=True,
                    help="""Name of sheet in Nasal Swab mapping data in XLSX
                    format to use for merge with freezer data""")
# LabKey sample file import
parser.add_argument('-l', '--labkey', required=True,
                    help="""File with all the samples stored in LabKey,
                    in CSV format, to use for merge with Nasal Swab data""")
# Stimulation sample file import
parser.add_argument('-i', '--drawdate', required=True,
                    help="""File with all the Nasal Swab creation date data in
                    XLSX format to use for merge with Nasal Swab data""")
parser.add_argument('-m', '--sheet', required=True,
                    help="""Name of sheet in Nasal Swab creation date data in
                    XLSX format to use for merge with freezer data""")
# Output file export
parser.add_argument('-o', '--output', required=True,
                    help="""Output file name that will be generate in
                    CSV format for FreezerPro""")
parser.add_argument('-v', '--verbose', help="If set, could print more infos.")
args = vars(parser.parse_args())

# Freezer file import args
f_freezer = args['freezer']
# Trizol file import args
f_nasalsw = args['nasalm']
n_nssheet = args['nasalms']
# LabKey file import args
f_labkey = args['labkey']
# Stimulation file import args
f_nsidate = args['drawdate']
n_nssdate = args['sheet']
# Output file export args
o_samples = args['output']
verbose = args['verbose']

# # Freezer file import args
# f_freezer = "../DataToImport/freezers.csv"
# # Nasal Swab mapping file import args
# f_nasalsw = "../DataToPrepare/NasalSwab/20160509_NasalSwab_SrcBoxMapping.xlsx"
# n_nssheet = "Merging"
# # LabKey file import args
# f_labkey = "../DataToPrepare/Common/samples_table_labkey.csv"
# # Stimulation file import args
# f_nsidate = "../DataToPrepare/NasalSwab/NasalSwab_DrawDates.xlsx"
# n_nssdate = "NasalSwab_DrawDates"
# # Output file export args
# o_samples = "../DataToImport/Nasal_Swab_rack_samples.csv"

# Read Freezer file
try:
    df_freezer = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '" + f_freezer + "' does not exist"
    exit()

# Read NasalSwab mapping file
try:
    df_nasalsw = pd.read_excel(f_nasalsw, n_nssheet)
except IOError:
    print "File '" + f_nasalsw + "' does not exist"
    exit()
except:
    print "Sheet '" + n_nssheet + "' does not exist in file '" + f_nasalsw + "'"
    print "Error:", sys.exc_info()[0]
    exit()

# Read LabKey file
try:
    df_labkey = pd.read_csv(f_labkey, dtype=object)
except IOError:
    print "File '" + f_labkey + "' does not exist"
    exit()

# Read stimulation file
try:
    df_nsidate = pd.read_excel(f_nsidate, n_nssdate)
except IOError:
    print "File '" + f_nsidate + "' does not exist"
    exit()
except:
    print "Sheet '" + n_nssdate + "' does not exist in file '" + f_nsidate + "'"
    print "Error:", sys.exc_info()[0]

'''
Defined reusable functions
'''
def df_dtypes_object(dataframe):
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(object)
    return dataframe

def complete_column(dataframe, column):
    above = ""
    # change column value
    for i in dataframe.index:
        if str(dataframe.loc[i][column]) == "nan":
            dataframe.loc[i][column] = above
        else:
            above = dataframe.loc[i][column]
            dataframe.loc[i][column] = above
    return dataframe

'''
Main script starts here
'''
# Convert all files read from excel as data frame of objects
df_nasalsw = df_dtypes_object(df_nasalsw)
df_nsidate = df_dtypes_object(df_nsidate)
# work only with Nasal Swab boxes and data
df_freezer = df_freezer.loc[df_freezer["BoxType"] == "Nasal_Box_9x9"]
df_labkey = df_labkey.loc[df_labkey["type"] == "NASAL_SWABS"]
del df_labkey["id"], df_labkey["auditTrail"], df_labkey["stimulusId"], df_labkey["type"]
# redraw df_nasalsw with only columns:
# RackID    BoxPosition BoxID   TubeScan
df_nasalsw_rnos = pd.DataFrame({'RackID': df_nasalsw['RackID'],
                                'BoxPosition': df_nasalsw['BoxPosition'],
                                'BoxID': df_nasalsw['BoxID'],
                                'TubeScan': df_nasalsw['TubeScan']})
df_nasalsw_lnos = pd.DataFrame({'RackID': df_nasalsw['RackID.1'],
                                'BoxPosition': df_nasalsw['BoxPosition.1'],
                                'BoxID': df_nasalsw['BoxID.1'],
                                'TubeScan': df_nasalsw['TubeScan.1']})
df_nasalsw = pd.concat([df_nasalsw_rnos, df_nasalsw_lnos])
# remove empty data in files read from Nasal Swab mapping
empties = df_nasalsw.loc[df_nasalsw["TubeScan"].isnull()].index
empties = empties.astype(object)
df_nasalsw = df_nasalsw.drop(empties)
df_nasalsw.reset_index(inplace=True)
del df_nasalsw['index'], empties
# FreezerPro requires the full location for tubes, need to repeat RackID
complete_column(df_nasalsw, "RackID")
# FreezerPro requires the full location for tubes, need to repeat BoxID
complete_column(df_nasalsw, "BoxID")
# change columns for merge with df_freezer
df_nasalsw["DonorIdscanned"] = df_nasalsw["TubeScan"]

# Nasal Swabs rack name is different compare to other data
# dirty version, found a better way to do it?
df_nasalsw["Level2"] = df_nasalsw["RackID"].str.replace(r'MIC-NasalRack_([1, 5, 7])', r'Left Rack 0\1')
df_nasalsw["Level2"] = df_nasalsw["Level2"].str.replace(r'MIC-NasalRack_([2, 4, 6, 8])', r'Right Rack 0\1')
df_nasalsw["Level2"] = df_nasalsw["Level2"].str.replace(r'MIC-NasalRack_(3)', r'Rack 0\1 + 4 boxes of stools samples (rack#5)')
# df_nasalsw["Level2"] = df_nasalsw["RackID"].str.replace(r'MIC-NasalRack_(\d{1})', r'Rack \1')
# df_nasalsw["Level2"] = df_nasalsw["RackID"].str.replace(r'MIC-NasalRack_(\d{1})', r'Rack 0\1')
df_nasalsw["Box"] = df_nasalsw["BoxID"].str.replace(r'MIC_NasalBox_(\d+)', r'box \1')
df_nasalsw["barcodeId"] = df_nasalsw["DonorIdscanned"]

# remove empty data in files read from Nasal Swab data
df_nsidate.rename(columns={ 'Box_ID': 'BoxID',
                            'Global.Unique.Id': 'DonorIdscanned'},
                 inplace = True)
empties = df_nsidate.loc[df_nsidate["DonorIdscanned"].isnull()].index
empties = empties.astype(object)
df_nsidate = df_nsidate.drop(empties)
df_nsidate.reset_index(inplace=True)
del df_nsidate['index']
# FreezerPro requires the full location for tubes, need to repeat BoxID
complete_column(df_nsidate, "BoxID")
df_nsidate["Box"] = "box " + df_nsidate["BoxID"].astype(str).str.replace(r'.0', '')
df_nsidate["visitId"] = df_nsidate["Visit"].str.replace(r'V', '')

df_nswnsd = pd.merge(df_nasalsw,
                     df_nsidate,
                     on=['Box', 'DonorIdscanned'],
                     how='inner')

df_nswfre = pd.merge(df_nasalsw,
                     df_freezer,
                     on=['Box', 'Level2'],
                     how='inner')

df_nasalsw["barcodeId"] = df_nasalsw["TubeScan"]

df_nswlab = pd.merge(df_labkey,
                     df_nasalsw,
                     on=['barcodeId'],
                     how='inner')
missing_tubes = list(set(df_nasalsw["barcodeId"]) - set(df_labkey["barcodeId"]))
if len(missing_tubes) > 0:
    print(len(missing_tubes), "tubes not found on LabKey data")
    if verbose:
        answer = raw_input("Print list of missing tubes?")
    else:
        answer = "No"
    if answer == "Yes" or answer == "yes" or answer == "Y" or answer == "y":
        print("\n".join([t for t in missing_tubes]))
# len(missing_tubes) -> 24
df_nswlabfre = pd.merge(df_nswlab,
                        df_freezer,
                        on=['Box', 'Level2'],
                        how='left')

# format output
df_nswlabfre.rename(columns={"barcodeId": "BarcodeID", "visitId": "VisitID",
                            "donorId": "DonorID", "batchId": "BatchID",
                            "volume": "Volume", "TubeScan": "Name",
                            "aliquotId": "AliquotID"},
                    inplace=True)
del df_nswlabfre["insertDate"], df_nswlabfre["updateDate"], \
    df_nswlabfre["deleted"], df_nswlabfre["RackID"]
df_nswlabfre["FreezerBarcode"] = "MIC_Freezer#_"+df_nswlabfre["Freezer"]
df_nswlabfre["ShelfBarcode"] = "MIC Freezer"+df_nswlabfre["Freezer"]+" Shelf"+\
                                df_nswlabfre["Shelf"]

# save result dataframe in a new CSV file
df_nswlabfre.to_csv(o_samples, index = False, header = True)
