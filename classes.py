import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math as m
import functions as fn
# TODO make it so that outputted numbers are rounded.

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
    # TODO add method to convert data to SI automatically

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
    this tends to be one variable being collected. In Excel, a collection is defined as
    a column with a header that describes what the values in that column represent.
    The header must contain that columns' units in parentheses after the name.
    """

    def __init__(self, name='New Collection', imported_data=None):
        """
        Constructor for the collection class. Filters the header into the name and the unit
        of the collection. All other data is imported raw and unfiltered. If no name is
        provided in the function call, wil default the name to 'New Collection' as the
        dictionary requires a key. If no data is provided, will create an empty list to
        store potential data.
        :param name:
        :param imported_data:
        """
        if imported_data is None:
            imported_data = []

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

        self.data = imported_data  # list

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


class CartPlot:

    def __init__(self, cl1=Collection(), cl2=Collection()):
        self.cl1 = cl1  # Independent variable collection
        self.x = self.cl1.data
        self.x_axis_name = str(self.cl1)

        self.cl2 = cl2  # Dependant variable collection
        self.y = self.cl2.data
        self.y_axis_name = str(self.cl2)
        self.name = self.cl2.name + ' vs ' + self.cl1.name

    def __str__(self):
        return self.name

    def default_plot(self):
        fig, my_plot = plt.subplots()

        my_plot.scatter(self.x, self.y)

        my_plot.set_xticks(np.arange(self.x[0], self.x[-1], self.x[-1] / 10))
        my_plot.set_yticks(np.arange(self.y[0], self.y[-1], self.y[-1] / 10))
        plt.show()

    def swap_axis(self):
        temp_collection = self.cl1
        self.cl1 = self.cl2
        self.cl2 = temp_collection
        # TODO make it so that the class reconstructs with the new collections
        print("Swapped the axis.")


class LinReg(CartPlot):

    def __init__(self, cl1, cl2, L=0.0001, iter=1000):
        super().__init__(cl1, cl2)
        # self.L = L
        # self.iter = iter

        self.m = 0.0
        self.m_err = 0.0
        self.b = 0.0
        self.b_err = 0.0
        self.r = 0.0
        self.p = 0.0
        self.std_err = 0.0

        self.n = len(cl1.data)

    def __str__(self):
        return_string = ''
        if self.b >= 0:
            return_string += 'y = (' + str(self.m) + u"\u00B1" + str(self.m_err) + ')x + (' + str(
                self.b) + u"\u00B1" + str(self.b_err) + ')'
        else:
            return_string += 'y = (' + str(self.m) + u"\u00B1" + str(self.m_err) + ')x - (' + str(
                -self.b) + u"\u00B1" + str(self.b_err) + ')'
        return_string += '\nR: ' + str(self.r) + '\tP: ' + str(self.p) + '\tStandard Error: ' + str(self.std_err)
        return return_string

    def func(self, x):
        return self.m * x + self.b

    def lower_func(self, x):
        return (self.m - self.m_err) * x + (self.b - self.b_err)
    def upper_func(self, x):
        return (self.m + self.m_err) * x + (self.b + self.b_err)


    def round_all(self, f=4):
        # TODO Move round all to collection class for self.x and self.y
        self.x = [fn.round_sig(i, f) for i in self.x]
        self.y = [fn.round_sig(i, f) for i in self.y]

        self.m = fn.round_sig(self.m, f)
        self.m_err = fn.round_sig(self.m_err, f)
        self.b = fn.round_sig(self.b, f)
        self.b_err = fn.round_sig(self.b_err, f)
        self.r = fn.round_sig(self.r, f)
        self.p = fn.round_sig(self.p, f)
        self.std_err = fn.round_sig(self.std_err, f)

    def default_plot(self, y=None):
        if y is None:
            y = self.y
        fig, my_plot = plt.subplots()

        y_max = max(max(y), max(self.y))
        y_min = min(min(y), min(self.y))

        my_plot.scatter(self.x, self.y, color='#3d405b')
        my_plot.plot(self.x, y, color='#e07a5f')

        if (self.m != 0) and (self.b != 0):
            my_plot.plot(self.x, [self.lower_func(i) for i in self.x], ls=':')
            my_plot.plot(self.x, [self.upper_func(i) for i in self.x], ls=':')

        my_plot.set_title(self.name)
        my_plot.grid()
        my_plot.set_xlabel(self.x_axis_name)
        my_plot.set_ylabel(self.y_axis_name)
        my_plot.set_xticks(np.arange(self.x[0], self.x[-1] + (self.x[-1] / 10), self.x[-1] / 10))
        my_plot.set_yticks(np.arange(y_min, y_max + (y_max / 10), y_max / 10))
        plt.show()

    def calc_reg(self):
        """
        for i in range(self.iter):
            if i % 100 == 0:
                print("Iteration: ", i)
            self.gradient_descent()
        :return:
        """
        self.m, self.b, self.r, self.p, self.std_err = stats.linregress(self.x, self.y)

        # Applying equation for error from paper
        s = m.sqrt(sum([(self.y[i] - self.m * self.x[i] - self.b) ** 2 for i in range(self.n)]) / (self.n - 2))
        self.m_err = s * m.sqrt(self.n / ((self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))
        self.b_err = s * m.sqrt(sum([self.x[i] ** 2 for i in range(self.n)]) / (
                (self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))

        self.round_all()
        self.default_plot([self.func(i) for i in self.x])
        print(self)

    def gradient_descent(self):
        # Currently unused
        m_grad = 0
        b_grad = 0
        for i in range(self.n):
            x = self.x[i]
            y = self.y[i]
            m_grad += -(2 / self.n) * x * (y - (self.m * x + self.b))
            b_grad += -(2 / self.n) * (y - (self.m * x + self.b))

        self.m = self.m - m_grad * self.L
        self.b = self.b - b_grad * self.L


class ExpReg(LinReg):

    def __init__(self, cl1, cl2):
        super().__init__(cl1, cl2)

        self.lny = [m.log(i) for i in self.y]

    def __str__(self):
        str_b = fn.round_sig(self.b, 3)
        str_b_err = fn.round_sig(self.b_err, 3)
        str_m = fn.round_sig(self.m, 3)
        str_m_err = fn.round_sig(self.m_err, 3)
        return_string = ''
        return_string += 'y = (' + str(str_b) + u"\u00B1" + str(str_b_err) + ') * e^(('
        return_string += str(str_m) + u"\u00B1" + str(str_m_err) + ')x)\n'
        return_string += '\nR: ' + str(self.r) + '\tP: ' + str(self.p) + '\tStandard Error: ' + str(self.std_err)
        return return_string

    def func(self, x):
        return self.b * m.exp(self.m * x)

    def lower_func(self, x):
        return (self.b -  self.b_err) * m.exp((self.m - self.m_err) * x)

    def upper_func(self, x):
        return (self.b + self.b_err) * m.exp((self.m + self.m_err) * x)

    def default_plot(self, y=None):
        if y is None:
            y = self.y

        fig, my_plot = plt.subplots()

        y_max = max(max(y), max(self.y))
        y_min = min(min(y), min(self.y))

        my_plot.scatter(self.x, self.y, color='#3d405b')
        my_plot.plot(self.x, y, color='#e07a5f')

        if (self.m != 0) and (self.b != 0):
            my_plot.plot(self.x, [self.lower_func(i) for i in self.x], ls=':')
            my_plot.plot(self.x, [self.upper_func(i) for i in self.x], ls=':')

        my_plot.set_title(self.name)
        my_plot.grid()
        my_plot.set_xlabel(self.x_axis_name)
        my_plot.set_ylabel(self.y_axis_name)
        my_plot.set_xticks(np.arange(self.x[0], self.x[-1] + (self.x[-1] / 10), self.x[-1] / 10))
        my_plot.set_yticks(np.arange(y_min, y_max + (y_max / 10), y_max / 10))

        plt.show()

    def calc_reg(self):
        self.m, self.b, self.r, self.p, self.std_err = stats.linregress(self.x, self.lny)

        # Applying equation for error from paper
        s = m.sqrt(sum([(self.lny[i] - self.m * self.x[i] - self.b) ** 2 for i in range(self.n)]) / (self.n - 2))
        self.m_err = s * m.sqrt(self.n / ((self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))
        self.b_err = s * m.sqrt(sum([self.x[i] ** 2 for i in range(self.n)]) / (
                (self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))

        self.b = m.exp(self.b)
        self.b_err = m.exp(self.b_err)

        self.round_all()
        self.default_plot([self.func(i) for i in self.x])
        print(self)