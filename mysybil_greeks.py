# mysybil_greeks.py
# Created by: MySybil.com
# Last Modified: October 6, 2020
# Description: Foundational code for options analysis

import math
from scipy.stats import norm
from trading_calendars import get_calendar 

class OptionAnalysis:
    """
    Object for estimating the implied volatility, calculating theoretical
    option prices and calculating the Greeks.

    Parameters
    ----------
    underlying_price : float
        The price of the stock underlying the option
    strike : float
        The strike price
    time_to_expiry : float
        The time remaining until the option expires in years
    dividend_yield : float
        The dividend yield (as a decimal, not percentage)
    opt_price : float
        The price of the option
    risk_free_rate : float
        The risk-free rate (as a decimal, not percentage)
    is_call : bool
        Whether the option is a call (if False, the option is a put)
    tolerance : float, optional, default: 1E-3
        The tolerance to use for estimating the implied volatility

    Attributes
    ----------
    self.up : float
    self.strike : float
    self.tte : float
    self.dy : float
    self.op : float
    self.rfr : float
    self.is_call : bool
    self.tol : float
    """
    def __init__(self, underlying_price, strike, time_to_expiry, dividend_yield,
                 opt_price, risk_free_rate, is_call, tolerance=1E-3):
        self.up = underlying_price
        self.strike = strike
        self.tte = time_to_expiry
        self.dy = dividend_yield
        self.op = opt_price
        self.rfr = risk_free_rate
        self.is_call = is_call
        self.tol = tolerance

    def _get_d(self, iv):
        d1 = ((math.log(self.up / self.strike) + self.tte
              * (self.rfr - self.dy + math.pow(iv, 2) / 2))
              / (iv * math.sqrt(self.tte)))
        d2 = d1 - iv * math.sqrt(self.tte)
        return d1, d2

    def get_option_value(self, implied_volatility):
        """Calculate the theoretical value of an option."""
        d1, d2 = self._get_d(implied_volatility)

        if self.is_call:
            opt_val = (self.up * math.exp(-self.dy * self.tte)
                       * norm.cdf(d1) - self.strike
                       * math.exp(-self.rfr * self.tte) * norm.cdf(d2)
            )
        else:
            opt_val = (self.strike * math.exp(-self.rfr * self.tte)
                       * norm.cdf(-d2) - self.up
                       * math.exp(-self.dy * self.tte) * norm.cdf(-d1)
            )
        return opt_val

    def get_market_year_fraction(self, start_date, end_date, adjustment):
        """Calculate the year fraction until the expiry date of an option in trading minutes.
      
        Parameters
        ----------
        start_date : string
            Inclusive start date for the time remaining [MM-DD-YYYY] ie: ('10-18-2020')
        end_date : string
            Inclusive end date for the time remaining [MM-DD-YYYY] ie: ('10-20-2020')
        adjustment : float
            [mins] An adjustment factor for handling intraday calculations 
        """
        mins = 390*len(get_calendar('XNYS').sessions_in_range(start_date, end_date)) + adjustment
        return mins/(252*390)

    def get_implied_volatility(self, max_iter=100):
        """Guess the implied volatility."""        
        known_min = 0
        known_max = 10.0
        iv_guess = (
            math.sqrt(2 * math.pi / self.tte) * (self.op / self.strike)
        )
        opt_val = self.get_option_value(iv_guess)
        diff = opt_val - self.op

        iterations = 0
        while abs(diff) > self.tol:
            if diff > 0:
                known_max = iv_guess
                iv_guess = (known_min + known_max) / 2
            else:
                known_min = iv_guess
                iv_guess = (known_min + known_max) / 2

            opt_val = self.get_option_value(iv_guess)
            diff = opt_val - self.op

            if iv_guess < 0.001:
                return 0

            iterations += 1
            if iterations > max_iter:
                print(f"Warning: Reached maximum number of iterations for "
                      + f"implied volatility guess for strike {self.strike}. "
                      + f"Returning 0...")
                return 0

        return iv_guess

    def get_greeks(self, implied_volatility):
        """Compute the Greeks."""
        T = 365.242199
        d1, d2 = self._get_d(implied_volatility)
        output = {"d1": d1, "d2": d2}
        output["gamma"] = (
            math.exp(-self.dy * self.tte)
            / (self.up * implied_volatility * math.sqrt(self.tte))
            * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
        )
        output["vega"] = (
            0.01 * self.up
            * math.exp(-self.dy * self.tte) * math.sqrt(self.tte)
            * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
        )

        if self.is_call:
            output["type"] = "call"
            output["delta"] = (
                math.exp(-self.dy * self.tte) * norm.cdf(d1)
            )
            output["theta"] = (
                1 / T * (
                    -(self.up * implied_volatility
                    * math.exp(-self.dy * self.tte) / (2 * math.sqrt(self.tte))
                    * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi))
                    - self.rfr * self.strike * math.exp(-self.rfr * self.tte)
                    * norm.cdf(d2) + self.dy * self.up
                    * math.exp(-self.dy * self.tte) * norm.cdf(d1)
                )
            )
            output["lambda"] = (
                self.up / self.op
                * math.exp(-self.dy * self.tte) * norm.cdf(d1)
            )
            output["rho"] = (
                0.01 * self.strike * self.tte
                * math.exp(-self.rfr * self.tte) * norm.cdf(d2)
            )
        else:
            output["type"] = "put"
            output["delta"] = (
                math.exp(-self.dy * self.tte) * (norm.cdf(d1) - 1)
            )
            output["theta"] = (
                1 / T * (
                    -(self.up * implied_volatility
                    * math.exp(-self.dy * self.tte) / (2 * math.sqrt(self.tte))
                    * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi))
                    - self.rfr * self.strike * math.exp(-self.rfr * self.tte)
                    * norm.cdf(-d2) + self.dy * self.up
                    * math.exp(-self.dy * self.tte) * norm.cdf(-d1)
                )
            )
            output["lambda"] = (
                -self.up / self.op
                * math.exp(-self.dy * self.tte) * norm.cdf(-d1)
            )
            output["rho"] = (
                -0.01 * self.strike * self.tte
                * math.exp(-self.rfr * self.tte) * norm.cdf(-d2)
            )

        return output
