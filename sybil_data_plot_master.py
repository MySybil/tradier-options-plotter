# sybil_data_plot_master.py
# Author: Teddy Rowan @ MySybil.com
# Last Modified: August 5, 2020
# Description: This script handles all the plotting for driver_sybil_data.py

from datetime import datetime
import time
import mplfinance as mpf
import pandas as pd

# mplfinance style documentation
# https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb


# Should we plot /timesales/ or /history/
def plot_data(data, should_use_history_endpoint, data_title, settings):
    if (should_use_history_endpoint):
        plot_history(data, data_title, settings)
    else:
        plot_timesales(data, data_title, settings)
    return 0


# Take in the formatted data and settings, and plot the corresponding chart.
def plot_history(data, data_title, settings):
    ohlc = [] # list of candlestick chart data
    
    if (type(data) == type({})):
        print("Insufficient trade data. Printing all data and terminating Program.")
        print(data)
        exit()
    
    for quote in data:
        quote_time = datetime.strptime(quote['date'], "%Y-%m-%d")
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc.append(pandas_data)

    if (len(ohlc)): #if there is any data
        df = pd.DataFrame(ohlc)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index(pd.DatetimeIndex(df['Date']))

        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }

        df = df.resample('1D').agg(ohlc_dict)
        #df = df.resample('1W').agg(ohlc_dict) #for longer dated options

        # Drop-weekends. Need to be careful about this if we sample by weekend.
        for index, row in df.iterrows():
            day_num = index.to_pydatetime().weekday()
            if (day_num > 4): # weekend
                df.drop(index, inplace=True)
        
        s  = mpf.make_mpf_style(base_mpf_style='yahoo', 
                                rc={'font.size':10, 
                                    'figure.figsize':(9.0, 9.0),
                                    }, 
                                y_on_right=False,
                                gridstyle='--'
                                )
        
        kwargs = dict(type='candle',volume=True)
        #plt = mpf.plot(df,**kwargs,style='yahoo', title=data_title)
                
        mpf.plot(df, **kwargs, style=s, 
                title=data_title, 
                datetime_format=' %m/%d',
                ylabel="Option Price ($)")
        # Note: (show_nontrading = False) didn't work.. hmm.
                        
    else:
        print("No option trades during period.")
    
    return

# Take in the formatted data and settings, and plot the corresponding time/sales chart.
def plot_timesales(data, data_title, settings):    
    ohlc = [] # list of candlestick chart data
    
    if (type(data) == type({})):
        print("Insufficient trade data. Printing all data and terminating Program.")
        print(data)
        exit()
    
    # Organize the data
    for quote in data:
        quote_time = datetime.strptime(quote['time'], "%Y-%m-%dT%H:%M:%S")
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc.append(pandas_data)

    if (len(ohlc)): 
        df = pd.DataFrame(ohlc)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index(pd.DatetimeIndex(df['Date']))

        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }
        df = df.resample('5min').agg(ohlc_dict)

        # drop resampled data that is outside of market hours. 
        for index, row in df.iterrows():
            hours = index.to_pydatetime().hour
            minutes = index.to_pydatetime().minute
            if (hours >= 16):
                df.drop(index, inplace=True)
            if (hours == 9 and minutes < 30):
                df.drop(index, inplace=True)
            if (hours < 9):
                df.drop(index, inplace=True)
        
        s  = mpf.make_mpf_style(base_mpf_style='yahoo', 
                                rc={'font.size':10, 
                                    'figure.figsize':(9.0, 9.0),
                                    }, 
                                y_on_right=False,
                                gridstyle='--'
                                )
        
        kwargs = dict(type='candle',volume=True)
        #plt = mpf.plot(df,**kwargs,style='yahoo', title=data_title)
                
        mpf.plot(df, **kwargs, style=s, 
                title=data_title, 
                datetime_format=' %H:%M',
                ylabel="Option Price ($)")
        
    else:
        print("No option trades during period.")
    return
