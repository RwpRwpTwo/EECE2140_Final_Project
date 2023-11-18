"""
import functions as fn
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib as mp
"""
import main
import csv


class master_data():
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
        new_collection = collection(name)
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
        rows = [r for r in reader]
        rows[0][0].replace('ufeff', '')
        for i in rows[0]:
            new_collections.append(collection(i))
        new_data = [list() for i in range(len(new_collections))]
        for i in range(1, len(rows)):
            for j in range(len(new_data)):
                new_data[j].append(rows[i][j])

        for i in range(len(new_collections)):
            new_collections[i].data = new_data[i]

        for i in new_collections:
            self.add_collection(i)


class unit():
    def __init__(self, str):
        self.representation = str

    def __str__(self):
        return self.representation


class collection():
    def __init__(self, name='New Collection', imported_data=[]):
        if [i for i in name if i=='(']:
            name = name.split('(')
            new_unit = name[1][0]
            name = name[0].replace(' ', '')
        else:
            new_unit = ''
        self.name = name  # string
        self.collect_unit = unit(new_unit)  # unit class
        self.data = imported_data  # list
        self.length = len(self.data)  # integer

    def __str__(self):
        return self.name + ' (' + str(self.collect_unit) + ')'

    def __add__(self, other):
        new_collection_data = []
        if self.length == other.length:
            for i in range(self.length):
                new_collection_data.append(self.data[i] + other.data[i])
        else:
            raise Exception('The collections must be the same length.')

        return collection('temp_collection', new_collection_data)

    def __sub__(self, other):
        new_collection_data = []
        if self.length == other.length:
            for i in range(self.length):
                new_collection_data.append(self.data[i] - other.data[i])
        else:
            raise Exception('The collections must be the same length.')

        return collection('temp_collection', new_collection_data)
