"""
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib as mp
import csv
"""
import classes as cl
import functions as fn
import sys

# Main function
def main():
    my_data = cl.master_data

    fn.read_from_file(my_data)

    usr_choice = int(input('What would you like to do?\n\t'
                           '1. Import data\n\t'
                           '2. Work with collections\n'))
    match usr_choice:
        case 1:
            pass
        case 2:
            fn.collection_portal(my_data)
        case _:
            print("That is not a valid input. Try again.")
    print("Program executed")


# Function call for main.
if __name__ == '__main__':
    main()
