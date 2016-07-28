#!/usr/bin/env python
import pandas as pd
import numpy as np
import argparse
import sys
import re

'''
Initialize arguments
'''

# parser = argparse.ArgumentParser(description="""Generate Nasal Swabs
#                     samples for FreezerPro from our data Excel & CSV files""")
# # Freezer file import
# parser.add_argument('-f', '--freezer', required=True,
#                     help="File with freezer data in CSV format for FreezerPro")
# # Trizol pellet file import
# parser.add_argument('-t', '--nasalm', required=True,
#                     help="""File with Nasal Swab mapping data in XLSX format
#                     for merge with freezer data""")
# parser.add_argument('-s', '--nasalms', required=True,
#                     help="""Name of sheet in Nasal Swab mapping data in XLSX
#                     format to use for merge with freezer data""")
# # LabKey sample file import
# parser.add_argument('-l', '--labkey', required=True,
#                     help="""File with all the samples stored in LabKey,
#                     in CSV format, to use for merge with Nasal Swab data""")
# # Stimulation sample file import
# parser.add_argument('-i', '--drawdate', required=True,
#                     help="""File with all the Nasal Swab creation date data in
#                     XLSX format to use for merge with Nasal Swab data""")
# parser.add_argument('-m', '--sheet', required=True,
#                     help="""Name of sheet in Nasal Swab creation date data in
#                     XLSX format to use for merge with freezer data""")
# # Output file export
# parser.add_argument('-o', '--output', required=True,
#                     help="""Output file name that will be generate in
#                     CSV format for FreezerPro""")
# args = vars(parser.parse_args())

# # Freezer file import args
# f_freezer = args['freezer']
# # Trizol file import args
# f_nasalsw = args['nasalm']
# n_nssheet = args['nasalms']
# # LabKey file import args
# f_labkey = args['labkey']
# # Stimulation file import args
# f_nsidate = args['drawdate']
# n_nssdate = args['sheet']
# # Output file export args
# o_samples = args['output']

# Freezer file import args
f_freezer = "../DataToImport/freezers.csv"
# Trizol file import args
f_nasalsw = "../DataToPrepare/NasalSwab/20160509_NasalSwab_SrcBoxMapping.xlsx"
n_nssheet = "Merging"
# LabKey file import args
f_labkey = "../DataToPrepare/Common/samples_table_labkey.csv"
# Stimulation file import args
f_nsidate = "../DataToPrepare/NasalSwab/NasalSwab_DrawDates.xlsx"
n_nssdate = "NasalSwab_DrawDates"
# Output file export args
o_samples = "../DataToImport/Nasal_Swab_rack_samples.csv"

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

'''
Main script starts here
'''
# Convert all files read from excel as data frame of objects
df_nasalsw = df_dtypes_object(df_nasalsw)
df_nsidate = df_dtypes_object(df_nsidate)
# work only with Nasal Swab boxes and data
df_freezer = df_freezer.loc[df_freezer["BoxType"] == "Nasal_Box_9x9"]
df_labkey = df_labkey.loc[df_labkey["type"] == "NASAL_SWABS"]
# remove empty data in files read from Nasal Swab mapping
empties = df_nasalsw.loc[df_nasalsw["TubeScan"].isnull()]
empties = empties.astype(object)
df_nasalsw.drop(empties)
# remove empty data in files read from Nasal Swab data
empties = df_nsidate.loc[df_nsidate["Global.Unique.Id"].isnull()]
empties = empties.astype(object)
df_nsidate.drop(empties)
# save result dataframe in a new CSV file
merge_ftls.to_csv(o_samples, index = False, header = True)
