# Trizol Pellet creation

## Objective

From freezers hierarchy and files of Trizol location + Stimulations, will
create a file to implement in FreezerPro for the Trizol Pellet samples.

## Expected file formats put in arguments

`-f|--freezer`, file with freezer data in CSV format for FreezerPro, with fields:

1. Freezer: freezer name
2. Freezer_Descr: freezer description
3. Level1: level 1 name (Shelf)
4. Level1_Descr: level 1 description
5. Level2: level 2 name (Rack)
6. Level2_Descr: level 2 description
7. Level3: level 3 name (Drawer), empty
8. Level3_Descr: level 3 description, empty
9. Box: box name
10. Box_Descr: box description
11. BoxType: box type (TC_Box_9x9)

`-t|--truculture`, file with truculture pellet data in XLSX format for merge with
freezer data, with fields:

1. RoomID: room ID where the freezer is located
2. FreezerID ShelfID: freezer shelf barcode
3. RackID: rack barcode
4. DonorID: tube barcode
5. BoxPos: box position in rack
6. Processed: if not empty, the barcode is already processed and were moved

`-l|--labkey`, file with all the samples stored in LabKey, in CSV format, to use
for merge with Trizol pellet data, with fields:

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

`-i|--stimulation`, file with all the stimulated data in XLSX format to use for
merge with Trizol pellet data, with fields:

1. DonorIDscanned: tube barcode
2. ExtractionName: extraction name
3. Donor_ID.: donor ID
4. Visit: visit ID
5. StimulationNumber: stimulus ID
6. StimulationName: stimulus Name
7. StimulationTime: stimulus time
8. TECAN_RackNumber: TECAN rack barcode
9. TECAN_RackPosition: TECAN rack position
10. Matrix_RackBarcodeScanned: new rack barcode(?)
11. Matrix_TubeBarcodeScanned: new tube barcode(?)
12. Matrix_TubePosition.: new tube position in box
13. QubitDate: Qubit ate
14. QubitConcentration_ngul: Qubit concentration
15. CaliperDate: Caliper date
16. CaliperConcentration_ngul: Caliper concentration
17. NanodropDate: Nanodrop date
18. NanodropConcentration_ngul: Nanodrop concentration
19. DilutionDate: dilution date
20. RNAvolume: sample RNA volume
21. NFwaterVolume: NF
22. CaliperRQS:
23. BioanalyzerRIN:
24. Nanodrop260_280:
25. Nanodrop260_230:

`-u|--stimulus`, file with all stimuli in CSV format to use for merge with Trizol
pellet data, with fields:

1. stimulusId: stimulus ID
2. name: stimulus name
3. type: stimulus type
4. description: stimulus description
5. sensor: stimulus sensor

## Expected file formats output in arguments

`-o|--output`, output file name of trizol pellet vials that will be generate in
CSV format for FreezerPro, with fields:

1. Box: box name
2. BoxType: box type (TC_Box_9x9)
3. Box_Descr: box description
4. Freezer_Descr: freezer description
5. Level1_Descr: level 1 description
6. Level2: level 2 name (Shelf)
7. Level2_Descr: level 2 description
8. Level3: level 3 name (Drawer)
9. Level3_Descr: level 3 description
10. RoomID: room ID
11. DonorID: donor ID
12. BoxPos: box position in rack
13. Freezer: freezer name
14. Level1: level 1 name (Shelf)
15. Position: tube position in box
16. StimulusID: stimulus ID
17. Sample Type: sample type (TC Source Tube)
18. StimulusName: stimulus name
19. CenterID: center ID
20. VisitID: visit ID
21. BatchID: batch ID
22. Name: tube name
23. BARCODE: tube barcode (FreezerPro field?)
24. Volume: sample volume
25. DonorIDscanned: tube barcode
26. ExtractionName: extraction name from stimulation experiment
27. StimulationName: stimulus name from stimulation experiment
28. StimulationTime: stimulus time from stimulation experiment
29. FreezeThaw: freeze thaw cycle (in user-defined field)
30. FreezerBarcode: freezer barcode (in user-defined field)
31. ShelfBarcode: shelf barcode (in user-defined field)
32. RackBarcode: rack barcode (in user-defined field)
33. BOX_BARCODE: box barcode (FreezerPro field)
34. BoxBarcode: box barcode (in user-defined field)
35. Sample Source: sample source, donor ID in cohort

## How to use

Type `./trizol_samples.py -h` to show help:

```
usage: trizol_samples.py [-h] -f FREEZER -t TRIZOL -s SHEET -o OUTPUT

Generate trizol pellet samples for FreezerPro from our data Excel file

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -t TRIZOL, --trizol TRIZOL
                        File with trizol pellet data in XLSX format for merge
                        with freezer data
  -s SHEET, --sheet SHEET
                        Name of sheet in trizol pellet data in XLSX format to
                        user for merge with freezer data
  -o OUTPUT, --output OUTPUT
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

**Example:**

```
./trizol_samples.py
 -f ../DataToImport/freezers_trizol_pellets_20170203.csv
 -t ../DataToPrepare/1.LabExMI_TrucultureMapping_21Nov2014_FinalVersion.xlsx
 -s FinalMapping -o ../DataToImport/TC_Trizol_rack_samples_20170309.csv
 -l ../DataToPrepare/Common/samples_table_labkey.csv
 -i ../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls
 -m 5000samples_WL_QCs_DL_02Jul2015
 -u ../DataToPrepare/LabExMI_Stimuli_List.csv
 -e 9,17,18,21,27,32,27
```
