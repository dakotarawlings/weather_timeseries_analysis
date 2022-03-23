#%%
#import flask tools
from flask import Flask, jsonify, render_template, request

#Import image an file processing tools
from PIL import Image
import io
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


class BoostedHybridModel:
    def __init__(self, model_1, model_2):
        self.model_1=model_1
        self.model_2=model_2
        self.y_column=None

    def fit(self, X_model_2, y):

        fourier_pairs=CalendarFourier(freq="A", order=3)
        X=fourier_pairs.in_sample(X_model_2.index)
        X['constant']=1
        X_model_1=X
        self.model_1.fit(X_model_1, y)
        y_fit=pd.Series(self.model_1.predict(X_model_1), index=X_model_1.index, name=y.name)
        y_residuals=y-y_fit
        self.model_2.fit(X_model_2, y_residuals)
        self.y_columns=y.name
        self.y_fit=y_fit
        self.y_residuals=y_residuals

    def predict(self, X_model_2):

        fourier_pairs=CalendarFourier(freq="A", order=3)
        X=fourier_pairs.in_sample(X_model_2.index)
        X['constant']=1
        X_model_1=X
        y_predict=pd.Series(self.model_1.predict(X_model_1), index=X_model_1.index, name=self.y_column)
        y_predict+=self.model_2.predict(X_model_2)
        return y_predict



def get_2_day_temp_forecast():
    modelFile = open('modelFile.p', 'rb')     
    pmodel = pickle.load(modelFile)

    df=get_recent_data.update_database()
    
    plot_data=df.dropna()

    two_day_data=df.iloc[[len(plot_data)+1]]
    X_model_2=two_day_data[[ 'ATMP_lag_2', 'ATMP_lag_3',
       'ATMP_lag_4', 'ATMP_lag_5', 'ATMP_lag_6', 'ATMP_lag_7', 'ATMP_lag_8',
        'WTMP_lag_2', 'WTMP_lag_3', 'WTMP_lag_4', 'WTMP_lag_5',
       'WTMP_lag_6', 'WTMP_lag_7', 'WTMP_lag_8', 'WSPD_lag_2']]

    y_predp=pmodel.predict(X_model_2)
    modelFile.close()
    return y_predp

forecast=get_2_day_temp_forecast()
