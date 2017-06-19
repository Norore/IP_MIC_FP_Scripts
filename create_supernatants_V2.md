# TruCulture Supernatant Visit 2 creation

## Objective

From freezer mapping and knowledge of how the tubes are stored in each box,
will generate an output file for implementation into FreezerPro for the
TruCulture supernatants, in Visit 2.

## Expected file formats read

file with data on donor and visit, provided by our LabKey server,
(../DataToPrepare/list_of_donors_visit2.csv), with fields:

1. SUBJID: donor ID
2. donorVisitVisit
3. VISIT0: did the donor come in Visit 0 (pilot study?)
4. VISIT1: did the donor come in Visit 1
5. VISIT2: dit the donor come in Visit 2
6. SVSTYYV0
7. SVSTMMV0
8. SVSTDDV0
9. SVSTYYV0T1
10. SVSTYYV1
11. SVSTMMV1
12. SVSTDDV1
13. SVSTYYV1T1
14. SVSTYYV2
15. SVSTMMV2
16. SVSTDDV2
17. SVSTYYV2T1
18. v1V0DT
19. v2V1DT

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

labkey database file have a missing donor for Visit 2, donor 402, need to use
file (../DataToPrepare/Common/LabExMISamples_Donor_402_Visit_2_2012_Week_42.csv),
with fields:

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

Supernatant Visit 2 output to implement in FreezerPro
(../DataToImport/TC_supernatants_samples_V2_all_20161027.csv), with fields:

1. Name: tube name
2. DonorID: donor ID
3. VisitID: visit ID
4. BatchID: batch ID
5. StimulusID: stimulus ID
6. AliquotID: aliquot ID
7. CreationDate: creation date
8. UpdateDate: update date
9. Position: tube position in box
10. Level2: level 2 name (Rack)
11. Volume: sample volume
12. StimulusName: stimulus name
13. ThawCycle: thaw cycle
14. BoxType: box type (96 (12 x 8) Well Plate)
15. Freezer: freezer name
16. Freezer_Descr: freezer description
17. Level1: level 1 name (Shelf)
18. Level1_Descr: level 1 description
19. Level2_Descr: level 2 description
20. Level3: level 3 name (Drawer)
21. Level3_Descr: level 3 description
22. Sample Type: sample type (PLASMA_1/2/3)
23. Box_Descr: box description
24. Box: box name
25. Sample Source: sample source, donor ID in cohort
26. Description: tube description
27. FreezerBarcode: freezer barcode (in user-defined field)
28. ShelfBarcode: shelf barcode (in user-defined field)
29. RackBarcode: rack barcode (in user-defined field)
30. DrawerBarcode: drawer barcode (in user-defined field)
31. BOX_BARCODE: box barcode (FreezerPro field)
32. BoxBarcode: box barcode (in user-defined field)

## How to use

No associated help. Directly input `./create_supernatants_V2.py` on terminal.
