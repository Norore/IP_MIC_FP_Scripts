# coding: utf-8
import pandas as pd
df = pd.read_excel("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/Supernatants_Derivatives_20161216.csv", dtype=object)
df = pd.read_excel("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/Supernatants_Derivatives_20161216.csv", dtypes=object)
df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/Supernatants_Derivatives_20161216.csv", dtypes=object)
df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/Supernatants_Derivatives_20161216.csv", dtype=object)
print(df["DonorID"].unique())
print(len(df["DonorID"].unique()))
pd.groupby("DonorID", on=["DonorID", "StimulusID"])
pd.groupby("DonorID", by=["DonorID", "StimulusID"])
pd.groupby(df, by="DonorID")
print(pd.groupby(df, by="DonorID"))
pd.groupby(df, by="DonorID").count
pd.groupby(df, by="DonorID").count()
pd.groupby(df, by="DonorID")["StimulusID"].count()
pd.groupby(df, by="DonorID")["StimulusID"].count() < 10
print(pd.groupby(df, by="DonorID")["StimulusID"].count() < 10)
pd.groupby(df, by="DonorID")["StimulusID"].count() < 10
pd.groupby(df, by="DonorID")["StimulusID"].count()
countstimdonor = pd.groupby(df, by="DonorID")["StimulusID"].count()
countstimdonor.head()
countstimdonor["StimulusID"]
countstimdonor.columns
df.groupby("DonorID")["StimulusID"].count()
dataframe(df.groupby("DonorID")["StimulusID"].count())
pd.DataFrame(df.groupby("DonorID")["StimulusID"].count())
pd.DataFrame(df.groupby("DonorID")["StimulusID"].count()).head()
pd.DataFrame(df.groupby("DonorID")["StimulusID"].count()).columns
countstimdonor = pd.DataFrame(df.groupby("DonorID")["StimulusID"].count())
countstimdonor[countstimdonor["StimulusID"] < 10]
df.groupby("Box")["StimulusID"].count()
df[df["Box"] == "MIC_Plasma_S39_V1_A1_F1_DX97-X00"]
unique(df[df["Box"] == "MIC_Plasma_S39_V1_A1_F1_DX97-X00"])
df.groupby("Box")["StimulusID"].distinct.count()
df.groupby("Box")["StimulusID"].nunique().count()
df.groupby("Box")["StimulusID"].nunique()
countboxstim = df.groupby("Box")["StimulusID"].nunique()
countboxstim[countboxstim["StimulusID"] > 1]
countboxstim = pd.DataFrame(df.groupby("Box")["StimulusID"].nunique())
countboxstim[countboxstim["StimulusID"] > 1]
len(df["StimulusID"].unique())
countstimdonor
df["StimulusID"].unique()
df.groupby("DonorID")["StimulusID"].count()
countstimdonor["StimulusID"].unique()
df["StimulusID"].count()
df["StimulusID"].nunique()
pd.nunique.__doc__()
pd.Series.nunique.__doc__()
df.groupby("StimulusID")["DonorID"].count()
df[df["StimulusID"] == "19.0"]
df[df["StimulusID"] == "19.0", "DonorID"]
df.loc[df["StimulusID"] == "19.0", "DonorID"]
df.loc[df["DonorID"] == "75.0", "StimulusID"]
df[df["StimulusID"] == "23.0", "StimulusName"].unique()
df[df["StimulusID"] == "23.0", "StimulusName"][0]
df.loc[df["StimulusID"] == "23.0", "StimulusName"][0]
df.loc[df["StimulusID"] == "23.0", "StimulusName"]
df.loc[df["StimulusID"] == "23.0", "StimulusName"].unique()
excludeddonors = [96, 104, 122, 167, 178, 219, 268, 279, 303, 308, 534, 701]
df["DonorID"] = df["DonorID"].astype(int)
df.loc[:,"DonorID"] = df["DonorID"].astype(int)
df.loc[:,"DonorID"] = df["DonorID"].astype(str).astype(int)
df.DonorID.dtypes
df.DonorID.dtype
df.dtypes
df = pd.read_csv("/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/Supernatants_Derivatives_20161216.csv")
excludeddonors = [96, 104, 122, 167, 178, 219, 268, 279, 303, 308, 534, 701]
df["DonorID"].head()
df["DonorID"].astype(int)
df["DonorID"] = df["DonorID"].astype(int)
df[df["DonorID"].isin(excludeddonors)]
df.groupby("Box")["StimulusID"].nunique()
countboxstim[countboxstim["StimulusID"] > 1]
boxes = ["MIC_Plasma_S17_V1_A1_F1_D801-896", "MIC_Plasma_S18_V1_A1_F1_D801-896", "MIC_Plasma_S23_V1_A1_F1_D801-896", "MIC_Plasma_S24_V1_A1_F1_D801-896"]
df[df["Box"].isin(boxes)]
df.loc[df["Box"].isin(boxes), "StimulusID"]
df.loc[df["Box"].isin(boxes), "StimulusID"].unique()
df.loc[df["Box"].isin(boxes[0]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[0]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[1]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[2]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[3]), "StimulusID"].unique()
df.loc[df["Box"].isin(boxes), "StimulusID"].unique()
df.loc[df["Box"].isin(boxes), ["StimulusID","DonorID"]].unique()
df.loc[df["Box"].isin(boxes), ["StimulusID","DonorID"]]
df.loc[df["Box"].str.contains(boxes[0]), "StimulusID"].unique()
boxes
df.loc[df["Box"].str.contains(boxes[1]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[2]), "StimulusID"].unique()
df.loc[df["Box"].str.contains(boxes[3]), "StimulusID"].unique()
get_ipython().magic(u'save 1-91 check_derivatives_20161216')
