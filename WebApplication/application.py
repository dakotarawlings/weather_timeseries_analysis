
#import flask tools
from flask import Flask, jsonify, render_template, request

#Import image an file processing tools

import numpy as np
import get_recent_data
import get_forecast
import pandas as pd
import pickle

from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from xgboost import XGBRegressor


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


#Call flask constructor
app=Flask(__name__)

#Define flask endpoint for the main html page

@app.route('/')
def index():

    return render_template('index.html')

#define an API endpoint that takes in an image file from a post reqest and returns

@app.route('/temperatureForecast', methods=['GET', 'POST'])
def predict():
    
    #monitor the success of the API through a success attribute
    response={'success': False}
            
    df=get_recent_data.update_database()

    plot_data=df.dropna()

    forecast_2_day=get_forecast.get_2_day_temp_forecast()
    
    response['data']=plot_data.to_json()
    response['forecast']=forecast_2_day.to_json()
    response['success']=True

    return jsonify(response)
   
if __name__=='__main__':
    app.run(debug=True)
    
      