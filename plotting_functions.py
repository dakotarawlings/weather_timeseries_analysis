#Functions for plotting timeseries data from a dataframe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL

import requests
import pandas as pd
import json
import datetime
from datetime import datetime
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import seaborn as sns

#%config InlineBackend.figure_format = 'retina'

def timeseries_plot(df, xdata, ydata, ax=None):

    fig, ax = plt.subplots()

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

    fig.autofmt_xdate()

    plt.rc(
        "figure",
        autolayout=True,
        figsize=(11, 4),
        titlesize=18,
        titleweight='bold',
    )
    plt.rc(
        "axes",

        labelweight="bold",
        labelsize='Large',
        titleweight="bold",
        titlesize=16,
        titlepad=10,
    )

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    df.plot(x=xdata, y=ydata, ax=ax)
    ax.grid(True)
    ax.tick_params(direction='in', which='both')
    ax.set_title(f'Time Plot of {ydata}')

    ax.set_xlabel('date', fontsize=16)
    ax.set_ylabel(ydata, fontsize=16)

    return ax


def timeseries_plot_grid(df, xdata, ydata_mat, ax=None):


    fig, ax = plt.subplots(len(ydata_mat), sharex=True)

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    plt.rc(
        "figure",
        autolayout=True,
        figsize=(11, 4*len(ydata_mat)),
        titlesize=18,
        titleweight='bold',
    )
    plt.rc(
        "axes",

        labelweight="bold",
        labelsize='Large',
        titleweight="bold",
        titlesize=16,
        titlepad=10,
    )
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    for i in range(len(ydata_mat)):

        ax[i].xaxis.set_major_locator(years)
        ax[i].xaxis.set_major_formatter(yearsFmt)
        ax[i].xaxis.set_minor_locator(months)

        ax[i].format_xdata = mdates.DateFormatter('%Y-%m-%d')

        fig.autofmt_xdate()
        
        ydata=ydata_mat[i]
        df.plot(x=xdata, y=ydata, ax=ax[i])
        ax[i].grid(True)
        ax[i].tick_params(direction='in', which='both')
        ax[i].set_title(f'Time Plot of {ydata}')

        ax[i].set_xlabel('date', fontsize=16)
        ax[i].set_ylabel(ydata, fontsize=16)

        return ax



