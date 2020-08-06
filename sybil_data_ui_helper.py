# sybil_data_ui_helper.py
# Last Modified: August 6, 2020
# Description: Uninteresting UI code to support run_sybil_plotter.py

import time

# Introduction screen for the scripts.
def intro_screen():
    print_sleep(2)
    print("*****************************************************************")
    print(" ")
    print("      Welcome To MySybil's Historic Options Data Plotter")
    print(" ")
    print("*****************************************************************")
    print_sleep(6)

# Insert blank lines and slowly pause to create a loading effect and guide the user.
def print_sleep(times):
    for i in range(times):
        print("*"); time.sleep(0.02)