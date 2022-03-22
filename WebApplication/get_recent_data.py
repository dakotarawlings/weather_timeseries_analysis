#%%
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import requests
import pandas as pd
from datetime import datetime


def get_realtime_data(station_number):
        STATIONNUMBER=str(station_number)
        URL=f'https://www.ndbc.noaa.gov/data/realtime2/{STATIONNUMBER}.txt'
        df_NDBC_realtime =pd.read_csv(URL, delim_whitespace=True)

        df_NDBC_realtime=df_NDBC_realtime.drop(index=0, axis=0)

        if 'mm' not in df_NDBC_realtime.columns:
                df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'mm':[0 for i in range(len(df_NDBC_realtime))]}))

        if '#YY' in df_NDBC_realtime.columns:
                df_NDBC_realtime = df_NDBC_realtime.rename(columns={'#YY': 'YYYY'})

        df_NDBC_realtime=df_NDBC_realtime.rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'})
        datedf=pd.to_datetime(df_NDBC_realtime[['year','month','day','hour','minute']])
        df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'datetime':datedf}))

        return df_NDBC_realtime      


# Funciton to recognize NaN values (most stations report errors/NaN values as "99..")
# Also convert all parameters to floats

def nines_to_nans(df_in, data_columns):

    df=df_in.copy(deep=True)

    for column in data_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

        df[column] = df[column].astype(float)

        #Here we change the value to NaN if it is close to the max value which is likely 99..
        max_value=max(df[column])

        if '99' in str(max_value):
            df[column]=df[column].apply(lambda x: np.NaN if x>max_value-1 else x)
    
    return df

#Format a dataframe after impoting from SQL
def format_df(df_in):
    df=df_in.copy(deep=True)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df=df.set_index('datetime')
    df["date"] = pd.to_datetime(df["date"])
    return df

def transform_data(df_in):
    df=df_in.copy()
    df=df[['ATMP', 'WTMP', 'WSPD']]
    df_cleaned = df_cleaned.interpolate(method='linear', axis=0).ffill().bfill()
    df_cleaned = df_cleaned.resample("H").mean()
    df_cleaned = df_cleaned.interpolate(method='linear', axis=0).ffill().bfill()
    df_engineered= df_engineered.resample("D").max()

def engineer_data(df_in):
    

