#!/usr/bin/env python
import pandas as pd

def df_dtypes_object(dataframe):
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(object)
    return dataframe

def complete_columns(dataframe, list_columns):
    for column in list_columns:
        dataframe[column] = pd.Series([dataframe.loc[0, column]]*len(dataframe))
    return dataframe

excludeddonors = [96, 104, 122, 167, 178, 219, 268, 279, 303, 308, 534, 701]
expecteddonors = [int(i+5001) if i+1 in excludeddonors else int(i+1) for i in range(1000)]
