
#import flask tools
from flask import Flask, jsonify, render_template, request

#Import image an file processing tools
from PIL import Image
import io
import numpy as np
import get_recent_data
import get_forecast
import pickle

#Call flask constructor
app=Flask(__name__)

#Define flask endpoint for the main html page

@app.route('/')
def index():

    df=get_recent_data.update_database()
    
    plot_data=df.dropna()

    forecast_2_day=get_forecast.get_2_day_temp_forecast()

    return render_template('index.html')

#define an API endpoint that takes in an image file from a post reqest and returns

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    #monitor the success of the API through a success attribute
    response={'success': False}
    
    #Check for a post request    
    if request.method=='POST':
        
        #Check for a media attribute in the json input
        if request.files.get('media'):
            
            #retrieve the file sent by the post request
            img_requested=request.files['media'].read()
            
            #set our success attribute to true ince we have successfully run our model
            response['success']=True

            #return our resonse JSON
    return jsonify(response)
   
if __name__=='__main__':
    app.run(debug=False)
    
      