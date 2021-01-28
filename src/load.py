import pandas as pd
import numpy as np
from sklearn import preprocessing

import os

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def loadDataFile(PATH, column):
    # load datafile
    print("Using data file {}".format(PATH))
    try:
        df = pd.read_csv(PATH, sep=",", header=0)    
        header_num = [ is_number(cell) for cell in df.columns ]
        if any(header_num):
            # change the numeric ones to floats
            df.columns.values[header_num] = df.columns[header_num].astype(float) 
            df.loc[-1] = df.columns # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index() 
            df.columns = np.arange(1, df.shape[1]+1)
    except:
        print("\tChoose valid data file")
    # if cluster column is specified, make that column the index of the dataframe
    names = {}
    if column:
        print("Using cluster column {}".format(column))
        if column.isdigit():
            column = int(column)
        try:
            df.index = df[column]
            # if classes are not numeric, they need to be encoded
            if df.index.dtype == object:
                names = df[column].astype('category').cat.codes.to_dict()
                df.index = df[column].astype('category').cat.codes.values
                names = dict(zip(names.values(), names.keys()))            
            # drop the cluster column, since it affects the clustering
            df = df.drop(columns = column)
        except:
            print("\tChoose valid cluster column") 
            column = ""
    
    # convert str data to categorical
    
    cat_columns = df.select_dtypes(['object']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.astype("category").cat.codes)
    df = df.select_dtypes(include=np.number)
    df = df.dropna()
    
    # scale the data
    min_max_scaler = preprocessing.MinMaxScaler()
    df = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns, index=df.index)

    return df, column, names 