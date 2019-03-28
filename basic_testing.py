import requests
import TradierParser
#runs with python3

#import pandas
#import numpy

# NEWS API works.
#r = requests.get("https://newsapi.org/v2/everything?q=Apple&from=2018-09-25&sortBy=popularity&apiKey=4583ba3bea6c4524b08aa8eed9479b07")
#print (r.status_code)
#print (r.headers)
#print (r.content)


# Want to try to figure out how to get quotes for Berkshire.
#url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=BRK.B"
# Response: unmatched_symbol

# Dictionaries are now done with colons not commas.
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}
#url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=SPX"
#url = "https://sandbox.tradier.com/v1/markets/timesales?symbol=CHGG&interval=15min&start=2019-03-18"
#url = "https://sandbox.tradier.com/v1/markets/history?symbol=CHGG&start=2019-03-10"
url = "https://sandbox.tradier.com/v1/markets/history?symbol=SPY&start=2019-03-10"

r = requests.get(url, headers=my_headers)


# this doesn't handle timeouts or errors at all. deal with that.

#print(r.text)
#print (r.status_code)
#print (r.headers)
#print (r.content)

# need to decode the data from bytes into a string.
#TradierParser.parse_single_quote(r.content.decode("utf-8")) # file name + function name
TradierParser.parse_multi_quote(r.content.decode("utf-8")) # file name + function name

