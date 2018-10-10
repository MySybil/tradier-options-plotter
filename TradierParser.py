class TradierQuote():
  symbol = "" # can't have empty classes


# Takes API Response from Tradier /quotes? with multiple quotes then substrings down to a single quote and parses them individually
def parse_multi_quote(data):
    while data.find("</quote>") != -1:
        single_quote = parse_target(data, "quote") #substrings down to a full single quote
        quote = parse_single_quote(single_quote) #
        print(vars(quote)) # print the variables

        # once the data is grabbed, move on to the next quote
        index = data.find("</quote>")
        data = data[index+len("</quote>"):]
        

# Takes API Response from Tradier /quotes? endpoint and formats the desired data. Returns a TradierQuote() object with the data
def parse_single_quote(data):
    quote = TradierQuote()
    #print(type(data))
    #print(data)
    
    targetList = ["symbol", "description", "last", "change", "change_percentage", "volume", "trade_date", "open", "high", "low", "close", "prevclose", "bid", "bidsize", "ask", "asksize"]
    # not parsing (for now):
    #  exch / type / average_volume / last_volume / week_52_low / week_52_high / bid_date / bidexch / ask_date / askexch / root_symbols
    
    for target in targetList:
        y = parse_target(data, target)
        if is_number(y):
            setattr(quote, target, float(y))
        else:
            setattr(quote, target, y)
    
    return quote

    
    
# Takes in the source download from the Tradier API and searches + parses it for the target and returns the target as a string.
# Target demo: "symbol" to parse "<symbol>AAPL</symbol>"
def parse_target(source, target):
    start = source.find("<" + target + ">") + len(target) + 2
    end = source.find("</" + target + ">")
    value = source[start:end]
    
    return(value)
    ## this works but is a bit annoying b/c of types when printing after the value is returned.
    ## prefer to just leave it as a string for now
    #if is_number(value):
    #    return float(value)
    #else:
    #    return(value)
    

# Returns true if the input is a number, false if not. Used to differentiate between string and floats that get parsed b/c the floats that get parsed end up stored as strings    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False