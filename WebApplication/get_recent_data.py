#%%
import sqlite3

from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

import numpy as np
import pandas as pd

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


#Format a dataframe after impoting from SQL
def format_df(df_in):
    df=df_in.copy(deep=True)
    df["date"] = pd.to_datetime(df["datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df=df.set_index('datetime')

    return df



# Funciton to recognize NaN values (most stations report errors/NaN values as "99..")
# Also convert all parameters to floats

def nines_to_nans(df_in, data_columns):

    df=df_in.copy(deep=True)

    for column in df.columns:
        df[column]=df[column].apply(lambda x: np.NaN if x=='MM' else x)

    for column in data_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')



        df[column] = df[column].astype(float)

        #Here we change the value to NaN if it is close to the max value which is likely 99..
        max_value=max(df[column])
        

        if '99' in str(max_value):
            df[column]=df[column].apply(lambda x: np.NaN if x>max_value-1 else x)
    
    return df





def clean_data(df_in):
    df=df_in.copy(deep=True)
    #Might want to have this as function input
    df=df[['ATMP', 'WTMP', 'WSPD']]
    df = df.interpolate(method='linear', axis=0).ffill().bfill()
    df= df.resample("D").max()
    df = df.interpolate(method='linear', axis=0).ffill().bfill()
    
    return df





def fourier_features(df_in):

    df=df_in.copy(deep=True)
    fourier_pairs=CalendarFourier(freq="A", order=3)


    dp=DeterministicProcess(
        index=df.index,
        constant=True,
        order=1,
        additional_terms=[fourier_pairs],
        drop=True,
    )

    X=dp.in_sample()

    df=df.join(X)

    return df



def make_lag_columns(df_in, num_lags, lag_column):

    df=df_in.copy(deep=True)
    new_cols=pd.DataFrame()
    for i in range(num_lags):
        lag=i+1
        new_lag_column=f'{lag_column}_lag_{lag}'
        new_col=df[lag_column].shift(periods=lag, freq='D').rename(new_lag_column)

        new_cols=new_cols.join(new_col, how='outer')

    df=df.join(new_cols, how='outer')
    return  df



def update_database():

        STATIONNUMBER='46053'

        data_columns=['ATMP', 'WTMP', 'WSPD']

        df=get_realtime_data(STATIONNUMBER)

        df=format_df(df)

        df=nines_to_nans(df, data_columns)

        df=clean_data(df)



        df=make_lag_columns(df, 8, 'ATMP')
        df=make_lag_columns(df, 8, 'WTMP')
        df=make_lag_columns(df, 2, 'WSPD')

        #df.dropna(inplace=True)

        #Save data to local SQLite database
        conn = sqlite3.connect(r"C:\Users\dakot\Desktop\DataScience\projects\weather_prediction\WebApplication\NDBC_recent_cleaned_data.db")
        df.to_sql(name=f'recent_data',con=conn,schema='NDBC_recent_cleaned_data.db',if_exists='replace') 

        return df

#df=update_database()



# %%
