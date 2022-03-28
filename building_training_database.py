
"""This script builds an SQL database for training our weather models

This script calls the NDBC scraper functions

"""

# %%
import sqlite3
import pandas as pd
import data_scraper_NDBC as scraper
# %%

#Call scraper func to get data
#Station just offshore of santa barbara
STATIONNUMBER='46053'
hist_df=scraper.get_historical_data(STATIONNUMBER, 1998, 2021)

# %%
#Save data to local SQLite database
conn = sqlite3.connect(r"C:\Users\dakot\Desktop\DataScience\projects\weather_prediction\NDBC_model_building_database.db")
hist_df.to_sql(name=f'NDBC_historical_raw_data_St{STATIONNUMBER}',con=conn,schema='NDBC_model_building_database.db',if_exists='replace') 

# %%
#Station in west Santa Barbara (roughly 60km west of the above station)
STATIONNUMBER='46054'
hist_df=scraper.get_historical_data(STATIONNUMBER, 1998, 2021)

# %%
#Save data to local SQLite database
conn = sqlite3.connect(r"C:\Users\dakot\Desktop\DataScience\projects\weather_prediction\NDBC_model_building_database.db")
hist_df.to_sql(name=f'NDBC_historical_raw_data_St{STATIONNUMBER}',con=conn,schema='NDBC_model_building_database.db',if_exists='replace') 








