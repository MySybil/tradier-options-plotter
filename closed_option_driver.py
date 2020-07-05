# closed_option_driver.py
# Author: MySybil.com
# Last Modified: January 2, 2020
# Description: This script is the sister script to driver_sybil_data.py and works for options that have already expired. The catch is that you need to already know all the info about the options since we can't fetch a list of past expiry dates or strikes available on a given date.

import sybil_data_ui_helper
import sybil_data_grab
import sybil_data_plot_master

# TODO: add back in support for stocks the don't trade anymore. (ie: YHOO). gets caught in the background_info call on line 36

def check_sentinel(input): # Check if the user wants to exit the program everytime they input anything
    if (input.lower() == "exit"): print("User Requested Program Termination."); exit()

API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.


# Settings can also be modified at runtime (non-persistent)
settings = {'shouldPrintData' : False, 
            'darkMode'  : True, 
            'watermark' : False, 
            'branding'  : "MySybil.com",
            'grid'      : True,
            'historyLimit' : 10,             #when we switch form /timesales to /history endpoint(days)
            'binning'   : 15}                #1/5/15 for time/sales. (time/sales < 35 days.)

# Start of code.
sybil_data_ui_helper.intro_screen(); # just some printing / instructions to introduce the program

symbol = input("Type 'settings' or enter a symbol to proceed: ").upper(); check_sentinel(symbol)
if (symbol.lower() == "settings"): # Does the user want to change the settings
    settings = sybil_data_grab.modify_settings(settings)    
    symbol = input("Enter a symbol to proceed: ").upper(); check_sentinel(symbol)


description = sybil_data_grab.background_info(symbol, API_KEY) # Display some info about the underlying
optionType = sybil_data_grab.option_type(symbol) # Does the user want to look at call options or put options


# Prompt the user to pick one of the expiry dates (no list display due to prior expiry)
date = input("Input the expiry date of the options in YYYY-mm-dd: "); check_sentinel(date)

# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2020

selectedPrice = input("Input the strike of interest: "); check_sentinel(selectedPrice)
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
