#%%
#import flask tools
from flask import Flask, jsonify, render_template, request

#Import image an file processing tools
import numpy as np
import get_recent_data
import pickle

import sqlite3

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split

from xgboost import XGBRegressor

from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from sklearn.linear_model import LinearRegression

from BoostedHybridModel import BoostedHybridModel

def get_temp_forecast():
    modelFile = open('TemperatureModel_OneDay.p', 'rb')     
    one_day_model = pickle.load(modelFile)
    modelFile.close()

    modelFile = open('TemperatureModel_TwoDay.p', 'rb')     
    two_day_model = pickle.load(modelFile) 
    modelFile.close()   

    df=get_recent_data.update_database()
 
    one_day_data=df.iloc[[len(df['ATMP'].dropna())]]

    X_model_2_oneDay=one_day_data[['ATMP_lag_1', 'ATMP_lag_2', 'ATMP_lag_3',
       'ATMP_lag_4', 'ATMP_lag_5', 'ATMP_lag_6', 'ATMP_lag_7', 'ATMP_lag_8',
       'WTMP_lag_1', 'WTMP_lag_2', 'WTMP_lag_3', 'WTMP_lag_4', 'WTMP_lag_5',
       'WTMP_lag_6', 'WTMP_lag_7', 'WTMP_lag_8', 'WSPD_lag_1', 'WSPD_lag_2']]

    two_day_data=df.iloc[[len(df['ATMP'].dropna())+1]]

    X_model_2_twoDay=two_day_data[[ 'ATMP_lag_2', 'ATMP_lag_3',
    'ATMP_lag_4', 'ATMP_lag_5', 'ATMP_lag_6', 'ATMP_lag_7', 'ATMP_lag_8',
        'WTMP_lag_2', 'WTMP_lag_3', 'WTMP_lag_4', 'WTMP_lag_5',
    'WTMP_lag_6', 'WTMP_lag_7', 'WTMP_lag_8', 'WSPD_lag_2']]


    forecast=one_day_model.predict(X_model_2_oneDay)
    forecast=forecast.append(two_day_model.predict(X_model_2_twoDay))

    return forecast

# forecast=get_temp_forecast()
# print(forecast.head())



