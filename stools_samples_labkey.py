#!/usr/bin/env python
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description="""Generate stools samples labkey
                                            format for FreezerPro from our csv
                                            source files, will be used to
                                            generate Stools aliquot samples CSV
                                            file""")
parser.add_argument('-d', '--directory', required=True,
                    help='Directory whose contains files')
# parser.add_argument('-s', '--stool', required=True,
#                     help="File with stools samples data in CSV format for merge with freezer data")
parser.add_argument('-o', '--output', required=True,
                    help="""Output file name that will be generate in CSV format
                    for FreezerPro""")
args = vars(parser.parse_args())

d_dir = args['directory']
o_samples = args['output']

if d_dir[-1] != "/":
    d_dir += "/*.csv"
else:
    d_dir += "*.csv"

try:
    l_files = glob.glob(d_dir.replace('\\', ''))
except IOError:
    print "Directory '"+d_dir+"' does not exist"
    exit()

# initialize list of dataframes
list_df = []
for f_stool in l_files:

    print ">>> Works on '"+f_stool+"' file <<<"

    try:
        df_stool = pd.read_csv(f_stool, dtype=object)
    except IOError:
        print "File '"+f_stool+"' does not exist"
    # remove useless columns
    keepcols = ["barcodeId", "donorId", "visitId", "type", "aliquotId",
                "weight", "comments"]
    try:
        df_stool = df_stool[keepcols]
    except KeyError:
        keepcols = ["barcodeId", "donorId", "visitId", "type", "aliquotId"]
        df_stool = df_stool[keepcols]
        df_stool["weight"] = "Unknown"
        df_stool["comments"] = "None"

    list_df.append(df_stool)

df_final = pd.concat(list_df)
# write final result in CSV file format
df_final.to_csv(o_samples, index=False, header=True)
