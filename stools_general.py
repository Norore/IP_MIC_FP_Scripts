#!/usr/bin/env python
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description="""Generate stools samples
                                             for FreezerPro from our data Excel
                                             file""")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-d', '--database', required=True,
                    help="""File that contains data from database for all
                         stools data.""")
parser.add_argument('-v', '--verbose', required=False,
                    help="""If set, will display text of each kind of step.
                    Accepted values:
                        - True
                        - T
                        - Yes
                        - Y
                        - 1
                    """)
parser.add_argument('-a', '--aliquots', required=True,
                    help="""Output file name of aliquots vials that will be
                         generate in CSV format for FreezerPro""")
parser.add_argument('-n', '--dna', required=True,
                    help="""Output file name of dna vials that will be
                         generate in CSV format for FreezerPro""")
parser.add_argument('-s', '--sources', required=True,
                    help="""Output file name of sources vials that will be
                         generate in CSV format for FreezerPro""")
args = vars(parser.parse_args())

f_freezer = args['freezer']
f_database = args['database']
a_samples = args['aliquots']
n_samples = args['dna']
s_samples = args['sources']
verbose = args['verbose']

if verbose in ["True", "T", "Yes", "Y", "1"]:
    verbose = True
else:
    verbose = False

try:
    df_freez = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_freezer))
    exit()

try:
    df_database = pd.read_csv(f_database, sep="\t", dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_database))
    exit()

print("Stools Source Samples")
print(df_database[["Id", "DonorId", "VisitId", "AliquotId", "AliquotingDate", \
                   "Comments"]].head())
print("{} unduplicated Id + DonorId".format(len(df_database[["Id", "DonorId"]].drop_duplicates())))
print("{} unique Id".format(df_database["Id"].nunique()))
print("{} unique DonorId".format(df_database["DonorId"].nunique()))

common_cols = ["Id", "DonorId", "VisitId", "AliquotId", "AliquotingDate", \
                "Comments"]
#df_database = df_database.loc[df_database["AliquotId"] != "1"].copy()
df_source = df_database[common_cols].copy()

df_source.to_csv(s_samples, header = True, index = False)

df_dna = df_database[common_cols + \
                     ["Aliquot_1_DNA_BC", "Aliquot_1_DNA_Location", \
                      "Aliquot_1_DNA_Box", "Aliquot_1_DNA_Date"]].copy()
df_dna.rename(columns={"Aliquot_1_DNA_BC": "Name",
                       "Aliquot_1_DNA_Box": "Box",
                       "Aliquot_1_DNA_Date": "CreationDate",
                       "Aliquot_1_DNA_Location": "Position",
                       "DonorId": "DonorID",
                       "AliquotId": "AliquotID",
                       "VisitId": "VisitID",
                       "Id": "SourceID"},
              inplace=True)

df_freez_dna = pd.merge(df_dna, df_freez, on="Box")
df_freez_dna["Sample Type"] = "FECES_DNA"
df_freez_dna["number"] = df_freez_dna["Position"].str.\
                                                  replace(r'[A-Z]([0-9]{2})', \
                                                  r'\1').astype(int).astype(str)
df_freez_dna["letter"] = df_freez_dna["Position"].str.\
                                                  replace(r'([A-Z])[0-9]{2}', \
                                                  r'\1')
df_freez_dna["Position"] = df_freez_dna["letter"] + " / " + \
                           df_freez_dna["number"]
del df_freez_dna["letter"], df_freez_dna["number"]
df_freez_dna.loc[:, "BOX_BARCODE"] = df_freez_dna["Box"]
df_freez_dna.loc[:, "BoxBarcode"] = df_freez_dna["Box"]
df_freez_dna.loc[:, "FreezerBarcode"] = df_freez_dna["Freezer"]
df_freez_dna.loc[:, "ShelfBarcode"] = df_freez_dna["Level1"]
df_freez_dna.loc[:, "RackBarcode"] = df_freez_dna["Level2"]
df_freez_dna.loc[:, "Sample Source"] = df_freez_dna["DonorID"]
df_freez_dna.loc[:, "Description"] = "Donor "+df_freez_dna["DonorID"]+\
                                     ", Visit "+df_freez_dna["VisitID"]+\
                                     ", Aliquot "+df_freez_dna["AliquotID"]

if verbose:
    print("Writing {} lines in file {}".format(len(df_freez_dna), n_samples))
df_freez_dna.to_csv(n_samples, index=False, header=True)

df_aliquot1 = df_database[common_cols + \
                          ["Aliquot_1_BC", \
                           "Aliquot_1_Weight", \
                           "Aliquot_1_Plate_Location", \
                           "Aliquot_1_Plate_Number"]].copy()
df_aliquot1.rename(columns={"Aliquot_1_BC": "Name",
                            "Aliquot_1_Weight": "Weight",
                            "Aliquot_1_Plate_Number": "Box",
                            "Aliquot_1_Plate_Location": "Position"},
                   inplace=True)
df_aliquot1.loc[:, "Sample Type"] = "Feces Aliquot L"
df_aliquot1.loc[:, "Fraction"] = "L"
df_aliquot2 = df_database[common_cols + \
                          ["Aliquot_2_BC", \
                           "Aliquot_2_Weight", \
                           "Aliquot_2_Plate_Location", \
                           "Aliquot_2_Plate_Number"]].copy()
df_aliquot2.rename(columns={"Aliquot_2_BC": "Name",
                            "Aliquot_2_Weight": "Weight",
                            "Aliquot_2_Plate_Number": "Box",
                            "Aliquot_2_Plate_Location": "Position"},
                   inplace=True)
df_aliquot2.loc[:, "Sample Type"] = "Feces Aliquot R1"
df_aliquot2.loc[:, "Fraction"] = "R1"
df_aliquot3 = df_database[common_cols + \
                          ["Aliquot_3_BC", \
                           "Aliquot_3_Weight", \
                           "Aliquot_3_Plate_Location", \
                           "Aliquot_3_Plate_Number"]].copy()
df_aliquot3.rename(columns={"Aliquot_3_BC": "Name",
                            "Aliquot_3_Weight": "Weight",
                            "Aliquot_3_Plate_Number": "Box",
                            "Aliquot_3_Plate_Location": "Position"},
                   inplace=True)
df_aliquot3.loc[:, "Sample Type"] = "Feces Aliquot R2"
df_aliquot3.loc[:, "Fraction"] = "R2"
df_aliquot4 = df_database[common_cols + \
                          ["Aliquot_4_BC", \
                           "Aliquot_4_Weight", \
                           "Aliquot_4_Plate_Location", \
                           "Aliquot_4_Plate_Number"]].copy()
df_aliquot4.rename(columns={"Aliquot_4_BC": "Name",
                            "Aliquot_4_Weight": "Weight",
                            "Aliquot_4_Plate_Number": "Box",
                            "Aliquot_4_Plate_Location": "Position"},
                   inplace=True)
df_aliquot4.loc[:, "Sample Type"] = "Feces Aliquot R3"
df_aliquot4.loc[:, "Fraction"] = "R3"
df_aliquots = pd.concat([df_aliquot1, df_aliquot2, df_aliquot3, df_aliquot4])
df_aliquots.rename(columns={"DonorId": "DonorID",
                            "AliquotId": "AliquotID",
                            "VisitId": "VisitID",
                            "Id": "SourceID"},
                   inplace=True)

df_freez_aliquot = pd.merge(df_aliquots, df_freez, on="Box")
#df_freez_aliquot["Sample Type"] = "FECES"

df_freez_aliquot["number"] = df_freez_aliquot["Position"].str.\
                                                          replace(r'[A-Z]([0-9]{2})', \
                                                          r'\1').astype(int).astype(str)
df_freez_aliquot["letter"] = df_freez_aliquot["Position"].str.\
                                                          replace(r'([A-Z])[0-9]{2}', \
                                                          r'\1')
df_freez_aliquot["Position"] = df_freez_aliquot["letter"] + " / " + \
                               df_freez_aliquot["number"]
df_freez_aliquot.loc[:, "BOX_BARCODE"] = df_freez_aliquot["Box"]
df_freez_aliquot.loc[:, "BoxBarcode"] = df_freez_aliquot["Box"]
df_freez_aliquot.loc[:, "FreezerBarcode"] = df_freez_aliquot["Freezer"]
df_freez_aliquot.loc[:, "ShelfBarcode"] = df_freez_aliquot["Level1"]
df_freez_aliquot.loc[:, "RackBarcode"] = df_freez_aliquot["Level2"]
df_freez_aliquot.loc[:, "Sample Source"] = df_freez_aliquot["DonorID"]
df_freez_aliquot.loc[:, "Description"] = "Donor "+df_freez_aliquot["DonorID"]+\
                                         ", Visit "+df_freez_aliquot["VisitID"]+\
                                         ", Aliquot "+df_freez_aliquot["AliquotID"]+\
                                         ", Fraction "+df_freez_aliquot["Fraction"]
del df_freez_aliquot["letter"], df_freez_aliquot["number"], \
    df_freez_aliquot["Fraction"]

if verbose:
    print("Writing {} lines in file {}".format(len(df_freez_aliquot), \
                                                a_samples))
df_freez_aliquot.to_csv(a_samples, index=False, header=True)
