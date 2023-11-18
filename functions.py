"""
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib as mp
"""
import sys
import classes as cl
import main

def collection_portal(my_data):

    loop_break = False
    while not loop_break:
        choice = int(input('Collection portal:\n\t'
                           '1. List all connections\n\t'
                           '2. Print a collection\n\t'
                           '3. Create new empty collection\n\t'
                           '4. Add two collections\n\t'
                           '5. Subtract two collections\n\t'
                           '6. Back to main menu\n'))
        match choice:
            case 1:
                print(my_data)
            case 2:
                print(my_data)
                name = input("What is the name of the collections who's values you would like to print?\n")
                referenced_object = my_data.collection_dictionary[name]
                print(referenced_object)
                print(referenced_object.print_values())
            case 3:
                name = input('What would you like the name of the new collection to be?\n')
                my_data.create_empty_collection(name)
                print(my_data.collection_dictionary[name])
            case 4:
                print(my_data)
                add_two_collections(my_data)
            case 5:
                print(my_data)
                subtract_two_collections(my_data)
            case 6:
                loop_break = True
            case _:
                print("That is not a valid input. Try again.")


def import_portal():
    pass


def add_two_collections(my_data):
    print('What are the names of the two collections you would like to add.\n'
          'Hit enter after inputting the first collection name.'
          'The sum \nwill be created as a new collection.\n')
    collection1 = input()
    collection2 = input()
    new_collection = my_data.collection_dictionary[collection1] + my_data.collection_dictionary[collection2]
    new_collection_name = input('What would you like the new collection to be named.')
    new_collection.name = new_collection_name
    my_data.add_collection(new_collection)
    print(new_collection)


def subtract_two_collections(my_data):
    print('What are the names of the two collections you would like to subtract.'
          'Hit enter after inputting the first collection name.'
          'The difference will be created as a new collection.\n')
    collection1 = input()
    collection2 = input()
    new_collection = my_data[collection1] - my_data[collection2]
    new_collection_name = input('What would you like the new collection to be named.')
    new_collection.name = new_collection_name
    my_data.add_collection(new_collection)
    print(new_collection)

def read_from_file(my_data, fxn=None):
    if fxn != None:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'rt', newline='', encoding='utf-8') as data_file:
                fxn()
        else:
            with open('sample_data.csv', 'rt', newline='', encoding='utf-8') as data_file:
                fxn()
    else:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'rt', newline='', encoding='utf-8') as data_file:
                my_data.auto_import(data_file)
        else:
            with open('sample_data.csv', 'rt', newline='', encoding='utf-8') as data_file:
                my_data.auto_import(data_file)
