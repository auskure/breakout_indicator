import pandas as pd
import numpy as np
import plotly.graph_objects as go


def price_chart_plotter(df, 
                        analysis_range_start, 
                        analysis_range_end, 
                        fig_name, 
                        pivot_position_column_name,
                        colour_used = "MediumPurple",
                        mode_used = "markers"
                        ):


    dfpl = df[analysis_range_start:analysis_range_end]
    fig = go.Figure(data = [go.Candlestick(x=dfpl.index,
                    open = dfpl['open'],
                    high = dfpl['high'],
                    low = dfpl['low'],
                    close = dfpl['close'])])

    fig.add_scatter(x = dfpl.index, 
                    y = dfpl['pivot_pos'], 
                    mode = mode_used,
                    marker=dict(size = 5, color = colour_used),
                    name = pivot_position_column_name)

    fig.update_layout(xaxis_rangeslider_visible = False)
    fig.show()
    fig.write_image('./outputs/' + fig_name)


def price_chart_plotter_with_breakout(df, 
                                    analysis_range_start, 
                                    analysis_range_end, 
                                    fig_name, 
                                    pivot_position_column_name,
                                    breakout_position_column_name,
                                    pivot_colour_used = "MediumPurple",
                                    breakout_colour_used = "MediumBlue",
                                    mode_used = "markers"):
    
    dfpl = df[analysis_range_start:analysis_range_end]
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=dfpl['open'],
                    high=dfpl['high'],
                    low=dfpl['low'],
                    close=dfpl['close'])])

    fig.add_scatter(x=dfpl.index, 
                    y=dfpl['pivot_pos'], 
                    mode="markers",
                    marker=dict(size=5, color=pivot_colour_used),
                    name=pivot_position_column_name)

    fig.add_scatter(x=dfpl.index, 
                    y=dfpl['breakout_pos'], 
                    mode="markers",
                    marker=dict(size=5, color=breakout_colour_used),
                    name=breakout_position_column_name)

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()
    fig.write_image('./outputs/' + fig_name)

