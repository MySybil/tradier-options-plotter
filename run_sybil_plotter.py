"""
run_sybil_plotter.py
Last Modified: October 7, 2020
Description: This script is designed as a free and open-source tool to help retail investors get 
and analyze historic options data.
"""

import tp_plot_manager as tpm #formerly pm
import tp_request_manager as trm #formerly sdg
import tp_settings as tps
import tp_ui_manager as tpu # formerly sui


tpu.intro_screen();
settings = tps.get_settings()
symbol = input("Enter a symbol to proceed: ").upper()

description = trm.background_info(symbol, settings['API_KEY']) 
option_type = trm.option_type(symbol)
settings['type'] = option_type
date_list   = trm.get_expiry_dates(symbol, settings['API_KEY']) 

date = input("Select an expiry date from the list above: ")
if (date not in date_list):
    print("The date: " + date + " is not valid. Terminating Program.")
    exit()

settings['expiry'] = date
# Save the expiry date for options calculations.

format_date = date.replace("-", "")[2:len(date.replace("-", ""))]
# Format the date string for Tradier's API formatting (strip dashes then strip 20 off the front of 2021)

strike_list = trm.get_strike_list(symbol, 
                                  date, 
                                  settings['API_KEY'])

selected_price = input("Select a strike from the list above: ")
if not (float(selected_price) in strike_list):
    print("No strike available for input price. Terminating Program.")
    exit()

settings['strike'] = selected_price
# Save the strike price for option calculations later.

selected_price = '{0:08d}'.format(int(float(selected_price)*1000)) 
# Format the price string for Tradier

start_date, should_use_history_endpoint = trm.get_start_date(int(settings['historyLimit']))
# Prompt user for date range and figure out which data type they're looking for.

option_symbol = symbol + format_date + option_type + selected_price 
# Full Tradier-formatted symbol for the option

data_name = symbol + " $" + str(float(selected_price)/1000) + option_type + " (" + date + ")"
# Plot title

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

# Make a candlestick plot of the option trade data
tpm.plot_data(trade_data, 
              underlying_data,
              should_use_history_endpoint, 
              data_name, 
              settings)
    
print("Program Reached End Of Execution.")
