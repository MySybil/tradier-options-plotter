"""
tp_plot_manager.py
Last Modified: October 8, 2020
Description: This script handles all the plotting for run_sybil_plotter.py

# mplfinance style documentation
# https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
"""

# General
# TODO: abstract the adj_time calculation from plot_timesales()
# TODO: clean up the volatility OHLC figures. 

# Scatterplot implied volatility
# TODO: get rid of seconds values in x-ticks in timesales plots
# TODO: make timesales ticks auto-updating on zoom. (try candles first)
# I need to change this into a convert xticks to xticklabel type thing.

from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import time

from mysybil_greeks import OptionAnalysis

# Are we plotting intraday or daily data?
def plot_data(data, underlying_data, should_use_history_endpoint, data_title, settings):
    if (should_use_history_endpoint):
        plot_history(data, 
                     underlying_data, 
                     data_title, 
                     settings)
    else:
        plot_timesales(data,
                       underlying_data,
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
    ohlc_iv = []
    for quote in data:
        quote_time = datetime.strptime(quote['date'], "%Y-%m-%d")
        iv = 0
        
        # Traverse the underlying data until we find the matching time period
        for underlying in ohlc_underlying:
            iv_close = 0
            if (quote_time == underlying[0]):
                trade_date = invert_date(quote['date'])
                expiry_date = invert_date(settings['expiry'])
        
                time_to_expiry = OptionAnalysis.get_market_year_fraction(trade_date, expiry_date, -1*390)
                # Find the year fraction of time remaining only looking at market minutes. (dates inclusive, so -390 (1day))
                
                sparta = OptionAnalysis(underlying[-2], float(settings['strike']), time_to_expiry, 0, quote['close'], settings['rfr'], settings['type'] == 'C')
                # Initialize the OptionAnalysis data [-2] is 'close'
                
                iv_open, iv_high, iv_low, iv_close = calculate_volatility_ohlc(sparta, quote, underlying)
                break
        
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume'], round(iv_close*100,2)
        ohlc.append(pandas_data)
        # Store the OHLC trade data

        if (iv_close):
            pandas_iv_data = quote_time, round(iv_open*100,2), round(iv_high*100,2), round(iv_low*100,2), round(iv_close*100,2), quote['volume']
            ohlc_iv.append(pandas_iv_data)
            # Store the OHLC implied volatility data

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
        # Resample and print the data

        #volatility_scatterplot(df, data_title)
        # Scatterplot of the implied volatility over time. 

        s = standard_style(settings)                
        kwargs = dict(type='candle', volume=True)        
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),                
                datetime_format=' %m/%d',
                tight_layout=settings['tight_layout'],
                block=False,
                ylabel="Option Price ($)")
                
    else:
        print("No option trades during period.")
        return
    
    # Candlestick-style implied volatility plot
    if (len(ohlc_iv)):
        df_iv = pd.DataFrame(ohlc_iv)
        df_iv.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df_iv = df_iv.set_index(pd.DatetimeIndex(df_iv['Date']))
        
        ohlc_iv_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }
        
        df_iv = df_iv.resample(settings['historyBinning']).agg(ohlc_iv_dict)
        df_iv = drop_weekends(df_iv)    
        # Resample the volatility data.
        
        s = volatility_style(settings)
        kwargs = dict(type='candle',volume=False)
        mpf.plot(df_iv, **kwargs, style=s, 
                mav=3,
                title=dict(title="\n\nImplied Volatility for " + data_title, weight='regular', size=11),               
                datetime_format=' %m/%d',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Implied Volatility (%)")        
    
    return

    
# Make a candlestick plot of intraday data.
def plot_timesales(data, underlying_data, data_title, settings):    
    check_data_validity(data)

    # ohlc for the underlying symbol. will use this to calculate IV
    ohlc_underlying = []
    for quote in underlying_data:
        quote_time = datetime.strptime(quote['time'], "%Y-%m-%dT%H:%M:%S")
        pandas_data = quote_time, quote['time'], quote['open'], quote['high'], quote['low'], quote['close'], quote['volume']
        ohlc_underlying.append(pandas_data)

    ohlc = []
    ohlc_iv = []
    for quote in data:
        quote_time = datetime.strptime(quote['time'], "%Y-%m-%dT%H:%M:%S")
        iv = 0
        
        for underlying in ohlc_underlying:
            iv_close = 0
            if (quote_time == underlying[0]):
                trade_date = invert_date(quote['time'][:10])
                expiry_date = invert_date(settings['expiry'])
                                
                adj_time = ((16-float(quote['time'][11:13]))*60 - float(quote['time'][14:16]))
                adj_time = (adj_time - 390*1) - int(settings['timesalesBinning'][:-3])
                # Adjust the time for intraday minutes.
                # Need to subtract binning b/c we're dealing with closes.
                # *2 seems to fit better w/ online data. I need to think about *1 vs *2
                
                time_to_expiry = OptionAnalysis.get_market_year_fraction(trade_date, expiry_date, adj_time)
                # Find the year fraction of time remaining only looking at market minutes. (dates inclusive, so -390 (1day))

                sparta = OptionAnalysis(underlying[-2], float(settings['strike']), time_to_expiry, 0, quote['close'], settings['rfr'], settings['type'] == 'C')
                # Initialize the OptionAnalysis data [-2] is 'close'
                
                iv_open, iv_high, iv_low, iv_close = calculate_volatility_ohlc(sparta, quote, underlying)
                # Calculate the volatility range for ohlc IV charts.
                
                break
                # Found corresponding data, no need to look further
            
        
        pandas_data = quote_time, quote['open'], quote['high'], quote['low'], quote['close'], quote['volume'], round(iv_close*100,2)
        ohlc.append(pandas_data)
        # Store the OHLC trade data
        
        if (iv_close):
            pandas_iv_data = quote_time, round(iv_open*100,2), round(iv_high*100,2), round(iv_low*100,2), round(iv_close*100,2), quote['volume']
            ohlc_iv.append(pandas_iv_data)
            # Store the OHLC implied volatility data

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

        df = df.resample(settings['timesalesBinning']).agg(ohlc_dict)
        df = drop_nonmarket_periods(df)
        print_data(df, settings)        
        # Resample and print the data

        #volatility_scatterplot(df, data_title)
        # Super basic plot of the implied volatility over time. 

        s = standard_style(settings)                
        kwargs = dict(type='candle',volume=True)  
        mpf.plot(df, **kwargs, style=s, 
                title=dict(title="\n\n" + data_title, weight='regular', size=11),               
                datetime_format=' %m/%d %H:%M',
                tight_layout=settings['tight_layout'],
                block=False, #False
                ylabel="Option Price ($)")        
             
    else:
        print("No option trades during period.")
        return
    
    # Candlestick-style implied volatility plot
    if (len(ohlc_iv)):
        df_iv = pd.DataFrame(ohlc_iv)
        df_iv.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df_iv = df_iv.set_index(pd.DatetimeIndex(df_iv['Date']))
        
        ohlc_iv_dict = {
            'Open':'first',
            'High':'max',
            'Low':'min',
            'Close':'last',
            'Volume':'sum'
        }
        
        df_iv = df_iv.resample(settings['timesalesBinning']).agg(ohlc_iv_dict)
        df_iv = drop_nonmarket_periods(df_iv)    
        # Resample the volatility data.
        
        s = volatility_style(settings)
        kwargs = dict(type='candle',volume=False)  
        mpf.plot(df_iv, **kwargs, style=s, 
                mav=3,
                title=dict(title="\n\nImplied Volatility for " + data_title, weight='regular', size=11),               
                datetime_format=' %m/%d %H:%M',
                tight_layout=settings['tight_layout'],
                block=True,
                ylabel="Implied Volatility (%)")        
    
    return


# Check if the user wants to print the trade data and then print it.
def print_data(dataframe, settings):
    if (settings['shouldPrintData']):
        pd.set_option('display.max_rows', None)
        print(dataframe)

# A simple scatterplot of the volatility data using only the 'close' datapoints
def volatility_scatterplot(my_df, title_str):
    plt.rcParams['figure.figsize'] = (8.0, 4.8)
    ax = my_df.plot(y='IV (%)', use_index=False, marker='s', markersize=3, linestyle='--', linewidth=0.5, alpha=0.75)
    
    labelfont = {'fontname':'DejaVu Sans', 'fontsize':9, 'weight':'light'}
    titlefont = {'fontname':'DejaVu Sans', 'fontsize':11, 'weight':'light'}
    
    tick_period = int(len(my_df.index)/7)
    # ajust the tick_period so we have a consistent amount of ticklabels on the plot
    
    ax.set_xticks(np.arange(len(my_df.index)/tick_period)*tick_period)
    ax.set_xticklabels(my_df.index[::tick_period], **labelfont)
    # Set the ticklabels as the index names. 
    
    ax.callbacks.connect('xlim_changed', on_xlims_change)
    #live update the xlabels TODO: implement this.
    
    plt.subplots_adjust(left=0.13, bottom=0.21, right=0.95, top=0.92, wspace=0.2, hspace=0)
    plt.ylabel('Implied Volatility (%)', **labelfont)
    plt.title('Implied Volatility for ' + title_str, **titlefont)
    plt.grid(which='major', color='#151515', linestyle='-', linewidth=0.50, alpha=0.75, zorder=1)    
    plt.minorticks_on()
    plt.grid(b=True,which='minor', color='#111111', linestyle='--', linewidth=0.50, alpha=0.3, zorder=0)
    
    plt.gca().xaxis.grid(which='both') 
    # horizontal lines only #ax = plt.gca()



# Calculate all the volatilities for the OHLC plot
def calculate_volatility_ohlc(option_data, quote_data, underlying_data):
    # Close-IV (Default)
    iv_close = option_data.get_implied_volatility()
    
    # Open-IV
    option_data.up = underlying_data[2]
    option_data.op = quote_data['open']
    iv_open = option_data.get_implied_volatility()
    
    # Max-IV
    if (option_data.is_call):
        option_data.up = underlying_data[4] #lowest underlying price
        # Max Call IV: low underlying price, high option price
    else:
        option_data.up = underlying_data[3] # highest underlying price
        # Max Put IV: high underlying price, high option price
    
    option_data.op = quote_data['high']
    iv_high = option_data.get_implied_volatility()

    # Min-IV
    if (option_data.is_call):
        option_data.up = underlying_data[3] #highest underlying price
        # Min Call IV: high underlying price, low option price
    else:
        option_data.up = underlying_data[4] #lowest underlying price
        # Min Put IV: low underlying price, low option price
    
    option_data.op = quote_data['low']
    iv_low = option_data.get_implied_volatility()

    return iv_open, iv_high, iv_low, iv_close


# Swap a date string from (MM-DD-YYYY) to (YYYY-MM-DD)
def invert_date(date_str):
    return date_str[5:] + '-' + date_str[:4]


# Whenever the plot is panned/zoomed, update the tick labels.
def on_xlims_change(axes):
    print("Dummy real-time update of xticklabels ()")
    ax1 = plt.gca()
    #print(ax1.get_xticks()) # [  0.  55. 110. 165. 220. 275. 330. 385.]
    # these are constant when pan/zooming. looks like i fucked them up earlier. 
    # if i remove set_xticks then they change properly but then the orig labels are fckd
    
    #ax1 = plt.gca()
    ##ax1.set_xticklabels(convert_xticks_to_dates(ax1.get_xticks(), ax.binning, plt.t1))
    #ax1.set_xticklabels(ax1.df.index[::ax1.tick_period])#, **labelfont)
    
    # need to do some sort of get_xticks. then convert. need to pass in the dataframe.
    #ax.tick_period = int(len(df.index)/7)
    #ax.datastore = df
    

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
    
    
# Standardized plot style between timesales and history trading plots
def standard_style(settings):
    return mpf.make_mpf_style(base_mpf_style='yahoo', 
                              rc={'font.size':9,
                                  'font.weight':'light',
                                  'axes.edgecolor':'black',
                                  'figure.figsize':(8.0, 4.8)
                                  }, 
                              y_on_right=False,
                              facecolor='w',
                              gridstyle=settings['gridstyle']
                              )


# Standardized plot style for the OHLC volatility plots
# https://github.com/matplotlib/mplfinance/tree/6cffdf1df8de3f3a7e8095ead68be00161688f2b/src/mplfinance/_styledata
def volatility_style(settings):
    return mpf.make_mpf_style(base_mpf_style='yahoo',
                              marketcolors = {#'candle': {'up': '#5555ff', 'down': '#5555ff'},
                                              #'edge': {'up': '#5555ff', 'down': '#5555ff'},
                                              'candle': {'up': '#55ccaa', 'down': '#cc55aa'},
                                              'edge': {'up': '#55ccaa', 'down': '#cc55aa'},
                                              'wick': {'up': '#bbbbff', 'down': '#bbbbff'},
                                              'ohlc': {'up': '#5555ff', 'down': '#5555ff'},
                                              'volume': {'up': '#1f77b4', 'down': '#1f77b4'},
                                              'vcedge': {'up': '#1f77b4', 'down': '#1f77b4'},
                                              'vcdopcod': False,
                                              'alpha': 0.75
                                              #'alpha': 0.50
                                              },
                              rc={'font.size':9,
                                  'font.weight':'light',
                                  #'axes.edgecolor':'black',
                                  'figure.figsize':(8.0, 4.8)
                                  },
                              y_on_right = False,
                              mavcolors = ['#000000'],
                              gridstyle = '--',
                              facecolor = 'w'
                              )
