import requests
import single_parser
import time
from datetime import datetime
#runs with python3

# Created by Teddy Rowan
# READ ME!!!!!!
# This script prompts the user for a symbol, expiry date, and history range of interest and plots the historic pricing for the selected option.
# The candlestick binning is 15 minutes if you're going back less than 35 days, or 1 day if you're going back further than 35 days. 
# There is no (?) error handling right now so be careful. 

API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.

my_headers = {'Authorization': API_KEY} # Tradier Authorization Header

# TODO: Validate user inputs
# TODO: Check API response for error messages. 
# TODO: Verbose / Data print settings / binning settings. Just throw a prompt at the start asking if the user wants to run the standard version or a modified one.

# For later
# TODO: Add volume line plot below candles
# TODO: Add technical indicators like moving averages, etc. 


print(" ")
print(" ")
print("*********************************************************")
print("*********************************************************")
print("****** WELCOME TO A HISTORIC OPTIONS DATA PLOTTER *******")
print("*********************************************************")
print("*********************************************************")
print(" ")
print("There is no error-handling in this right now so try to be a grown-up and not fuck everything up.")
print("--")
print(" ")

# Prompt the user for the underlying symbol of interest
symbol = input("Select an underlying symbol (that's a stock ticker retard): ")
type(symbol)

# Does the user want to look at call options or put options
optionType = input("Type C for Calls or P for Puts: ")
type(optionType)

if (optionType == "C"):
    print("Selected Call Options for " + symbol)
else:
    if (optionType == "P"):
        print("Selected Put Options for " + symbol)
    else:
        #exit() #let's try to keep the user going a bit.
        optionType = "C"
        


# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
single_parser.parse_multi_quote(rDates.content.decode("utf-8"), "date")

# TODO: Error Handling for no option dates. Should probably move the printing of the dates back into this script instead of having it in the parser.

# Prompt the user to pick one of the expiry dates
date = input("Select an expiry date from the list above: ")
type(date)

# TODO: Check whether the input date is in the list of dates. issue is that parser doesn't return the list right now, just prints it.

# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = single_parser.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")
print(strikeList)

selectedPrice = input("Select a strike from the list above: ")
type(selectedPrice)

if not (selectedPrice in strikeList or str(selectedPrice + ".0") in strikeList):
    print("How hard is it to pick a strike from the list...? Fuck me.")
    selectedPrice = strikeList[(int)(len(strikeList)/2)] #pick the middle strike.
    print("I guess I'm choosing for you... Strike = $ " + selectedPrice)
    
# Tradier Formatting is lolz and terrible
tmp = int(float(selectedPrice)*1000)
selectedPrice = '{0:08d}'.format(tmp)


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range (YYYY-mm-dd): ")
type(startDate)

# TODO: Error handling. Make sure that the start date is valid.


# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2019

# Find out how far back the user wants to look and if it's more than 35 days, use the history endpoint insteal of the timesales endpoint
datenum = datetime.strptime(startDate, "%Y-%m-%d")
startDateTime = time.mktime(datenum.timetuple())
nowTime = time.mktime(datetime.now().timetuple())

history = 0 # should we use the history endpoint.
if (nowTime - startDateTime > 35*24*60*60): # if it's been more than 35 days, plot daily data
    history = 1


# Set either a /history/ or a /timesales/ url
if (history):
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
print(rData.text)

# parse and plot the data
if (history):
    single_parser.parse_history_quote(rData.content.decode("utf-8"), data_name)
else:
    single_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name)



