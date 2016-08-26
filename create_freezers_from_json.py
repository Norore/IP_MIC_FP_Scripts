#!/usr/bin/env python
import json
import argparse

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

header = "Freezer,"
nb_lvls = freezers["levels"]
for i in range(nb_lvls):
    i = str(i + 1)
    header += "Level" + i + ","
    header += "Level" + i + "_Desc,"
header += "Box,BoxType"

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
                            string = freezer["name"] + "," + shelf + ",," + rack['name'] + "," \
                                          + compartment + "," + box["name"] + ",,box " + str(boxnum) \
                                          + "," + rack["boxtype"]
                            outfile.write(string + "\n")

            if "Aliquot L" in compartment or "Aliquot R" in compartment:
                for a in freezer["racks"][shelf][c]["samples aliquot"]:
                    for aa in range(a["first"], a["last"] + 1):
                        string = freezer["name"] + "," + shelf + ",," + a['name'] + "," \
                                      + compartment + ",,,box " + str(aa) + "," + a["boxtype"]
                        outfile.write(string + "\n")

            if "Trizol" in compartment:
                for t in freezer["racks"][shelf][c]["trizol"]:
                    for tt in range(t["compartments"]["boxes"]):
                        tt = str(tt + 1)
                        string = freezer["name"] + "," + shelf + ",," + t['name'] + "," \
                                      + compartment + ",,,box " + tt + "," + t["compartments"]["boxtype"]
                        outfile.write(string + "\n")

            if "DNA" in compartment:
                for d in freezer["racks"][shelf][c]["stools DNA"]:
                    for dd in range(d["compartments"]["boxes"]):
                        dd = str(dd + 1)
                        string = freezer["name"] + "," + shelf + ",," + d['name'] + "," \
                                      + compartment + ",,,box " + dd + "," + d["compartments"]["boxtype"]
                        outfile.write(string + "\n")

            if "Stool Samples Source" in compartment:
                for o in freezer["racks"][shelf][c]["stool source"]:
                    for oo in range(o["compartments"]["boxes"]):
                        oo = str(oo + 1)
                        string = freezer["name"] + "," + shelf + ",," + o['name'] + "," \
                                      + compartment + ",,,box " + oo + "," + o["compartments"]["boxtype"]
                        outfile.write(string + "\n")

            if "Nasal" in compartment:
                for n in freezer["racks"][shelf][c]["nasal"]:
                    for nn in range(n["compartments"]["boxes"]):
                        nn = str(nn + 1)
                        string = freezer["name"] + "," + shelf + ",," + n['name'] + "," \
                                      + compartment + ",,,box " + nn + "," + n["compartments"]["boxtype"]
                        outfile.write(string + "\n")

outfile.close()
