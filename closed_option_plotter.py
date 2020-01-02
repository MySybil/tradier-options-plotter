import requests
#import tradier_parser
import time
from datetime import datetime
#runs with python3

# TODO: this needs a giant refactor to match up with the updated version of run_plotter.py
# In fact, I'm about to delete tradier_parser so it will soon be unable to run in its current state.

print("This code is deprecated as of January 2, 2020 commit #82.")
print("Now terminating program."); exit()
return # just in case ...?


API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj'
my_headers = {'Authorization': API_KEY}

settings = {'shouldPrintData' : False, 
            'darkMode' : True, 
            'branding' : True, 
            'binning' : 15} #need to implement binning options.



print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("********************#*********************************************")
print(" ")
print("   Welcome To MySybil's (expired) Historic Options Data Plotter")
print(" ")
print("**************************#***************************************")
print("* This program assumes you already know the date and strikes you want.")
print("* Created by Teddy Rowan at MySybil.com")
print("* Type 'exit' at any time to terminate program.")
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)



# Prompt the user for the underlying symbol of interest
print("*\n*"); time.sleep(0.05)
symbol = input("Select an underlying symbol: ")
type(symbol)
tradier_parser.check_input_for_sentinel(symbol)
symbol = symbol.upper() #only for display on plots reasons.

# Display the last trade price for the underlying.
uPrice = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol
rPrice = requests.get(uPrice, headers=my_headers)
lastPrice = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "last")
print("The last trade price for " + symbol + " was: $"+ lastPrice[0])

# Does the user want to look at call options or put options
print("*\n*"); time.sleep(0.05)
optionType = input("Type C for Calls or P for Puts: ")
type(optionType)
optionType = optionType.upper()
tradier_parser.check_input_for_sentinel(optionType)

if (optionType == "C"):
    print("Selected Call Options for " + symbol)
else:
    if (optionType == "P"):
        print("Selected Put Options for " + symbol)
    else:
        print("Invalid selection. Terminating program.")
        exit()
        
        
# Prompt the user to pick one of the expiry dates
date = input("Input the expiry date of the options in YYYY-mm-dd: ")
type(date)


selectedPrice = input("Input the strike of interest: ")
type(selectedPrice)

# Tradier Formatting is lolz
# Tradier Formatting is lolz and terrible
tmp = int(float(selectedPrice)*1000)
selectedPrice = '{0:08d}'.format(tmp)


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range (YYYY-mm-dd): ")
type(startDate)
tradier_parser.check_input_for_sentinel(startDate)


# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2019

# Find out how far back the user wants to look and if it's more than 35 days, use the history endpoint insteal of the timesales endpoint
try:
    datenum = datetime.strptime(startDate, "%Y-%m-%d")
except ValueError:
        print("Invalid date format. Terminating Program.")
        exit()
startDateTime = time.mktime(datenum.timetuple())
nowTime = time.mktime(datetime.now().timetuple())

shouldRunHistory = False # should we use the history endpoint.
if (nowTime - startDateTime > 35*24*60*60): # if it's been more than 35 days, plot daily data
    shouldRunHistory = True


# Too lazy to take this out of a for-loop. Legacy from when it did multiple options.
if (shouldRunHistory):
    url = "https://sandbox.tradier.com/v1/markets/history?symbol=" + symbol + format_date + optionType + selectedPrice + "&start=" + startDate
else:
    url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=" + symbol + format_date + optionType + selectedPrice + "&interval=15min&start=" + startDate

data_name = ""
if (optionType == "C"):
    data_name = symbol + " Calls Expiring: " + date + " w/ Strike: $" + str(float(selectedPrice)/1000)
    print("Now grabbing " + data_name)
else:
    data_name = symbol + " Puts Expiring: " + date + " w/ Strike: $" + str(float(selectedPrice)/1000)
    print("Now grabbing " + data_name)

rData = requests.get(url, headers=my_headers) #actually download the data
if (settings['shouldPrintData']):
    print(rData.text)
    
if (shouldRunHistory):
    tradier_parser.parse_history_quote(rData.content.decode("utf-8"), data_name, settings)
else:
    tradier_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name, settings)


