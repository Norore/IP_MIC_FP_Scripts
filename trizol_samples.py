#!/usr/bin/env python
import pandas as pd
import numpy as np
import argparse
import sys
import re

'''
Initialize arguments
'''

parser = argparse.ArgumentParser(description="""Generate trizol pellet
                    samples for FreezerPro from our data Excel file""")
# Freezer file import
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
# Trizol pellet file import
parser.add_argument('-t', '--truculture', required=True,
                    help="""File with truculture pellet data in XLSX format
                    for merge with freezer data""")
parser.add_argument('-s', '--sheet', required=True,
                    help="""Name of sheet in trizol pellet data in XLSX
                    format to user for merge with freezer data""")
# LabKey sample file import
parser.add_argument('-l', '--labkey', required=True,
                    help="""File with all the samples stored in LabKey,
                    in CSV format, to use for merge with Trizol pellet data""")
# Stimulation sample file import
parser.add_argument('-i', '--stimulation', required=True,
                    help="""File with all the stimulated data in XLSX
                    format to use for merge with Trizol pellet data""")
parser.add_argument('-m', '--sheet2', required=True,
                    help="""Name of sheet in stimulated data in XLSX
                    format to use for merge with freezer data""")
# Output file export
parser.add_argument('-o', '--output', required=True,
                    help="""Output file name that will be generate in
                    CSV format for FreezerPro""")
args = vars(parser.parse_args())

# Freezer file import args
f_freezer = args['freezer']
# Trizol file import args
f_trucult = args['truculture']
n_trsheet = args['sheet']
# LabKey file import args
f_labkey = args['labkey']
# Stimulation file import args
f_stimul = args['stimulation']
n_stsheet = args['sheet2']
# Output file export args
o_samples = args['output']

# Read Freezer file
try:
    df_freezer = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '" + f_freezer + "' does not exist"
    exit()

# Read Trizol file
try:
    truc_data = pd.read_excel(f_trucult, n_trsheet)  # use sheet 'FinalMapping'
except IOError:
    print "File '" + f_trucult + "' does not exist"
    exit()
except:
    print "Sheet '" + n_trsheet + "' does not exist in file '" + f_trucult + "'"
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
    df_stimul = pd.read_excel(f_stimul, n_stsheet)
except IOError:
    print "File '" + f_stimul + "' does not exist"
    exit()
except:
    print "Sheet '" + n_stsheet + "' does not exist in file '" + f_stimul + "'"
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
# dataframe from excel can't be load as dtype object, conversion
truc_data = df_dtypes_object(truc_data)

# change info in samples moved at Fernbach building
indexes = list(truc_data.loc[truc_data["Processed"].isnull() == False].index)
df_fern = truc_data.loc[indexes]
df_fern.reset_index(inplace=True)
del df_fern["index"]
df_fern["FreezerID ShelfID"] = df_fern['FreezerID ShelfID'].str.\
    replace(r'[0-9]{4}', r'1538')
truc_data.drop(indexes, inplace=True)
truc_data.reset_index(inplace=True)
del truc_data["index"]
truc_data = pd.concat([truc_data, df_fern])
del truc_data["Processed"]
# remove samples with no box
indexes = list(truc_data.loc[truc_data["DonorID"].str.contains("no box")].index)
truc_data.drop(indexes, inplace=True)
truc_data.reset_index(inplace=True)
del truc_data["index"]
indexes = list(truc_data.loc[truc_data["DonorID"].str.contains("No box")].index)
truc_data.drop(indexes, inplace=True)
truc_data.reset_index(inplace=True)
del truc_data["index"]
# remove samples with no donor
indexes = list(truc_data.loc[truc_data["DonorID"].str.contains("No donor")].index)
truc_data.drop(indexes, inplace=True)
truc_data.reset_index(inplace=True)
del truc_data["index"]
indexes = list(truc_data.loc[truc_data["DonorID"].str.contains("No Donor")].index)
truc_data.drop(indexes, inplace=True)
truc_data.reset_index(inplace=True)
del truc_data["index"]

# rename column 'FreezerID ShelfID' to 'FreezerLoc'
truc_data.rename(columns={"FreezerID ShelfID": "FreezerLoc"}, inplace=True)

# split column 'FreezerLoc' into 3 new columns: 'MIC', 'FreezerID' and 'ShelfID'
newcols = pd.DataFrame(truc_data.FreezerLoc.str.split().tolist(),
                       columns=["MIC", "FreezerID", "ShelfID"])
newcols["FreezerID"] = newcols["FreezerID"].str.replace('Freezer', '')
newcols["ShelfID"] = newcols["ShelfID"].str.replace('Shelf', 'Shelf ')
# remove 'MIC' column which is not necessary
del newcols["MIC"]

# replace 'MIC-TruCRack_' string by 'Rack ' for a good merge in next instructions
truc_data["RackID"] = truc_data["RackID"].str.replace('MIC-TruCRack_', 'Rack ')
# create column 'FreezerID'
truc_data["FreezerID"] = newcols["FreezerID"]
truc_data["FreezerBarcode"] = "MIC_Freezer#_" + newcols["FreezerID"]
# create column 'ShelfID'
truc_data["ShelfID"] = newcols["ShelfID"]
truc_data["ShelfBarcode"] = "MIC Freezer" + newcols["FreezerID"] + " " + newcols["ShelfID"].str.replace(" ", "")
# remove column 'FreezerLoc' which is not yet necessary
del truc_data["FreezerLoc"]

# calculate, for each donor and each BoxPos, the 'box number' to assign
values = []
for value in truc_data["BoxPos"]:
    if int(value) % 2 == 0:
        values.append("box " + str(int(value) / 2))
    else:
        values.append("box " + str((int(value) + 1) / 2))
# create column 'Box' with the 'box number' assigned to each donor
truc_data["Box"] = values

'''
    Create columns 'Position' and 'Stimulus' for each donor.
    To each donor, there is 40 TruCulture Trizol pellet tubes.
    For each donor, the script will add new lines with the tube
        position and the stimulus number.
'''
# time consuming!
# initialize a new DataFrame from truculture sample file
dic = truc_data.ix[0]
dic["Sample Type"] = "TC_Source_Tube"
dic["Position"] = 1
dic["StimulusID"] = 1
df_trucult = pd.DataFrame(columns=dic.index)
c = 0
for l in range(0, len(truc_data)):
    dic = truc_data.ix[l]
    dic["Sample Type"] = "TC_Source_Tube"
    # 'BoxPos' is even, tubes are positionned from position 41 to 80
    if int(dic["BoxPos"]) % 2 == 0:
        for p in range(42, 82):
            dic["Position"] = int(p)
            dic["StimulusID"] = int(p - 41)
            df_trucult.loc[c] = dic.values
            c += 1
    else:
        # 'BoxPos' is odd, tubes are positionned from position 1 to 40
        for p in range(1, 41):
            dic["Position"] = int(p)
            dic["StimulusID"] = int(p)
            df_trucult.loc[c] = dic.values
            c += 1

# rename columns for merge the dataframes
df_trucult.rename(columns={"FreezerID": "Freezer", "ShelfID": "Level1",
                           "RackID": "Level2"}, inplace=True)
# add column 'Name' that is necessary to create vial samples
df_trucult["Name"] = df_trucult["DonorID"]

''' Populate columns
add columns:
    CenterID: center number (1: Rennes)
    DonorID: donor number
    VisitID: visit number (1 or 2)
    BatchID: batch identifier (A or B)
columns generated from datatest['DonorID']
'''

df_trucult['CenterID'] = df_trucult['DonorID'].str.\
                        replace(r'([0-9]{1})[0-9]{4}[0-9]{1}[A-Z]{1}', r'\1')
df_trucult['VisitID'] = df_trucult['DonorID'].str.\
                        replace(r'[0-9]{1}[0-9]{4}([0-9]{1})[A-Z]{1}', r'\1')
df_trucult['BatchID'] = df_trucult['DonorID'].str.\
                        replace(r'[0-9]{1}[0-9]{4}[0-9]{1}([A-Z]{1})', r'\1')
df_trucult['DonorID'] = df_trucult['DonorID'].str.\
                        replace(r'[0-9]{1}([0-9]{4})[0-9]{1}[A-Z]{1}', r'\1')\
                        .str.replace(r'^0+', '')

# keep only TruCulture Trizol pellets data from Freezer CSV file
trizol = df_freezer.loc[df_freezer["Level2_Desc"].str.contains('Trizol')]

# merge trizol and datatest
merge_ft = pd.merge(trizol,
                    df_trucult,
                    on=['Freezer', 'Level1', 'Level2', 'Box'],
                    how='inner')
merge_ft = df_dtypes_object(merge_ft)

# keep only TRUCULTURE type from LabKey CSV file
truculture = df_labkey.loc[df_labkey['type'] == 'TRUCULTURE']
# rename some columns for merge
truculture.rename(columns={'donorId': 'DonorID', 'visitId': 'VisitID',
                           'batchId': 'BatchID', 'stimulusId': 'StimulusID',
                           'barcodeId': 'barcode'},
                  inplace=True)

# merge merge_ft and truculture
merge_ft['DonorID'] = merge_ft['DonorID'].astype(int)
merge_ft['VisitID'] = merge_ft['VisitID'].astype(int)
merge_ft['StimulusID'] = merge_ft['StimulusID'].astype(int)
truculture['DonorID'] = truculture['DonorID'].astype(int)
truculture['VisitID'] = truculture['VisitID'].astype(int)
truculture['StimulusID'] = truculture['StimulusID'].astype(int)
merge_ftl = pd.merge(merge_ft,
                     truculture,
                     on=['DonorID', 'VisitID', 'BatchID', 'StimulusID'],
                     how='left')
merge_ftl = df_dtypes_object(merge_ftl)

'''
    create DonorIDscanned column from :
        DonorID, VisitID, StimulusID, BatchID and CenterID
'''
# DonorID is not in the same format as df_stimul["DonorIDscanned"]
merge_ftl["DonorFormat"] = [str(i).zfill(4) for i in merge_ftl["DonorID"]]
# StimulusID is not in the same format as df_stimul["DonorIDscanned"]
merge_ftl["StimulusFormat"] = [str(i).zfill(2) for i in merge_ftl["StimulusID"]]
# generate column DonorIDscanned for dataframe merge_ftl
l_donors = []
for idx in range(len(merge_ftl)):
    l_donors.append("".join([str(i) for i in
                              merge_ftl.ix[idx][['CenterID',
                                                 'DonorFormat',
                                                 'VisitID',
                                                 'BatchID',
                                                 'StimulusFormat']]]))
merge_ftl["DonorIDscanned"] = l_donors
del merge_ftl['DonorFormat'], merge_ftl['StimulusFormat']
merge_ftl["volume"] = int(3000)
merge_ftl = df_dtypes_object(merge_ftl)

df_stimul.rename(columns={"Donor_ID.": "DonorID", "Visit": "VisitID",
                          "StimulationNumber": "StimulusID",},
                 inplace=True)
df_stimul = df_dtypes_object(df_stimul)
# clean df_stimul
# remove test tubes
spikelist = df_stimul.loc[df_stimul["DonorIDscanned"].str.
                              match(r"Spike") == True].index
blanclist = df_stimul.loc[df_stimul["DonorIDscanned"].str.
                              match(r"Blanc") == True].index
indexlist = list(spikelist) + list(blanclist)
df_stimul.drop(indexlist, inplace=True)
df_stimul.reset_index(inplace=True)
del df_stimul["index"]

# if _E2$ or _E2_[0-9]{2}$ in DonorIDscanned, increase NbExtraction
df_stimul["NbExtraction"] = 1
extract2index = df_stimul.loc[df_stimul["DonorIDscanned"].str
                        .match(r'[0-9]{6}[AB][0-9]{2}_E2$')].index
extract2index = list(extract2index)
# 285 extract2index expected
extract2donors = df_stimul.loc[extract2index]["DonorIDscanned"].values
extract2donors = list(extract2donors)
list_donors = [re.sub(r'^([0-9]{6}[AB][0-9]{2})_E2$', r'\1', i)
               for i in extract2donors]
donorsindex = []
for donor in list_donors:
    donorsindex.append(df_stimul.loc[df_stimul["DonorIDscanned"] == donor]
                       ["DonorIDscanned"].index.get_values()[0])
# change number of extractions
dic = df_stimul.ix[0]
for e in donorsindex:
    dic = df_stimul.ix[e]
    dic["NbExtraction"] = 2
    df_stimul.loc[e] = dic
# remove _E2$ lines
df_stimul.drop(extract2index, inplace=True)
df_stimul.reset_index(inplace=True)
del df_stimul["index"]

extract3index = df_stimul.loc[df_stimul["DonorIDscanned"].str.\
                        match(r'[0-9]{6}[AB][0-9]{2}_E2_[0-9]{2}$')].index
extract3index = list(extract3index)
# 51 extract3index expected
extract3donors = df_stimul.loc[extract3index]["DonorIDscanned"].values
extract3donors = list(extract3donors)
list_donors = [re.sub(r'^([0-9]{6}[AB][0-9]{2})_E2_[0-9]{2}$', r'\1', i)
               for i in extract3donors]
donorsindex = []
for donor in list_donors:
    donorsindex.append(df_stimul.loc[df_stimul["DonorIDscanned"] == donor]
                       ["DonorIDscanned"].index.get_values()[0])
dic = df_stimul.ix[0]
for e in donorsindex:
    dic = df_stimul.ix[e]
    dic["NbExtraction"] = 3
    df_stimul.loc[e] = dic
# remove _E2_[0-9]{2}$ lines
df_stimul.drop(extract3index, inplace=True)
df_stimul.reset_index(inplace=True)
del df_stimul["index"]
df_stimul = df_dtypes_object(df_stimul)
merge_ftl["VisitID"] = merge_ftl["VisitID"].astype(int)
merge_ftl["DonorID"] = merge_ftl["DonorID"].astype(int)
df_stimul = df_stimul.drop_duplicates()

# works with duplicated DonorIDscanned
donorsduplicated = df_stimul.loc[df_stimul["DonorIDscanned"].
    duplicated()]["DonorIDscanned"].values.tolist()
for e in donorsduplicated:
    df = df_stimul.loc[df_stimul["DonorIDscanned"].str.contains(e)][["DonorIDscanned", "ExtractionName"]]
    # same DonorIDscanned, different run
    if len(df.loc[df_stimul[["DonorIDscanned", "ExtractionName"]].
        duplicated()]["DonorIDscanned"].values.tolist()) == 0:
        donors_dup_first_id = df.loc[df["DonorIDscanned"].
            duplicated(keep="last")]["DonorIDscanned"].index[0]
        donors_dup_last_id = df.loc[df["DonorIDscanned"].
            duplicated(keep="first")]["DonorIDscanned"].index[0]
        # change NbExtraction for first index
        dic = df_stimul.ix[0]
        dic = df_stimul.ix[donors_dup_first_id]
        dic["NbExtraction"] = 2
        df_stimul.loc[donors_dup_first_id] = dic
        # remove last duplicate line
        df_stimul.drop(donors_dup_last_id, inplace=True)
    # same DonorIDscanned, same run, tube scanned twice?
    else:
        donors_dup_first_id = df.loc[df["DonorIDscanned"].
            duplicated(keep="last")]["DonorIDscanned"].index[0]
        donors_dup_last_id = df.loc[df["DonorIDscanned"].
            duplicated(keep="first")]["DonorIDscanned"].index[0]
        # change DonorIDscanned for last index
        dic = df_stimul.ix[0]
        dic = df_stimul.ix[donors_dup_last_id]
        dic["DonorIDscanned"] = str(dic["DonorIDscanned"]) \
                                + str("_trouble")
        df_stimul.loc[donors_dup_last_id] = dic
df_stimul.reset_index(inplace=True)
del df_stimul["index"]

df_stimul["DonorID"] = df_stimul["DonorID"].astype(int)
df_stimul["VisitID"] = df_stimul["VisitID"].astype(int)
df_stimul["StimulusID"] = df_stimul["StimulusID"].astype(int)

merge_ftl["DonorID"] = merge_ftl["DonorID"].astype(int)
merge_ftl["VisitID"] = merge_ftl["VisitID"].astype(int)
merge_ftl["StimulusID"] = merge_ftl["StimulusID"].astype(int)

merge_ftls = pd.merge(merge_ftl,
                      df_stimul,
                      on=['DonorIDscanned', 'VisitID',
                          'DonorID', 'StimulusID'],
                      how='left')
merge_ftls["NbExtraction"] = merge_ftls["NbExtraction"].\
    replace(np.nan, r'0').astype(int)
merge_ftls["volume"] = (merge_ftls["volume"] -
                        (600*merge_ftls["NbExtraction"])).astype(int)
# remove columns that will not be usefull in FreezerPro
rm_columns = ["id", "type", "well", "auditTrail", "deleted",
              "insertDate", "updateDate", "aliquotId",
              "QubitDate", "QubitConcentration_ngul", "CaliperDate",
              "CaliperConcentration_ngul", "NanodropDate",
              "NanodropConcentration_ngul", "DilutionDate", "RNAvolume",
              "NFwaterVolume", "CaliperRQS", "BioanalyzerRIN",
              "Nanodrop260_280", "Nanodrop260_230"]
for col in rm_columns:
    del merge_ftls[col]

merge_ftls["Position"] = merge_ftls["Position"].astype(int)
merge_ftls["BoxPos"] = merge_ftls["BoxPos"].astype(int)

# rename columns
merge_ftls.rename(columns={"volume": "Volume",
                           "Matrix_TubePosition.": "Matrix_TubePosition",
                           "NbExtraction": "FreezeThaw",
                           "rackId": "RackID"},
                 inplace=True)

# save result dataframe in a new CSV file
merge_ftls.to_csv(o_samples, index=False, header=True)