import requests
import TradierParser
#runs with python3

# for some reason i can't get any function not to throw errors everywhere. standard me not knowing python..
#def my_function(fname):
#  print(fname + " Refsnes"
  #return


# NEWS API works.
#r = requests.get("https://newsapi.org/v2/everything?q=Apple&from=2018-09-25&sortBy=popularity&apiKey=4583ba3bea6c4524b08aa8eed9479b07")
#print (r.status_code)
#print (r.headers)
#print (r.content)


# Dictionaries are now done with colons not commas.
my_headers = {'Authorization': 'Bearer 5f1ga0KR0Ys1YlQhWtRAQAPKW8Iy'}
url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=MU"
r = requests.get(url, headers=my_headers)


#print(r.text)
#print (r.status_code)
#print (r.headers)
#print (r.content)

# need to decode the data from bytes into a string.
TradierParser.parseQuote(r.content.decode("utf-8")) # file name + function name

    
#my_function("blegsfs")
#return
    

