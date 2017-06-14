
# Create freezers

## Objective

FreezerPro requires files in CSV format for freezer creation with upload. This
script will create freezer hierarchy from JSON files.

# File input format

File input will depends of the type of samples to implement

### TruCulture Trizol pellet

Here is an example of JSON format for boxes of TruCulture Trizol pellet:

{"levels": 3,
 "freezers": [
	{"name": "MIC_Freezer_1532",
	"shelves": ["MIC Freezer1532 Shelf4"],
	"main_compartments": {
		"MIC Freezer1532 Shelf4": [
			"TruCulture Trizoll Pellet"
		]
	},
	"racks": {
		"MIC Freezer1532 Shelf4": [
      {
        "trizol": [
  				{"name": "MIC-TruCRack_2",
  				"compartments":
  					{"boxtype": "TC_Box_9x9",
  					"boxes": 10},
  				"description": ""TruCulture Trizol Pellet, Rack 2""
          },
  				{"name": "MIC-TruCRack_3",
  				"compartments":
  					{"boxtype": "TC_Box_9x9",
  					"boxes": 10},
  				"description": ""TruCulture Trizol Pellet, Rack 3""
  				}
  			]
			}
    ]
	}}
]}

### TruCulture Supernatants

Here is an example of JSON format for boxes of TruCulture Supernatants:

{"levels": 3,
 "freezers": [
	{"name": "MIC_Freezer_1532",
	"shelves": ["MIC Freezer1532 Shelf 1"],
	"main_compartments": {
		"MIC Freezer1532 Shelf 1": [
			""TruCulture Supernatants, Aliquot 1, Visit 1, women""
		]
	},
	"racks": {
		"MIC Freezer1532 Shelf 1": [
      {
  			"simulations": [
  				{"name": "D001>>096_V1",
  				"boxtype": "96 (12 x 8) Well Plate",
  				"compartments": [
  					{"name": "S01-07_V1_A1",
  					"first": 1,
  					"last": 7},
  					{"name": "S08-14_V1_A1",
  					"first": 8,
  					"last": 14},
  					{"name": "S15-21_V1_A1",
  					"first": 15,
  					"last": 21},
  					{"name": "S22-28_V1_A1",
  					"first": 22,
  					"last": 28},
  					{"name": "S29-35_V1_A1",
  					"first": 29,
  					"last": 35},
  					{"name": "S36-40_V1_A1",
  					"first": 36,
  					"last": 40}
  				],
  				"description": ""Rack donors 1 to 96, visit 1""},
  				{"name": "D201>>296_V1",
  				"boxtype": "96 (12 x 8) Well Plate",
  				"compartments": [
  					{"name": "S01-07_V1_A1",
  					"first": 1,
  					"last": 7},
  					{"name": "S08-14_V1_A1",
  					"first": 8,
  					"last": 14},
  					{"name": "S15-21_V1_A1",
  					"first": 15,
  					"last": 21},
  					{"name": "S22-28_V1_A1",
  					"first": 22,
  					"last": 28},
  					{"name": "S29-35_V1_A1",
  					"first": 29,
  					"last": 35},
  					{"name": "S36-40_V1_A1",
  					"first": 36,
  					"last": 40}
  				],
  				"description": ""Rack donors 201 to 296, visit 1""}
        ]
			}
    ]
	}}
]}

### Stool Source

Here is an example of JSON format for boxes of Stool Source boxes:

{"levels": 3,
 "freezers": [
	{"name": "MIC_Freezer_1533",
	"shelves": ["MIC Freezer1533 Shelf1"],
	"main_compartments": {
		"MIC Freezer1533 Shelf1": [
			"Stool Samples Source Tubes"
		]
	},
	"racks": {
		"MIC Freezer1533 Shelf1": [
      {
  			"stool source":
          [{"name": "Rack 1",
    				"compartments":
    					{"boxtype": "48 (12 x 8) Stool Well Plate",
    					"boxes": 10},
    				"description": "Stool Samples Source tubes"
            },
    				{"name": "Rack 2",
    				"compartments":
    					{"boxtype": "48 (12 x 8) Stool Well Plate",
    					"boxes": 10},
    				"description": "Stool Samples Source tubes"
    				}
    			]
      }
    ]
	}}
]}

### Stool Aliquot

Here is an example of JSON format for boxes of Stool Aliquot boxes:

{"levels": 3,
 "freezers": [
	{"name": "MIC_Freezer_1535",
	"shelves": ["MIC Freezer1535 Shelf1"],
	"main_compartments": {
		"MIC Freezer1535 Shelf1": [
			"Stool Samples Aliquot R2"
		]
	},
	"racks": {
		"MIC Freezer1535 Shelf1": [
			{
        "samples aliquot": [
  				{"name": "Box 1 to 7",
  				"boxtype": "96 (12 x 8) Stool Well Plate",
  				"first": 1,
  				"last": 7,
  				"description": "Stool Samples Aliquot R2"},
  				{"name": "Box 8 to 14",
  				"boxtype": "96 (12 x 8) Stool Well Plate",
  				"first": 8,
  				"last": 14,
  				"description": "Stool Samples Aliquot R2"},
  				{"name": "Box 15 to 18",
  				"boxtype": "96 (12 x 8) Stool Well Plate",
  				"first": 15,
  				"last": 18,
  				"description": "Stool Samples Aliquot R2"}
       ]
      }
    ]
	}}
]}

### Stool DNA

Here is an example of JSON format for boxes of Stool DNA boxes:

{"levels": 3,
 "freezers": [
	{"name": "MIC_Freezer_1532",
	"shelves": ["MIC Freezer1532 Shelf2"],
	"main_compartments": {
		"MIC Freezer1532 Shelf2": [
			"Stools DNA"
		]
	},
	"racks": {
		"MIC Freezer1532 Shelf2": [
			{
        "stools DNA": [
  				{"name": "Box 1 to 7",
  				"compartments":
  					{"boxtype": "96 (12 x 8) Well Plate",
            "first": 1,
            "last": 7},
  				"description": "Stools DNA"
  				},
  				{"name": "Box 8 to 14",
  				"compartments":
  					{"boxtype": "96 (12 x 8) Well Plate",
            "first": 8,
  					"last": 14},
  				"description": "Stools DNA"
  				},
  				{"name": "Box 15 to 18",
  				"compartments":
  					{"boxtype": "96 (12 x 8) Well Plate",
            "first": 15,
  					"last": 18},
  				"description": "Stools DNA"
  				}
	     ]
     }
    ]
	}}
]}

## File output format

     1. Freezer: freezer name
     2. Freezer_Descr: freezer descript
     3. Level1: level 1 name (Shelf)
     4. Level1_Descr: level 1 description
     5. Level2: level 2 name (Rack)
     6. Level2_Descr: level 2 description
     7. Level3: level 3 name (Drawer)
     8. Level3_Descr: level 3 description
     9. Box: box name
    10. Box_Descr: box description
    11. BoxType: box type


usage: create_freezers_from_json.py [-h] -f FREEZER -o OUTFILE

optional arguments:
  -h, --help            show this help message and exit
  -f FREEZER, --freezer FREEZER
                        File with freezer data in CSV format for FreezerPro
  -o OUTFILE, --outfile OUTFILE
                        Output file name that will be generate in CSV format
                        for FreezerPro
