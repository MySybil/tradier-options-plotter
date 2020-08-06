# run_sybil_plotter.py
# Last Modified: August 5, 2020
# Description: This script is designed as a free and open-source tool to help retail investors get and analyze historic options data.

import sybil_data_grab as sdg
import sybil_data_plot_master as pm
import sybil_data_ui_helper as sui
import sybil_data_settings

# BUG:  why do i need to resize the figures to get them to show properly

sui.intro_screen();
settings = sybil_data_settings.get_settings()
symbol = input("Enter a symbol to proceed: ").upper()

description = sdg.background_info(symbol, settings['API_KEY']) 
option_type = sdg.option_type(symbol)
date_list   = sdg.get_expiry_dates(symbol, settings['API_KEY']) 

# Prompt the user to pick one of the expiry dates and validate the data
date = input("Select an expiry date from the list above: ")
if (date not in date_list):
    print("The date: " + date + " is not valid. Terminating Program.")
    exit()

# Format the date string for Tradier's API formatting (strip dashes then strip 20 off the front of 2021)
format_date = date.replace("-", "")[2:len(date.replace("-", ""))]

strike_list = sdg.get_strike_list(symbol, 
                                date, 
                                settings['API_KEY'])

selected_price = input("Select a strike from the list above: ")
if not (float(selected_price) in strike_list):
    print("No strike available for input price. Terminating Program.")
    exit()

# Format the price string for Tradier
selected_price = '{0:08d}'.format(int(float(selected_price)*1000)) 
# Prompt user for date range
start_date, should_use_history_endpoint = sdg.get_start_date(int(settings['historyLimit']))
# Full Tradier-formatted symbol for the option
option_symbol = symbol + format_date + option_type + selected_price 
# Plot title
data_name = symbol + " $" + str(float(selected_price)/1000) + option_type + " (" + date + ")"

# Download the trade data and plot it
print("Now downloading trade data for: " + data_name)
trade_data = sdg.get_trade_data(option_symbol, 
                                start_date, 
                                settings['downloadBinning'], 
                                should_use_history_endpoint, 
                                settings['API_KEY'])

pm.plot_data(trade_data, 
            should_use_history_endpoint, 
            data_name, 
            settings)
    
print("Program Reached End Of Execution.")
