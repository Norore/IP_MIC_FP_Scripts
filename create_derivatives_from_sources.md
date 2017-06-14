# Generate aliquot samples for FreezerPro from original samples file

## Objective

User may want to create aliquots, or derivatives, from samples in freezers. It
will be necessary to update samples in FreezerPro, create derivatives, and, may
be, to remove or move samples.

## Warning

For input_file parameter, user may have download a full report from its samples.

## Expected file formats put in arguments

--input_file, file from FreezerPro database, with fields:

1. UID: unique identifier, defined by FreezerPro
2. Name: tube name
3. Description: tube description
4. Sample Type: type of sample
5. Vials: number of vials associated to the tube
6. Volume: sample volume
7. Sample Source: source sample, by default, donor in cohort
8. Owner: sample owner
9. Created At: creation date, FreezerPro
10. Expiration: expiration date, FreezerPro
11. AliquotID: Aliquot ID
12. VisitID: Visit ID
13. StimulusID: Stimulus ID
14. StimulusName: Stimulus Name
15. BatchID: Batch ID
16. DonorID: Donor ID
17. ThawCycle: number of thaw cycle, FreezerPro
18. CreationDate: sample creation date
19. UpdateDate: sample update date
20. FreezerBarcode: freezer barcode
21. ShelfBarcode: shelf barcode
22. RackBarcode: rack barcode
23. DrawerBarcode: drawer barcode
24. BoxBarcode: box barcode
25. RFID: RFID, defined by FreezerPro
26. BARCODE: tube barcode, could be set, if not, defined by FreezerPro
27. Freezer: freezer name
28. Level1: first level name (Shelf)
29. Level2: second level name (Rack)
30. Level3: third level name (Drawer)
31. Level4: empty
32. Level5: empty
33. Box: box name
34. Position: tube position in box

--directory, directory with Excel files that contains aliquot data to use,
in 3 sheets (1 sheet per box), with fields
1. AliquotingDate: aliquoting
2. SrcBox_BoxID: source box barcode, provider
3. SrcBox_LabExID: source box barcode, LabExMI
4. SrcBox_TubeScan: source tube
5. Well VisionMate: source tube position in
6. Well Expected: source tube position expected in
7. Al1Box_BoxID: fraction 1 box barcode, provider
8. Al1Box_LabExID: fraction 1 box barcode, LabExMI
9. Al1Box_TubeCtrl: fraction 1 tube control barcode
10. Al1Box_TubeScan: fraction 1 tube barcode
11. Well VisionMate: fraction 1 tube position in box
12. Well Expected: fraction 1 tube position expected in box
13. Al2Box_BoxID: fraction 2 box barcode, provider format
14. Al2Box_TubeCtrl: fraction 2 tube control barcode
15. Al2Box_TubeScan: fraction 2 tube barcode
16. Well VisionMate: fraction 2 tube position in box
17. Well Expected: fraction 2 tube position expected in box

--remove_tubes, file of excluded tubes, with fields:
1. BarcodeId_Source: source tube barcode
2. Date_Users: 20160826_R1_BCCP
3. SrcTF_Barcode: source box barcode, Thermo format
4. SrcBox_Barcode: source box barcode, LabExMI format
5. SrcVisionMate_Well: source tube position in box
6. SrcExpected_Well: source tube position expected in box
7. F1TF_Barcode: fraction 1 box barcode, Thermo format
8. F1Box_Barcode: fraction 1 box barcode, LabExMI format
9. BarcodeId_F1: fraction 1 tube barcode
10. F1VisionMate_Well: fraction 1 tube position in box
11. F1Expected_Well: fraction 1 tube position expected in box
12. F2TF_Barcode: fraction 2 box barcode, Thermo format
13. BarcodeId_F2: fraction 2 tube barcode
14. F2VisionMate_Well: fraction 2 tube position in box
15. F2Expected_Well: fraction 2 tube position expected in box
16. DonorId: donor ID
17. VisitId: visit ID
18. BatchId: batch ID
19. Type: sample type
20. StimulusId: stimulus ID
21. AliquotId: aliquot ID

--change_tubes, file of tubes to replace (tube from the wrong StimulusID), with
fields:
1. BarcodeId_Source: source tube barcode
2. Date_Users: 20160826_R1_BCCP
3. SrcTF_Barcode: source box barcode, Thermo format
4. SrcBox_Barcode: source box barcode, LabExMI format
5. SrcVisionMate_Well: source tube position in box
6. SrcExpected_Well: source tube position expected in box
7. F1TF_Barcode: fraction 1 box barcode, Thermo format
8. F1Box_Barcode: fraction 1 box barcode, LabExMI format
9. BarcodeId_F1: fraction 1 tube barcode
10. F1VisionMate_Well: fraction 1 tube position in box
11. F1Expected_Well: fraction 1 tube position expected in box
12. F2TF_Barcode: fraction 2 box barcode, Thermo format
13. BarcodeId_F2: fraction 2 tube barcode
14. F2VisionMate_Well: fraction 2 tube position in box
15. F2Expected_Well: fraction 2 tube position expected in box
16. DonorId: donor ID
17. VisitId: visit ID
18. BatchId: batch ID
19. Type: sample type
20. StimulusId: stimulus ID
21. AliquotId: aliquot ID

--replace_tubes, file of tubes for replace (tube from the wrong barcode), with
fields:
1. Position: tube position
2. NewBarcode: new tube barcode
3. OldBarcode: previous tube barcode

--add_tubes, file of tubes to add, need to be in same format as run files
from argument --directory, only one sheet, with fields:
1. SrcBox_LabExID: source box barcode, LabExMI format
2. SrcBox_TubeScan: source tube barcode
3. Well VisionMate: source tube position in box
4. Well Expected: source tube position expected in box
5. Al1Box_BoxID: fraction 1 box barcode, Thermo format
6. Al1Box_LabExID: fraction 1 box barcode, LabExMI format
7. Al1Box_TubeCtrl: fraction 1 control tube barcode
8. Al1Box_TubeScan: fraction 1 tube barcode
9. Well VisionMate: fraction 1 tube position in box
10. Well Expected: fraction 1 tube position expected in box
11. Al2Box_BoxID: fraction 2 box barcode, Thermo format
12. Al2Box_TubeCtrl: fraction 2 control tube barcode
13. Al2Box_TubeScan: fraction 2 tube barcode
14. Well VisionMate: fraction 2 tube position in box
15. Well Expected: fraction 2 tube position expected in box

--freezers, file with location of each box of fractions in freezers, from
FreezerPro, with fields:
1. Box: box name in freezer
2. Freezer: freezer name
3. Freezer_Descr: freezer description
4. Level1: level 1 name (Shelf)
5. Level1_Descr: level 1 description
6. Level2: level 2 name (Rack)
7. Level2_Descr: level 2 description
8. Level3: level 3 name (Drawer)
9. Level3_Descr: level 3 description

Expected file formats output in arguments

--output_file, output file with aliquot samples data in CSV format for
FreezerPro import, with fields:
1. ParentID: parent unique identifier, defined by FreezerPro
2. Name: tube name
3. BARCODE: tube barcode
4. Position: tube position in box
5. Volume: sample volume
6. Freezer: freezer name
7. Freezer_Descr: freezer description
8. Level1: level 1 name (Shelf)
9. Level1_Descr: level 1 description
10. Level2: level 2 name (Rack)
11. Level2_Descr: level 2 description
12. Level3: level 3 name(Drawer)
13. Level3_Descr: level 3 description
14. BoxType: type of box
15. Box: box name
16. Box_Descr: box description
17. ThermoBoxBarcode: box barcode from Thermo
18. BOX_BARCODE: box barcode
19. CreationDate: sample creation date
20. UpdateDate: sample update date
21. AliquotID: aliquot ID
22. DonorID: donor ID
23. StimulusID: stimulus ID
24. StimulusName: stimulus name
25. VisitID: visit ID
26. ThawCycle: number of thaw cycle
27. Sample Source: sample source, by default, donor in cohort
28. Description: tube description
29. BatchID: batch ID
30. Sample Type: sample type
31. ShelfBarcode: shelf barcode
32. RackBarcode: rack barcode
33. DrawerBarcode: drawer barcode

--update_file, file with original samples data in CSV format for FreezerPro
original samples update, with fields:
1. RFID: RFID of source tube to update in FreezerPro
2. Volume: volume
3. UpdateDate: update date
4. Position: position
5. DonorID: donor ID

--moved_file, file with original samples data in CSV format for FreezerPro
original samples to move, with fields:
1. UID: unique identifier defined by FreezerPro
2. BOX_BARCODE: box barcode
3. CONTAINER_BARCODE: container barcode

```
usage: create_derivatives_from_sources.py [-h] -i INPUT_FILE -d DIRECTORY
                                          [-r REMOVE_STIMULI]
                                          [-e REMOVE_TUBES] [-c CHANGE_TUBES]
                                          [-p REPLACE_TUBES] [-a ADD_TUBES] -f
                                          FREEZERS -o OUTPUT_FILE -u
                                          UPDATE_FILE -m MOVED_FILE

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input file with original samples data in CSV format
                        from FreezerPro report
  -d DIRECTORY, --directory DIRECTORY
                        Directory with aliquot sample files to use
  -r REMOVE_STIMULI, --remove_stimuli REMOVE_STIMULI
                        List of excluded stimuli. Need to be exactly like
                        9,31,40
  -e REMOVE_TUBES, --remove_tubes REMOVE_TUBES
                        File of excluded tubes.
  -c CHANGE_TUBES, --change_tubes CHANGE_TUBES
                        File of tubes to replace (tube from the wrong
                        StimulusID)
  -p REPLACE_TUBES, --replace_tubes REPLACE_TUBES
                        File of tubes to replace (tube with wrong barcode)
  -a ADD_TUBES, --add_tubes ADD_TUBES
                        File of tubes to add, need to be in same format as run
                        files from argument --directory
  -f FREEZERS, --freezers FREEZERS
                        File with location of each box of aliquots in freezers
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file with aliquot samples data in CSV format
                        for FreezerPro import
  -u UPDATE_FILE, --update_file UPDATE_FILE
                        File with original samples data in CSV format for
                        FreezerPro original samples update
  -m MOVED_FILE, --moved_file MOVED_FILE
                        File with original samples data in CSV format for
                        FreezerPro original samples to move
```
