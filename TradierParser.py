# need to create a class and then import it and save this to it.

# parsing:
#  symbol / description / type / last / change / change_percentage / volume / trade_date / open / high / low / close / prevclose

# not parsing (for now):
#  exch / average_volume / last_volume / week_52_low / week_52_high / bid / bidsize / bid_date / bidexch / ask / asksize / ask_date / askexch / root_symbols

def parseQuote(data):
    #print(type(data))
    #print(data)
    
    targetList = ["symbol", "description", "type", "last", "change", "change_percentage", "volume", "trade_date", "open", "high", "low", "close", "prevclose"]
    
    for x in targetList:
      find_value(data, x)   
    
    
def find_value(source, target):
    start = source.find("<" + target + ">") + len(target) + 2
    end = source.find("</" + target + ">")
    value = source[start:end]
    print(target + ": " + value)
    