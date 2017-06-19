# TruCulture Supernatant Visit 1 creation

## Objective

From freezer mapping and knowledge of how the tubes are stored in each box,
will generate an output file for implementation into FreezerPro for the
TruCulture supernatants, in Visit 1.

## Expected file formats read

freezer mapping (../DataToImport/freezers_supernatants.csv), with fields:

1. Freezer: freezer name
2. Freezer_Descr: freezer description
3. Level1: level 1 name (Shelf)
4. Level1_Descr: level 1 description
5. Level2: level 2 name (Rack)
6. Level2_Descr: level 2 description
7. Level3: level 3 name (Drawer)
8. Level3_Descr: level 3 description
9. Box: box name
10. Box_Descr: box description
11. BoxType: box type (96 (12 x 8) Well Plate)

specific donors mapping (../DataToPrepare/donors_X97_X00.json), will look like:

    {
      "A": [97, 197, 297, 397, 497, 597, 697, 797, 897, 997],
      "B": [98, 198, 298, 398, 498, 598, 698, 798, 898, 998],
      "C": [99, 199, 299, 399, 499, 599, 699, 799, 899, 999],
      "D": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    }
where key "A" is the line value in box, and value in list form is the DonorID
in each well of current line.

stimulus informations (../DataToPrepare/LabExMI_Stimuli_List.csv), with fields:

1. stimulusId: stimulus ID
2. name: stimulus name
3. type: stimulus type
4. description: stimulus description
5. sensor: stimulus sensor

labkey database file (../DataToPrepare/Common/samples_table_labkey.csv), with
fields:

1. id: line number
2. barcodeId: tube barcode
3. donorId: donor ID
4. visitId: visit ID
5. batchId: batch ID
6. type: type of sample
7. stimulusId: stimulus ID
8. volume: sample volume
9. aliquotId: aliquot ID
10. rackId: rack ID
11. well: tube position in box
12. auditTrail: ?
13. deleted: ?
14. insertDate: insertion date
15. updateDate: update date

## Expected file formats writted
Supernatant Visit 1 output to implement in FreezerPro
(../DataToImport/TC_supernatants_samples_V1_all_20161027.csv), with fields:

1. AliquotID: aliquot ID
2. Box: box name
3. BoxType: box type (96 (12 x 8) Well Plate)
4. Box_Descr: box description
5. DonorID: donor ID
6. Freezer: freezer name
7. Freezer_Descr: freezer description
8. Level1: level 1 name (Shelf)
9. Level1_Descr: level 1 description
10. Level2: level 2 name (Rack)
11. Level2_Descr: level 2 description
12. Level3: level 3 name (Drawer)
13. Level3_Descr: level 3 description
14. Position: tube position in box
15. StimulusID: stimulus ID
16. StimulusName: stimulus name
17. VisitID: visit ID
18. Volume: sample volume
19. ThawCycle: sample thaw cycle
20. Sample Source: sample source, donor ID in cohort
21. Description: tube description
22. Sample Type: sample type (PLASMA_1/2/3)
23. Name: tube name
24. BatchID: batch ID
25. CreationDate: sample creation date
26. UpdateDate: sample update date
27. FreezerBarcode: freezer barcode (in user-defined field)
28. ShelfBarcode: shelf barcode (in user-defined field)
29. RackBarcode: rack barcode (in user-defined field)
30. DrawerBarcode: drawer barcode (in user-defined field)
31. BOX_BARCODE: box barcode (FreezerPro field)
32. BoxBarcode: box barcode (in user-defined field)

## How to use

No associated help. Directly input `./create_supernatants_V1.py` on terminal.
