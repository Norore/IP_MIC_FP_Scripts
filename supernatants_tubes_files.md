# Supernatant tubes: files creation

## create_supernatants_V1.py

### Files used:

1. ../FreezerPro/DataToImport/freezers_supernatants.csv
1. ../FreezerPro/DataToPrepare/donors_X97_X00.json
1. ../FreezerPro/DataToPrepare/LabExMI_Stimuli_List.csv
1. ../FreezerPro/DataToPrepare/Common/samples_table_labkey.csv

### File generated:

+ ../FreezerPro/DataToImport/TC_supernatants_samples_V1_all_20161027.csv

### Steps:

1. Read file 1 with columns:
   | Name | Description
   | ---- | -----------
   | Freezer | Freezer name
   | Freezer_Descr | Description of the freezr
   | Level1 | First compartment level: **Shelf**
   | Level1_Descr | Description of Level1
   | Level2 | Second compartment level: **Rack**
   | Level2_Descr | Description of Level2
   | Level3 | Third compartement level: **Drawer**
   | Level3_Descr | Description of Level3
   | Box | Box name
   | Box_Descr | Description of the box
   | BoxType | Type of box: **96 (12 x 8) Well Plate**

2. Prepare file by adding columns:
   | Name | Description | Column source
   | ---- | ----------- | ------
   | VisitID | Visit ID, could be 1 or 2 | Level3
   | AliquotID | Aliquot ID, could be 1, 2 or 3 | Level3
   | StimulusID | Stimulus ID, could be an integer between 1 and 40 | Box

3. Create well position dataframe:
   | Name | Description
   | ---- | -----------
   | AliquotID | Aliquot ID, could be 1, 2 or 3
   | VisitID | Visit ID, could be 1 or 2
   | StimulusID | Stimulus ID, could be an integer between 1 and 40
   | Position | Well position, could be an integer between 1 and 96
