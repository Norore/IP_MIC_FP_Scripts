# Stool Aliquots and DNA creation

## Objective

Generate stools Aliquot and DNA samples for FreezerPro from TXT data file
provided by Stanislas and stool source samples mapping.

## Expected file formats put in arguments

`-f|--frezer`, file with freezer data in CSV format for FreezerPro, with fields:

1. Box: box name in freezer
2. Freezer: freezer name
3. Freezer_Descr: freezer description
4. Level1: level 1 name (Shelf)
5. Level1_Descr: level 1 description
6. Level2: level 2 name (Rack)
7. Level2_Descr: level 2 description
8. Level3: level 3 name (Drawer)
9. Level3_Descr: level 3 description

`-d|--database`, file that contains data from database for all stools data, with
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


`-s|--sources`, input file name of sources vials in CSV format provided by FreezerPro,
with fields:

    *Need to be defined*

## Expected file format output in arguments

`-a|--aliquots`, output file name of aliquots vials that will be generate in CSV
format for FreezerPro, with fields:

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

`-n|--dna`, output file name of dna vials that will be generate in CSV format for
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

## How to use

Type `./stools_aliquots_dna_samples.py -h` to show help:

```
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
```

**Example:**

```
./stools_aliquots_dna_samples.py
 -f ../DataToImport/freezers_stool_samples_20170601.csv
 -d ../DataToPrepare/Stools/20150330094054_STOOL_DB.txt
 -s /path/to/FreezerPro_export.csv
 -a ../DataToImport/Stools_Samples_Aliquots_20170619.csv
 -n ../DataToImport/Stools_Samples_DNA_20170619.csv
```
