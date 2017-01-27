#!/usr/bin/env python
import pandas as pd
from IPython.display import display, Markdown, HTML

# print table without index column
"""
"""
def table_wo_index(df):
    table = HTML(re.sub('(<tr.*>\n) +<th>.*</th>\n', '\\1', df._repr_html_()))
    return(table)

"""
"""
def show_columns(df):
    display(Markdown("List of the *%d* columns:" % len(df.columns)))
    display(Markdown(";\n".join(["1. "+col for col in df.columns])+"."))

"""
"""
def compare_two_columns(df, col1, col2, rev=False, method="count", show=True):
    if method == "count":
        col2percol1 = pd.DataFrame(df.groupby(col1)[col2].count())
    if method == "unique":
        col2percol1 = pd.DataFrame(df.groupby(col1)[col2].unique())
    if method == "nunique":
        col2percol1 = pd.DataFrame(df.groupby(col1)[col2].nunique())
    else:
        col2percol1 = pd.DataFrame(df.groupby(col1)[col2].count())
    col2percol1.loc[:, col1] = col2percol1.index
    col2percol1.reset_index(drop=True, inplace=True)
    if show:
        if rev:
            col2percol1_out = col2percol1.rename(columns={col1: "Nb_"+col1})
            display(col2percol1_out[[col2, "Nb_"+col1]])
        else:
            col2percol1_out = col2percol1.rename(columns={col2: "Nb_"+col2})
            display(col2percol1_out[[col1, "Nb_"+col2]])

    return(col2percol1)
