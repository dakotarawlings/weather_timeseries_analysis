
#Functions to access data from NOAA national bouy data center (NDBC) 

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import requests
import pandas as pd
import json
from datetime import datetime
import plotting_functions


def get_historical_data(station_number, start_year, end_year):

        STATIONNUMBER=str(station_number)
        start_year=int(start_year)
        end_year=int(end_year)
        URL='https://www.ndbc.noaa.gov/view_text_file.php'

        df_NDBC_historical=pd.DataFrame()
        for year in range(start_year, end_year+1):
                parameters={'filename':f'{STATIONNUMBER}h{str(year)}.txt.gz',
                        'dir':'data/historical/stdmet/'
                        }
                r=requests.get(URL, params=parameters)

                df_NDBC_year =pd.read_csv(r.url, delim_whitespace=True)

                df_NDBC_year=df_NDBC_year.drop(index=0, axis=0)

                if 'mm' not in df_NDBC_year.columns:
                        df_NDBC_year=df_NDBC_year.join(pd.DataFrame({'mm':[0 for i in range(len(df_NDBC_year))]}))

                if '#YY' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'#YY': 'YYYY'})

                if 'YY' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'YY': 'YYYY'})
                        df_NDBC_year['YYYY']=df_NDBC_year['YYYY'].apply(lambda x: int('19'+str(x)) if len(str(x))==2 else x)

                if 'WD' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'WD': 'WDIR'})

                if 'BAR' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'BAR': 'PRES'})
                       
                        
                df_NDBC_historical=df_NDBC_historical.append(df_NDBC_year, ignore_index=True)              

                time.sleep(np.random.randint(5,20))

        datedf=pd.to_datetime(df_NDBC_historical[['YYYY','MM','DD','hh', 'mm']].rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'}))
        df_NDBC_historical=df_NDBC_historical.join(pd.DataFrame({'date':datedf}))
        df_NDBC_historical=df_NDBC_historical.rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'})

        return df_NDBC_historical



def get_realtime_data(station_number):
        STATIONNUMBER=str(station_number)
        URL=f'https://www.ndbc.noaa.gov/data/realtime2/{STATIONNUMBER}.txt'
        df_NDBC_realtime =pd.read_csv(URL, delim_whitespace=True)

        df_NDBC_realtime=df_NDBC_realtime.drop(index=0, axis=0)

        if 'mm' not in df_NDBC_realtime.columns:
                df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'mm':[0 for i in range(len(df_NDBC_realtime))]}))

        if '#YY' in df_NDBC_realtime.columns:
                df_NDBC_realtime = df_NDBC_realtime.rename(columns={'#YY': 'YYYY'})

        datedf=pd.to_datetime(df_NDBC_realtime[['YYYY','MM','DD','hh','mm']].rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'}))
        df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'datetime':datedf}))

        df_NDBC_realtime=df_NDBC_realtime.rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'})


        return df_NDBC_realtime


def plot_parameter(df, parameter):
        df[parameter] = pd.to_numeric(df[parameter], errors='coerce')
        df = df.dropna(subset=[parameter])

        df[parameter] = df[parameter].astype(float)

        df = df[(df[parameter]>0) & (df[parameter]<99)]
        plotting_functions.timeseries_plot(df, 'datetime', parameter)


def clean_data(df, parameter):
        df[parameter] = pd.to_numeric(df[parameter], errors='coerce')
        df = df.dropna(subset=[parameter])

        df[parameter] = df[parameter].astype(float)

        df = df[(df[parameter]>0) & (df[parameter]<99)]
        return df
# # %%
# STATIONNUMBER='46053'

# hist_df=get_historical_data(STATIONNUMBER, 2000, 2000)

# # %%

# curr_df=get_realtime_data(STATIONNUMBER)

# # %%

# plot_parameter(hist_df, 'ATMP')

