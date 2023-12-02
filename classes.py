"""
import functions as fn
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib as mp
"""
import main
import csv


# TODO create class which performs and represents regressions


class MasterData:
    def __init__(self):
        self.collection_dictionary = {}

    def __str__(self):
        """
        Method to print all collections.
        """
        counter = 0
        return_string = ''
        for i in self.collection_dictionary:
            return_string += str(self.collection_dictionary[i])
            return_string += '|'
            if counter % 7 == 1:
                return_string += '\n'
        return return_string

    def create_empty_collection(self, name):
        """
        Creates a new collection which contains no data.
        :param name:
        :return:
        """
        new_collection = Collection(name)
        self.collection_dictionary[name] = new_collection

    def add_collection(self, new_collection):
        """
        Adds a collection to the master collection dictionary.
        :param new_collection:
        :return success or error message:
        """
        self.collection_dictionary[new_collection.name] = new_collection
        return 'Collection' + new_collection.name + 'added successfully'

    def remove_collection(self, collection_name):
        """
        Removes a collection from the master collection dictionary.
        :param collection_name:
        :return success or error message:
        """
        if collection_name in self.collection_dictionary:
            self.collection_dictionary.pop(collection_name)
            return collection_name.name + 'removed successfully.'
        else:
            return 'That is not a valid collection name.'

    def auto_import(self, file):
        """
        Method which will automatically import all the data from a csv.
        :param file object:
        :return:
        """
        new_collections = []
        reader = csv.reader(file, dialect='excel')

        # Corrects bug where "\ufeff" is included
        rows = [[c.replace('\ufeff', '') for c in row] for row in reader]

        rows = [r for r in rows]

        for i in rows[0]:
            new_collections.append(Collection(i))

        new_data = [list() for i in range(len(new_collections))]

        for i in range(1, len(rows)):
            for j in range(len(new_data)):
                new_data[j].append(rows[i][j])

        new_data = [[float(j) for j in i] for i in new_data]

        for i in range(len(new_collections)):
            new_collections[i].data = new_data[i]

        for i in new_collections:
            self.add_collection(i)


class Unit:
    prefixes = {'m': 10 ** (-3),
                'c': 10 ** (-2),
                'd': 10 ** (-1),
                'de': 10,
                'h': 10 ** 2,
                'k': 10 ** 3}

    def __init__(self, str):
        self.representation = str

    def __str__(self):
        return self.representation


class Collection:
    """
    A collection represents a list of data associated with a string value. In practice,
    this tends to be one variable being collected. In excel, a collection is defined as
    a column with a header that describes what the values in that column represent.
    The header must contain that columns' units in parenthesis after the name.
    """

    def __init__(self, name='New Collection', imported_data=[]):
        """
        Constructor for the collection class. Filters the header into the name and the unit
        of the collection. All other data is imported raw and unfiltered. If no name is
        provided in the function call, wil default the name to 'New Collection' as the
        dictionary requires a key. If no data is provided, will create an empty list to
        store potential data.
        :param name:
        :param imported_data:
        """

        # For loop to filter out name and unit
        if [i for i in name if i == '(']:
            name = name.split('(')
            new_unit = name[1][0]
            name = name[0].replace(' ', '')
            # name = name.replace('ufeff', '')
        else:
            new_unit = ''
        self.name = name  # string

        self.collect_unit = Unit(new_unit)  # unit class

        self.data = imported_data # list

        self.length = len(self.data)  # integer

    def __str__(self):
        """
        Function which creates the string representation for the collection class. Only returns
        the name and the unit. Neglcts the data itself.
        :return:
        """
        return self.name + ' (' + str(self.collect_unit) + ')'

    def print_values(self):
        """
        Method which prints the data of a collection.
        :return:
        """
        return_string = ''
        counter = 0
        for i in self.data:
            return_string += i + ' '
            counter += 1
            if counter % 5 == 0:
                return_string += '\n'

        return return_string

    def __add__(self, other):
        new_collection_data = []
        if self.length == other.length:
            for i in range(self.length):
                new_collection_data.append(self.data[i] + other.data[i])
        else:
            raise Exception('The collections must be the same length.')

        return Collection('temp_collection', new_collection_data)

    def __sub__(self, other):
        new_collection_data = []
        if self.length == other.length:
            for i in range(self.length):
                new_collection_data.append(self.data[i] - other.data[i])
        else:
            raise Exception('The collections must be the same length.')

        return Collection('temp_collection', new_collection_data)


class Regression:

    def __init__(self):
        pass

    def __str__(self):
        pass

class LinReg(Regression):

    def __init__(self):
        pass

    def __str__(self):
        pass

class ExpReg(Regression):

    def __init__(self):
        pass

    def __str__(self):
        pass