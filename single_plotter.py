import requests
import single_parser
import time
from datetime import datetime
#runs with python3

# Written by Teddy Rowan
# READ ME!!!!!!
# This script prompts the user for a symbol, expiry date, and history range of interest and plots the historic pricing for the selected option.
# The candlestick binning is 15 minutes if you're going back less than 35 days, or 1 day if you're going back further than 35 days. 
# There is no (?) error handling right now so be careful. 

# If you're just going to run it once or whatever this key is fine to use, but if you're going to run it a lot go and sign up for your own key. IT'S FREE, it takes 30 seconds.
# https://developer.tradier.com/user/sign_up
API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj'

print("-------")
print("-------")
print("HEY DOPE! There is no error-handling in this right now so try to be a grown-up and not fuck everything up.")
print("-------")
print("Also. If you're going to run this more than just to test it out, get your own API key. It's free for fucksake. And that way we don't hit rate-limiting.")
print("-------")


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
        print("Invalid input you fucking retard. I guess we're looking at calls.")
        optionType = "C"
        

# Tradier Authorization Header
my_headers = {'Authorization': API_KEY}

# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
single_parser.parse_multi_quote(rDates.content.decode("utf-8"), "date")

# Prompt the user to pick one of the expiry dates
date = input("Select an expiry date from the list above: ")
type(date)


# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = single_parser.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")

# Format the price strings to the standard Tradier price format
updatedList = []
print(strikeList)
#for price in strikeList:
#    print(price)

selectedPrice = input("Select a strike from the list above: ")
type(selectedPrice)

# Tradier Formatting is lolz
new = int(float(selectedPrice)*1000)
updatedList.append('{0:08d}'.format(new)) #edit courtesy: /u/Wallstreet_Fox


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range: ")
type(startDate)


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


# Too lazy to take this out of a for-loop. Legacy from when it did multiple options.
for price in updatedList:
    if (history):
        url = "https://sandbox.tradier.com/v1/markets/history?symbol=" + symbol + format_date + optionType + price + "&start=" + startDate
    else:
        url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=" + symbol + format_date + optionType + price + "&interval=15min&start=" + startDate

    data_name = ""
    if (optionType == "C"):
        data_name = symbol + " Calls Expiring: " + date + " w/ Strike: $" + str(float(price)/1000)
        print("Now grabbing " + data_name)
    else:
        data_name = symbol + " Puts Expiring: " + date + " w/ Strike: $" + str(float(price)/1000)
        print("Now grabbing " + data_name)
    
    rData = requests.get(url, headers=my_headers)
    
    if (history):
        single_parser.parse_history_quote(rData.content.decode("utf-8"), data_name)
    else:
        single_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name)



