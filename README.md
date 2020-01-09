# MySybil Historic Options Data

This set of scripts aims to provide anyone who wants it free access to historic options trade data. Whether you use this simply to view option prices over time, or as a starting point to build from, my main hope is that it saves you time and provides you with a level of independence from your broker and any major websites that aim to make money off of you.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Required Python Modules:
```
requests
time
datetime
mpl_finance
matplotlib
```

### Installation

Clone the repository, make sure that you have all the dependencies installed, then run with Python3 "driver_sybil_data.py"

As a quick example, run the script and the first prompt should be to "Type 'settings' or enter a symbol to proceed: "

```
Enter: SPY
```

You'll be prompted to enter either calls or puts.

```
Select call options by entering: C
```

The script will download a list of all available options dates and prompt you to enter one.
```
Enter: 2021-01-15
```

You'll be prompted to select a strike.
```
Enter: 325
```

You'll be prompted for the earliest trade data you want to look at:
```
Enter: 2019-01-01
```

The program should download all the data and then display a candlestick chart of the daily trade data.


## Additional Notes

There is an API key hard-coded into the script, it's totally cool for you to use this while deciding if you want to continue to use this script or not, but there is rate-limiting on it and the potential for that to become a problem. If you do plan to use this script frequently or build on-top of it, please head over to developer.tradier.com and sign up for free for an account and get your own API key.

## Authors

* **Teddy Rowan** @  MySybil.com

## Acknowledgments

* I would like to thank Tradier for providing free access to their sandbox API to get free historic options quotes.
