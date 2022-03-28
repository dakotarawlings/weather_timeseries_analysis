
"""Functions for calling current and historical hourly weather data from NOAA national bouy data center (NDBC) 

This script allows the user to call historical data from the NOAA NDBC

This file can also be imported as a module and contains the following
functions:

    * get_realtime_data - returns a pandas dataframe of current data from a specified station
    * get_historical_data - historical data from a station over a specfied date range

"""

#%%
#Data manipulation packages
import numpy as np
import pandas as pd
#Other packages
import time
import requests
import plotting_functions


def get_historical_data(station_number, start_year, end_year):
        """Scrapes historical hourly NDBC data from the web and returns a dataframe

        Args:
                station_number (str or int): The identification number of the NOAA NDBC station 
                start_year (str or int): format YYYY begining of the date range for which data will be scraped
                end_year (str or int): format YYYY end of the date range for which data will be scraped

        Returns:
                dataframe: A pandas dataframe of all raw data for the specified station over the specified year range
        """

        #convert all params to strings
        STATIONNUMBER=str(station_number)
        start_year=int(start_year)
        end_year=int(end_year)

        #Base url for any historical data from a NDBC
        URL='https://www.ndbc.noaa.gov/view_text_file.php'

        #initialize dataframe
        df_NDBC_historical=pd.DataFrame()

        #Loop through each year in the specified year range and append to dataframe
        for year in range(start_year, end_year+1):
                
                #use requests to format a http string for the desired data
                parameters={'filename':f'{STATIONNUMBER}h{str(year)}.txt.gz',
                        'dir':'data/historical/stdmet/'
                        }
                r=requests.get(URL, params=parameters)

                #use pandas to call raw data from url into pandas df
                df_NDBC_year =pd.read_csv(r.url, delim_whitespace=True)

                #drop the first column because sometimes it contains secondary column information
                df_NDBC_year=df_NDBC_year.drop(index=0, axis=0)
                #some datasets do not have minutes as a column so we add this if they are not present
                if 'mm' not in df_NDBC_year.columns:
                        df_NDBC_year=df_NDBC_year.join(pd.DataFrame({'mm':[0 for i in range(len(df_NDBC_year))]}))
                #Convert columns formatted as #YY to YYY
                if '#YY' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'#YY': 'YYYY'})
                #Some columns in the 1900s were formattted as YY so we change the column title to YYYY and add 19
                if 'YY' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'YY': 'YYYY'})
                        df_NDBC_year['YYYY']=df_NDBC_year['YYYY'].apply(lambda x: int('19'+str(x)) if len(str(x))==2 else x)
                #Convert columns named WD to WDIR
                if 'WD' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'WD': 'WDIR'})
                #Convert columns named BAR to PRES
                if 'BAR' in df_NDBC_year.columns:
                        df_NDBC_year = df_NDBC_year.rename(columns={'BAR': 'PRES'})
                       
                # Append each years data to the dataframe        
                df_NDBC_historical=df_NDBC_historical.append(df_NDBC_year, ignore_index=True)              
                #Pause for a random period of time between each call to avoid overloading the server
                time.sleep(np.random.randint(5,20))
        #The raw data has seperate columns for yr, mnth, etc so we format the columns as a datetime obj
        datedf=pd.to_datetime(df_NDBC_historical[['YYYY','MM','DD','hh', 'mm']].rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'}))
        #join our datetime df column to our dataframe
        df_NDBC_historical=df_NDBC_historical.join(pd.DataFrame({'date':datedf}))
        #Rename columns in main df (MODIFY SO THESE ARE JUST DELETED)
        df_NDBC_historical=df_NDBC_historical.rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'})

        return df_NDBC_historical



def get_realtime_data(station_number):
        """Scrapes current NDBC hourly data from the web and returns a dataframe

        Args:
                station_number (str or int): The identification number of the NOAA NDBC station 

        Returns:
                dataframe: A pandas dataframe of all raw data for the specified station
        """
        #Call data from specified station number and store in pandas df
        STATIONNUMBER=str(station_number)
        URL=f'https://www.ndbc.noaa.gov/data/realtime2/{STATIONNUMBER}.txt'
        df_NDBC_realtime =pd.read_csv(URL, delim_whitespace=True)
        #drop the first row because it sometimes has additional column info
        df_NDBC_realtime=df_NDBC_realtime.drop(index=0, axis=0)
        #add minute column if it is not present
        if 'mm' not in df_NDBC_realtime.columns:
                df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'mm':[0 for i in range(len(df_NDBC_realtime))]}))
        #convert #YY column heading to YYYY to standardize
        if '#YY' in df_NDBC_realtime.columns:
                df_NDBC_realtime = df_NDBC_realtime.rename(columns={'#YY': 'YYYY'})
        #convert date columns to column of datetime objects and append to dataframe
        df_NDBC_realtime=df_NDBC_realtime.rename(columns={'YYYY': 'year', 'MM': 'month', 'DD': 'day', 'hh': 'hour', 'mm':'minute'})
        datedf=pd.to_datetime(df_NDBC_realtime[['year','month','day','hour','minute']])
        df_NDBC_realtime=df_NDBC_realtime.join(pd.DataFrame({'datetime':datedf}))

        return df_NDBC_realtime


#The rest of this is throwaway code (DELETE)
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

def main():
        STATIONNUMBER='46053'
        hist_df=get_historical_data(STATIONNUMBER, 2000, 2000)
        #curr_df=get_realtime_data(STATIONNUMBER)
        plot_parameter(hist_df, 'ATMP')


if __name__ == "__main__":
    main()


