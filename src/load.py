import pandas as pd
import numpy as np
from sklearn import preprocessing

import os

def loadDataFile(PATH, column):
    # load datafile
    print("Using data file {}".format(PATH))
    try:
        df = pd.read_csv(PATH, sep=",", header=0)
        no_header = any(cell.isdigit() for cell in df.columns)
        if no_header:
            df.loc[-1] = df.columns.astype(float)  # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index() 
            df.columns = np.arange(0, df.shape[1])
    except:
        print("\tChoose valid data file")
    # if class column is specified, make that column the index of the dataframe
    names = {}
    if column:
        print("Using class column {}".format(column))
        if column.isdigit():
            column = int(column)
        try:
            df.index = df[column]
            # if classes are not numeric, they need to be encoded
            if df.index.dtype == object:
                names = df[column].astype('category').cat.codes.to_dict()
                df.index = df[column].astype('category').cat.codes.values
                names = dict(zip(names.values(), names.keys()))            
            # drop the class column, since it affects the clustering
            df = df.drop(columns = column)
        except:
            print("\tChoose valid class column") 
            column = ""
    
    # return only the numeric data
    df = df.select_dtypes(include=np.number)
    df = df.dropna()
    
    # scale the data
    min_max_scaler = preprocessing.MinMaxScaler()
    df = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns, index=df.index)

    return df, column, names 