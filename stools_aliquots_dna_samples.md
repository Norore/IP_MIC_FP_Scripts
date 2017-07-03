
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

usage: stools_aliquots_dna_samples.py [-h] -f FREEZER -d DATABASE [-s SOURCES]
                                      [-a ALIQUOTS] [-n DNA] [-v VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -d DATABASE, --database DATABASE
                        File that contains data from database (Stanislas file)
                        for all stools data.
  -s SOURCES, --sources SOURCES
                        Input file name of sources vials that are necessary to
                        generate the ParentID field for Aliquot and DNA tubes.
  -a ALIQUOTS, --aliquots ALIQUOTS
                        Output file name of aliquots vials that will be
                        generate in CSV format for FreezerPro
  -n DNA, --dna DNA     Output file name of dna vials that will be generate in
                        CSV format for FreezerPro
  -v VERBOSE, --verbose VERBOSE
                        If set, will display text of each kind of step.
                        Accepted values: - True - T - Yes - Y - 1
