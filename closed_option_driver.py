"""
closed_option_driver.py
Last Modified: August 5, 2020
Description: This script is the sister script to run_sybil_plotter.py and works for options
 that have already expired. The catch is that you need to already know all the info about the
 options since we can't fetch a list of past expiry dates or strikes available on a given date.
"""

import tp_plot_manager as tpm #formerly pm
import tp_request_manager as trm #formerly sdg
import tp_settings as tps
import tp_ui_manager as tpu # formerly sui



tpu.intro_screen(); # just some printing / instructions to introduce the program
settings    = tps.get_settings()
symbol      = input("Enter a symbol to proceed: ").upper()
option_type = input("Select calls [c] or puts [p]: ").upper()
settings['type'] = option_type

# Prompt the user to pick one of the expiry dates (no list display due to prior expiry)
date = input("Input the expiry date of the options in [YYYY-mm-dd]: ")
settings['expiry'] = date

# Format the date string for Tradier's API formatting (strip dashes then strip 20 off the front of 2021)
format_date = date.replace("-", "")[2:len(date.replace("-", ""))]

selected_price = input("Input the strike price of the option: ")
settings['strike'] = selected_price

# Format the price string for Tradier
selected_price = '{0:08d}'.format(int(float(selected_price)*1000)) 
# Prompt user for date range
start_date, should_use_history_endpoint = trm.get_start_date(int(settings['historyLimit']))
# Full Tradier-formatted symbol for the option
option_symbol = symbol + format_date + option_type + selected_price 
# Plot title
data_name = symbol + " $" + str(float(selected_price)/1000) + option_type + " (" + date + ")"

split_ratio = input("Enter the size of the stock split [0 if no split]: ")
# Was there a stock split between the period of the option data and now. 

# Download the trade data and plot it
print("Now downloading trade data for: " + data_name)
trade_data = trm.get_trade_data(option_symbol, 
                                start_date, 
                                settings['downloadBinning'], 
                                should_use_history_endpoint, 
                                settings['API_KEY'])

# Let's get data on the underlying and then match it up and calculate the IV at every point.
underlying_data = trm.get_underlying_data(symbol,
                                          start_date, 
                                          settings['downloadBinning'], 
                                          should_use_history_endpoint, 
                                          settings['API_KEY'])

# If there was a stock split, adjust the share price to account and keep IV calculation accurate. 
underlying_data = tpu.stock_split_adjustment(float(split_ratio),
                                             underlying_data)

tpm.plot_data(trade_data, 
             underlying_data,
             should_use_history_endpoint, 
             data_name, 
             settings)
    
print("Program Reached End Of Execution.")