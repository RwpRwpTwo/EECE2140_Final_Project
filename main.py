"""
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib as mp
"""
import classes as cl
import functions as fn

# Main function
def main():
    my_data = cl.MasterData()

    fn.read_from_file(my_data)
    loop_break = False
    while not loop_break:
        usr_choice = int(input('What would you like to do?\n\t'
                               '1. Work with collections\n\t'
                               '2. Plot & Perform Regressions\n\t'
                               '3. Import data\n\t'
                               '4. Exit the program\n'))
        match usr_choice:
            case 1:
                fn.collection_portal(my_data)
            case 2:
                fn.plotting_portal(my_data)
            case 3:
                fn.import_portal(my_data)

            case 4:
                loop_break = True
            case _:
                print("That is not a valid input. Try again.")


# Function call for main.
if __name__ == '__main__':
    main()
