"""
sybil_data_ui_helper.py
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