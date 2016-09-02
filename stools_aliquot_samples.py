#!/usr/bin/env python
import pandas as pd
import argparse
import glob

parser = argparse.ArgumentParser(description="Generate stools aliquot samples for FreezerPro from our data Excel file")
parser.add_argument('-f', '--freezer', required=True,
                    help="File with freezer data in CSV format for FreezerPro")
parser.add_argument('-d', '--directory', required=True,
                    help='')
# parser.add_argument('-s', '--stool', required=True,
#                     help="File with stools samples data in CSV format for merge with freezer data")
parser.add_argument('-o', '--output', required=True,
                    help="Output file name that will be generate in CSV format for FreezerPro")
args = vars(parser.parse_args())

f_freezer = args['freezer']
# f_stool = args['stool']
d_dir = args['directory']
o_samples = args['output']

if d_dir[-1] != "/":
    d_dir += "/*.csv"
else:
    d_dir += "*.csv"

try:
    df_freez = pd.read_csv(f_freezer, dtype=object)
except IOError:
    print "File '"+f_freezer+"' does not exist"
    exit()

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
        df_stool = pd.read_csv(f_stool, sep=";", dtype=object)
    except IOError:
        print "File '"+f_stool+"' does not exist"
    # columns 2 and 3 are empty
    # column 5 only contains the building's name
    # remove columns 2, 3 and 5
    del df_stool["Unnamed: 1"], df_stool["Unnamed: 2"], df_stool["Location"]
    if "Unnamed: 6" in df_stool.columns:
        del df_stool["Unnamed: 6"]
    # df_stool["RackBarcode"] = df_stool.columns[0]
    # df_stool["RackBarcode"] = df_stool["RackBarcode"].str.replace("Rack: ", "")
    # rename columns
    df_stool.columns = ["Box", "Freezer", "Shelf"]#, "RackBarcode"]

    # split column Box
    newcols = pd.DataFrame(df_stool["Box"].str.split(",").tolist(),
                           columns=["Position", "Box", "Name"])

    # change position format for FreezerPro database
    df_stool["Position"] = newcols["Position"].str.replace(r'([A-Z]+)[0]?(\d+)', r'\2/\1')
    df_stool["BoxBarcode"] = newcols["Box"]
    df_stool["Box"] = newcols["Box"].str.replace(r'MIC_Feces_Box[0]?(\d+)_[LR][123]?', r'box \1')
    freezer = 'Freezer '+str(list(df_stool["Freezer"].unique()).pop())
    df_stool["ShelfBarcode"] = df_stool["Shelf"]
    df_stool["Shelf"] = df_stool["Shelf"].str.replace(r'' + freezer + 'Shelf(\d+)', r'Shelf \1')
    df_stool["Name"] = newcols["Name"]

    del newcols

    # add Sample Type name "Stool"
    df_stool["Sample Type"] = "Stool"

    # need to know the corresponding Level2
    # prepare a dictionary with the list of boxes
    d_box = {}
    for nb_box in range(1, 19):
        if nb_box < 8:
            d_box["box "+str(nb_box)] = "Box 1 to 7"
        elif nb_box < 15:
            d_box["box "+str(nb_box)] = "Box 8 to 14"
        else:
            d_box["box "+str(nb_box)] = "Box 15 to 18"

    # create boxes dataframe
    boxes = pd.DataFrame(d_box.items(), columns=["Box", "Level2"], dtype=object)
    # merge dataframes boxes and data using Box key column
    dataset = pd.merge(df_stool, boxes, on=["Box"])

    # remove lines with "No Tube" in column Name
    notubes = set(df_stool.loc[df_stool["Name"] == "No Tube"].index.tolist())
    # remove lines with "No Read" in columns Name
    noreads = set(df_stool.loc[df_stool["Name"] == "No Read"].index.tolist())
    to_drop = list(notubes.union(noreads))

    if len(to_drop) > 0:
        dataset.drop(to_drop, inplace=True)

    # select lines in freezers with "stools" in column "Level2_Desc"
    stools = df_freez.loc[df_freez["Level2_Desc"].str.contains("Stool Samples Aliquot")]

    # merge stools data with freezer location
    dataset.rename(columns={"Shelf": "Level1"}, inplace=True)
    result = pd.merge(stools, dataset, on=["Freezer", "Level1", "Level2", "Box"], how="inner")
    result["FreezerBarcode"] = "Freezer MIC_Freezer#_" + result["Freezer"].astype(str)
    result["ShelfBarcode"] = "MIC Freezer" + result["Freezer"].astype(str) + " " + result["Level1"].str.replace(" ", "")
    list_df.append(result)

df_final = pd.concat(list_df)
# write final result in CSV file format
df_final.to_csv(o_samples, index=False, header=True)
