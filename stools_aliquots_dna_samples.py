#!/usr/bin/env python
"""
# Stool Aliquots and DNA creation

## Objective

Generate stools Aliquot and DNA samples for FreezerPro from TXT data file
provided by Stanislas and stool source samples mapping.

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


-s|--sources, input file name of sources vials in CSV format provided by FreezerPro,
with fields:
     1. UID: unique identifier, defined by FreezerPro
     2. Name: tube name
     3. Description: tube description
     4. Sample Type: type of sample
     5. Vials: number of vials associated to the tube
     6. Volume: sample volume
     7. Sample Source: source sample, by default, donor in cohort
     8. Sample Group: sample group
     9. Owner: sample owner
    10. Created At: creation date, FreezerPro
    11. Expiration: expiration date, FreezerPro
    12. AliquotingDate: aliquoting date
    13. Troubles: if tube present a problem or is not expected
    14. AliquotID: aliquot ID
    15. Comments: could contains comments about the stool sample
    16. DonorID: donor ID
    17. VisitID: visit ID
    18. RackBarcode: rack barcode
    19. BoxBarcode: box barcode
    20. FreezerBarcode: freezer barcode
    21. ShelfBarcode: shelf barcode
    22. RFID: RFID, defined by FreezerPro
    23. BARCODE: tube barcode, could be set, if not, defined by FreezerPro
    24. Freezer: freezer name
    25. Level1: first level name (Shelf)
    26. Level2: second level name (Rack)
    27. Level3: empty
    28. Level4: empty
    29. Level5: empty
    30. Box: box name
    31. Position: tube position in box

## Expected file format output in arguments

-a|--aliquots, output file name of aliquots vials that will be generate in CSV
format for FreezerPro, with fields:
     1. BARCODE: tube barcode, could be set, if not, defined by FreezerPro
     2. ParentID: stool source UID
     3. Troubles: if source tube present a problem or is not expected
     4. DonorID: donor ID
     5. VisitID: visit ID
     6. AliquotID: aliquot ID
     7. AliquotingDate: aliquoting date
     8. Comments: could contains comments about the stool source sample
     9. Name: tube name
    10. Weight: sample weight
    11. Position: tube position in box
    12. Box: box name
    13. Sample Type: sample type (Feces Aliquot L/R1/R2/R3)
    14. Freezer: freezer name
    15. Freezer_Descr: freezer description
    16. Level1: level 1 name (Shelf)
    17. Level1_Descr: level 1 description
    18. Level2: level 2 name (Rack)
    19. Level2_Descr: level 2 description
    20. Level3: level 3 name (Drawer)
    21. Level3_Descr: level 3 description
    22. Box_Descr:
    23. Box_Descr: box description
    24. BoxType: box type (96 (12 x 8) Stool Well Plate)
    25. BoxBarcode: box barcode (in user-defined fields for the sample type)
    26. FreezerBarcode: box barcode (in user-defined fields for the sample type)
    27. ShelfBarcode: shelf barcode (in user-defined fields for the sample type)
    28. RackBarcode: rack barcode (in user-defined fields for the sample type)
    29. Sample Source: sample source, donor ID in cohort
    30. Description: tube description
    31. SourceID: stool source donor ID

-n|--dna, output file name of dna vials that will be generate in CSV format for
FreezerPro, with fields:
     1. BARCODE: tube barcode, could be set, if not, defined by FreezerPro
     2. ParentID: stool source UID
     3. Troubles: if source tube present a problem or is not expected
     4. DonorID: donor ID
     5. VisitID: visit ID
     6. AliquotID: aliquot ID
     7. AliquotingDate: aliquoting date
     8. Comments: could contains comments about the stool source sample
     9. Name: tube name
    10. Position: tube position in box
    11. Box: box name
    12. CreationDate: creation date of DNA stool sample
    13. Freezer: freezer name
    14. Freezer_Descr: freezer description
    15. Level1: level 1 name (Shelf)
    16. Level1_Descr: level 1 description
    17. Level2: level 2 name (Rack)
    18. Level2_Descr: level 2 description
    19. Level3: level 3 name (Drawer)
    20. Level3_Descr: level 3 description
    21. Box_Descr: box description
    22. BoxType: box type (96 (12 x 8) Stool Well Plate)
    23. Sample Type: sample type (Feces Aliquot L/R1/R2/R3)
    24. BOX_BARCODE: box barcode (FreezerPro field)
    25. BoxBarcode: box barcode (in user-defined fields for the sample type)
    26. FreezerBarcode: box barcode (in user-defined fields for the sample type)
    27. ShelfBarcode: shelf barcode (in user-defined fields for the sample type)
    28. RackBarcode: rack barcode (in user-defined fields for the sample type)
    29. Sample Source: sample source, donor ID in cohort
    30. Description: tube description
    31. SourceID: stool source donor ID
"""
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description=print(__doc__))
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-d', '--database', required=True,
                    help="""File that contains data from database (Stanislas
                         file) for all stools data.""")
parser.add_argument('-s', '--sources', required=False,
                    help="""Input file name of sources vials that are necessary
                         to generate the ParentID field for Aliquot and DNA
                         tubes.""")
parser.add_argument('-a', '--aliquots', required=False,
                    help="""Output file name of aliquots vials that will be
                         generate in CSV format for FreezerPro""")
parser.add_argument('-n', '--dna', required=False,
                    help="""Output file name of dna vials that will be
                         generate in CSV format for FreezerPro""")
parser.add_argument('-v', '--verbose', required=False,
                    help="""If set, will display text of each kind of step.
                    Accepted values:
                        - True
                        - T
                        - Yes
                        - Y
                        - 1
                    """)

args = vars(parser.parse_args())

f_freezer = args['freezer']
f_database = args['database']
f_sources = args['sources']
a_samples = args['aliquots']
n_samples = args['dna']
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

try:
    df_sources = pd.read_csv(f_sources, sep=",", dtype=object)
except IOError:
    print("File '{}' does not exist".format(f_sources))
    exit()

df_sources = df_sources[["BARCODE", "UID", "Troubles"]]

common_cols = ["Id", "DonorId", "VisitId", "AliquotId", "AliquotingDate", \
                "Comments"]
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
                       "Id": "BARCODE"},
                 inplace=True)

df_freez_dna = pd.merge(df_dna, df_freez, on="Box")
df_freez_dna["Sample Type"] = "Stools DNA"
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

"""
    From source vials dataframe, find the BARCODE from Parent source and get
    the UID to generate the field ParentID
"""

df_freez_dna = pd.merge(df_sources, df_freez_dna, on="BARCODE")

df_freez_dna.loc[:, "SourceID"] = df_freez_dna["BARCODE"]
df_freez_dna.loc[:, "BARCODE"] = df_freez_dna["Name"]
df_freez_dna.rename(columns={"UID": "ParentID"}, inplace=True)
df_freez_dna.loc[:, "Box_Descr"] = df_freez_dna["Box_Descr"] + " of " + \
                                df_freez_dna["Level2_Descr"]

if verbose:
    print("Writing {} lines in file {}".format(len(df_freez_dna), n_samples))
if verbose:
    print("File {} generated with {} lines and {} columns".format(n_samples, \
                                                                  df_freez_dna.shape[0],
                                                                  df_freez_dna.shape[1]))
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
df_aliquot1.loc[:, "Sample Type"] = "Stool Aliquot L"
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
df_aliquot2.loc[:, "Sample Type"] = "Stool Aliquot R1"
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
df_aliquot3.loc[:, "Sample Type"] = "Stool Aliquot R2"
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
df_aliquot4.loc[:, "Sample Type"] = "Stool Aliquot R3"
df_aliquot4.loc[:, "Fraction"] = "R3"
df_aliquots = pd.concat([df_aliquot1, df_aliquot2, df_aliquot3, df_aliquot4])
df_aliquots.rename(columns={"DonorId": "DonorID",
                            "AliquotId": "AliquotID",
                            "VisitId": "VisitID",
                            "Id": "BARCODE"},
                   inplace=True)

df_freez_aliquot = pd.merge(df_aliquots, df_freez, on="Box")

df_freez_aliquot.loc[:, "number"] = df_freez_aliquot["Position"].str.\
                                                          replace(r'[A-Z]([0-9]{2})', \
                                                          r'\1').astype(int).astype(str)
df_freez_aliquot.loc[:, "letter"] = df_freez_aliquot["Position"].str.\
                                                          replace(r'([A-Z])[0-9]{2}', \
                                                          r'\1')
df_freez_aliquot.loc[:, "Position"] = df_freez_aliquot["letter"] + " / " + \
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

"""
    From source vials dataframe, find the BARCODE from Parent source and get
    the UID to generate the field ParentID
"""
df_freez_aliquot = pd.merge(df_sources, df_freez_aliquot, on="BARCODE")

df_freez_aliquot.loc[:, "SourceID"] = df_freez_aliquot["BARCODE"]
df_freez_aliquot.loc[:, "BARCODE"] = df_freez_aliquot["Name"]
df_freez_aliquot.rename(columns={"UID": "ParentID"}, inplace=True)
df_freez_aliquot.loc[:, "Box_Descr"] = df_freez_aliquot["Box_Descr"] + " of " + \
                                    df_freez_aliquot["Level2_Descr"]

if verbose:
    print("Writing {} lines in file {}".format(len(df_freez_aliquot), \
                                                a_samples))
if verbose:
    print("File {} generated with {} lines and {} columns".format(a_samples, \
                                                                  df_freez_aliquot.shape[0],
                                                                  df_freez_aliquot.shape[1]))
df_freez_aliquot.to_csv(a_samples, index=False, header=True)
