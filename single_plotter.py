import requests
import single_parser
import time
from datetime import datetime
#runs with python3

# Written by Teddy Rowan
# This script prompts the user for a symbol, expiry date, and history range of interest and prints out all the options trades for the underlying symbol for that expiry date. Useful for monitoring abnormal options activity and identifying large positions after the fact. 

API_KEY = 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'

# need to also make it support further back dates. using history endpoint instead of timesales

# Prompt the user for the underlying symbol of interest
symbol = input("Select an underlying symbol: ")
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
        print("Invalid input")


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

# Tradier Formatting
new = int(float(selectedPrice)*1000)
if (new < 10000):
    updatedList.append("0000" + str(new))
elif (new < 100000):
    updatedList.append("000" + str(new))
elif (new < 1000000):
    updatedList.append("00" + str(new))
elif (new < 10000000):
    updatedList.append("0" + str(new))
else:
    updatedList.append(str(new))


# Prompt the user for how long of a history they are interested in
startDate = input("Input a start date for the data range: ")
type(startDate)


# I need to do like a date difference to find out how long it's been then figure out whether it should be timesales or history as the endpoint

# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2019

# how far back from now is the start date
datenum = datetime.strptime(startDate, "%Y-%m-%d")
startDateTime = time.mktime(datenum.timetuple())
nowTime = time.mktime(datetime.now().timetuple())


history = 0
if (nowTime - startDateTime > 35*24*60*60): # if it's been more than 35 days, plot daily data
    history = 1


# Iterate through the list of strikes and get the volume and vwap for each contract
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

    time.sleep(1) #sleep for a second so that the requests come back in the proper order


