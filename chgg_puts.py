import requests
import TradierParser
#runs with python3

#import pandas
#import numpy


# Dictionaries are now done with colons not commas.
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}

# Normal Quote
#url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=CHGG"

# Get options chains
#/v1/markets/options/chains
#/v1/markets/options/chains?symbol=msft&expiration=2013-06-07
#url = "https://sandbox.tradier.com/v1/markets/options/chains?symbol=CHGG&expiration=2019-05-17"

#Get options strikes
#/v1/markets/options/strikes
#https://api.tradier.com/v1/markets/options/strikes?symbol=msft&expiration=2013-06-07

#Time and Sales -- no good on past dates? need to go through /history?
#https://api.tradier.com/v1/markets/timesales?symbol=AAPL
url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=CHGG190418P00040000"

#History
url = "https://sandbox.tradier.com/v1/markets/history?symbol=CHGG190315P00040000"


r = requests.get(url, headers=my_headers)


# this doesn't handle timeouts or errors at all. deal with that.

#print(r.text)
#print (r.status_code)
#print (r.headers)
print (r.content)

# need to decode the data from bytes into a string.
#TradierParser.parse_single_quote(r.content.decode("utf-8")) # file name + function name
#TradierParser.parse_multi_quote(r.content.decode("utf-8")) # file name + function name

