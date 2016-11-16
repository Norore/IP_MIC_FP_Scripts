#!/usr/bin/env python
import json
import argparse
import re

parser = argparse.ArgumentParser(description="Generate freezers file in CSV format from JSON file format.")
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
    print "Input file " + f_freezer + " does not exist"
    exit(1)
try:
    outfile = open(o_freezer, "w")
except IOError:
    print "Output file " + o_freezer + " can't be writte"
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
                            Columns order:
                            Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,Level2_Descr,Level3,
                            Level3_Descr,Box,Box_Descr,BoxType
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

            # if "Aliquot L" in compartment or "Aliquot R" in compartment:
            #     for a in freezer["racks"][shelf][c]["samples aliquot"]:
            #         for aa in range(a["first"], a["last"] + 1):
            #             string = freezer["name"] + "," + shelf + ",," + a['name'] + "," \
            #                           + compartment + ",,,box " + str(aa) + "," + a["boxtype"]
            #             outfile.write(string + "\n")
            #
            if "Trizol" in compartment:
                for t in freezer["racks"][shelf][c]["trizol"]:
                    for tt in range(t["compartments"]["boxes"]):
                        """
                        Columns order:
                        Freezer,Freezer_Descr,Level1,Level1_Descr,Level2,Level2_Descr,Level3,
                        Level3_Descr,Box,Box_Descr,BoxType
                        """
                        l_freez = freezer["name"].split("_")
                        l_shelf = shelf.split()[2:].pop()
                        l_shelf = l_shelf.replace("Shelf", "Shelf ")
                        tt = str(tt + 1)
                        box_descr = t["description"][:-1] + ", Box "+tt+"\""
                        string = freezer["name"] + ",Freezer "+l_freez[2]+"," + \
                                 shelf + ","+l_shelf+"," + t["name"] + \
                                 "," + t["description"] + ",,," \
                                 "Box " + tt + "," + box_descr + "," + t["compartments"]["boxtype"]
                        outfile.write(string + "\n")

            # if "DNA" in compartment:
            #     for d in freezer["racks"][shelf][c]["stools DNA"]:
            #         for dd in range(d["compartments"]["boxes"]):
            #             dd = str(dd + 1)
            #             string = freezer["name"] + "," + shelf + ",," + d['name'] + "," \
            #                           + compartment + ",,,box " + dd + "," + d["compartments"]["boxtype"]
            #             outfile.write(string + "\n")
            #
            # if "Stool Samples Source" in compartment:
            #     for o in freezer["racks"][shelf][c]["stool source"]:
            #         for oo in range(o["compartments"]["boxes"]):
            #             oo = str(oo + 1)
            #             string = freezer["name"] + "," + shelf + ",," + o['name'] + "," \
            #                           + compartment + ",,,box " + oo + "," + o["compartments"]["boxtype"]
            #             outfile.write(string + "\n")
            #
            # if "Nasal" in compartment:
            #     for n in freezer["racks"][shelf][c]["nasal"]:
            #         for nn in range(n["compartments"]["boxes"]):
            #             nn = str(nn + 1)
            #             string = freezer["name"] + "," + shelf + ",," + n['name'] + "," \
            #                           + compartment + ",,,box " + nn + "," + n["compartments"]["boxtype"]
            #             outfile.write(string + "\n")

outfile.close()
