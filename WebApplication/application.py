
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

from BoostedHybridModel import BoostedHybridModel

#Call flask constructor

app=Flask(__name__)

#Define flask endpoint for the main html page

@app.route('/')
def index():

    return render_template('index.html')

#define an API endpoint that takes in an image file from a post reqest and returns

@app.route('/weatherForecast', methods=[ 'GET'])

def temperatureForecast():
    
    
    #monitor the success of the API through a success attribute
    response={'success': False}
            
    df=get_recent_data.update_database()

    plot_data=df.dropna()
    
    plot_data=plot_data.tail(10)
    forecast_2_day=get_forecast.get_temp_forecast()
    
    response['data']=plot_data.to_json()
    response['forecast']=forecast_2_day.to_json()
    response['success']=True

    return jsonify(response)


   
if __name__=='__main__':
    
    app.run(debug=True)
    
      