
"""Function to call NOAA API for daily sumaries of weather data from NOA weather stations (land stations)

Unfortunately, It seems that noaa does not offer any easy way to get real-time data from their land weather stations
As a result, for these functions, you can only get data up to 3-days before the API call
For this reason, I mostly use data from the national buoy data center (NDBC) (see my data scraping script for NDBC data)
For my live weather prediciotn projects It is much easier to scrape live data from a NOA NDBC (vs a NOA land station)

This file can also be imported as a module and contains the following
functions:

    * get_station_data - returns a pandas dataframe of current data from a specified station

"""
#%%

import numpy as np
import pandas as pd
import time
import requests
import pandas as pd
import json
from datetime import datetime
from datetime import date
from datetime import timedelta

def get_station_data(station_id,data_type, start_year, end_year):
    """Scrapes daily summary data from NOA land station over specified period of time

    see https://www.ncdc.noaa.gov/cdo-web/webservices/v2 for more information on API
    Args:
            station_id (str or int): The identification number of the NOAA NDBC station 
            data_type (str): The parameter to be called from the station (TAVG, TMAX, TMIN, AWIND, etc) see NOAA website for more
            start_year (str or int): format YYYY begining of the date range for which data will be scraped
            end_year (str or int): format YYYY end of the date range for which data will be scraped

    Returns:
            dataframe: A pandas dataframe of all raw data for the specified station over the specified year range
    """

    #convert years to ints
    start_year=int(start_year)
    end_year=int(end_year)

    #establish access token (from NOAA website), base URL for API
    URL='https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
    access_token='XnbdvzFKULZrPBREmligzKHMEbArrPQV'
    header={'token': access_token}

    #initialize df
    df=pd.DataFrame()

    #I interpret the year as the jan 1st of that year so I add a year if it is the current date to get data all the way up tot he current month
    if end_year==datetime.now().year:
        end_year+=1

    #loop through each year in the date range and append data to df
    for year in range(start_year, end_year):

        #establish parameters for the api call
        parameters={'stationid':station_id,
                'datasetid':'GHCND',
                'datatypeid':data_type,
                'limit':'1000',
                'startdate':f'{str(year)}-01-01',
                'enddate':f'{str(year+1)}-01-01'
                }
        #Change the end date parameter to the current date  if the year is the current year
        #again we can only get data up to 3 days ago so this is the most recent date
        if year==datetime.now().year:
            today = date.today()
            yesterday = today - timedelta(days = 3)
            parameters['enddate']=str(yesterday)

        # make requests with parameters
        r=requests.get(URL, params=parameters, headers=header)

        #get the response JSON
        data=json.loads(r.text)
        #get the JSON element that has our data
        data=[item for item in data['results'] if item['datatype']==data_type]
        #parse out the dates
        dates=[item['date'] for item in data]
        #parse ou the data values from the dictionary
        data_vals=[item['value'] for item in data]
        #initiate a dataframe
        df_data=pd.DataFrame()
        #Conver the date column strings to datetime objects
        df_data['date']=[datetime.strptime(date,"%Y-%m-%dT%H:%M:%S") for date in dates]
        #If the data is temperature convert to celsius
        if data_type=='TMAX' or data_type=='TMIN':
            data_vals=[float(v)/10.0*1.8+32 for v in data_vals]
        #add the data to the dataframe
        df_data[data_type]=data_vals
        df=df.append(df_data)
        #pause for a random period of time in between each API call to avoid overloading the server
        time.sleep(np.random.randint(5,15))
    
    return df
    
#If the script is called as main, we make a test API call    
def main():
    data_type='AWND'
    #data_type='TMAX'
    station_id='GHCND:USW00023190'

    df_temp=get_station_data(station_id,data_type, 2000, 2022)

    # %%
    import plotting_functions
    plotting_functions.timeseries_plot(df_temp, 'date', 'AWND')


if __name__ == "__main__":
    main()


