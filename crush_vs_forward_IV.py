# this is going to be a test for how accurate forward IV is to measure IV crush

# choose a stock, let's say AAPL then maybe do NFLX / FB after, we grab the historic option prices then calculate the forward IV after earnings then look at the move after earnings and see how things turned out.

# it might be best to actually do this not in python but in MATLAB or something instead but py is probably fine. certainly for grabbing the data at least.

# steps
# 1: find earnings dates for AAPL
# 2: download historic options chains for 2-week period before earnings. ATM and probably a couple around there
# 3: download the stock data for the 2-weeks before and the 1-week after
# 4: match-up the stock data with the option data then calculate the IV going into earnings as well as the forward IV.
# 5: calculate the new IV after earnings with the new stock price and see how the crush compared to the expected crush via forward IV