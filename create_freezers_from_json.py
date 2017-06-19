#!/usr/bin/env python
"""
# Create freezers

## Objective

FreezerPro requires files in CSV format for freezer creation with upload. This
script will create freezer hierarchy from JSON files.

# File input format

File input (-f|--freezer) will depends of the type of samples to implement.

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
  				"description": "\"TruCulture Trizol Pellet, Rack 2\""
          },
  				{"name": "MIC-TruCRack_3",
  				"compartments":
  					{"boxtype": "TC_Box_9x9",
  					"boxes": 10},
  				"description": "\"TruCulture Trizol Pellet, Rack 3\""
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
			"\"TruCulture Supernatants, Aliquot 1, Visit 1, women\""
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
  				"description": "\"Rack donors 1 to 96, visit 1\""},
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
  				"description": "\"Rack donors 201 to 296, visit 1\""}
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

-o|--output, output file name of freezer(s) that will be generate in CSV format
for FreezerPro, with fields:
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
"""

import json
import argparse
import re
import pprint

parser = argparse.ArgumentParser(description=print(__doc__))
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-o', '--outfile', required=True,
                    help="Output file name that will be generate in CSV format for FreezerPro")
args = vars(parser.parse_args())

f_freezer = args["freezer"]
o_freezer = args["outfile"]

try:
    with open(f_freezer, "r") as infile:
        freezers = json.load(infile)
except IOError:
    print("Input file '{}' does not exist".format(f_freezer))
    exit(1)
try:
    outfile = open(o_freezer, "w")
except IOError:
    print("Output file '{}' can't be writte".format(o_freezer))
    exit(1)

header = "Freezer,Freezer_Descr,"
nb_lvls = freezers["levels"]
for i in range(nb_lvls):
    i = str(i + 1)
    header += "Level" + i + ","
    header += "Level" + i + "_Descr,"
header += "Box,Box_Descr,BoxType"

outfile.write(header + "\n")

nt = 1  # number of trizol box
for freezer in freezers["freezers"]:
    # shelves
    for i, shelf in enumerate(freezer["shelves"]):
        # compartments
        for c, compartment in enumerate(freezer["main_compartments"][shelf]):
            # Racks
            if "Supernatants" in compartment:
                for rack in freezer["racks"][shelf][c]["simulations"]:
                    for box in rack["compartments"]:
                        for boxnum in range(box["first"], box["last"] + 1):
                            """
                            ### TruCulture Supernatants

                            Columns order:
                            Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,
                            Level2_Descr,Level3,Level3_Descr,Box,Box_Descr,
                            BoxType
                            """
                            l_freez = freezer["name"].split("_")
                            l_shelf = shelf.split()
                            tmp_rack = rack["name"].replace(">>", " ")
                            tmp_rack = tmp_rack.replace("_", " ")
                            l_rack = tmp_rack.split()
                            l_rack[0] = l_rack[0].replace("D", "")
                            l_rack[2] = l_rack[2].replace("V", "")
                            str_rack = "\"Rack donors "+str(int(l_rack[0]))+\
                                        " to "+ str(int(l_rack[1]))+", visit "+\
                                        l_rack[2]+"\""
                            if len(l_rack) > 3:
                                l_rack[3] = l_rack[3].replace("D", "")
                                l_rack[5] = l_rack[4].replace("V", "")
                                str_rack = "\"Rack donors "+str(int(l_rack[0]))+ \
                                            " to "+ str(int(l_rack[1]))+ \
                                            " and donors "+str(int(l_rack[3]))+\
                                            " to "+str(int(l_rack[4]))+ \
                                            ", visit "+l_rack[2]+"\""
                            # "Drawer with plasma for donors 901 to 996, stimulus 1 to 7, visit 1, aliquot 1"
                            drawer = box["name"].replace("-", " ")
                            drawer = drawer.replace("_", " ")
                            drawer = drawer.replace("S", "")
                            drawer = drawer.replace("A", "")
                            drawer = drawer.replace("V", "")
                            l_drawer = drawer.split()
                            str_drawer = "\"Drawer with plasma for donors "+\
                                            str(int(l_rack[0]))+" to "+\
                                            str(int(l_rack[1]))+", stimulus "+\
                                            str(int(l_drawer[0]))+" to "+\
                                            str(int(l_drawer[1]))+",visit "+\
                                            str(int(l_drawer[2]))+", aliquot "+\
                                            str(int(l_drawer[3]))+"\""
                            if len(l_rack) > 3:
                                str_drawer = "\"Drawer with plasma for donors "+\
                                                str(int(l_rack[0]))+" to "+\
                                                str(int(l_rack[1]))+" and donors "+\
                                                str(int(l_rack[3]))+" to "+\
                                                str(int(l_rack[4]))+", stimulus "+\
                                                str(int(l_drawer[0]))+" to "+\
                                                str(int(l_drawer[1]))+",visit "+\
                                                str(int(l_drawer[2]))+", aliquot "+\
                                                str(int(l_drawer[3]))+"\""
                            str_idbox = "MIC_S"+str(boxnum)+"_V"+\
                                        str(int(l_drawer[2]))+"_A"+\
                                        str(int(l_drawer[3]))+"_D"+\
                                        str(int(l_rack[0]))+"-"+\
                                        str(int(l_rack[1]))
                            # "Box of stimulus 7 for donors 901 to 996, visit 1, aliquot 1"
                            str_box = "\"Box of stimulus "+str(boxnum)+" for donors "+\
                                        str(int(l_rack[0]))+" to "+\
                                        str(int(l_rack[1]))+", visit "+\
                                        str(int(l_drawer[2]))+", aliquot "+\
                                        str(int(l_drawer[3]))+"\""
                            if len(l_rack) > 3:
                                str_idbox += " MIC_S"+str(boxnum)+"_V"+\
                                            str(int(l_drawer[2]))+"_A"+\
                                            str(int(l_drawer[3]))+"_D"+\
                                            str(int(l_rack[3]))+"-"+\
                                            str(int(l_rack[4]))
                                str_box = "\"Box of stimulus "+str(boxnum)+" for donors "+\
                                            str(int(l_rack[0]))+" to "+\
                                            str(int(l_rack[1]))+" and donors "+\
                                            str(int(l_rack[3]))+" to "+\
                                            str(int(l_rack[4]))+", visit "+\
                                            str(int(l_drawer[2]))+", aliquot "+\
                                            str(int(l_drawer[3]))+"\""
                            string = freezer["name"] + ",Freezer "  + \
                                        l_freez[2] + "," + \
                                        shelf + "," + " ".join(l_shelf[2:]) + \
                                        "," + rack['name'] + "," + str_rack + \
                                        ",MIC_Plasma_" + box["name"] + \
                                        ","+str_drawer+"," + str_idbox + \
                                        ","+str_box+"," + rack["boxtype"]
                            outfile.write(string + "\n")

            if "Trizol" in compartment:
                for t in freezer["racks"][shelf][c]["trizol"]:
                    for tt in range(t["compartments"]["boxes"]):
                        """
                        ### TruCulture Trizol Pellets
                        Columns order:
                        Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,
                        Level2_Descr,Level3,Level3_Descr,Box,Box_Descr,BoxType
                        """
                        l_freez = freezer["name"].split("_")
                        l_shelf = shelf.split()[2:].pop()
                        l_shelf = l_shelf.replace("Shelf", "Shelf ")
                        tt = str(tt + 1)
                        box_descr = t["description"][:-1] + ", Box "+tt+"\""
                        string = freezer["name"] + ",Freezer "+str(l_freez[2])+"," + \
                                 shelf + ","+str(l_shelf)+"," + t["name"] + \
                                 "," + t["description"] + ",,," \
                                 "Box " + tt + "," + box_descr + "," + t["compartments"]["boxtype"]
                        outfile.write(string + "\n")

            if "Stool Samples Source Tubes" in compartment or "Stools DNA" in compartment:
                if "Stools DNA" in compartment:
                    for o in freezer["racks"][shelf][c]["stools DNA"]:
                        for oo in range(o["compartments"]["first"], \
                                        o["compartments"]["last"]+1):
                            """
                            ### Stools DNA

                            Columns order:
                            Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,
                            Level2_Descr,Level3,Level3_Descr,Box,Box_Descr,BoxType
                            """
                            l_freez = freezer["name"].split("_")
                            l_shelf = shelf.split()[2:].pop()
                            l_shelf = l_shelf.replace("Shelf", "Shelf ")
                            oo = str(oo)
                            if "Stools DNA" in compartment:
                                if len(oo) < 2:
                                    box = "Box0"+oo
                                else:
                                    box = "Box"+oo
                            else:
                                box = o["description"]
                            box_descr = o["description"][:-1] + ", Box "+oo+"\""
                            string = freezer["name"] + ",Freezer "+str(l_freez[2])+ \
                                     "," + shelf + "," + str(l_shelf) + "," + \
                                     compartment + "," + compartment + "," + \
                                     o['name'] + ",\"" + compartment + ", " + \
                                     o["name"].lower() + "\"," \
                                     + box + ",Box " + \
                                     oo + "," + \
                                     o["compartments"]["boxtype"]
                            outfile.write(string + "\n")
                else:
                    for o in freezer["racks"][shelf][c]["stool source"]:
                        for oo in range(o["compartments"]["boxes"]):
                            """
                            ### Stools Source

                            Columns order:
                            Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,
                            Level2_Descr,Level3,Level3_Descr,Box,Box_Descr,BoxType
                            """
                            l_freez = freezer["name"].split("_")
                            l_shelf = shelf.split()[2:].pop()
                            l_shelf = l_shelf.replace("Shelf", "Shelf ")
                            oo = str(oo+1)
                            box = "BOX"+oo
                            box_descr = o["description"][:-1] + ", Box "+oo+"\""
                            string = freezer["name"] + ",Freezer "+str(l_freez[2])+ \
                                     "," + shelf + "," + str(l_shelf) + "," + \
                                     compartment + "," + compartment + "," + \
                                     o['name'] + ",\"" + compartment + ", " + \
                                     o["name"].lower() + "\"," \
                                     + box + ",Box " + \
                                     oo + "," + \
                                     o["compartments"]["boxtype"]
                            outfile.write(string + "\n")


            if "Stool Samples Aliquot" in compartment:
                for o in freezer["racks"][shelf][c]["samples aliquot"]:
                    for oo in range(o["first"], o["last"]+1):
                        """
                        ### Stools Aliquots (L + R1 + R2 + R3)

                        Columns order:
                        Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,
                        Level2_Descr,Level3,Level3_Descr,Box,Box_Descr,BoxType
                        """
                        l_freez = freezer["name"].split("_")
                        l_shelf = shelf.split()[2:].pop()
                        l_shelf = l_shelf.replace("Shelf", "Shelf ")
                        oo = str(oo)
                        if len(oo) < 2:
                            nbbox = "0" + oo
                        else:
                            nbbox = oo
                        rack = "MIC_Feces_Box"+nbbox
                        rack += compartment.replace("Stool Samples Aliquot ", "_")
                        box_descr = o["description"][:-1] + ", Box "+oo+"\""
                        string = freezer["name"] + ",Freezer "+str(l_freez[2])+ \
                                 "," + shelf + "," + str(l_shelf) + "," + \
                                 compartment + "," + compartment +"," + \
                                 o['name'] + ",\"" + compartment + ", " + \
                                 o["name"].lower() + "\"," \
                                 + rack + ",Box " + \
                                 oo + "," + \
                                 o["boxtype"]
                        outfile.write(string + "\n")

            # if "Nasal" in compartment:
            #     for n in freezer["racks"][shelf][c]["nasal"]:
            #         for nn in range(n["compartments"]["boxes"]):
            #             nn = str(nn + 1)
            #             string = freezer["name"] + "," + shelf + ",," + n['name'] + "," \
            #                           + compartment + ",,,box " + nn + "," + n["compartments"]["boxtype"]
            #             outfile.write(string + "\n")

outfile.close()
