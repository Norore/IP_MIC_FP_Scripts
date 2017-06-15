#!/usr/bin/env python
import pandas as pd
import argparse
import os.path
import sys
import re

parser = argparse.ArgumentParser(description="Generate supernatants samples for FreezerPro from our data Excel file")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-t', '--supernatant', required=True,
                    help="File with supernatants data in XLSX format for merge with freezer data")
parser.add_argument('-s', '--sheet', required=True,
                    help="Name of sheet in supernatant data in XLSX format to use for merge with freezer data")
parser.add_argument('-o', '--output', required=True,
                    help="Output file name that will be generate in CSV format for FreezerPro")
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_trizol  = args['supernatant']
ns_sheet  = args['sheet']
o_samples = args['output']

try:
    df = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '"+f_freezer+"' does not exist"
    exit(1)

try:
    data = pd.read_excel(f_trizol, sheetname=ns_sheet)
except IOError:
    print "File '"+f_trizol+"' does not exist"
    exit(1)
except:
    print "Sheet '"+ns_sheet+"' does not exist in file '"+f_trizol+"'"
    print "Error:",sys.exc_info()[0]
    exit(1)

# be sure all columns are of type object
for col in data.columns:
    data[col] = data[col].astype(object)

"""
List of columns of interest:
    - DonorIDscanned
    - ExtractionName
    - Donor_ID.
    - Visit
    - StimulationNumber
    - StimulationName
    - StimulationTime
    - Matrix_RackBarcodeScanned
    - Matrix_TubeBarcodeScanned
    - Matrix_TubePosition.
"""
datacols = data[["DonorIDscanned", "ExtractionName", "Donor_ID.", "Visit",
                 "StimulationNumber",	"StimulationName", "StimulationTime",
                 "Matrix_RackBarcodeScanned", "Matrix_TubeBarcodeScanned",
                 "Matrix_TubePosition."]]

datacols.rename(columns={"Donor_ID.": "DonorID",
                         "Matrix_RackBarcodeScanned": "Box",
                         "Matrix_TubeBarcodeScanned": "Name",
                         "Matrix_TubePosition.": "Position"}, inplace=True)
datacols["Freezer"] = ["Fernbach"]*len(datacols)
datacols["Level1"] = ["Shelf 1"]*len(datacols)
datacols["Level2"] = ["Stimulated RNA"]*len(datacols)
datacols["Sample Type"] = ["RNA stimulated"]*len(datacols)

# remove false samples lines
spikelist = datacols.loc[datacols["DonorIDscanned"].str.match(r"Spike") == True].index.get_values()
blanclist = datacols.loc[datacols["DonorIDscanned"].str.match(r"Blanc") == True].index.get_values()
indexlist = list(spikelist) + list(blanclist)
dataset = datacols.drop(datacols.index[indexlist])
dataset.reset_index(inplace=True)
del dataset["index"]

# change position format for FreezerPro database
dataset["Position"] = dataset["Position"].str.replace(r'([A-Z]+)[0]?(\d+)', r'\2 / \1')

dataset.to_csv(o_samples, index=False, header=True)
