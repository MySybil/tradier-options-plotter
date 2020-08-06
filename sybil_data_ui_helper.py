#sybil_data_ui_helper()
# Last Modified January 1, 2020
# Description: This script is just used to abstract uninteresting UI code that I don't want in the main codebase

import time

# just some printing / instructions to introduce the program
def intro_screen():
    print_sleep(2)
    print("*****************************************************************")
    print(" ")
    print("      Welcome To MySybil's Historic Options Data Plotter")
    print(" ")
    print("*****************************************************************")
    print_sleep(6)
    
def print_sleep(times):
    for i in range(times):
        print("*"); time.sleep(0.02)