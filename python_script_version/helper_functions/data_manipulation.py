import pandas as pd
import pandas_ta as ta
import numpy as np

def read_csv(data_location, data_prefix = '../data/'):
    df = pd.read_csv(data_prefix + data_location)
    return df

def rename_columns(df):
    df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
        }, inplace=True)
    return df

def clean_data(df):
    #filtering the dataframe so that volume does not have a zero value
    df=df[df['volume']!=0] 

    #reset the indexes to accomodate removing of volume = 0 entries
    df.reset_index(drop=True, inplace=True) 

    return df

def backtest_format(data):
    #renaming the columns in the dataframe
    data.rename(columns={
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'close': 'Close',
    'volume': 'Volume'
    }, inplace=True)

    data.set_index("Gmt time", inplace=True)
    data.index = pd.to_datetime(data.index, format='%d.%m.%Y %H:%M:%S.%f').floor('S')

    return data

def strat_output_writer(strat, strat_name, output_folder = 'outputs'):

    toWrite = open('./{}/'.format(output_folder) + '{}.txt'.format(strat_name), 'w')
    toWrite.write(str(strat))