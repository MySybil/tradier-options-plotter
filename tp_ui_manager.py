"""
tp_ui_manager.py
Last Modified: August 6, 2020
Description: Uninteresting UI code to support run_sybil_plotter.py

TODO: obviously the intro screen needs updating like crazy. low priority. 
"""

import time

def intro_screen():
    print_sleep(2)
    print("*****************************************************************\n ")
    print("      Welcome To MySybil's Historic Options Data Plotter\n ")
    print("*****************************************************************")
    print_sleep(6)

# Insert blank lines and slowly pause to create a loading effect and guide the user.
def print_sleep(times):
    for i in range(times):
        print("*")
        time.sleep(0.02)
        
        
# Adjust the underlying data for stock-splits if there was one.         
def stock_split_adjustment(ratio, underlying):
    if ratio == 0:
        return underlying

    new_list = []
    for entry in underlying:
        tmp_dict = {}
        tmp_dict['date'] = entry['date']
        tmp_dict['open'] = float(entry['open'])*ratio
        tmp_dict['high'] = float(entry['high'])*ratio
        tmp_dict['low'] = float(entry['low'])*ratio
        tmp_dict['close'] = float(entry['close'])*ratio
        tmp_dict['volume'] = float(entry['volume'])*ratio
        new_list.append(tmp_dict)
    
    return new_list
    
