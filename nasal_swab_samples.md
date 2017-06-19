# Nasal Swab creation

## About

This script is a draft, it will probably be withdraw later

## How to use

Type `./nasal_swab_samples.py -h` to show help:

```
usage: nasal_swab_samples.py [-h] -f FREEZER -t NASALM -s NASALMS -l LABKEY -i
                             DRAWDATE -m SHEET -o OUTPUT [-v VERBOSE]

Generate Nasal Swabs samples for FreezerPro from our data Excel & CSV files

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -t NASALM, --nasalm NASALM
                        File with Nasal Swab mapping data in XLSX format for
                        merge with freezer data
  -s NASALMS, --nasalms NASALMS
                        Name of sheet in Nasal Swab mapping data in XLSX
                        format to use for merge with freezer data
  -l LABKEY, --labkey LABKEY
                        File with all the samples stored in LabKey, in CSV
                        format, to use for merge with Nasal Swab data
  -i DRAWDATE, --drawdate DRAWDATE
                        File with all the Nasal Swab creation date data in
                        XLSX format to use for merge with Nasal Swab data
  -m SHEET, --sheet SHEET
                        Name of sheet in Nasal Swab creation date data in XLSX
                        format to use for merge with freezer data
  -o OUTPUT, --output OUTPUT
                        Output file name that will be generate in CSV format
                        for FreezerPro
  -v VERBOSE, --verbose VERBOSE
                        If set, could print more infos.
```

**Example:**
