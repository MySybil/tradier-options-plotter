class TradierQuote():
  symbol = "" # can't have empty classes


# Takes API Response from Tradier /quotes? with multiple quotes then substrings down to a single quote and parses them individually

def parse_multi_quote(data):
    while data.find("</data>") != -1:
        single_quote = parse_target(data, "data") #substrings down to a full single quote
        quote = parse_single_quote(single_quote) #
        print(vars(quote)) # print the variables

        # once the data is grabbed, move on to the next quote
        index = data.find("</data>")
        data = data[index+len("</data>"):]
        
def parse_multi_quote(data, tag):
    while data.find("</" + tag + ">") != -1:
        single_quote = parse_target(data, tag) #substrings down to a full single quote
        print(single_quote)
        
        # once the data is grabbed, move on to the next quote
        index = data.find("</" + tag + ">")
        data = data[index+len("</" + tag + ">"):]
        
def parse_strikes(data):
    tag = "strike"
    targetList = [];
    while data.find("</" + tag + ">") != -1:
        single_quote = parse_target(data, tag) #substrings down to a full single quote
        #print(single_quote)
        
        targetList.append(single_quote) # how to do this properly
        
        # once the data is grabbed, move on to the next quote
        index = data.find("</" + tag + ">")
        data = data[index+len("</" + tag + ">"):]

    #print(targetList)
    return targetList
    

# Takes API Response from Tradier /quotes? endpoint and formats the desired data. Returns a TradierQuote() object with the data
def parse_single_quote(data):
    quote = TradierQuote()
    #print(type(data))
    #print(data)
    
    print(data)
    
    targetList = ["time", "timestamp", "volume", "vwap"]
    
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