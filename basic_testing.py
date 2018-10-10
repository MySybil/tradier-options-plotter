import requests
import TradierParser
#runs with python3

# NEWS API works.
#r = requests.get("https://newsapi.org/v2/everything?q=Apple&from=2018-09-25&sortBy=popularity&apiKey=4583ba3bea6c4524b08aa8eed9479b07")
#print (r.status_code)
#print (r.headers)
#print (r.content)


# Dictionaries are now done with colons not commas.
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}
#url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=MU"
url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=SPY190118C00300000"
r = requests.get(url, headers=my_headers)


#print(r.text)
#print (r.status_code)
#print (r.headers)
#print (r.content)

# need to decode the data from bytes into a string.
TradierParser.parse_quote(r.content.decode("utf-8")) # file name + function name

