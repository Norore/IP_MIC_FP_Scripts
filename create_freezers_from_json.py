#!/usr/bin/env python
import json
import re
import argparse
import os.path

parser = argparse.ArgumentParser(description="Generate freezers file in CSV format from JSON file format.")
parser.add_argument('-f', '--freezer', required=True, \
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
	print "Input file "+f_freezer+" does not exist"
	exit(1)
try:
	outfile = open(o_freezer, "w")
except IOError:
	print "Output file "+o_freezer+" can't be writte"
	exit(1)

header = "Freezer,"
nb_lvls = freezers["levels"]
for i in range(nb_lvls):
	i = str(i+1)
	header += "Level"+i+","
header += "Box,BoxType"

outfile.write(header+"\n")

nt = 1 # number of trizol box
for freezer in freezers["freezers"]:
	# shelves
	for i,s in enumerate(freezer["shelves"]):
		# compartments
		for c in freezer["main_compartments"][s]:
			# Racks
			if "Supernatants" in c:
				for rack in freezer["racks"][s]["simulations"]:
					for b in rack["compartments"]:
						for bb in range(b["first"], b["last"]+1):
							outfile.write(freezer["name"]+","+s+","+c+","\
							+rack["name"]+","+b["name"]+",box "+str(bb)\
							+","+rack["boxtype"]+"\n")
			if "Aliquot L" in c or "Aliquot R1" in c:
				for a in freezer["racks"][s]["samples aliquot"]:
					for aa in range(a["first"],	a["last"]+1):
						outfile.write(freezer["name"]+","+s+","+c+","\
						+a["name"]+",,box "+str(aa)+","+a["boxtype"]+"\n")
			if "Trizol" in c:
				for t in freezer["racks"][s]["trizol"]:
					for tt in range(t["compartments"]["boxes"]):
						tt = str(tt+1)
						outfile.write(freezer["name"]+","+s+","+c+","\
						+t["name"]+",,box "+tt+","+t["compartments"]["boxtype"]+"\n")
			if "DNA" in c:
				for d in freezer["racks"][s]["stools DNA"]:
					for dd in range(d["compartments"]["boxes"]):
						dd = str(dd+1)
						outfile.write(freezer["name"]+","+s+","+c+","\
						+d["name"]+",,box "+dd+","+d["compartments"]["boxtype"]+"\n")
			if "Stool Samples source" in c:
				for o in freezer["racks"][s]["stool source"]:
					for oo in range(o["compartments"]["boxes"]):
						oo = str(oo+1)
						outfile.write(freezer["name"]+","+s+","+c+","\
						+o["name"]+",,box "+oo+","+o["compartments"]["boxtype"]+"\n")
			if "Nasal" in c:
				for n in freezer["racks"][s]["nasal"]:
					for nn in range(n["compartments"]["boxes"]):
						nn = str(nn+1)
						outfile.write(freezer["name"]+","+s+","+c+","\
						+n["name"]+",,box "+nn+","+n["compartments"]["boxtype"]+"\n")

outfile.close()

