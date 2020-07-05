#sybil_data_grab.py
# Author: MySybil.com
# Last Modified January 8, 2020
# Description: This script handles all the data grabbing / formatting for driver_sybil_data.py 

import sybil_data_ui_helper
import requests
import time
from datetime import datetime

# Verify that the ticker is valid and grab/print some daily trade info for the underlying.
def background_info(ticker, api_key):
    price_response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': ticker},
        headers={'Authorization': api_key, 'Accept': 'application/json'}
    )
    if (price_response.status_code == 401): # only need to check here, key cannot be changed after this call.
        print("Invalid API Key. Terminating Program."); exit()
    price_json = price_response.json()
    try:
        quote = price_json['quotes']['quote']
    except KeyError:
        print("Could not find data for symbol: (" + ticker + "). Terminating program."); exit()

    print_quote_info(quote) # print information about the daily trading range.
    return quote['description'] # return the full name of the company for plots and whatnot

# Print background info about the company / daily trading range.
def print_quote_info(quote):
    sybil_data_ui_helper.print_sleep(1)
    print("You have selected " + quote['description'] + " (" + quote['symbol'] + ").")
    print("The Daily Price Range [low/high] is: $ [" + str(quote['low']) + " / " + str(quote['high']) + "]")
    print("The Last Trade Price was: $" + str(quote['last']) + " and Today's Volume is: " + '{:,.0f}'.format(quote['volume']))
    if (float(quote['change_percentage']) >= 0):
        print("The Stock Price is UP +" + str(quote['change_percentage']) + "% on the day.")
    else:
        print("The Stock Price is DOWN " + str(quote['change_percentage']) + "% on the day.")
    return

# Does the user want to look at call options or put options.
def option_type(symbol):
    sybil_data_ui_helper.print_sleep(1)
    input_str = input("Type C for Calls or P for Puts: ").upper(); check_sentinel(input_str)
    if (input_str == "C"):
        print("Selected Call Options for " + symbol)
    elif (input_str == "P"):
        print("Selected Put Options for " + symbol)
    else:
        print("Invalid option type input. Terminating program."); exit()
    
    return input_str

# Download and print a list of all available expiry dates for options for the symbol
def get_expiry_dates(ticker, api_key):
    dates_response = requests.get('https://sandbox.tradier.com/v1/markets/options/expirations?',
        params={'symbol': ticker},
        headers={'Authorization': api_key, 'Accept': 'application/json'}
    )
    dates_json = dates_response.json()
    dates_list = dates_json['expirations']['date']
    
    if (len(dates_list)):
        print(dates_list)
    else:
        print("No options available for symbol: " +  ticker + ". Terminating Program."); exit()
    
    sybil_data_ui_helper.print_sleep(1)
    return dates_list

# Download and print a list of all available strikes for the expiry date.
def get_strike_list(ticker, expiry, api_key):
    strike_list_response = requests.get('https://sandbox.tradier.com/v1/markets/options/strikes?',
        params={'symbol': ticker, 'expiration': expiry},
        headers={'Authorization': api_key, 'Accept': 'application/json'}
    )
    strikes_json = strike_list_response.json()
    strikeList = strikes_json['strikes']['strike']
    print("List of available strike prices: ")
    print(strikeList)
    
    return strikeList

# Prompt the user for the earliest date in which they want to get data for, then determine whether to retrieve /history/ or /timesales/ data.
def get_start_date(history_limit):
    start_date = input("Input a start date for the data range (YYYY-mm-dd): "); check_sentinel(start_date)
    try:
        start_datenum = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Terminating Program."); exit()

    start_date_seconds = time.mktime(start_datenum.timetuple())
    current_time_seconds = time.mktime(datetime.now().timetuple()) #seconds since the input date

    should_use_history_endpoint = False
    if (current_time_seconds - start_date_seconds > history_limit*24*60*60):
        should_use_history_endpoint = True

    return start_date, should_use_history_endpoint

# Get a timeseries of all the trade data.
def get_trade_data(option_symbol, start_date, binning, should_use_history_endpoint, api_key):
    if(should_use_history_endpoint):
        trade_data_response = requests.get('https://sandbox.tradier.com/v1/markets/history?',
            params={'symbol': option_symbol, 'start': start_date},
            headers={'Authorization': api_key, 'Accept': 'application/json'}
        )
        trade_data_json = trade_data_response.json()
        return(trade_data_json['history']['day'])
    else:
        trade_data_response = requests.get('https://sandbox.tradier.com/v1/markets/timesales?',
            params={'symbol': option_symbol, 'start': start_date, 'interval':(str(int(binning))+"min")},
            headers={'Authorization': api_key, 'Accept': 'application/json'}
        )
        trade_data_json = trade_data_response.json()
        return (trade_data_json['series']['data'])


# Allow the user to modify the settings for the program at runtime.
def modify_settings(settings):
    sybil_data_ui_helper.print_sleep(3)
    print("The following runtime settings of this program can be modified.")
    print(settings)
    
    status = ""
    while (status.lower() != "done"):
        print("Type 'done' to return to program execution."); print("*"); time.sleep(0.05)
        status = input("Which setting would you like to change: "); check_sentinel(status)
        
        # Boolean settings just get flipped if the user wants to modify them.
        if (status.lower() == "darkmode"):
            settings['darkMode'] = not settings['darkMode'];
        if (status.lower() == "watermark"):
            settings['watermark'] = not settings['watermark'];
        if (status.lower() == "grid"):
            settings['grid'] = not settings['grid'];
        if (status.lower() == "shouldprintdata"):
            settings['shouldPrintData'] = not settings['shouldPrintData'];
        
        # Non-boolean settings modifications require additional inputs.
        if (status.lower() == "binning"):
            new_bin = input("Please input your desired binning (1/5/15 min): "); check_sentinel(new_bin)
            if (int(new_bin) == 1 or int(new_bin) == 5 or int(new_bin) == 15):
                settings['binning'] = int(new_bin)
            else:
                print("Invalid input. Binning remains unmodified.")
        
        if (status.lower() == "historylimit"):
            new_lim = input("Please input your desired day limit to transition to daily data (<35): "); check_sentinel(new_lim)
            try:
                settings['historyLimit'] = int(new_lim)
            except ValueError:
                print("Invalid input. History limit remains unmodified.")        
        
        if (status.lower() == "branding"):
            new_brand = input("Please input your desired branding: "); check_sentinel(new_brand)
            settings['branding'] = new_brand
        
        
        if (status.lower() == "api_key"):
            new_key = input("Please input an API_KEY (ie: Bearer xx...xx): "); check_sentinel(new_key)
            settings['API_KEY'] = new_key
        
        
        sybil_data_ui_helper.print_sleep(3)
        print("The runtime settings are now currently:")
        print(settings)
        
    sybil_data_ui_helper.print_sleep(3)
    return settings
    
# Check all user inputs for "exit" to see if they want to terminate the program
def check_sentinel(input):
    if (input.lower() == "exit"):
        print("User Requested Program Termination.")
        exit()
