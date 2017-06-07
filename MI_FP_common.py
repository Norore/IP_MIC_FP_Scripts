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
    def list_index(column):
        list_index = dataframe.loc[dataframe[column].notnull()].index.tolist()
        indexes = []
        for ind in range(len(list_index)-1):
            if ind < len(list_index):
                indexes.append([list_index[ind], list_index[ind+1]-1])
        indexes.append([list_index[ind+1], dataframe.index.values[-1]])
        return(indexes)

    if isinstance(list_columns, str):
        column = list_columns
        indexes = list_index(column)
        for i in indexes:
            dataframe.loc[i[0]:i[1], column] = dataframe.loc[i[0],:][column]
    else:
        for column in list_columns:
            indexes = list_index(column)
            for i in indexes:
                dataframe.loc[i[0]:i[1], column] = dataframe.loc[i[0],:][column]
    return(dataframe)

excludeddonors = [96, 104, 122, 167, 178, 219, 268, 279, 303, 308, 534, 701]
expecteddonors = [int(i+5001) if i+1 in excludeddonors else int(i+1) for i in range(1000)]
