# run_plotter.py
# Created by: Teddy Rowan @ MySybil.com
# Last Modified: January 1, 2020
# Description: This script is designed as a free and open-source tool to help retail investors get and analyze historic options data.

import requests
import time
from datetime import datetime

import tradier_parser # to be phased out by xml parsing
import sybil_data_ui_helper
import sybil_data_grab

# TODO: ReadME / instructions on git for how to use/run the script

# Check if the user wants to exit the program everytime they input anything
def check_sentinel(input):
    if (input == "exit"): print("User Requested Program Termination."); exit()


API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.
my_headers = {'Authorization': API_KEY} # Tradier Authorization Header

# Settings can also be modified at runtime (non-persistent)
settings = {'shouldPrintData' : False, 
            'darkMode'  : True, 
            'watermark' : False, 
            'branding'  : "MySybil.com",
            'grid'      : True,
            'historyLimit' : 1,            #when we switch form time/sales to /history
            'binning'   : 15}               #1/5/15 for time/sales. (time/sales < 35 days.)

sybil_data_ui_helper.intro_screen(); # just some printing / instructions to introduce the program
sybil_data_ui_helper.print_sleep(1)

symbol = input("Type 'settings' or enter a symbol to proceed: "); check_sentinel(symbol)
if (symbol.lower() == "settings"): # Does the user want to change the settings
    settings = sybil_data_grab.modify_settings(settings)    
    symbol = input("Enter a symbol to proceed: "); check_sentinel(symbol)

symbol = symbol.upper() # Formatting for plot titles and co.


sybil_data_grab.background_info(symbol, API_KEY) # Display some info about the underlying
optionType = sybil_data_grab.option_type(symbol) # Does the user want to look at call options or put options


# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
dateList = tradier_parser.parse_multi_quote(rDates.content.decode("utf-8"), "date")

if (len(dateList)):
    print(dateList)
else:
    print("No options available for symbol: " +  symbol + ". Terminating Program."); exit()
    

# Prompt the user to pick one of the expiry dates
sybil_data_ui_helper.print_sleep(1)
date = input("Select an expiry date from the list above: "); check_sentinel(date)

if (date not in dateList):
    print("The date: " + date + " is not valid. Terminating Program."); exit()


# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = tradier_parser.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")
print(strikeList)

selectedPrice = input("Select a strike from the list above: "); check_sentinel(selectedPrice)

if not (selectedPrice in strikeList or str(selectedPrice + ".0") in strikeList):
    print("No strike available for input price. Terminating Program."); exit()
    
        
# Tradier Formatting is lolz and terrible
tmp = int(float(selectedPrice)*1000)
selectedPrice = '{0:08d}'.format(tmp)


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range (YYYY-mm-dd): "); check_sentinel(startDate)


# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2019

# Find out how far back the user wants to look and if it's more than 35 days, use the history endpoint insteal of the timesales endpoint
try:
    datenum = datetime.strptime(startDate, "%Y-%m-%d")
except ValueError:
        print("Invalid date format. Terminating Program."); exit()

startDateTime = time.mktime(datenum.timetuple())
nowTime = time.mktime(datetime.now().timetuple()) #seconds since the input date

shouldRunHistory = False # should we use the /history/ or the /timesales/ endpoint
if (nowTime - startDateTime > int(settings['historyLimit'])*24*60*60):
    shouldRunHistory = True


# Set either a /history/ or a /timesales/ url
if (shouldRunHistory):
    url = "https://sandbox.tradier.com/v1/markets/history?symbol=" + symbol + format_date + optionType + selectedPrice + "&start=" + startDate
else:
    url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=" + symbol + format_date + optionType + selectedPrice + "&interval=" + str(int(settings['binning'])) + "min&start=" + startDate

data_name = "" # for plot titles
if (optionType == "C"):
    data_name = symbol + " $" + str(float(selectedPrice)/1000)  + " Strike Call Expiring " + date
else:
    data_name = symbol + " $" + str(float(selectedPrice)/1000)  + " Strike Put Expiring " + date

print("Now grabbing " + data_name)
rData = requests.get(url, headers=my_headers) #actually download the data

if (settings['shouldPrintData']):
    print(rData.text)

# parse and plot the data
if (shouldRunHistory):
    tradier_parser.parse_history_quote(rData.content.decode("utf-8"), data_name, settings)
else: #timesales instead
    tradier_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name, settings)


