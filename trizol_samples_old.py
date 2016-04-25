#!/usr/bin/env python
import pandas as pd
import argparse
import os.path
import sys

parser = argparse.ArgumentParser(description="Generate trizol pellet samples for FreezerPro from our data Excel file")
parser.add_argument('-f', '--freezer', required=True, \
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-t', '--trizol', required=True, \
                    help="File with trizol pellet data in XLSX format for merge with freezer data")
parser.add_argument('-s', '--sheet', required=True, \
                    help="Name of sheet in trizol pellet data in XLSX format to user for merge with freezer data")
parser.add_argument('-o', '--output', required=True, \
                    help="Output file name that will be generate in CSV format for FreezerPro")
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_trizol = args['trizol']
n_sheet = args['sheet']
o_samples = args['output']

try:
    df = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '" + f_freezer + "' does not exist"
    exit(1)

try:
    data = pd.read_excel(f_trizol, n_sheet)  # use sheet 'FinalMapping'
except IOError:
    print "File '" + f_trizol + "' does not exist"
    exit(1)
except:
    print "Sheet '" + n_sheet + "' does not exist in file '" + f_trizol + "'"
    print "Error:", sys.exc_info()[0]
    exit(1)

for col in data.columns:
    data[col] = data[col].astype(object)

# rename column 'FreezerID ShelfID' to 'FreezerLoc'
data.rename(columns={"FreezerID ShelfID": "FreezerLoc"}, inplace=True)

# split column 'FreezerLoc' into 3 new columns: 'MIC', 'FreezerID' and 'ShelfID'
newcols = pd.DataFrame(data.FreezerLoc.str.split().tolist(), columns=["MIC", "FreezerID", "ShelfID"])
newcols["FreezerID"] = newcols["FreezerID"].str.replace('Freezer', '')
newcols["ShelfID"] = newcols["ShelfID"].str.replace('Shelf', 'Shelf ')
# remove 'MIC' column which is not necessary
del newcols["MIC"]

# replace 'MIC-TruCRack_' string by 'Rack ' for a good merge in next instructions
data["RackID"] = data["RackID"].str.replace('MIC-TruCRack_', 'Rack ')
# create column 'FreezerID'
data["FreezerID"] = newcols["FreezerID"]
# create column 'ShelfID'
data["ShelfID"] = newcols["ShelfID"]
# remove column 'FreezerLoc' which is not yet necessary
del data["FreezerLoc"]

# remove samples moved at Fernbach building and reset index
indexes = list(data.loc[data["Processed"].isnull() == False].index)
data.drop(indexes, inplace=True)
data.reset_index(inplace=True)
# I don't know why pandas keep the old index in a new column named 'index'
del data["index"], data["Processed"]

# calculate, for each donor and each BoxPos, the 'box number' to assign
values = []
for value in data["BoxPos"]:
    if int(value) % 2 == 0:
        values.append("box " + str(int(value) / 2))
    else:
        values.append("box " + str((int(value) + 1) / 2))
# create column 'Box' with the 'box number' assigned to each donor
data["Box"] = values

'''
	Create columns 'Position' and 'Stimulus' for each donor.
	To each donor, there is 40 TruCulture Trizol pellet tubes.
	For each donor, the script will add new lines with the tube position and the stimulus number
'''
# time consuming!
# initialize a new DataFrame
dic = data.ix[0]
dic["Sample Type"] = "Trizol"
dic["Position"] = 1
dic["Stimulus"] = 1
datatest = pd.DataFrame(columns=dic.index)
c = 0
for l in range(0, len(data)):
	dic = data.ix[l]
    dic["Sample Type"] = "Trizol"
    # 'BoxPos' is even, tubes are positionned from position 41 to 80
    if int(dic["BoxPos"]) % 2 == 0:
        for p in range(42, 82):
            dic["Position"] = p
            dic["Stimulus"] = p - 41
            datatest.loc[c] = dic.values
            c += 1
    else:
        # 'BoxPos' is odd, tubes are positionned from position 1 to 40
        for p in range(1, 41):
            dic["Position"] = p
            dic["Stimulus"] = p
            datatest.loc[c] = dic.values
            c += 1

# rename columns for merge the dataframes
datatest.rename(columns={"FreezerID": "Freezer", "ShelfID": "Level1", "RackID": "Level3"}, inplace=True)
# add column 'Name' that is necessary to create vial samples
datatest["Name"] = datatest["DonorID"]

# keep only TruCulture Trizol pellets data from Freezer CSV file
trizol = df.loc[df["Level2"].str.contains('Trizol')]

# merge datasets
result = pd.merge(trizol, datatest, on=['Freezer', 'Level1', 'Level3', 'Box'], how='inner')

# save result dataframe in a new CSV file
result.to_csv(o_samples, index=False, header=True)
