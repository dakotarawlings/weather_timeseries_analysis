#This script builds an SQL database for training the weather model with the desired parameters
#Over the desired period of time using the NOAA scraper functions

# %%
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import pandas as pd
from datetime import datetime

import data_scraper_NDBC as scraper
import plotting_functions
# %%

#Call scraper func to get data (only need to do this once)
#Station just offshore of santa barbara
STATIONNUMBER='46053'
hist_df=scraper.get_historical_data(STATIONNUMBER, 1998, 2021)
#curr_df=scraper.get_realtime_data(STATIONNUMBER)
#scraper.plot_parameter(hist_df, 'WSPD')


# %%
#Save data to local SQLite database
conn = sqlite3.connect(r"C:\Users\dakot\Desktop\DataScience\projects\weather_prediction\NDBC_model_building_database.db")
hist_df.to_sql(name=f'NDBC_historical_raw_data_St{STATIONNUMBER}',con=conn,schema='NDBC_model_building_database.db',if_exists='replace') 


# %%
#Station in west Santa Barbara (roughly 60km west of the above station)
STATIONNUMBER='46054'
hist_df=scraper.get_historical_data(STATIONNUMBER, 1998, 2021)
#curr_df=scraper.get_realtime_data(STATIONNUMBER)
#scraper.plot_parameter(hist_df, 'WSPD')


# %%
#Save data to local SQLite database
conn = sqlite3.connect(r"C:\Users\dakot\Desktop\DataScience\projects\weather_prediction\NDBC_model_building_database.db")
hist_df.to_sql(name=f'NDBC_historical_raw_data_St{STATIONNUMBER}',con=conn,schema='NDBC_model_building_database.db',if_exists='replace') 








