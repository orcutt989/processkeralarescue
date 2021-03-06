"""
 Script reads the csv file describing the details of people requiring help.
"""

__author__ = "Shameer Sathar"
__license__ = "MIT"
__version__ = "1.0.1"

# imports
import pandas as pd
import numpy as np

import os
import re

def getLat(data):
    if ((data[0] == '(')):
        data = data[1:-1]
    if re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', data) is not None:
        lat, long = [float(x) for x in data.split(',')]
    else:
        lat, long = False, False
    return lat

def getLon(data):
    if ((data[0] == '(')):
        data = data[1:-1]
    if re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', data) is not None:
        lat, long = [float(x) for x in data.split(',')]
    else:
        lat, long = False, False
    return long

def getLocError(data):
    if data == 'accurate':
        return 0
    elif (' Meters' in data):
        return float(data.split()[0])
    else:
        return 10000

def read_data():
    df = pd.read_json('data/data.json')
    df['LatValid'] = df['latlng']
    df['LonValid'] = df['latlng']
    df['LatValid'] = df['latlng'].apply(getLat)
    df['LonValid'] = df['latlng'].apply(getLon)
    df = df[df['LonValid'] != False]
    df['datetime'] = pd.to_datetime(df['dateadded'])
    df['locError'] = df['latlng_accuracy'].apply(getLocError)
    df = df[df.locError < 500]
    return df

def get_plot_data(list_requirements, rad_value):
    df = read_data()
    list_requirements = list_requirements
    for requirement in list_requirements:
        if requirement == 'needfoodandwater':
            df = df[(df['needfood'] == True)]
        else:
            df = df[df[requirement] == True]
    if (rad_value == 'requested_within_3_hours'):
        df = df[df.datetime > pd.Timestamp.now() -  pd.Timedelta(hours=3)]
    elif (rad_value == 'requested_today'):
        df = df[df.datetime > pd.Timestamp.now() -  pd.Timedelta(hours=24)]
    elif (rad_value == 'requested_yesterday'):
        df = df[(df.datetime > (pd.Timestamp.now() -  pd.Timedelta(hours=48)))\
         & (df.datetime < (pd.Timestamp.now() -  pd.Timedelta(hours=24)))]
    elif (rad_value == 'requested_yesterday'):
        df = df[(df.datetime <= (pd.Timestamp.now() -  pd.Timedelta(hours=48)))]
    else:
        df = df
    return df
