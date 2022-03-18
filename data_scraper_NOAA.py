#Functions to call NOAA API for daily sumaries of weather data from NOA weather stations
#Unfortunately, It seems that noaa does not offer any easy way to get real-time data from their land weather stations
# As a result, for these functions, I only get data up to 3-days before the API call
#For this reason, I mostly use data from the national buoy data center (NDBC) (see my data scraping script for NDBC data)
# For my live weather prediciotn projects It is much easier to scrape live data from a NOA NDBC (vs a NOA land station)

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import time

import requests
import pandas as pd
import json
from datetime import datetime
from datetime import date
from datetime import timedelta
####Update so that 2021 or 2022 goes to current date
def get_station_data(station_id,data_type, start_year, end_year):
    URL='https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
    access_token='XnbdvzFKULZrPBREmligzKHMEbArrPQV'
    header={'token': access_token}

    df=pd.DataFrame()

    if end_year==datetime.now().year:
        end_year+=1

    for year in range(start_year, end_year):

        start_year=int(start_year)
        end_year=int(end_year)


        parameters={'stationid':station_id,
                'datasetid':'GHCND',
                'datatypeid':data_type,
                'limit':'1000',
                'startdate':f'{str(year)}-01-01',
                'enddate':f'{str(year+1)}-01-01'
                }

        if year==datetime.now().year:
            today = date.today()
            yesterday = today - timedelta(days = 3)
            parameters['enddate']=str(yesterday)

        r=requests.get(URL, params=parameters, headers=header)

        d=json.loads(r.text)

        data=[item for item in d['results'] if item['datatype']==data_type]

        dates=[item['date'] for item in data]

        data_vals=[item['value'] for item in data]

        df_data=pd.DataFrame()

        df_data['date']=[datetime.strptime(date,"%Y-%m-%dT%H:%M:%S") for date in dates]

        if data_type=='TMAX' or data_type=='TMIN':
            data_vals=[float(v)/10.0*1.8+32 for v in data_vals]

        df_data[data_type]=data_vals

        df=df.append(df_data)

        time.sleep(np.random.randint(5,15))
    
    return df
    
    
# %%

data_type='AWND'
#data_type='TMAX'
station_id='GHCND:USW00023190'

df_temp=get_station_data(station_id,data_type, 2000, 2022)


# %%
import plotting_functions
plotting_functions.timeseries_plot(df_temp, 'date', 'AWND')


