"""
tp_settings.py
Last Modified: October 6, 2020
Description: This script handles the run-time settings for MySybil's tradier-options-plotter. 
Modify them here and they will apply to bother run_sybil_plotter.py and closed_option_driver.py
"""

def get_settings():
    settings_dict = {'API_KEY'          : 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj',
                    # Communal API key, use to demo the scripts but please get your own for continued use. 
                    # Sign up for free @ developer.tradier.com
                    
                    'shouldPrintData'   : True,
                    # True/False
                    # Do you want the data logged to the command line right before it is plotted?

                    'historyLimit'      : 10,
                    # Integer from 1 to 40
                    # The crossover limit (in days) between intraday versus daily data. 

                    'gridstyle'         : '--',
                    #'--' or '-' or 'None'
                    # Grid-style for the plots.
                    
                    'tight_layout'      : False,
                    # True/False
                    # Minimize white-space surrounding the figure and bring the title inside the bounds of the plot.

                    'historyBinning'    : '1D',
                    # '1D' or '7D' or '3D' or etc. Untested support for 1W / 1M / etc.
                    # The data binning for non-intraday plots.
                    
                    'timesalesBinning'  : '1min',
                    # '1min' or '5min' or '15min' or '60min'.
                    # The data binning for intraday plots.
                    
                    'downloadBinning'   : 1,
                    # '1' or '5' or '15' (minutes)
                    # The binning to download intraday data (not to plot, the data is resampled to your choosing later).
                    # Keep this at 1 (minute) unless you're downloading intraday data going back further than 20 days or stressing the API.
                    
                    'rfr'               : 0.002
                    # Float in the 0.001 to 0.05 range depending on treasury rates and interval time.
                    # The risk-free-rate for dealing with options in decimal. 
                }
    
    # Validate the settings
    if (settings_dict['historyLimit'] > 40):
        print("WARNING: historyLimit larger than intraday data support from Tradier API. Reducing to 40 days.")
        settings_dict['historyLimit'] = 40
    
    if (settings_dict['historyLimit'] > 20 and settings_dict['downloadBinning'] < 5):
        print("WARNING: Download binning interval too small for historyLimit. Increasing binning to 5min")
        settings_dict['downloadBinning'] = 5
    
    if not (type(settings_dict['shouldPrintData']) == bool):
        print("WARNING: Invalid input for shouldPrintData. Required <type> boolean. Setting equal True.")
        settings_dict['shouldPrintData'] = True
    
    if not (type(settings_dict['tight_layout']) == bool):
        print("WARNING: Invalid input for tight_layout. Required <type> boolean. Setting equal False.")
        settings_dict['tight_layout'] = False


    # TODO: validate historyBinning
    # TODO: validate timesalesBinning
    # TODO: validate downloadBinning
    
    return settings_dict