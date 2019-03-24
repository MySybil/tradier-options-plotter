import requests
import TradierParser
#runs with python3

#import pandas
#import numpy


# Dictionaries are now done with colons not commas.
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}
url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=CHGG"
#url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=SPY190118C00300000,MU,AAPL"

r = requests.get(url, headers=my_headers)


# this doesn't handle timeouts or errors at all. deal with that.

print(r.text)
#print (r.status_code)
#print (r.headers)
#print (r.content)

# need to decode the data from bytes into a string.
#TradierParser.parse_single_quote(r.content.decode("utf-8")) # file name + function name
#TradierParser.parse_multi_quote(r.content.decode("utf-8")) # file name + function name

