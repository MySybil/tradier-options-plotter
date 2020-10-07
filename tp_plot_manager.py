"""
tp_plot_manager.py
Last Modified: August 16, 2020
Description: This script handles all the plotting for run_sybil_plotter.py

# mplfinance style documentation
# https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
"""

from datetime import datetime
import time
import pandas as pd
import mplfinance as mpf
from mysybil_greeks import OptionAnalysis

# Are we plotting intraday or daily data?
def plot_data(data, underlying_data, should_use_history_endpoint, data_title, settings):
    if (should_use_history_endpoint):
        plot_history(data, 
                     underlying_data, 
                     data_title, 
                     settings)
    else:
        # Not yet implemented underyling_data grab for timesales
        plot_timesales(data, 
                       data_title, 
                       settings)
    return 0


# Make a plot of daily or longer data
def plot_history(data, underlying_data, data_title, settings):
    check_data_validity(data)
    
    # ohlc for the underlying symbol. will use this to calculate IV
    ohlc_underlying = []
    for quote in underlying_data:
        quote_time = datetime.strptime(quote['date'], "%Y-%m-%d")
        pandas_data = quote_time, quote['date'], quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc_underlying.append(pandas_data)
    
    ohlc = []
    for quote in data:
        quote_time = datetime.strptime(quote['date'], "%Y-%m-%d")
        iv = 0
        
        # Traverse the underlying data until we find the matching time period
        for underlying in ohlc_underlying:
            if (quote_time == underlying[0]):
                trade_date = invert_date(quote['date'])
                expiry_date = invert_date(settings['expiry'])
        
                blank_tte = 0 # need something to initialize the class
                sparta = OptionAnalysis(underlying[-2], float(settings['strike']), blank_tte, 0, quote['close'], settings['rfr'], settings['type'] == 'C')
                # Initialize the OptionAnalysis data [-2] is 'close'
                
                time_to_expiry = sparta.get_market_year_fraction(trade_date, expiry_date, -1*390)
                # Find the year fraction of time remaining only looking at market minutes. (dates inclusive, so -390 (1day))
                
                sparta.tte = time_to_expiry
                iv = sparta.get_implied_volatility()
                break
        
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume'], round(iv*100,2)
        ohlc.append(pandas_data)

    if (len(ohlc)):
        df = pd.DataFrame(ohlc)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'IV (%)']
        df = df.set_index(pd.DatetimeIndex(df['Date']))

        ohlc_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum',
            'IV (%)':'last'
        }

        df = df.resample(settings['historyBinning']).agg(ohlc_dict)
        df = drop_weekends(df)
                
        print_data(df, settings)        
        s = standard_style(settings)        
        
        #df.plot(y='IV (%)', use_index=True)
        # Super basic plot of the implied volatility over time. 
        
        kwargs = dict(type='candle', volume=True)        
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),                
                datetime_format=' %m/%d',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Option Price ($)")
                
        
                
    else:
        print("No option trades during period.")
    
    return

    
# Make a candlestick plot of intraday data.
def plot_timesales(data, data_title, settings):    
    check_data_validity(data)

    ohlc = []
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

        df = df.resample(settings['timesalesBinning']).agg(ohlc_dict)
        df = drop_nonmarket_periods(df)
        print_data(df, settings)        

        s = standard_style(settings)                
        kwargs = dict(type='candle',volume=True)  
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),               
                datetime_format=' %m/%d %H:%M',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Option Price ($)")        
    else:
        print("No option trades during period.")
        
    return


# Check if the user wants to print the trade data and then print it.
def print_data(dataframe, settings):
    if (settings['shouldPrintData']):
        pd.set_option('display.max_rows', None)
        print(dataframe)


# Swap a date string from (MM-DD-YYYY) to (YYYY-MM-DD)
def invert_date(date_str):
    return date_str[5:] + '-' + date_str[:4]
    

# If there's only one trade in then it returns a dictionary instead of a list of dict
def check_data_validity(source):
    if (type(source) == type({})):
        print("Insufficient trade data. Printing all data and terminating Program.")
        print(source)
        exit()


# Drop-weekends from resampled data. Need to be careful about this if we resample to weekly/monthly.
def drop_weekends(dataframe):
    for index, row in dataframe.iterrows():
        day_num = index.to_pydatetime().weekday()
        if (day_num > 4): # weekend
            dataframe.drop(index, inplace=True)
    
    return dataframe


# Drop resampled periods for timesales data that falls outside of trading hours
def drop_nonmarket_periods(dataframe):
    for index, row in dataframe.iterrows():
        hours = index.to_pydatetime().hour
        minutes = index.to_pydatetime().minute
        day_num = index.to_pydatetime().weekday()

        if (day_num > 4): # weekend
            dataframe.drop(index, inplace=True)
        elif (hours >= 16):
            dataframe.drop(index, inplace=True)
        elif (hours == 9 and minutes < 30):
            dataframe.drop(index, inplace=True)
        elif (hours < 9):
            dataframe.drop(index, inplace=True)
    
    return dataframe
    
    
# Standardized plot style between the two plot types
def standard_style(settings):
    return mpf.make_mpf_style(base_mpf_style='yahoo', 
                              rc={'font.size':10,
                                  'font.weight':'light',
                                  'axes.edgecolor':'black',
                                  'figure.figsize':(8.0, 4.8)
                                  }, 
                              y_on_right=False,
                              facecolor='w',
                              gridstyle=settings['gridstyle']
                              )



## Full control over style, the issue is you need to do all of it. Can't just do part of it. 
## This is done inside of mpf.make_mpf_style.
#                                marketcolors = {'candle': {'up': 'None', 'down': 'None'},
#                                                'edge': {'up': 'g', 'down': 'r'},
#                                                'wick': {'up': 'k', 'down': 'k'},
#                                                'ohlc': {'up': 'k', 'down': 'k'},
#                                                'volume': {'up': '#1f77b4', 'down': '#1f77b4'},
#                                                'vcedge': {'up': '#1f77b4', 'down': '#1f77b4'},
#                                                'vcdopcod': False,
#                                                'alpha': 0.9,
#                                                },
#                                marketcolors  = {'candle'  : {'up':'w', 'down':'#0095ff'},
#                                                 'edge'    : {'up':'w', 'down':'#0095ff'}},


## For watermarking. Set returnfig=True and return fig, axes = mpf.plot(...)
#      waterstr = 'Watermark'
#      props = dict(boxstyle='square', 
#                    facecolor='none', 
#                    alpha=0, 
#                    edgecolor='none')
#       labelfont = {'fontname':'DejaVu Sans', 'fontsize':40, 'color':'r', 'alpha':0.20}
#       axes[0].text(0.20, 0.65, waterstr, 
#                   transform=axes[0].transAxes, 
#                   bbox=props, 
#                   **labelfont)
#       fig.savefig('watermark_demo.png')

