import pandas as pd
import numpy as np
from scipy import stats
from backtesting import Strategy
from backtesting import Backtest


from helper_functions.data_manipulation import read_csv,rename_columns,clean_data
from helper_functions.data_manipulation import backtest_format,strat_output_writer

from helper_functions.column_adder import add_ema,add_trend_signal,add_pivot_signal,add_pivot_points
from helper_functions.column_adder import add_breakout_signal,add_breakout_points,add_RSI

from helper_functions.graph_plotter import price_chart_plotter,price_chart_plotter_with_breakout

from helper_functions.backtest import MyStrat_1, MyStrat_2


#variable declaration
data_file = "EURUSD_Candlestick_1_D_BID_05.05.2003-28.10.2023.csv"

#pivot analysis variables
ema_value = 50 #for the moving average. 50 means 50ema.
ema_backcandles = 15 #number of candles to check for uptrend and downtrend with respect to EMA
ema_column_name = 'EMASignal' #column name of the ema signal
pivot_window = 6 #number of candles involved in the pivot search
pivot_signal_column_name = 'isPivot' #column name of the pivot signal
pivot_position_column_name = 'pivot_pos' #column name of the pivot coordinates
price_chart_fig_name = 'price_chart.png' #figure name of the price chart
analysis_range_start = 1000 
analysis_range_end = 2000

#breakout variables
breakout_backcandles = 40 #number of candles to check for the breakout trend
breakout_window = 6 #number of candles involved in the breakout search
breakout_column_name = 'pattern_detected' #column name of the breakout signal
breakout_position_column_name = 'breakout_pos' #column name of the breakout coordinates
breakout_chart_fig_name = "breakout_chart.png" #figure name of the price chart with breakout points
backtest_points = 5000 #number of datapoints involved in backtesting

#strategy variables
strategy_1_name = 'strat_1'
strategy_2_name = 'strat_2'

#reading in the data
df = read_csv(data_file)

#renaming the columns in the dataframe
df = rename_columns(df)

#data cleaning
df = clean_data(df)


#adding EMA into the dataframe as a column
df = add_ema(df, ema_value)

#adding EMA signal into the dataframe. This signal checks for downtrends and uptrends
df = add_trend_signal(ema_backcandles, df, ema_column_name)

#adding a signal which tells if each point is a pivot
df = add_pivot_signal(df, pivot_window, pivot_signal_column_name)

#adding a point to the pivots for visualisation
df = add_pivot_points(df, pivot_position_column_name) 


#plotting the price chart with the pivot points
price_chart_plotter(df, 
                    analysis_range_start, 
                    analysis_range_end, 
                    price_chart_fig_name, 
                    pivot_position_column_name)


#adding a column which checks for breakout patterns
df = add_breakout_signal(df, breakout_column_name, breakout_backcandles, breakout_window)

#adding a point to the breakouts for visualisation
df = add_breakout_points(df, breakout_position_column_name)

#plotting the price chart with the pivot and breakout points
#we observe that a breakout pattern has occured at the 1507 mark
price_chart_plotter_with_breakout(df, 
                                analysis_range_start, 
                                analysis_range_end, 
                                breakout_chart_fig_name, 
                                pivot_position_column_name,
                                breakout_position_column_name)

#creating a new dataframe, for backtesting
data = df[:backtest_points].copy()

#renaming the columns in the dataframe
data = backtest_format(data) 

data = add_RSI(data)

#running strategies.  Their explanations can be found in helper_functions.backtests
bt = Backtest(data, MyStrat_1, cash=10000, margin=1/5)
strat_1 = bt.run()

bt = Backtest(data, MyStrat_2, cash=10000, margin=1/5)
strat_2 = bt.run()

#strategy performance will be saved in the output folder
strat_output_writer(strat_1, strategy_1_name)
strat_output_writer(strat_2, strategy_2_name)

