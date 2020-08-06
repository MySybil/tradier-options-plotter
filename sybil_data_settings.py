# sybil_data_settings.py
# Last Modified: August 6, 2020
# Description: This script handles the run-time settings for MySybil's tradier-options-plotter. Modify them here and they will apply across the board. 

def get_settings():
    settings_dict = {'API_KEY'          : 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj', #public key
                    'shouldPrintData'   : True,           # Now prints dataframe 
                    'historyLimit'      : 10,             # when to switch form /timesales to /history endpoint(days)
                    'gridstyle'         : '--',           # '--' / '-' / 'None'
                    'tight_layout'      : False,          # tight vs normal layout for figures
                    'historyBinning'    : '1D',           # '1D' / '7D' / etc 
                    'timesalesBinning'  : '5min',         # '1min' / '5min' / '15min'            
                    'downloadBinning'   : 1}              # binning to download (not display) intraday data. keep at 1
    
    return settings_dict