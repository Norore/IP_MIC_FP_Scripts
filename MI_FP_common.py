#!/usr/bin/env python
import pandas as pd

def df_dtypes_object(dataframe):
    """
        Convert each field of dataframe as type object

        dataframe - dataframe
    """
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(object)
    return dataframe

def complete_columns(dataframe, list_columns):
    """
        From a dataframe, complete selected columns with value in line before

        dataframe    - dataframe
        list_columns - list of columns
    """
    for column in list_columns:
        dataframe[column] = pd.Series([dataframe.loc[0, column]]*len(dataframe))
    return dataframe

excludeddonors = [96, 104, 122, 167, 178, 219, 268, 279, 303, 308, 534, 701]
expecteddonors = [int(i+5001) if i+1 in excludeddonors else int(i+1) for i in range(1000)]
