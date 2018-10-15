import math
from scipy.stats import norm #norm.cdf(x) # cool

# Binary-Search algorithm to backsolve implied-volatility in the BS-Model. Bases IV on the midpoint of the bid/ask spread.
# Usually takes about 15 loops, so I haven't bothered to optimize away from Binary-Search (not sure what you folks will be doing)
def calculateIV(spotPrice, strike, years, div, midpoint, RFR, isCall):
    tolerance = 0.001 # Option price tolerance in $. Usually << compared to spread, 0.001 is overkill
    difference = tolerance + 1 # anything > tolerance to start, to push int while loop
    
    # Min IV and Max Possible IV.
    knownMin = 0        # IV has to be above 0
    knownMax = 10.0     # cut in half right away -- valid for IV up to 500%.
    IVGuess = knownMax
    
    # This is off by a pretty large bit if not very close to ATM. Need to adjust the rest as well if I choose to use it.
    #double IVApprox = sqrt(2*M_PI/years_to_expiry)*midpoint/strike;
    #NSLog(@"initial iv approx: %.2f %%", IVApprox*100); //
    
    iterations = 0
    
    while (abs(difference) > tolerance):
        if (difference > 0): # IV Guess too high
            knownMax = IVGuess
            IVGuess = (knownMin + knownMax)/2
        else:
            knownMin = IVGuess
            IVGuess = (knownMin + knownMax)/2
        
        d1 = (math.log(spotPrice/strike) + years*(RFR-div+(IVGuess*IVGuess)/2))/(IVGuess*math.sqrt(years))
        d2 = d1 - IVGuess*math.sqrt(years)
        
        if isCall:
            val = spotPrice*math.exp(-div*years)*norm.cdf(d1) - strike*math.exp(-RFR*years)*norm.cdf(d2)
        else:
            val = strike*math.exp(-RFR*years)*norm.cdf(-d2) - spotPrice*math.exp(-div*years)*norm.cdf(-d1)
        
        difference = val - midpoint
        
        # testing
        #print("IVGuess: " + str(IVGuess))
        #print("value: " + str(val))
        
        # With low liquidity options, the midpoint can sometimes be less than intrinsic value, in this case I flag the option so I know that the IV is sketchy, but I would still prefer to have a value so I run calculateIV() again but with the ask price substituted for the midpoint.
        if (IVGuess < 0.001):
            print("IV < 0.1 %.") # Probably deep ITM / OTM, maybe issues with spread
            return 0
        
        iterations += 1
        if (iterations > 100): # Legacy that I don't think ever hits anymore.
            print("Shit is broken. IV calc max iterations hit. Return 0")
            return 0
    
    return IVGuess


## test1
## expected output: 20%. real: 19.897%
aa = calculateIV(14, 13, 0.5, 0.03, 1.34, 0.03, 1) #call example
print("IV: " + str(aa*100) + " %. Expected output: 20.0%")
## expected output: 20%. real: 20.081%
bb = calculateIV(14, 13, 0.5, 0.03, 0.36, 0.03, 0) #put version
print("IV: " + str(bb*100) + " %. Expected output: 20.0%")

## test2 -- CGC Jan 18, 2019 35C. $21.55 midpoint w/ IV 81.15 %. output: 81.21%
aa2 = calculateIV(55.18, 35, 94/365.24, 0.00, 21.54, 0.02, 1) #call example
print("IV: " + str(aa2*100) + " %. Expected output: 81.15%")
bb2 = calculateIV(55.18, 35, 94/365.24, 0.00, 1.18, 0.02, 0) #put version. output: 81.21%
print("IV: " + str(bb2*100) + " %. Expected output: 81.15%")