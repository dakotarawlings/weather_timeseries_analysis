# Live Weather Forecaster Santa Barbara

<p align="center">
  <img src="readme_images/homepage.png" width="600" >
</p>

### Web App Link: http://weatherwebapp.us-west-1.elasticbeanstalk.com/

## Overview
* Built a web scraper from scratch 
* Created SQLite database 

## Resources
**Python version:** 3.8

**Packages:** sqlite3, pandas, numpy, sklearn, XGBoost, seaborn, requests, flask, pickle

**Languages:** python, MYSQL, AWS, EB, amazon RDS, SQLite, JavaScript, HTML, CSS

## Web Scraping
* Built a web scraper from scratch using python 
* Extracted features such as:
* Stored raw data in SQLite database

## Data Cleaning and Feature Engineering
* Extracted features 

## Exploratory Data Analysis
Used data visualization and basic summary statistics to analyze the distribution of variables, correlation between variables, outliers, data range, etc.


<p float="left" align="center">
  <img src="readme_pictures/heatmap.png" height="300" />
  <img src="readme_pictures/boxplots.png" height="300" /> 
  <img src="readme_pictures/wordcloud.png" height="300" />
</p>

  
## Model Development
* I split the data into train and test sets (20% test) with the price as the target variable
  
## Model performance
The Boosted Hybrid model achieved a 1-day forecast MAE of 0.9 C and a two day forecast MAE of 1.1 C

## Model Productionalization

<p align="center">
  <img src="readme_pictures/homepage.png" width="600" >
</p>

* Created flask API endpoint 
* Wrote a full stack web application in HTML, CSS, and JavaScript which calls the flask API, and displays tcurrent and forecasted weather parameters using chart.js
* Hosted the web application on AWS EB: http://weatherwebapp.us-west-1.elasticbeanstalk.com/

## Fture work
* Improved error handling in the web app and the API
