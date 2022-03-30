"""This script defines a class for building a boosted hybrid model for timeseries prediction

This file can be imported as a module and contains the following class:

    Class: BoostedHybridModel

    Attributes:
        model_1 (obj): First model to be used for fitting forier features to the data
        model_2 (obj): Second model to be used for fitting residuals 

    Methods:
        fit(X_model_2, y): fit timeseries data to the boosted hybrid model
        predict(X_model_2): Generate a forecast for data for which the target is unknown (forecast horizon)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

class BoostedHybridModel:
    """
    Class for building a boosted hybrid model for timeseries prediction

    Attributes:
        model_1 (obj): First model to be used for fitting forier features to the data
        model_2 (obj): Second model to be used for fitting residuals 

    Methods:
        fit(X_model_2, y): fit timeseries data to the boosted hybrid model
        predict(X_model_2): Generate a forecast for data for which the target is unknown (forecast horizon)
    """

    def __init__(self, model_1, model_2):
        """
        Args:
            model_1 (obj): First model to be used for fitting forier features to the data
            model_2 (obj): Second model to be used for fitting residuals 
        """

        self.model_1=model_1
        self.model_2=model_2
        self.y_column=None

    def fit(self, X_model_2, y):
        """Gets and prints the spreadsheet's header columns

        Args:
            X_model_2 (dataframe): dataframe of features (training data)
            y (dataframe): dataframe of targets (training data)
        """

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
        """Gets and prints the spreadsheet's header columns

        Args:
            X_model_2 (dataframe): Dataframe of features (test data)
        Returns:
            dataframe: dataframe of predicted targets
        """

        fourier_pairs=CalendarFourier(freq="A", order=3)
        X=fourier_pairs.in_sample(X_model_2.index)
        X['constant']=1
        X_model_1=X
        y_predict=pd.Series(self.model_1.predict(X_model_1), index=X_model_1.index, name=self.y_column)
        y_predict+=self.model_2.predict(X_model_2)
        return y_predict
