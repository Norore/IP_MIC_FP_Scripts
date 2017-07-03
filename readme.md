# About

Contains script to prepare Excel data file for FreezerPro importations.

# Scripts

## Folders

* __AnalyzeDataToImport/__: reports, generated in R, of final file output analysed.
* __Archives__: archives of old scripts.

## Python scripts

* __create_derivatives_from_sources.py__: generates derivatives (fractions) of samples for FreezerPro from original samples file
* __create_freezers_from_json.py__: generates the freezers file in CSV format for FreezerPro from a JSON file format
* __create_supernatants_V1.py__: creates file for Supernatant data in our Freezers, for Visit 1
* __create_supernatants_V2.py__: creates file for Supernatant data in our Freezers, for Visit 2
* __MI_FP_common.py__: script with functions used by majority of scripts describe in this documentation
* __nasal_swab_samples.py__: draft of script that should generate Nasal Swab samples for FreezerPro
* __stools_aliquots_dna_samples.py__: generates Stool Aliquots and DNA samples file for FreezerPro from an existing file of Stool Source samples from FreezerPro
* __stools_source_samples.py__: generates Stool Source samples file for FreezerPro
* __supernatants_tube_files.py__: generates supernatants samples for FreezerPro from a CSV file create from the samples LabKey table.
* __trizol_samples.py__: generates trizol pellet samples for FreezerPro from an Excel file

## README files

* [create_derivatives_from_sources.md](create_derivatives_from_sources.md)
* [create_freezers_from_json.md](create_freezers_from_json.md)
* [create_supernatants_V1.md](create_supernatants_V1.md)
* [create_supernatants_V2.md](create_supernatants_V2.md)
* [MI_FP_common.md](MI_FP_common.md)
* [nasal_swab_samples.md](nasal_swab_samples.md)
* [stools_aliquots_dna_samples.md](stools_aliquots_dna_samples.md)
* [stools_source_samples.md](stools_source_samples.md)
* [supernatants_tubes_files.md](supernatants_tubes_files.md)
* [trizol_samples.md](trizol_samples.md)
