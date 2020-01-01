#sybil_data_grab.py

import sybil_data_ui_helper
import tradier_parser # for sentinel check.

def option_type(symbol):
    sybil_data_ui_helper.print_sleep(1)
    input_str = input("Type C for Calls or P for Puts: "); input_str = input_str.upper()
    check_input_for_sentinel(input_str)
    if (input_str == "C"):
        print("Selected Call Options for " + symbol)
    elif (input_str == "P"):
        print("Selected Put Options for " + symbol)
    else:
        print("Invalid option type input. Terminating program."); exit()
    
    return input_str
    
    
    
# Check all user inputs for "exit" to see if they want to terminate the program
def check_input_for_sentinel(input):
    if (input == "exit"):
        print("User Requested Program Termination.")
        exit()
