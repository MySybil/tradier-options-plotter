import requests
import parser_options_full
import time
#runs with python3

# Written by Teddy Rowan
# This script prompts the user for a symbol, expiry date, and history range of interest and prints out all the options trades for the underlying symbol for that expiry date. Useful for monitoring abnormal options activity and identifying large positions after the fact. 


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
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}

# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
parser_options_full.parse_multi_quote(rDates.content.decode("utf-8"), "date")

# Prompt the user to pick one of the expiry dates
date = input("Select an expiry date from the list above: ")
type(date)


# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = parser_options_full.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")

# Format the price strings to the standard Tradier price format
updatedList = []
for price in strikeList:
    print(price)

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

# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2019



# Iterate through the list of strikes and get the volume and vwap for each contract
for price in updatedList:
    url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=" + symbol + format_date + optionType + price + "&interval=15min&start=" + startDate
    if (optionType == "C"):
        print("Now grabbing " + symbol + " calls dated: " + date + " w/ price: " + price)
    else:
        print("Now grabbing " + symbol + " puts dated: " + date + " w/ price: " + price)
    
    rData = requests.get(url, headers=my_headers)
    parser_options_full.parse_data_quote(rData.content.decode("utf-8"))
    time.sleep(1) #sleep for a second so that the requests come back in the proper order


