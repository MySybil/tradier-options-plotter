import requests
import single_parser
import time
from datetime import datetime
#runs with python3

# The candlestick binning is 15 minutes if you're going back less than 35 days, or 1 day if you're going back further than 35 days. Make this tuneable. 

#API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.
my_headers = {'Authorization': API_KEY} # Tradier Authorization Header

# TODO: Check API response for error messages. 
# TODO: Verbose / Data print settings / binning settings. Just throw a prompt at the start asking if the user wants to run the standard version or a modified one.

# For later
# TODO: Add volume line plot below candles
# TODO: Add technical indicators like moving averages, etc. 

# Settings
shouldPrintData = False #True
#binning = 15
#settings = {shouldPrintData, binning}

print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*****************************************************************")
print(" ")
print("      Welcome To MySybil's Historic Options Data Plotter")
print(" ")
print("*****************************************************************")
print("Created by Teddy Rowan at MySybil.com")
print("Type 'exit' at any time to terminate program.")
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)


#TODO: let the user modify settings at runtime.
#print("*\n*"); time.sleep(0.05)
#shouldModifySettings = input("Type y/yes to modify program settings or enter to continue: ")
#type(shouldModifySettings)
#single_parser.check_input_for_sentinel(shouldModifySettings)
#if (shouldModifySettings.lower() == "y" or shouldModifySettings.lower() == "yes"):
    #print("user wants to modify settings.")
#    print("The Following Settings Can Be Modified: ")
#    print(settings)
#else:
#    print("Running with default settings.")



# Prompt the user for the underlying symbol of interest
print("*\n*"); time.sleep(0.05)
symbol = input("Select an underlying symbol: ")
type(symbol)
single_parser.check_input_for_sentinel(symbol)
symbol = symbol.upper() #only for display on plots reasons.

# Display the last trade price for the underlying.
uPrice = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol
rPrice = requests.get(uPrice, headers=my_headers)
lastPrice = single_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "last")
print("The last trade price for " + symbol + " was: $"+ lastPrice[0])

# Does the user want to look at call options or put options
print("*\n*"); time.sleep(0.05)
optionType = input("Type C for Calls or P for Puts: ")
type(optionType)
optionType = optionType.upper()
single_parser.check_input_for_sentinel(optionType)

if (optionType == "C"):
    print("Selected Call Options for " + symbol)
else:
    if (optionType == "P"):
        print("Selected Put Options for " + symbol)
    else:
        print("Invalid selection. Terminating program.")
        exit()
        


# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
dateList = single_parser.parse_multi_quote(rDates.content.decode("utf-8"), "date")

if (len(dateList)):
    print(dateList)
else:
    print("No options available for symbol: " +  symbol + ". Terminating Program.")
    exit()
    

# Prompt the user to pick one of the expiry dates
print("*\n*"); time.sleep(0.05)
date = input("Select an expiry date from the list above: ")
type(date)
single_parser.check_input_for_sentinel(date)

if (date not in dateList):
    print("The date: " + date + " is not valid. Terminating Program.")
    exit()


# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = single_parser.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")
print(strikeList)

selectedPrice = input("Select a strike from the list above: ")
type(selectedPrice)
single_parser.check_input_for_sentinel(selectedPrice)

if not (selectedPrice in strikeList or str(selectedPrice + ".0") in strikeList):
    print("No strike available for input price. Terminating Program.")
    exit()
    
        
# Tradier Formatting is lolz and terrible
tmp = int(float(selectedPrice)*1000)
selectedPrice = '{0:08d}'.format(tmp)


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range (YYYY-mm-dd): ")
type(startDate)
single_parser.check_input_for_sentinel(startDate)


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
nowTime = time.mktime(datetime.now().timetuple()) #seconds since the input date

shouldRunHistory = False # should we use the history endpoint.
if (nowTime - startDateTime > 35*24*60*60): # if it's been more than 35 days, plot daily data
    shouldRunHistory = True


# Set either a /history/ or a /timesales/ url
if (shouldRunHistory):
    url = "https://sandbox.tradier.com/v1/markets/history?symbol=" + symbol + format_date + optionType + selectedPrice + "&start=" + startDate
else:
    url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=" + symbol + format_date + optionType + selectedPrice + "&interval=15min&start=" + startDate

data_name = "" # for plot titles
if (optionType == "C"):
    data_name = symbol + " Calls Expiring: " + date + " w/ Strike: $" + str(float(selectedPrice)/1000)
    print("Now grabbing " + data_name)
else:
    data_name = symbol + " Puts Expiring: " + date + " w/ Strike: $" + str(float(selectedPrice)/1000)
    print("Now grabbing " + data_name)

rData = requests.get(url, headers=my_headers) #actually download the data

if (shouldPrintData):
    print(rData.text)

# parse and plot the data
if (shouldRunHistory):
    single_parser.parse_history_quote(rData.content.decode("utf-8"), data_name)
else:
    single_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name)


