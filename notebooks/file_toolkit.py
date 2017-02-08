#!/usr/bin/env python
import pandas as pd
from IPython.display import display, Markdown, HTML
import matplotlib.pyplot as plt

def table_wo_index(df):
    """
        Return a HTML table without the dataframe index

        df - dataframe
    """
    table = HTML(re.sub('(<tr.*>\n) +<th>.*</th>\n', '\\1', df._repr_html_()))
    return(table)

def show_columns(df):
    """
        Display the list of columns of a dataframe

        df - dataframe
    """
    display(Markdown("List of the *%d* columns:" % len(df.columns)))
    display(Markdown(";\n".join(["1. "+col for col in df.columns])+"."))

def compare_two_columns(df, col1, col2, rev=False, method="count", show=True):
    """
        From a dataframe, compares 2 columns, display result and return new
        dataframe

        df     - dataframe
        col1   - column 1 name
        col2   - column 2 name
        rev    - if True, display dataframe in reverse column order (col2, col1)
        method - method used by groupby function:
                    - count
                    - unique
                    - nunique
        show   - if False, only return the new dataframe
    """
    d_method = {"count": pd.DataFrame(df.groupby(col1)[col2].count()),
                "unique": pd.DataFrame(df.groupby(col1)[col2].unique()),
                "nunique": pd.DataFrame(df.groupby(col1)[col2].nunique())}
    if method in d_method.keys():
        col2percol1 = d_method[method]
    else:
        col2percol1 = d_method["count"]

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

def label_nb_barh(ax, rects):
    """
        Add label value in ticks for horizontal bar plot

        ax    - subplot object
        rects - ax.barh object
    """
    for rect in rects:
        width = rect.get_width()
        ax.text(width, rect.get_y() + rect.get_height()/2.,
                '%d' % int(width),
                ha='center', va='center',
               bbox=dict(facecolor='white', edgecolor='none', alpha=0.5))

def label_nb_barv(ax, rects):
    """
        Add label value in ticks for vertical bar plot

        ax    - subplot object
        rects - ax.barh object
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
