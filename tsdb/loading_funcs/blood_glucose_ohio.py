"""
Scripts related to dataset Blood Glucose Ohio 2020.

For more information please ask Knut Stroemmen (knut.stroemmen@unibe.ch).
"""

# Created by Wenjie Du <wenjay.du@gmail.com> and Rafael Morand <afael.morand@unibe.ch>
# License: BSD-3-Clause

import os

import pandas as pd


def load_blood_glucose_ohio(local_path):
    """Load dataset Blood Glucose Ohio <2018, 2020>.

    Parameters
    ----------
    local_path : str,
        The local path where the data is stored. (Unlike the other datasets, 
        this dataset is private and not available for download.)

    Returns
    -------
    data : dict
        A dictionary contains ['train_X', 'test_X']. 
        The data was presplit to have the first part of every individuals dat in the train set. 
        Not all RecordIDs are present in the test set because some time series had limited data.
    """
    # get all file paths in local_path
    train_df = load_files(local_path, "training")
    test_df  = load_files(local_path, "testing")
    data = {
        "train_X": train_df,
        "test_X": test_df,
        "main_freq": 288
    }
    return data

def load_files(local_path, mode):
    file_paths = get_file_paths(local_path, mode) # get all file paths in local_path
    all_df = pd.DataFrame() # create an empty DataFrame
    # iterate over all file paths and concatenate the DataFrames
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df = set_dtype(df)
        df = df.drop(columns=['5minute_intervals_timestamp'])
        df = df.drop(columns=['missing_cbg'])
        df = df.drop(columns=['hr'])
        df['RecordID'] = extract_record_id(local_path, file_path, mode)
        all_df = pd.concat([all_df, df])
    return all_df
        
def get_file_paths(local_path, mode):
    refined_path = os.path.join(local_path, mode)
    file_paths = [os.path.join(refined_path, f) for f in os.listdir(refined_path) if os.path.isfile(os.path.join(refined_path, f))]
    return file_paths

def set_dtype(df):
    df['time']      = pd.to_datetime(df['time'])
    df['cbg']       = df['cbg'].astype('float16')
    df['finger']    = df['finger'].astype('float16')
    df['basal']     = df['basal'].astype('float16')
    df['gsr']       = df['gsr'].astype('float16')
    df['carbInput'] = df['carbInput'].astype('float16')
    df['bolus']     = df['bolus'].astype('float16')
    return df

def extract_record_id(local_path, file_path, mode):
    return os.path.basename(file_path).replace(local_path, "").replace(f"-{mode}.csv", "")
