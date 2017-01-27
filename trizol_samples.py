#!/usr/bin/env python
import pandas as pd
import numpy as np
import argparse
import sys
import re
from MI_FP_common import *

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
# Stimulus info file import
parser.add_argument('-u', '--stimulus', required=True,
                    help="""File with all stimuli in CSV
                    format to use for merge with Trizol pellet data""")
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
# Stimulus file import args
f_stimulus = args['stimulus']
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

# Read stimulus file
try:
    df_stimulus = pd.read_csv(f_stimulus, dtype=object)
except IOError:
    print "File '" + f_stimulus + "' does not exist"
    exit()

'''
Main script starts here
'''
# dataframe from excel can't be load as dtype object, conversion
truc_data = df_dtypes_object(truc_data)

# change info in samples moved at Fernbach building
df_fernbach = truc_data.loc[truc_data["Processed"].isnull() == False]
df_fernbach.reset_index(drop=True, inplace=True)
df_fernbach.loc[:, "FreezerID ShelfID"] = df_fernbach['FreezerID ShelfID'].str.\
                                            replace(r'[0-9]{4}', r'1538')

truc_data = truc_data.loc[truc_data["Processed"].isnull()]
truc_data.reset_index(drop=True, inplace=True)

truc_data = pd.concat([truc_data, df_fernbach])
truc_data.reset_index(drop=True, inplace=True)
del truc_data["Processed"]

# remove samples with no box
truc_data = truc_data.loc[~(truc_data["DonorID"].isin(["no box", "No box", \
                                                      "No donor", "No Donor"]))]
truc_data.reset_index(drop=True, inplace=True)

# rename column 'FreezerID ShelfID' to 'FreezerLoc'
truc_data.rename(columns={"FreezerID ShelfID": "FreezerLoc",
                          "RackID": "Level2"}, inplace=True)

# split column 'FreezerLoc' into 3 new columns: 'MIC', 'FreezerID' and 'ShelfID'
newcols = pd.DataFrame(truc_data.FreezerLoc.str.split().tolist(),
                       columns=["MIC", "FreezerID", "ShelfID"])
newcols.loc[:, "FreezerID"] = newcols["FreezerID"].str.replace('Freezer', '')
newcols.loc[:, "ShelfID"] = newcols["ShelfID"].str.replace('Shelf', 'Shelf ')
# remove 'MIC' column which is not necessary
del newcols["MIC"]

# create column 'FreezerID'
newcols["FreezerID"] = newcols["FreezerID"].astype(str)
truc_data["Freezer"] = "MIC_Freezer_" + newcols["FreezerID"]
# create column 'ShelfID'
newcols.loc[:, "ShelfID"] = newcols["ShelfID"].astype(str)
truc_data.loc[:, "Level1"] = "MIC Freezer" + newcols["FreezerID"] + \
                             " " + newcols["ShelfID"].str.replace(" ", "")
# remove column 'FreezerLoc' which is not yet necessary
del truc_data["FreezerLoc"]

# calculate, for each donor and each BoxPos, the 'box number' to assign
values = []
for value in truc_data["BoxPos"]:
    if int(value) % 2 == 0:
        values.append("Box " + str(int(value) / 2))
    else:
        values.append("Box " + str((int(value) + 1) / 2))
# create column 'Box' with the 'box number' assigned to each donor
truc_data.loc[:, "Box"] = values

'''
    Create columns 'Position' and 'Stimulus' for each donor.
    To each donor, there is 40 TruCulture Trizol pellet tubes.
    For each donor, the script will add new lines with the tube
        position and the stimulus number.
'''

boxpos, position, stimulusid = [], [], []
for nb_boxpos in range(1, 21):
    if nb_boxpos % 2 == 0:
        for pos in range(42, 82):
            boxpos.append(nb_boxpos)
            position.append(pos)
            stimulusid.append(pos-41)
    if nb_boxpos % 2 == 1:
        for pos in range(1, 41):
            boxpos.append(nb_boxpos)
            position.append(pos)
            stimulusid.append(pos)

boxes = pd.DataFrame({'BoxPos': boxpos, 'Position': position,
                      'StimulusID': stimulusid}, dtype=object)
boxes.loc[:, "Sample Type"] = ["TC Source Tube"]*len(stimulusid)
boxes.loc[:, "StimulusID"] = boxes["StimulusID"].astype(int)

# prepare stimulus dataframe
del df_stimulus["type"], df_stimulus["description"], df_stimulus["sensor"]
df_stimulus.rename(columns={"stimulusId": "StimulusID", "name": "StimulusName"},
                    inplace = True)
df_stimulus.loc[:, "StimulusID"] = df_stimulus["StimulusID"].astype(int)

df_boxes = pd.merge(boxes, df_stimulus, on=["StimulusID"])
df_trucult = pd.merge(truc_data, df_boxes, on=["BoxPos"])

# add column 'Name' that is necessary to create vial samples
df_trucult.loc[:, "Name"] = df_trucult["DonorID"]

''' Populate columns
add columns:
    CenterID: center number (1: Rennes)
    DonorID: donor number
    VisitID: visit number (1 or 2)
    BatchID: batch identifier (A or B)
columns generated from datatest['DonorID']
'''

df_trucult.loc[:, 'CenterID'] = df_trucult['DonorID'].str.\
                                replace(r'([0-9]{1})[0-9]{4}[0-9]{1}[A-Z]{1}', \
                                        r'\1')
df_trucult.loc[:, 'VisitID'] = df_trucult['DonorID'].str.\
                               replace(r'[0-9]{1}[0-9]{4}([0-9]{1})[A-Z]{1}', \
                                       r'\1')
df_trucult.loc[:, 'BatchID'] = df_trucult['DonorID'].str.\
                               replace(r'[0-9]{1}[0-9]{4}[0-9]{1}([A-Z]{1})', \
                                       r'\1')
df_trucult.loc[:, 'DonorID'] = df_trucult['DonorID'].str.\
                               replace(r'[0-9]{1}([0-9]{4})[0-9]{1}[A-Z]{1}', \
                                       r'\1').str.replace(r'^0+', '')

print("{} unique DonorID in df_trucult.".\
        format(df_trucult["DonorID"].nunique()))
print(df_trucult.groupby("DonorID")["Name"].nunique())

# keep only TruCulture Trizol pellets data from Freezer CSV file
trizol = df_freezer.loc[df_freezer["Level2_Descr"].str.contains('Trizol')]
# drop duplicates
indexes = df_trucult[['DonorID', 'VisitID', 'BatchID', 'StimulusID']].\
                        drop_duplicates(keep="first").index
df_trucult = df_trucult.loc[indexes]
df_trucult.reset_index(inplace=True)
del df_trucult["index"]

print("{} unique Level1 in df_trucult.".\
        format(df_trucult["Level1"].nunique()))
print("{} unique Level1 in trizol.".\
        format(trizol["Level1"].nunique()))

# merge trizol and datatest
merge_ft = pd.merge(trizol,
                    df_trucult,
                    on=['Freezer', 'Level1', 'Level2', 'Box'],
                    how='inner')
merge_ft = df_dtypes_object(merge_ft)
print("{} unique Level1 in merge_ft.".\
        format(merge_ft["Level1"].nunique()))

# keep only TRUCULTURE type from LabKey CSV file
truculture = df_labkey.loc[df_labkey['type'] == 'TRUCULTURE']
# rename some columns for merge
truculture.rename(columns={'donorId': 'DonorID', 'visitId': 'VisitID',
                           'batchId': 'BatchID', 'stimulusId': 'StimulusID',
                           'barcodeId': 'BARCODE'},
                  inplace=True)

print("{} unique DonorID in truculture.".\
        format(truculture["DonorID"].nunique()))

# drop line if no DonorID
indexes = list(merge_ft.loc[merge_ft["DonorID"].isnull() == True].index)
merge_ft.drop(indexes, inplace=True)
merge_ft.reset_index(inplace=True)
del merge_ft["index"]

# merge merge_ft and truculture
merge_ft.loc[:, 'DonorID'] = merge_ft['DonorID'].astype(int)
merge_ft.loc[:, 'VisitID'] = merge_ft['VisitID'].astype(int)
merge_ft.loc[:, 'StimulusID'] = merge_ft['StimulusID'].astype(int)
truculture.loc[:, 'DonorID'] = truculture['DonorID'].astype(int)
truculture.loc[:, 'VisitID'] = truculture['VisitID'].astype(int)
truculture.loc[:, 'StimulusID'] = truculture['StimulusID'].astype(int)
merge_ftl = pd.merge(merge_ft,
                     truculture,
                     on=['DonorID', 'VisitID', 'BatchID', 'StimulusID'],
                     how='inner')
merge_ftl.loc[:, "BoxType"] = trizol["BoxType"].unique()[0]
merge_ftl = df_dtypes_object(merge_ftl)

print("{} unique DonorID in merge_ftl.".\
        format(merge_ftl["DonorID"].nunique()))

'''
    create DonorIDscanned column from :
        DonorID, VisitID, StimulusID, BatchID and CenterID
'''
# DonorID is not in the same format as df_stimul["DonorIDscanned"]
merge_ftl.loc[:, "DonorFormat"] = [str(i).zfill(4) \
                                    for i in merge_ftl["DonorID"]]
# StimulusID is not in the same format as df_stimul["DonorIDscanned"]
merge_ftl.loc[:, "StimulusFormat"] = [str(i).zfill(2) \
                                        for i in merge_ftl["StimulusID"]]
# generate column DonorIDscanned for dataframe merge_ftl
l_donors = []
for idx in range(len(merge_ftl)):
    l_donors.append("".join([str(i) for i in
                              merge_ftl.ix[idx][['CenterID',
                                                 'DonorFormat',
                                                 'VisitID',
                                                 'BatchID',
                                                 'StimulusFormat']]]))
merge_ftl.loc[:, "DonorIDscanned"] = l_donors
del merge_ftl['DonorFormat'], merge_ftl['StimulusFormat']
merge_ftl.loc[:, "volume"] = int(3000)
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
df_stimul.loc[:, "NbExtraction"] = 1
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

extract3index = df_stimul.loc[df_stimul["DonorIDscanned"].str. \
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
merge_ftl.loc[:, "VisitID"] = merge_ftl["VisitID"].astype(int)
merge_ftl.loc[:, "DonorID"] = merge_ftl["DonorID"].astype(int)
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
        dic["DonorIDscanned"] = str(dic["DonorIDscanned"]) + \
                                str("_trouble")
        df_stimul.loc[donors_dup_last_id] = dic
df_stimul.reset_index(inplace=True)
del df_stimul["index"]

df_stimul.loc[:, "DonorID"] = df_stimul["DonorID"].astype(int)
df_stimul.loc[:, "VisitID"] = df_stimul["VisitID"].astype(int)
df_stimul.loc[:, "StimulusID"] = df_stimul["StimulusID"].astype(int)

merge_ftl.loc[:, "DonorID"] = merge_ftl["DonorID"].astype(int)
merge_ftl.loc[:, "VisitID"] = merge_ftl["VisitID"].astype(int)
merge_ftl.loc[:, "StimulusID"] = merge_ftl["StimulusID"].astype(int)

merge_ftls = pd.merge(merge_ftl,
                      df_stimul,
                      on=['DonorIDscanned', 'VisitID',
                          'DonorID', 'StimulusID'],
                      how='left')
merge_ftls.loc[:, "NbExtraction"] = merge_ftls["NbExtraction"].\
    replace(np.nan, r'0').astype(int)
merge_ftls.loc[:, "volume"] = (merge_ftls["volume"] -
                        (600*merge_ftls["NbExtraction"])).astype(int)

# remove columns that will not be usefull in FreezerPro
rm_columns = ["id", "type", "well", "auditTrail", "deleted",
              "insertDate", "updateDate", "aliquotId",
              "QubitDate", "QubitConcentration_ngul", "CaliperDate",
              "CaliperConcentration_ngul", "NanodropDate",
              "NanodropConcentration_ngul", "DilutionDate", "RNAvolume",
              "NFwaterVolume", "CaliperRQS", "BioanalyzerRIN",
              "Nanodrop260_280", "Nanodrop260_230", "TECAN_RackNumber",
              "TECAN_RackPosition", "Matrix_RackBarcodeScanned",
              "Matrix_TubeBarcodeScanned", "Matrix_TubePosition.", "rackId"]
for col in rm_columns:
    del merge_ftls[col]

merge_ftls.loc[:, "Position"] = merge_ftls["Position"].astype(int)
merge_ftls.loc[:, "BoxPos"] = merge_ftls["BoxPos"].astype(int)

# rename columns
merge_ftls.rename(columns={"volume": "Volume",
                           "NbExtraction": "FreezeThaw"},
                  inplace=True)

merge_ftls.loc[:, "FreezerBarcode"] = merge_ftls["Freezer"]
merge_ftls.loc[:, "ShelfBarcode"] = merge_ftls["Level1"]
merge_ftls.loc[:, "RackBarcode"] = merge_ftls["Level2"]
merge_ftls.loc[:, "Name"] = merge_ftls["BARCODE"]

'''
Box and BoxBarcode should have this barcode:
    CDDDDVB:
        * C -> CenterID
        * D -> DonorID (4 digits)
        * V -> VisitID
        * B -> BatchID
'''
merge_ftls.loc[:, "DonorID"] = merge_ftls["DonorID"].astype(str)
merge_ftls.loc[:, "F_Donor"] = merge_ftls["DonorID"]

merge_ftls.loc[:, "F_Donor"] = merge_ftls["F_Donor"].str.zfill(4)

merge_ftls.loc[:, "CenterID"] = merge_ftls["CenterID"].astype(str)
merge_ftls.loc[:, "VisitID"] = merge_ftls["VisitID"].astype(str)
merge_ftls.loc[:, "BatchID"] = merge_ftls["BatchID"].astype(str)
merge_ftls.loc[:, "FLAG"] = merge_ftls["CenterID"] + merge_ftls["F_Donor"] \
                     + merge_ftls["VisitID"] + merge_ftls["BatchID"]

df_boxbc = merge_ftls[["Freezer", "Level1", "Level2", "Box", "FLAG"]].drop_duplicates()
df_boxbc.loc[:, "Location"] = df_boxbc["Freezer"] + " " + df_boxbc["Level1"] + " " \
                              + df_boxbc["Level2"] + " " + df_boxbc["Box"]

dic_boxbc = { k:" ".join(df_boxbc.loc[df_boxbc["Location"] == k, "FLAG"]\
                            .unique()) for k in df_boxbc["Location"].unique()}

df_dicbox = pd.DataFrame({"Location": dic_boxbc.keys(), \
                          "BOXBARCODE": dic_boxbc.values()}, dtype=object)

merge_boxloc = pd.merge(df_dicbox, df_boxbc, on=["Location"])\
                [["FLAG", "BOXBARCODE"]]

merge_final = pd.merge(merge_ftls, merge_boxloc, on=["FLAG"])
merge_final.loc[:, "Box"] = merge_final["BOXBARCODE"]
del merge_final["F_Donor"], merge_final["FLAG"]

# save result dataframe in a new CSV file
merge_final.to_csv(o_samples, index=False, header=True)
