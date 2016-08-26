#!/usr/bin/env python
import pandas as pd
import argparse
import re

parser = argparse.ArgumentParser(description="Generate stools samples for FreezerPro from our data Excel file")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-l', '--labkey', required=True,
                    help="""File with all the samples stored in LabKey,
                    in CSV format, to use for merge with Trizol pellet data""")
parser.add_argument('-o', '--output', required=True,
                    help="Output file name that will be generate in CSV format for FreezerPro")
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_labkey = args['labkey']
o_samples = args['output']

try:
    df_freezer = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '"+f_freezer+"' does not exist"
    exit()

try:
    df_labkey = pd.read_csv(f_labkey, dtype=object)
except IOError:
    print "File '"+f_labkey+"' does not exist"
    exit()

df_super = df_freezer.loc[df_freezer["Level2_Desc"].str.contains("Supernatants")]
df_super.reset_index(inplace=True)
del df_super["index"]

# Create new colum to work in it to prepare merges
df_super["DonorInfos"] = df_super["Level2"]
df_super["donor_start"] = df_super["Level2"]
df_super["donor_stop"] = df_super["Level2"]
# split lines Donors [0-9]{3}>>[0-9]{3} | Donors [0-9]{3}>>[0-9]{3}
inc = 1
lines = len(df_super)
for i in range(lines):
    if re.match(r'^Donors [0-9]{3}>>[0-9]{3}$', df_super.iloc[i]["Level2"]):
        regex = re.compile(r'^Donors ([0-9]{3})>>([0-9]{3})$')
        df_super.loc[i, "donor_start"] = int(
            regex.sub(r'\1', df_super.iloc[i]["Level2"]))
        df_super.loc[i, "donor_stop"] = int(
            regex.sub(r'\2', df_super.iloc[i]["Level2"]))

    elif re.match(r'^Donors [0-9]{3}>>[0-9]{3} \| Donors '
                  r'[0-9]{3}>>[0-9]{3}$', df_super.iloc[i]["Level2"]):
        regex = re.compile(r'^(Donors ([0-9]{3})>>([0-9]{3})) \| (Donors ([0-9]{3})>>([0-9]{3}))$')
        df_super.loc[i, "DonorInfos"] = regex.sub(
            r'\1', df_super.iloc[i]["Level2"])
        df_super.loc[i, "donor_start"] = int(
            regex.sub(r'\2', df_super.iloc[i]["Level2"]))
        df_super.loc[i, "donor_stop"] = int(
            regex.sub(r'\3', df_super.iloc[i]["Level2"]))
        df_super.loc[i+inc] = df_super.iloc[i]
        df_super.loc[i+inc, "DonorInfos"] = regex.sub(
            r'\4', df_super.iloc[i]["Level2"])
        df_super.loc[i+inc, "donor_start"] = int(
            regex.sub(r'\5', df_super.iloc[i]["Level2"]))
        df_super.loc[i+inc, "donor_stop"] = int(
            regex.sub(r'\6', df_super.iloc[i]["Level2"]))
        inc += 1

    elif re.match(r'^Donors X[0-9]{2}>>X[0-9]{2}$',
                  df_super.iloc[i]["Level2"]):
        regex = re.compile(r'^Donors X([0-9]{2})>>X([0-9]{2})$')
        df_super.loc[i, "donor_start"] = int(
            regex.sub(r'\1', df_super.iloc[i]["Level2"]))
        df_super.loc[i, "donor_stop"] = int(
            regex.sub(r'\2', df_super.iloc[i]["Level2"]))

    else:
        df_super.loc[i, "DonorInfos"] = df_super.iloc[i]["Level2"]

l_donors = df_super["DonorInfos"].unique().tolist()
dic = df_super[["DonorInfos", "donor_start", "donor_stop"]].ix[0]
dic["DonorID"] = 1
dic["Position"] = 1
df_tomerge = pd.DataFrame(columns=dic.index)
count = 0
for di in l_donors:
    if re.match(r'^Donors', di):
        pos = 1
        get_index = pd.DataFrame.drop_duplicates(
            df_super.loc[df_super["DonorInfos"].str.contains(di)]
            [["DonorInfos", "donor_start", "donor_stop"]]).index
        dic = df_super[["DonorInfos", "donor_start", "donor_stop"]].ix[get_index[0]]
        for d in range(dic["donor_start"], dic["donor_stop"]+1):
            dic["DonorID"] = d
            dic["Position"] = pos
            df_tomerge.loc[count] = dic.values
            count += 1
            pos += 1

# merge df_super and df_tomerge
df_infreezers = pd.merge(df_super, df_tomerge, on=["DonorInfos",
                                                   "donor_start", "donor_stop"])

# prepare columns to use for merge
df_infreezers["AliquotID"] = df_infreezers["Level2_Desc"].str.\
    replace(r'^TruCulture Supernatants, Aliquot ([1-3]), Visit ([1-2]), \w+', r'\1')
df_infreezers["VisitID"] = df_infreezers["Level2_Desc"].str.\
    replace(r'^TruCulture Supernatants, Aliquot ([1-3]), Visit ([1-2]), \w+', r'\2')
df_infreezers["StimulusID"] = df_infreezers["Box"].str.replace(r'box ([0-9]{1,2})', r'\1')

# prepare labkey data for merge
del df_labkey["id"], df_labkey["auditTrail"], df_labkey["well"], \
    df_labkey["deleted"], df_labkey["insertDate"], df_labkey["updateDate"]
df_labkey.rename(columns={"barcodeId": "BarcodeID", "donorId": "DonorID",
                          "visitId": "VisitID", "batchId": "BatchID",
                          "type": "Type", "stimulusId": "StimulusID",
                          "volume": "Volume", "aliquotId": "AliquotID",
                          "rackId": "RackID"},
                 inplace=True)

# get only PLASMA_ lines
df_labkey = df_labkey.loc[df_labkey["Type"].str.contains("PLASMA_")]
df_labkey["OriginalDonorID"] = df_labkey["DonorID"]

df_toreplace = df_labkey.loc[df_labkey["DonorID"].str.contains(r'^5[0-9]{3}$')]
df_toreplace["DonorID"] = df_toreplace["OriginalDonorID"].str.replace(r'^5([0-9]{3})$', r'\1')
df_labkey["DonorID"] = df_labkey["OriginalDonorID"].str.replace(r'^5([0-9]{3})$', r'\1')
df_toreplace["DonorID"] = df_toreplace["DonorID"].astype(int)
df_toreplace["OriginalDonorID"] = df_toreplace["OriginalDonorID"].astype(int)
df_toreplace["DonorID"] = df_toreplace["DonorID"].astype(int)
df_toreplace["OriginalDonorID"] = df_toreplace["OriginalDonorID"].astype(int)

l_excluded = df_toreplace["DonorID"].unique().tolist()

for e in l_excluded:
    df_todrop = df_labkey.loc[df_labkey["OriginalDonorID"] == e]
    df_labkey.drop(df_todrop.index, inplace=True)
df_labkey.reset_index(inplace=True)
del df_labkey["index"]

# prepare columns type for merge
df_infreezers["AliquotID"] = df_infreezers["AliquotID"].astype(int)
df_labkey["AliquotID"] = df_labkey["AliquotID"].astype(int)
df_infreezers["DonorID"] = df_infreezers["DonorID"].astype(int)
df_labkey["DonorID"] = df_labkey["DonorID"].astype(int)
df_infreezers["VisitID"] = df_infreezers["VisitID"].astype(int)
df_labkey["VisitID"] = df_labkey["VisitID"].astype(int)
df_infreezers["StimulusID"] = df_infreezers["StimulusID"].astype(int)
df_labkey["StimulusID"] = df_labkey["StimulusID"].astype(int)

result = pd.merge(df_infreezers, df_labkey, on=["DonorID", "AliquotID",
                                                "VisitID", "StimulusID"],
                  how='inner')

result.to_csv(o_samples, index=False, header=True)
