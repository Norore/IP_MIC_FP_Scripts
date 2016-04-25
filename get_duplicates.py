import pandas as pd

root = "/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToPrepare/"
f_freezer = "/Volumes/LabExMI/Users/Nolwenn/FreezerPro/DataToImport/freezers.csv"
f_trucult = root+"1.LabExMI_TrucultureMapping_21Nov2014_FinalVersion.xlsx"
n_trsheet = "FinalMapping"
f_labkey = root+"samples_table_labkey.csv"
f_stimul = root+"3.5000samples_WL_QCs_DL_02Jul2015.xls"
n_stsheet = "5000samples_WL_QCs_DL_02Jul2015"
o_samples = root+"TC_Trizol_rack_samples.csv"

df_freezer = pd.read_csv(f_freezer, dtype=object)
truc_data = pd.read_excel(f_trucult, n_trsheet)  # use sheet 'FinalMapping'
df_labkey = pd.read_csv(f_labkey, dtype=object)
df_stimul = pd.read_excel(f_stimul, n_stsheet)

df_stimul = pd.read_excel("/Volumes/LabExMI/Users/"
                          "Nolwenn/FreezerPro/DataToPrepare/"
                          "3.5000samples_WL_QCs_DL_02Jul2015.xls",
                          "5000samples_WL_QCs_DL_02Jul2015")

donorsduplicated = df_stimul.loc[df_stimul["DonorIDscanned"].
    duplicated()]["DonorIDscanned"].index.tolist()
dic = df_stimul.ix[0]
df_dupli = pd.DataFrame(columns=dic.index)
c = 0
for e in donorsduplicated:
    dic = df_stimul.loc[e]
    df_dupli.loc[c] = dic
    c += 1
df_dupli.to_csv("/Volumes/LabExMI/Users/Nolwenn/"
                "FreezerPro/DonorIDscanned_duplicated.csv",
                sep=";", index=False, header=True)

donorsduplicated = df_stimul.loc[df_stimul["DonorIDscanned"].
    duplicated()]["DonorIDscanned"].values.tolist()
dic = df_stimul.ix[0]
df_dupli = pd.DataFrame(columns=dic.index)
c = 0
for e in donorsduplicated:
    dic = df_stimul.loc[df_stimul["DonorIDscanned"].str.contains(e)]
    for l in dic.index:
        df_dupli.loc[c] = dic.loc[l]
        c += 1
df_dupli.to_csv("/Volumes/LabExMI/Users/Nolwenn/"
                "FreezerPro/DonorIDscanned_duplicated.csv",
                sep=";", index=False, header=True)