# run_plotter.py ## driver_sybil_data.py
# Created by: Teddy Rowan @ MySybil.com
# Last Modified: January 1, 2020
# Description: This script is designed as a free and open-source tool to help retail investors get and analyze historic options data.

import requests
import time
from datetime import datetime

import tradier_parser
import sybil_data_ui_helper
import sybil_data_grab
import sybil_data_plot_master

# TODO: ReadME / instructions on git for how to use/run the script

def check_sentinel(input): # Check if the user wants to exit the program everytime they input anything
    if (input == "exit"): print("User Requested Program Termination."); exit()


API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.
my_headers = {'Authorization': API_KEY} # Tradier Authorization Header

# Settings can also be modified at runtime (non-persistent)
settings = {'shouldPrintData' : False, 
            'darkMode'  : True, 
            'watermark' : False, 
            'branding'  : "MySybil.com",
            'grid'      : True,
            'historyLimit' : 10,             #when we switch form /timesales to /history endpoint(days)
            'binning'   : 15}               #1/5/15 for time/sales. (time/sales < 35 days.)

# Start of code.
sybil_data_ui_helper.intro_screen(); # just some printing / instructions to introduce the program

symbol = input("Type 'settings' or enter a symbol to proceed: "); check_sentinel(symbol)
if (symbol.lower() == "settings"): # Does the user want to change the settings
    settings = sybil_data_grab.modify_settings(settings)    
    symbol = input("Enter a symbol to proceed: "); check_sentinel(symbol)

symbol = symbol.upper() # Formatting for plot titles and co.


description = sybil_data_grab.background_info(symbol, API_KEY) # Display some info about the underlying
optionType = sybil_data_grab.option_type(symbol) # Does the user want to look at call options or put options
dateList = sybil_data_grab.get_expiry_dates(symbol, API_KEY)

# Prompt the user to pick one of the expiry dates
date = input("Select an expiry date from the list above: "); check_sentinel(date)
if (date not in dateList):
    print("The date: " + date + " is not valid. Terminating Program."); exit()

# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2020


strikeList = sybil_data_grab.get_strike_list(symbol, date, API_KEY)
selectedPrice = input("Select a strike from the list above: "); check_sentinel(selectedPrice)
if not (float(selectedPrice) in strikeList):
    print("No strike available for input price. Terminating Program."); exit()

selectedPrice = '{0:08d}'.format(int(float(selectedPrice)*1000)) #format the price string for Tradier
startDate, should_use_history_endpoint = sybil_data_grab.get_start_date(int(settings['historyLimit']))
option_symbol = symbol + format_date + optionType + selectedPrice #full Tradier-formatted symbol for the option

data_name = symbol + " $" + str(float(selectedPrice)/1000)  + " Put Data Expiring " + date
if (optionType == "C"):
    data_name = symbol + " $" + str(float(selectedPrice)/1000)  + " Call Data Expiring " + date
print("Now grabbing " + data_name)


# good data is as expected. need to verify with plot_master. 
trade_data = sybil_data_grab.get_trade_data(option_symbol, startDate, settings['binning'], should_use_history_endpoint, API_KEY)
sybil_data_plot_master.plot_data(trade_data, should_use_history_endpoint, data_name, settings)

if (settings['shouldPrintData']):
    print(trade_data)
    
print("Program Reached End Of Execution."); exit()
