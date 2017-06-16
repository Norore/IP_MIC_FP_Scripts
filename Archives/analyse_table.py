#!/usr/bin/env python
import pandas as pd
import argparse

'''
parser = argparse.ArgumentParser(description="Generate output analyse file "
                                             "for the table in CSV format.")
parser.add_argument('-f', '--file', required=True,
                    help="File with table in CSV format to analyse")
parser.add_argument('-t', '--type', required=False,
                    help="The type of file used to generate the analysis.\n"
                         "Valid types are:\n"
                         "\t- freezers: analyze file with freezers infos "
                         "in CSV format\n"
                         "If empty, will only do a general analysis.")
parser.add_argument('-o', '--outfile', required=True,
                    help="Output file name that will be generate in markdown "
                         "format for analyse results")
args = vars(parser.parse_args())

f_analysis = args["file"]
t_analysis = args["type"]
o_analysis = args["outfile"]

try:
    with open(f_analysis, "r") as infile:
        infile = pd.csv_read(infile, dtype=object)
except IOError:
    print "Input file " + f_freezer + " does not exist"
    exit(1)
try:
    outfile = open(o_freezer, "w")
except IOError:
    print "Output file " + o_freezer + " can't be writte"
    exit(1)
try:
    type = t_analysis
except DoesNotExist:
    type = "default"
'''


def default(infile, outfile):
    outfile.write("List of columns:\n")
    outfile.write("\n".join(
        [ c for c in infile.columns]
    ) + "\n")

    outfile.write("Number of values per column:\n")
    outfile.write(str(infile.count())+"\n")


def freezers(infile, outfile):
    default(infile, outfile)

if __name__ == "__main__":
    infile = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/"
                         "DataToImport/TC_Trizol_rack_samples.csv", dtype=object)
    outfile = open("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/AnalyzedData/"
              "test.txt", "w")
    vtype = 'default'
    cases = ['default', 'freezers']

    if vtype in cases:
        if vtype == 'default':
            default(infile, outfile)
        elif vtype == 'freezers':
            freezers(infile, outfile)
        else:
            default(infile, outfile)
    else:
        default(infile, outfile)
    outfile.close()