
## Objective

## Expected file formats put in arguments

--frezer, file with freezer data in CSV format for FreezerPro, with fields:
    1. Box: box name in freezer
    2. Freezer: freezer name
    3. Freezer_Descr: freezer description
    4. Level1: level 1 name (Shelf)
    5. Level1_Descr: level 1 description
    6. Level2: level 2 name (Rack)
    7. Level2_Descr: level 2 description
    8. Level3: level 3 name (Drawer)
    9. Level3_Descr: level 3 description

--database, file that contains data from database for all stools data, with
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

--location, ile that contains location of each tubes in each box for stools
source samples, with fields:
    1. Level1: level 1 name (Shelf)
    2. Level3: level 3 name (Rack)
    3. Box_Descr: box description (Box number)
    4. Position: tube position in box
    5. BARCODE: tube barcode
    6. BOX_BARCODE: box barcode

## Expected file formats output in arguments
     1. BARCODE: tube barcode
     2. DonorID: donor ID
     3. VisitID: visit ID
     4. AliquotID: aliquot ID
     5. AliquotingDate: aliquoting date
     6. Comments: could contains comments about the stool sample
     7. Level1: level 1 name (Shelf)
     8. Box_Descr: box description
     9. Position: tube position in box
    10. BOX_BARCODE: box barcode
    11. Freezer: freezer name
    12. Freezer_Descr: freezer description
    13. Level1_Descr: level 1 description
    14. Level2: level 2 name (Rack)
    15. Level2_Descr: level 2 description
    16. Box: box name
    17. BoxType: box type
    18. Sample Type: sample type
    19. Sample Source: sample source
    20. Description: tube description
    21. FreezerBarcode: freezer barcode
    22. ShelfBarcode: shelf barcode
    23. RackBarcode: rack barcode


usage: stools_source_samples.py [-h] -f FREEZER -d DATABASE -l LOCATION -o
                                OUTPUT [-v VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -d DATABASE, --database DATABASE
                        File that contains data from database for all stools
                        data.
  -l LOCATION, --location LOCATION
                        File that contains location of each tubes in each box
                        for stools source samples
  -o OUTPUT, --output OUTPUT
                        Output file name of sources vials that will be
                        generate in CSV format for FreezerPro
  -v VERBOSE, --verbose VERBOSE
                        If set, will display text of each kind of step.
                        Accepted values: - True - T - Yes - Y - 1
