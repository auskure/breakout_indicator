import pandas as pd
import pandas_ta as ta
import numpy as np


def add_ema(df, ema_value):
    df['EMA'] = ta.ema(df.close, length=ema_value)

    return df

def add_trend_signal(ema_backcandles, df, ema_column_name):
    """
    function that checks for an uptrend, downtrend and neutral signals.
    args: number of backcandles to test, main dataframe to analyse
    returns: 1-d array containing signals. 1 if downtrend, 2 if uptrend and 3 if neutral
    """
    EMAsignal = [0]*len(df)
    for row in range(ema_backcandles, len(df)):
        upTrend = 1
        downTrend = 1
        for i in range(row-ema_backcandles, row+1):
            if max(df.open[i], df.close[i])>=df.EMA[i]: 
                #if the highest point is higher than the ema, there is no downtrend
                downTrend=0
            if min(df.open[i], df.close[i])<=df.EMA[i]:
                #if the lowest point is lower than the ema, there is no uptrend
                upTrend=0
        if upTrend==1 and downTrend==1:
            #neutral signal
            EMAsignal[row]=3
        elif upTrend==1:
            #uptrend signal
            EMAsignal[row]=2
        elif downTrend==1:
            #downtrend signal
            EMAsignal[row]=1

    df[ema_column_name] = EMAsignal 
    return df


def isPivot(df, candle, window):
    """
    function that detects if a candle is a pivot/fractal point
    args: candle index, window before and after candle to test if pivot
    returns: 1 if pivot high, 2 if pivot low, 3 if both and 0 default
    """
    if candle-window < 0 or candle+window >= len(df):
        #out of range
        return 0
    
    pivotHigh = 1
    pivotLow = 2
    for i in range(candle-window, candle+window+1):
        if df.iloc[candle].low > df.iloc[i].low:
            #candle is not the lowest in the window
            pivotLow=0
        if df.iloc[candle].high < df.iloc[i].high:
            #candle is not the highest in the window
            pivotHigh=0
    if (pivotHigh and pivotLow):
        return 3
    elif pivotHigh:
        return pivotHigh
    elif pivotLow:
        return pivotLow
    else:
        return 0

def add_pivot_signal(df, pivot_window, pivot_signal_column_name):
    #checking if each point is a pivot
    df[pivot_signal_column_name] = df.apply(lambda x: isPivot(df, x.name,pivot_window), axis=1) 

    return df

def pointpos(x):
    """
    function that adds a marker for the pivot points
    args: pivot signal
    returns: the y coordinate of the point to be plotted. 
    For low pivots, the point is plotted below. For high pivots, the point is plotted above.
    """
    if x['isPivot']==2:
        #lows should be plotted below datapoint
        return x['low']-1e-3
    elif x['isPivot']==1:
        #highs should be plotted above datapoint
        return x['high']+1e-3
    else:
        return np.nan

def add_pivot_points(df, pivot_position_column_name):
    df[pivot_position_column_name] = df.apply(lambda row: pointpos(row), axis=1) 
    return df

def detect_breakout_structure(df, candle, backcandles, window):
    """
    function that attempts to detect a breakout structure.
    Attention! window should always be greater than the pivot window! to avoid look ahead bias
    args: candles, number in window, window size
    returns: 1 if bullish breakout, 2 if bearish breakout
    """
    if (candle <= (backcandles+window)) or (candle+window+1 >= len(df)):
        return 0
    
    localdf = df.iloc[candle-backcandles-window:candle-window] #window must be greater than pivot window to avoid look ahead bias
    highs = localdf[localdf['isPivot'] == 1].high.tail(3).values
    lows = localdf[localdf['isPivot'] == 2].low.tail(3).values
    levelbreak = 0
    zone_width = 0.01
    if len(lows)==3:
        #checking for three low pivots
        support_condition = True
        mean_low = lows.mean()
        #checking that each low is within the zone_width
        for low in lows:
            if abs(low-mean_low)>zone_width:
                support_condition = False
                break
        if support_condition and (mean_low - df.loc[candle].close)>zone_width*2:
            levelbreak = 1

    if len(highs)==3:
        #checking for three high pivots
        resistance_condition = True
        mean_high = highs.mean()
        #checking that each high is within the zone_width
        for high in highs:
            if abs(high-mean_high)>zone_width:
                resistance_condition = False
                break
        if resistance_condition and (df.loc[candle].close-mean_high)>zone_width*2:
            levelbreak = 2
    return levelbreak

def add_breakout_signal(df, breakout_column_name, breakout_backcandles, breakout_window):

    df[breakout_column_name] = df.apply(lambda row: detect_breakout_structure(df,
                                                                            row.name, 
                                                                            breakout_backcandles, 
                                                                            breakout_window),
                                                                            axis=1)
    return df 

def pointposbreak(x):
    #adding the marker for the pivots.
    """
    function that adds a marker for the breakout points
    args: breakout signal
    returns: the y coordinate of the point to be plotted. 
    For bullish breakouts, the point is plotted below. For bearish breakouts, the point is plotted above.
    """
    if x['pattern_detected']==1:
        #lows should be plotted below datapoint
        return x['low']-2e-3
    elif x['pattern_detected']==2:
        #highs should be plotted above datapoint
        return x['high']+2e-3
    else:
        return np.nan

def add_breakout_points(df, breakout_position_column_name):
    #adding a point to the breakouts for visualisation
    df[breakout_position_column_name] = df.apply(lambda row: pointposbreak(row), axis=1) 
    return df

def add_RSI(df, referenced_column = 'Close'):
    df['RSI'] = ta.rsi(df[referenced_column]) #adding RSI into the dataframe
    return df
