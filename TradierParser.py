# need to create a class and then import it and save this to it.

def parseQuote(data):
    print(type(data))
    
    #bleh = "there is a <symbol> hidden in here"
    #print(bleh.find('<symbol>'))
    
    # issue is that data isn't a string...
    print(data.find('<symbol>'))

    start = data.find("<symbol>") + 8 # 8 for length of <symbol>
    end = data.find("</symbol>")
    
    symbol = data[start:end]
    print("Symbol:" + symbol)
    
    #print(data)