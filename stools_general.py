#!/usr/bin/env python
"""
# Stool general

## Objective

Generate stools samples for FreezerPro from data Excel file provided by
Stanislas.

This script is almost out of date, you will probably better use the following
scripts:
    * stools_source_samples.py
    * stools_aliquot_samples.py

## Expected file formats put in arguments

-f|--frezer, file with freezer data in CSV format for FreezerPro, with fields:
    1. Box: box name in freezer
    2. Freezer: freezer name
    3. Freezer_Descr: freezer description
    4. Level1: level 1 name (Shelf)
    5. Level1_Descr: level 1 description
    6. Level2: level 2 name (Rack)
    7. Level2_Descr: level 2 description
    8. Level3: level 3 name (Drawer)
    9. Level3_Descr: level 3 description

-d|--database, file that contains data from database for all stools data, with
fields:
     1. Id: stool source tube barcode
     2. DonorId: donor ID
     3. VisitId: visit ID
     4. AliquotId: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool sample
     7. Aliquot_1_BC: stool aliquot L tube barcode
     8. Aliquot_1_Weight: stool aliquot L weight sample
     9. Aliquot_1_Plate_Location: stool aliquot L tube position in box
    10. Aliquot_1_Plate_Number: stool aliquot L box barcode
    11. Aliquot_1_DNA_BC: stool DNA tube barcode
    12. Aliquot_1_DNA_Location: stool DNA tube position in box
    13. Aliquot_1_DNA_Box: stool DNA box barcode
    14. Aliquot_1_DNA_Date: stool DNA sample aliquoting date
    15. Aliquot_2_BC: stool aliquot R1 tube barcode
    16. Aliquot_2_Weight: stool aliquot R1 weight sample
    17. Aliquot_2_Plate_Location: stool aliquot R1 tube position in box
    18. Aliquot_2_Plate_Number: stool aliquot R1 box barcode
    19. Aliquot_3_BC: stool aliquot R2 tube barcode
    20. Aliquot_3_Weight: stool aliquot R2 weight sample
    21. Aliquot_3_Plate_Location: stool aliquot R2 tube position in box
    22. Aliquot_3_Plate_Number: stool aliquot R2 box barcode
    23. Aliquot_4_BC: stool aliquot R3 tube barcode
    24. Aliquot_4_Weight: stool aliquot R3 weight sample
    25. Aliquot_4_Plate_Location: stool aliquot R3 tube position in box
    26. Aliquot_4_Plate_Number: stool aliquot R3 box barcode

## Expected file format output in arguments

`-s|--source`, output file name of sources vials that will be generate in CSV
format for FreezerPro, with fields:

    1. Id: tube barcode
    2. DonorId: donor ID
    3. VisitId: visit ID
    4. AliquotId: aliquot ID
    5. AliquotingDate: aliquoting date
    6. Comments: could contains comments about the stool source sample

-a|--aliquots, output file name of aliquots vials that will be generate in CSV
format for FreezerPro, with fiels:
     1. SourceID: stool source barcode
     2. DonorID: donor ID
     3. VisitID: visit ID
     4. AliquotID: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool source sample
     7. Name: tube name
     8. Weight: sample weight
     9. Position: tube position in box
    10. Box: box name
    11. Sample Type: sample type (Feces Aliquot L/R1/R2/R3)
    12. Freezer: freezer name
    13. Freezer_Descr: freezer description
    14. Level1: level 1 name (Shelf)
    15. Level1_Descr: level 1 description
    16. Level2: level 2 name (Rack)
    17. Level2_Descr: level 2 description
    18. Level3: level 3 name (Drawer)
    19. Level3_Descr: level 3 description
    20. Box_Descr: box description
    21. BoxType: box type (96 (12 x 8) Stool Well Plate)
    22. BOX_BARCODE: box barcode (FreezerPro field)
    23. BoxBarcode: box barcode (in user-defined fields for the sample type)
    24. FreezerBarcode: box barcode (in user-defined fields for the sample type)
    25. ShelfBarcode: shelf barcode (in user-defined fields for the sample type)
    26. RackBarcode: rack barcode (in user-defined fields for the sample type)
    27. Sample Source: sample source, donor ID in cohort
    28. Description: tube description

-d|--dna, output file name of dna vials that will be generate in CSV format for
FreezerPro, with fields:
     1. SourceID: stool source barcode
     2. DonorID: donor ID
     3. VisitID: visit ID
     4. AliquotID: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool source sample
     7. Name: tube name
     8. Position: tube position in box
     9. Box: box name
    10. CreationDate: stool DNA sample aliquoting date
    11. Freezer: freezer name
    12. Freezer_Descr: freezer description
    13. Level1: level 1 name (Shelf)
    14. Level1_Descr: level 1 description
    15. Level2: level 2 name (Rack)
    16. Level2_Descr: level 2 description
    17. Level3: level 3 name (Drawer)
    18. Level3_Descr: level 3 description
    19. Box_Descr: box description
    20. BoxType: box type (96 (12 x 8) Well Plate)
    21. Sample Type: sample type (FECES_DNA)
    22. BOX_BARCODE: box barcode (FreezerPro field)
    23. BoxBarcode: box barcode (in user-defined fields for the sample type)
    24. FreezerBarcode: freezer barcode (in user-defined fields for the sample type)
    25. ShelfBarcode: shelf barcode (in user-defined fields for the sample type)
    26. RackBarcode: rack barcode (in user-defined fields for the sample type)
    27. Sample Source: sample source, donor ID in cohort
    28. Description: tube description

-s|--sources, output file name of sources vials that will be generate in CSV
format for FreezerPro, with fields:
    1. Id: tube barcode
    2. DonorId: donor ID
    3. VisitId: visit ID
    4. AliquotId: aliquot ID
    5. AliquotingDate: aliquoting date
    6. Comments: could contains comments about the stool sample
"""
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description=print(__doc__))
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
