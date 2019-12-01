import requests
import tradier_parser
import time
from datetime import datetime
#runs with python3

# Script Created by Teddy Rowan for MySybil.com
# Last Modified November 29, 2019

# TODO: ReadME / write script summary.

API_KEY = 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj' # public key.
my_headers = {'Authorization': API_KEY} # Tradier Authorization Header

# TODO: /history/ quote. support for daily/weekly/monthly binning.
# TODO: Add volume line plot below candles
# TODO: Add technical indicators like moving averages, etc. 
# TODO: make the day division pretty big. like linewidth 3. alpha 0.25. '--'

# TODO: I'm pretty sure the parser is set up to grab all the company info in one parse call but I need to actually look at it and remember how. 

# You can modify the settings at runtime but the changes aren't persistent, so if you want to permanently change the settings you should do it here. 
settings = {'shouldPrintData' : False, 
            'darkMode'  : True, 
            'watermark' : False, 
            'branding'  : "MySybil.com",
            'grid'      : True,
            'historyLimit' : 7,            #when we switch form time/sales to /history
            'binning'   : 15}               #1/5/15 for time/sales. (time/sales < 35 days.)

print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*****************************************************************")
print(" ")
print("      Welcome To MySybil's Historic Options Data Plotter")
print(" ")
print("*****************************************************************")
print("* Created by Teddy Rowan at MySybil.com")
print("* Type 'exit' at any time to terminate program.")
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)
print("*\n*"); time.sleep(0.05)


# Prompt the user for the underlying symbol of interest
print("*"); time.sleep(0.05)
symbol = input("Type 'settings' or enter a symbol to proceed: ")
type(symbol)
tradier_parser.check_input_for_sentinel(symbol)

if (symbol.lower() == "settings"):
    print("*"); time.sleep(0.05)
    print("*"); time.sleep(0.05)
    print("*"); time.sleep(0.05)
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
            type(new_bin)
            tradier_parser.check_input_for_sentinel(new_bin)
            if (int(new_bin) == 1 or int(new_bin) == 5 or int(new_bin) == 15):
                settings['binning'] = int(new_bin)
            else:
                print("Invalid input. Binning remains unmodified.")
        
        if (status.lower() == "historylimit"):
            new_lim = input("Please input your desired day limit to transition to daily data (<35): ")
            type(new_lim)
            tradier_parser.check_input_for_sentinel(new_lim)
            try:
                settings['historyLimit'] = int(new_lim)
            except ValueError:
                print("Invalid input. History limit remains unmodified.")        
        
        if (status.lower() == "branding"):
            new_brand = input("Please input your desired branding: ")
            type(new_brand)
            tradier_parser.check_input_for_sentinel(new_brand)
            settings['branding'] = new_brand
        
        
        print("*"); time.sleep(0.05)
        print("*"); time.sleep(0.05)
        print("*"); time.sleep(0.05)
        print("The runtime settings are now currently:")
        print(settings)

    print("*"); time.sleep(0.05)
    print("*"); time.sleep(0.05)
    print("*"); time.sleep(0.05)
    symbol = input("Enter a symbol to proceed: ") #need to get user to re-enter a symbol
    type(symbol)
    tradier_parser.check_input_for_sentinel(symbol)

symbol = symbol.upper() #only for display on plots reasons.

# Display the last trade price for the underlying.
uPrice = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol #url for request
rPrice = requests.get(uPrice, headers=my_headers) #make the request
company_name = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "description")
if (len(company_name) == 0): #check validity of symbol input
    print("Unable to locate company info for symbol: (" + symbol + "). Terminating program.")
    exit()
    
lastPrice = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "last")
lowPrice = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "low")
highPrice = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "high")
volume = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "volume")
volume[0] = '{:,.0f}'.format(int(volume[0])) #format w/ commas
change_perc = tradier_parser.parse_multi_quote(rPrice.content.decode("utf-8"), "change_percentage")
print("*"); time.sleep(0.05)
print("You have selected " + company_name[0] + " (" + symbol + ").")
print("The Daily Price Range [low/high] is: $ [" + lowPrice[0] + "," + highPrice[0] + "]")
print("The Last Trade Price was: $" + lastPrice[0] + " and Today's Volume is: " + volume[0])
if (float(change_perc[0]) >= 0):
    print("The Stock Price is UP +" + change_perc[0] + "% on the day.")
else:
    print("The Stock Price is DOWN " + change_perc[0] + "% on the day.")


# Does the user want to look at call options or put options
print("*"); time.sleep(0.05)
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
        


# Grab, parse, and print all the available expiry dates for the symbol.
url_dates = "https://sandbox.tradier.com/v1/markets/options/expirations?symbol=" + symbol
rDates = requests.get(url_dates, headers=my_headers)
dateList = tradier_parser.parse_multi_quote(rDates.content.decode("utf-8"), "date")

if (len(dateList)):
    print(dateList)
else:
    print("No options available for symbol: " +  symbol + ". Terminating Program.")
    exit()
    

# Prompt the user to pick one of the expiry dates
print("*"); time.sleep(0.05)
date = input("Select an expiry date from the list above: ")
type(date)
tradier_parser.check_input_for_sentinel(date)

if (date not in dateList):
    print("The date: " + date + " is not valid. Terminating Program.")
    exit()


# Grab a list of all the prices available, then parse and format them properly
url_strikes = "https://sandbox.tradier.com/v1/markets/options/strikes?symbol=" + symbol + "&expiration=" + date
rStrikes = requests.get(url_strikes, headers=my_headers)
strikeList = tradier_parser.parse_strikes(rStrikes.content.decode("utf-8"))

print("List of available strike prices: ")
print(strikeList)

selectedPrice = input("Select a strike from the list above: ")
type(selectedPrice)
tradier_parser.check_input_for_sentinel(selectedPrice)

if not (selectedPrice in strikeList or str(selectedPrice + ".0") in strikeList):
    print("No strike available for input price. Terminating Program.")
    exit()
    
        
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
else:
    tradier_parser.parse_timesales_quote(rData.content.decode("utf-8"), data_name, settings)


