import sys
import classes as cl
import math as m

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
        try:
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
        except KeyError:
            print("Thay is an invalid collection name, returning to collection menu...")
        except Exception as v:
            print(v)
            print("An error occurred, returning to collection menu...")


def plotting_portal(my_data):
    loop_break = False
    while not loop_break:
        choice = int(input('Collection portal:\n\t'
                           '1. Plot two collections\n\t'
                           '2. Perform linear regression\n\t'
                           '3. Perform exponential regression\n\t'
                           '4. Back to main menu\n'))
        try:
            match choice:
                case 1:
                    print(my_data)
                    n1 = input("Enter the name of the independant variable collection.\n")
                    n2 = input("Enter the name of the dependant variable collection\n")
                    p = cl.CartPlot(my_data.collection_dictionary[n1], my_data.collection_dictionary[n2])

                    p.default_plot()
                case 2:
                    print(my_data)
                    n1 = input("Enter the name of the independant variable collection.\n")
                    n2 = input("Enter the name of the dependant variable collection\n")
                    r = cl.LinReg(my_data.collection_dictionary[n1], my_data.collection_dictionary[n2])
                    r.calc_reg()

                    choice = input("Would you like to input expected values for a regression?\n"
                                   "For yes type 'yes'. For no type anything.\n")

                    if choice == 'yes':
                        r.usr_reg()
                        r.MSE_to_usr_def()

                    r.default_plot()
                case 3:
                    print(my_data)
                    n1 = input("Enter the name of the independant variable collection.\n")
                    n2 = input("Enter the name of the dependant variable collection\n")
                    expr = cl.ExpReg(my_data.collection_dictionary[n1], my_data.collection_dictionary[n2])
                    expr.calc_reg()

                    choice = input("Would you like to input expected values for a regression?\n"
                                   "For yes type 'yes'. For no type anything.\n")

                    if choice == 'yes':
                        expr.usr_reg()
                        expr.MSE_to_usr_def()

                    expr.default_plot()

                case 4:
                    loop_break = True
                case _:
                    print("That is not a valid input. Try again.")
        except KeyError:
            print("That is an invalid collection name, returning to plotting menu...")
        except Exception as v:
            print(v)
            print("An error occurred, returning to plotting menu...")


def import_portal(my_data):
    """
    TODO Add ability to import specific columns.
    :param my_data:
    :return:
    """
    input_file = input("Enter the path to the file.\n")
    read_from_file(my_data, input_file)


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


def read_from_file(my_data, f='data/sample_data.csv', fxn=None):
    if fxn != None:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'rt', newline='', encoding='utf-8-sig') as data_file:
                fxn()
        else:
            with open(f, 'rt', newline='', encoding='utf-8-sig') as data_file:
                fxn()
    else:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'rt', newline='', encoding='utf-8-sig') as data_file:
                my_data.auto_import(data_file)
        else:
            with open(f, 'rt', newline='', encoding='utf-8-sig') as data_file:
                my_data.auto_import(data_file)

def round_sig(x, sig=4):
    try:
        return round(x, sig - int(m.floor(m.log10(abs(x)))) - 1)
    except Exception as v:
        print(x, " could not be converted due to ", v, ".")
        return x

