import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math as m
import functions as fn


class MasterData:
    """
    A class which stores collections. It consists of one dictionary who's keys
    are the headers to each collection and whos values are the collection objects.
    """

    def __init__(self):
        self.collection_dictionary = {}

    def __str__(self):
        # Prints the headers of each collection.
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
        :param name: The name of the collection being made.
        :return: Creates new empty collection and returns nothing.
        """
        new_collection = Collection(name)
        self.collection_dictionary[name] = new_collection

    def add_collection(self, new_collection):
        """
        Adds a collection to the master collection dictionary.
        :param new_collection: A collection object.
        :return void: The new collection is added to the dictionary.
        """
        self.collection_dictionary[new_collection.name] = new_collection
        return 'Collection' + new_collection.name + 'added successfully'

    def remove_collection(self, collection_name):
        """
        Removes a collection from the master collection dictionary.
        :param collection_name:
        :return success or error message:
        """

        # Checks if the collection is in the dictionary before removing.
        if collection_name in self.collection_dictionary:
            self.collection_dictionary.pop(collection_name)
            return collection_name.name + 'removed successfully.'
        else:
            return 'That is not a valid collection name.'

    def auto_import(self, file):
        """
        Automatically creates collections out of each column and imports them
        into the master dictionary
        :param file: A file object
        :return void:
        """
        new_collections = []
        reader = csv.reader(file, dialect='excel')

        # Corrects bug where "\ufeff" is included
        rows = [[c.replace('\ufeff', '') for c in row] for row in reader]
        rows = [r for r in rows]

        # Creates collection objects out of headers.
        for i in rows[0]:
            new_collections.append(Collection(i))

        # Creates a list which stores lists of the new data values.
        new_data = [list() for i in range(len(new_collections))]

        # Reads in data to new_data var
        for i in range(1, len(rows)):
            for j in range(len(new_data)):
                new_data[j].append(rows[i][j])

        # Converts all data to floats
        new_new_data = []
        for i in new_data:
            inner_list = []
            for j in i:
                try:
                    inner_list.append(float(j))
                except ValueError:
                    print("Non numeric value in row", j)
                except Exception as v:
                    print(v)
            new_new_data.append(inner_list)
        new_data = new_new_data


        # Adds data to collections
        for i in range(len(new_collections)):
            new_collections[i].data = new_data[i]

        # Adds the newly created collections to the dictionary
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
        self.round_all()
        return_string = ''
        for i in self.data:
            return_string += str(i) + '\n'
        return return_string

    def round_all(self):
        for i in range(len(self.data)):
            self.data[i] = fn.round_sig(self.data[i], 4)

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
        self.__init__(self.cl1, self.cl2)
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

        self.usr_m = 0.0
        self.usr_b = 0.0
        self.MSE = 0.0
        self.user_reg = False

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

    def usr_func(self, x):
        return self.usr_m * x + self.usr_b

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

        upper_y = [self.upper_func(i) for i in self.x]
        lower_y = [self.lower_func(i) for i in self.x]
        user_y = [self.usr_func(i) for i in self.x]
        y = [self.func(i) for i in self.x]
        fig, my_plot = plt.subplots()

        y_max = max(max(self.y), max(user_y), max(upper_y), max(y))
        y_min = min(min(self.y), min(user_y), min(lower_y), min(y))

        original_data = my_plot.scatter(self.x, self.y, color='#3d405b', label='Original data')
        regression = my_plot.plot(self.x, y, color='#e07a5f', label='Regression')

        if (self.m != 0) and (self.b != 0):
            lower = my_plot.plot(self.x, lower_y, ls=':', color='#e07a5f', label='Lower Bound')
            upper = my_plot.plot(self.x, upper_y, ls=':', color='#e07a5f', label='Upper Bound')

        if self.usr_reg == True:
            expected = my_plot.plot(self.x, user_y, color='#81b29a', label='User defined regression')

        # my_plot.legend(loc='outside lower center')
        my_plot.set_title(self.name)
        my_plot.grid()
        my_plot.set_xlabel(self.x_axis_name)
        my_plot.set_ylabel(self.y_axis_name)
        my_plot.set_xticks(np.arange(self.x[0], self.x[-1] + (self.x[-1] / 10), self.x[-1] / 10))
        my_plot.set_yticks(np.arange(y_min, y_max + (y_max / 10), (abs(y_max) + abs(y_min) / 10)))

        plt.show()

    def usr_reg(self):
        print("y = mx+b")
        self.usr_m = float(input("Input the expected m.\n"))
        self.usr_b = float(input("Input the expected b.\n"))
        self.user_reg = True

    def calc_reg(self):
        self.m, self.b, self.r, self.p, self.std_err = stats.linregress(self.x, self.y)

        # Applying equation for error from paper
        s = m.sqrt(sum([(self.y[i] - self.m * self.x[i] - self.b) ** 2 for i in range(self.n)]) / (self.n - 2))
        self.m_err = s * m.sqrt(self.n / ((self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))
        self.b_err = s * m.sqrt(sum([self.x[i] ** 2 for i in range(self.n)]) / (
                (self.n * sum([self.x[i] ** 2 for i in range(self.n)])) - (
                sum([self.x[i] for i in range(self.n)]) ** 2)))

        self.round_all()
        print(self)

    def MSE_to_usr_def(self):
        """
        For each value:
        1. Check if within error of regression
        2a. If within, skip
        2b. if not within, return minimum of the difference to each error line
        :return:
        """
        self.MSE = 0.0
        for i in range(self.n):
            up = self.upper_func(self.x[i])
            low = self.lower_func(self.x[i])
            curr_point = self.usr_func(self.x[i])
            if not ((low <= curr_point) and (curr_point <= up)):
                self.MSE += (min(abs(curr_point - up), abs(curr_point - low))) ** 2

        print("Mean Squared Error:", self.MSE)


class ExpReg(LinReg):

    def __init__(self, cl1, cl2):
        super().__init__(cl1, cl2)

        self.lny = [m.log(i) for i in self.y]
        self.user_reg = False

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
        return (self.b - self.b_err) * m.exp((self.m - self.m_err) * x)

    def upper_func(self, x):
        return (self.b + self.b_err) * m.exp((self.m + self.m_err) * x)

    def usr_reg(self):
        print("y = B*e^(A*x)")
        self.usr_m = float(input("Input the expected A.\n"))
        self.usr_b = float(input("Input the expected B.\n"))
        self.user_reg = True

    def usr_func(self, x):
        return self.usr_b * m.exp(self.usr_m * x)

    def default_plot(self):
        upper_y = [self.upper_func(i) for i in self.x]
        lower_y = [self.lower_func(i) for i in self.x]
        user_y = [self.usr_func(i) for i in self.x]
        y = [self.func(i) for i in self.x]
        fig, my_plot = plt.subplots()

        y_max = max(max(self.y), max(user_y), max(upper_y), max(y))
        y_min = min(min(self.y), min(user_y), min(lower_y), min(y))

        original_data = my_plot.scatter(self.x, self.y, color='#3d405b', label='Original data')
        regression = my_plot.plot(self.x, y, color='#e07a5f', label='Regression')

        if (self.m != 0) and (self.b != 0):
            lower = my_plot.plot(self.x, lower_y, ls=':', color='#e07a5f', label='Lower Bound')
            upper = my_plot.plot(self.x, upper_y, ls=':', color='#e07a5f', label='Upper Bound')

        if self.user_reg == True:
            expected = my_plot.plot(self.x, user_y, color='#81b29a', label='User defined regression')

        # my_plot.legend(loc='outside lower center')
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
        print(self)

    def MSE_to_usr_def(self):
        """
        For each value:
        1. Check if within error of regression
        2a. If within, skip
        2b. if not within, return minimum of the difference to each error line
        :return:
        """
        self.MSE = 0.0
        for i in range(self.n):
            up = self.upper_func(self.x[i])
            low = self.lower_func(self.x[i])
            curr_point = self.usr_func(self.x[i])
            if not ((low <= curr_point) and (curr_point <= up)):
                self.MSE += (min(abs(curr_point - up), abs(curr_point - low))) ** 2

        print("Mean Squared Error:", self.MSE)
