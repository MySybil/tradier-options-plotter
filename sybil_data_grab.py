#sybil_data_grab.py
# Script Created by Teddy Rowan for MySybil.com
# Last Modified January 1, 2020
# Description: This script handles all the data grabbing for run_plotter.py 


import sybil_data_ui_helper
import tradier_parser # for sentinel check.
import requests
import time

# Verify that the ticker is valid and grab/print some daily trade info for the underlying.
def background_info(ticker, api_key):
    price_response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': ticker},
        headers={'Authorization': api_key, 'Accept': 'application/json'}
    )
    price_json = price_response.json()
    try:
        quote = price_json['quotes']['quote']
    except KeyError:
        print("Could not find data for symbol: (" + ticker + "). Terminating program."); exit()
    sybil_data_ui_helper.print_sleep(1)
    print("You have selected " + quote['description'] + " (" + quote['symbol'] + ").")
    print("The Daily Price Range [low/high] is: $ [" + str(quote['low']) + " / " + str(quote['high']) + "]")
    print("The Last Trade Price was: $" + str(quote['last']) + " and Today's Volume is: " + '{:,.0f}'.format(quote['volume']))
    if (float(quote['change_percentage']) >= 0):
        print("The Stock Price is UP +" + str(quote['change_percentage']) + "% on the day.")
    else:
        print("The Stock Price is DOWN " + str(quote['change_percentage']) + "% on the day.")

# Does the user want to look at call options or put options.
def option_type(symbol):
    sybil_data_ui_helper.print_sleep(1)
    input_str = input("Type C for Calls or P for Puts: "); input_str = input_str.upper()
    check_input_for_sentinel(input_str)
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
    
    return dates_list

def modify_settings(settings):
    sybil_data_ui_helper.print_sleep(3)
    print("The following runtime settings of this program can be modified.")
    print(settings)
    
    status = ""
    while (status.lower() != "done"):
        print("Type 'done' to return to program execution.")
        print("*"); time.sleep(0.05)
        status = input("Which setting would you like to change: ")
        tradier_parser.check_input_for_sentinel(status)
        if (status.lower() == "darkmode"):
            settings['darkMode'] = not settings['darkMode'];
        if (status.lower() == "watermark"):
            settings['watermark'] = not settings['watermark'];
        if (status.lower() == "grid"):
            settings['grid'] = not settings['grid'];
        if (status.lower() == "shouldprintdata"):
            settings['shouldPrintData'] = not settings['shouldPrintData'];
        
        # branding / historyLimit / binning need additional user inputs
        if (status.lower() == "binning"):
            new_bin = input("Please input your desired binning (1/5/15 min): ")
            tradier_parser.check_input_for_sentinel(new_bin)
            if (int(new_bin) == 1 or int(new_bin) == 5 or int(new_bin) == 15):
                settings['binning'] = int(new_bin)
            else:
                print("Invalid input. Binning remains unmodified.")
        
        if (status.lower() == "historylimit"):
            new_lim = input("Please input your desired day limit to transition to daily data (<35): ")
            tradier_parser.check_input_for_sentinel(new_lim)
            try:
                settings['historyLimit'] = int(new_lim)
            except ValueError:
                print("Invalid input. History limit remains unmodified.")        
        
        if (status.lower() == "branding"):
            new_brand = input("Please input your desired branding: ")
            tradier_parser.check_input_for_sentinel(new_brand)
            settings['branding'] = new_brand
        
        
        sybil_data_ui_helper.print_sleep(3)
        print("The runtime settings are now currently:")
        print(settings)
        
    sybil_data_ui_helper.print_sleep(3)
    return settings
    
# Check all user inputs for "exit" to see if they want to terminate the program
def check_input_for_sentinel(input):
    if (input == "exit"):
        print("User Requested Program Termination.")
        exit()
