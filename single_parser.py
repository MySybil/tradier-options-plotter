import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

class TradierQuote():
  symbol = "" # can't have empty classes

#timestamp is seconds since 1970
# if you want the data parsed in text, in parse_data_quote uncomment print(vars(quote))

# going to need to timestamp swap it myself by calculating how many periods there are and backsolving that shit.

# ughh there's some bug where data is showing up with negative binning. maybe time zone dependent?


# Takes API Response from Tradier /quotes? with multiple quotes then substrings down to a single quote and parses them individually
def parse_data_quote(data):
    vTimestamp = []
    vVwap = []
    ohlc = []
    t1 = 0 #first timestamp
    data_min = 1000000
    data_max = 0
    t_last = 0;
    
    while data.find("</data>") != -1:
        single_quote = parse_target(data, "data") #substrings down to a full single quote
        quote = parse_single_quote(single_quote) #
        #print(vars(quote)) # print the variables # too much data now. makes no sense to print it all.
        if (t1 == 0):
            #print(quote.timestamp)
            t1 = quote.timestamp
            t1diff = t1 % 24*60*60 # seconds into the day for first trade.
            #print(t1diff)
            #t1 = t1 - t1diff + 13.5*60*60 # to get to 9.30am. should this be 9.5 or 13.5?
            #print(t1)
            # why the fuck is the first time at 9.30am w/ mod. leaps day or some shit.
            t1 = t1 - t1diff
            
        
        t_last = convert_timestamp(quote.timestamp, 15*60, t1)
        
        append_me = t_last, quote.open, quote.high, quote.low, quote.close, quote.volume
        ohlc.append(append_me)
        
        if (quote.low < data_min):
            data_min = quote.low
        if (quote.high > data_max):
            data_max = quote.high
        
        vVwap.append(quote.vwap)
        vTimestamp.append(convert_timestamp(quote.timestamp, 15*60, t1))
        
        
        
        # once the data is grabbed, move on to the next quote
        index = data.find("</data>")
        data = data[index+len("</data>"):]
        
    if (len(ohlc)):
        fig = plt.figure()
        ax1 = plt.subplot2grid((1,1), (0,0))
        ax1.grid(False)
        candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        # need to figure out the conversion from time to mdates
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

        plt.ylabel("Option Price ($)")
        plt.xlabel("Binning Periods Since First Data Point (To Be Fixed)")
        plt.subplots_adjust(left=0.10, bottom=0.20, right=0.95, top=0.90, wspace=0.2, hspace=0)
        #plt.hold(True)
        plt.plot(vTimestamp, vVwap, 'b--', alpha=0.25, Linewidth=1.0)
        
        plt.ylim(top=data_max*1.1)
        plt.ylim(bottom=data_min*0.9)
        
        # get min/max of previous data. constrain boundaries. iterate from t1 to last and plot a vertical line from min to max for each one. 
        ii = -0.5 # be inbetween data points.
        while (ii < t_last):
            plt.plot([ii, ii], [data_min*0.9, data_max*1.1], 'k-', Linewidth=1.0, alpha=0.35)
            ii += 6.5*60*60/(15*60) + 1 #15*60 is the binning
        
        plt.show()
    else:
        print("No option trades during period.")
      
# this should at least put it to 1 per then just need to scale and shit or something
def convert_timestamp(timestamp, binning, t0):
    # this will give the zero-origin binning period of the data point
    tconvert = (timestamp-t0)/binning 
    
    # need to remove the after hours data points. so calculate how many first
    tdays = (int)(tconvert/(24*60*60/binning))
    
    # now remove the appropriate number of after hours binnings
    tadjust = tconvert - tdays*(17.5*60*60/binning - 1) # w/out -1 it was doubling up a data point on the day crossover. double negative. 
    
    return tadjust # ok perfect (well perfectly awful)
        
        
def parse_multi_quote(data, tag):
    dateList = []
    while data.find("</" + tag + ">") != -1:
        single_quote = parse_target(data, tag) #substrings down to a full single quote
        #print(single_quote) # this is what prints the dates
        dateList.append(single_quote)
        
        # once the data is grabbed, move on to the next quote
        index = data.find("</" + tag + ">")
        data = data[index+len("</" + tag + ">"):]        

    print(dateList)
    
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
    
    targetList = ["time", "timestamp", "volume", "vwap", "high", "low", "open", "close"]    
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