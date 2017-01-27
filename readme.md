# About

Contains script to prepare Excel data file for FreezerPro importations.

# Scripts

## Folders

* __AnalyzeDataToImport/__:
* __notebooks__:

## Python scripts

* __create_aliquots_from_sources.py__: generates aliquot samples for FreezerPro from original samples file
* __create_derivatives_from_sources.py__: generates derivatives (fractions) of samples for FreezerPro from original samples file
* __create_freezers_from_json_v2.py__: generates the freezers file in CSV format for FreezerPro from a JSON file format -- **Up-to-date**
* __create_freezers_from_json.py__: generates the freezers file in CSV format for FreezerPro from a JSON file format -- **Withdraw**
* __create_supernatants_V1.py__: creates file for Supernatant data in our Freezers, for Visit 1 -- need to be update
* __create_supernatants_V2.py__: creates file for Supernatant data in our Freezers, for Visit 2 -- need to be update
* __get_duplicates.py__: short script to get the DonorIDscanned duplicate tube names from file ../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls
* __stools_samples.py__: generates stools samples aliquots for FreezerPro from a directory with CSV files.
* __stimuli_samples_tmp.py__: generates supernatants samples for FreezerPro from an Excel file. Call *_tmp* because the boxes are not yet mapped
* __stools_aliquot_samples.py__:
* __stools_samples_labkey.py__:
* __supernatants_samples.py__: generates supernatants samples for FreezerPro from a CSV file create from the samples LabKey table.
* __trizol_samples.py__: generates trizol pellet samples for FreezerPro from an Excel file

### create_aliquots_from_sources.py

Type `./create_aliquots_from_sources.py -h` to show help:

```
usage: create_aliquots_from_sources.py [-h] -i INPUT_FILE -d DIRECTORY -o
                                       OUTPUT_FILE -u UPDATE_FILE

Generate aliquot samples for FreezerPro from original samples file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input file with original samples data in CSV format
                        from FreezerPro report
  -d DIRECTORY, --directory DIRECTORY
                        Directory with aliquot sample files to use
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file with aliquot samples data in CSV format
                        for FreezerPro import
  -u UPDATE_FILE, --update_file UPDATE_FILE
                        File with original samples data in CSV format for
                        FreezerPro original samples update
```

Example:

### create_derivatives_from_sources.py

Type `./create_derivatives_from_sources.py -h` to show help:

```
usage: create_derivatives_from_sources.py [-h] -i INPUT_FILE -d DIRECTORY
                                          [-r REMOVE_STIMULI]
                                          [-e REMOVE_TUBES] [-c CHANGE_TUBES]
                                          [-a ADD_TUBES] -f FREEZERS -o
                                          OUTPUT_FILE -u UPDATE_FILE

Generate derivatives (fractions) samples for FreezerPro from original samples file

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
```

Example:

```
./create_derivatives_from_sources.py
 -i ../FPFilesToUpdate/freezer_1532_all_data_20161207.csv
 -d /Volumes/LabExMI/SampleManagement/TruCSupernatant_Aliquoting_Summer2016/WorkingSheets/
 -r 9,31
 -e ../DataToPrepare/Aliquoting/Excluded_Tubes.xlsx
 -c ../DataToPrepare/Aliquoting/Error_Tubes.xlsx
 -a ../DataToPrepare/Aliquoting/Add_Tubes.xlsx
 -f ../DataToPrepare/Aliquoting/box_location_20161221.csv
 -o ../DataToImport/Supernatants_Derivatives_F1F2_20170118.csv
 -u ../DataToImport/Supernatants_Samples_Derivatived_F1F2_20170118.csv
 -p ../DataToPrepare/Aliquoting/ReplaceSourceBarcode.xlsx
```

### create_freezers_from_json_v2.py

Type `./create_freezers_from_json_v2.py -h` to show help:

```
usage: create_freezers_from_json_v2.py [-h] -f FREEZER -o OUTFILE

Generate freezers file in CSV format from JSON file format.

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -o OUTFILE, --outfile OUTFILE
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

Example:

```
./create_freezers_from_json.py
 -f ../DataToPrepare/freezers_trizol_pellets.json
 -o ../DataToImport/freezers_trizol_pellets_20161116.csv
```

### create_freezers_from_json.py

Type `./create_freezers_from_json.py -h` to show help:

```
usage: create_freezers_from_json.py [-h] -f FREEZER -o OUTFILE

Generate freezers file in CSV format from JSON file format.

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -o OUTFILE, --outfile OUTFILE
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

Example:

```
./create_freezers_from_json.py -f ../DataToPrepare/freezers.json
 -o ../DataToImport/freezers.csv
```

### create_supernatants_V1.py

No associated help. Directly input `./create_supernatants_V1.py` on terminal.

### create_supernatants_V2.py

No associated help. Directly input `./create_supernatants_V2.py` on terminal.

### get_duplicates.py

A draft script to help to manage how to work with the DonorIDscanned duplicated tube names
from file `../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls`, for the script `trizol_samples.py`

### stools_samples.py

Type `./stools_samples.py -h` to show help:

```
usage: stools_samples.py [-h] -f FREEZER -d DIRECTORY -o OUTPUT

Generate stools samples for FreezerPro from our data Excel file

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -d DIRECTORY, --directory DIRECTORY
  -o OUTPUT, --output OUTPUT
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

Example:

```
./stools_samples.py -f ../DataToImport/freezers.csv
 -d ../DataToPrepare/Stools/Congelateur1535_R2/
 -o ../DataToImport/Stools_freezer1535_R2_samples.csv
```

### supernatants_samples.py

Type `./supernatants_samples.py -h` to show help:

```
usage: supernatants_samples.py [-h] -f FREEZER -l LABKEY -o OUTPUT

Generate stools samples for FreezerPro from our data Excel file

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -l LABKEY, --labkey LABKEY
                        File with all the samples stored in LabKey, in CSV
                        format, to use for merge with Trizol pellet data
  -o OUTPUT, --output OUTPUT
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

Example:

```
./supernatants_samples.py -f ../DataToImport/freezers.csv
 -l ../DataToPrepare/Common/samples_table_labkey.csv
 -o ../DataToImport/TC_supernatants_samples.csv
```

### stimuli_samples_tmp.py

Type `./stimuli_samples_tmp.py -h` to show help:

```
usage: stimuli_samples_tmp.py [-h] -f FREEZER -t SUPERNATANT -s SHEET1 -r
                              REPEATED -e SHEET2 -o OUTPUT

Generate supernatants samples for FreezerPro from our data Excel file

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -t SUPERNATANT, --supernatant SUPERNATANT
                        File with supernatants data in XLSX format for merge
                        with freezer data
  -s SHEET, --sheet SHEET
                        Name of sheet in supernatant data in XLSX format to
                        use for merge with freezer data
  -o OUTPUT, --output OUTPUT
                        Output file name that will be generate in CSV format
                        for FreezerPro
```

Example:

```
./stimuli_samples_tmp.py -f ../DataToImport/freezers.csv -t ../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls
 -s 5000samples_WL_QCs_DL_02Jul2015 -o ../DataToImport/Stimuli_rack_samples.csv
```

### trizol_samples.py

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

Example:

```
./trizol_samples.py -f ../DataToImport/freezers.csv
 -t ../DataToPrepare/1.LabExMI_TrucultureMapping_21Nov2014_FinalVersion.xlsx
 -s FinalMapping
 -o ../DataToImport/TC_Trizol_rack_samples.csv
 -l ../DataToPrepare/Common/samples_table_labkey.csv
 -i ../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls
 -m 5000samples_WL_QCs_DL_02Jul2015
```
