# About

Contains script to prepare Excel data file for FreezerPro importations.

# Scripts

Currently 3 python scripts:
* __create_freezers_from_json.py__: generates the freezers file in CSV format for FreezerPro from a JSON file format
* __get_duplicates.py__: short script to get the DonorIDscanned duplicate tube names from file ../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls
* __stools_samples.py__: generates stools samples aliquots for FreezerPro from a directory with CSV files.
* __supernatants_samples.py__: generates supernatants samples for FreezerPro from a CSV file create from the samples LabKey table.
* __stimuli_samples_tmp.py__: generates supernatants samples for FreezerPro from an Excel file. Call *_tmp* because the boxes are not yet mapped
* __trizol_samples.py__: generates trizol pellet samples for FreezerPro from an Excel file
* __trizol_samples_old.py__: save previous version of __trizol_samples.py__

## create_freezers_from_json.py

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
./create_freezers_from_json.py -f ../DataToPrepare/freezers.json -o ../DataToImport/freezers.csv

## get_duplicates.py

A draft script to help to manage how to work with the DonorIDscanned duplicated tube names
from file `../DataToPrepare/3.5000samples_WL_QCs_DL_02Jul2015.xls`, for the script `trizol_samples.py`

# stools_samples.py

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

## supernatants_samples.py

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

## stimuli_samples_tmp.py

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

## trizol_samples.py

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
