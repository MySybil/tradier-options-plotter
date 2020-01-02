#sybil_data_grab.py
# Script Created by Teddy Rowan for MySybil.com
# Last Modified January 1, 2020
# Description: This script handles all the data grabbing for run_plotter.py 


import sybil_data_ui_helper
import tradier_parser # for sentinel check.
import requests

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
    
    
    
# Check all user inputs for "exit" to see if they want to terminate the program
def check_input_for_sentinel(input):
    if (input == "exit"):
        print("User Requested Program Termination.")
        exit()
