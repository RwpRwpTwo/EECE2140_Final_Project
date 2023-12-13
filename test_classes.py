from unittest import TestCase
import classes as cl

data = cl.MasterData()


class TestMasterData(TestCase):
    def test_auto_import(self):
        with open('data/sample_data.csv', 'rt', newline='', encoding='utf-8-sig') as file:
            data.auto_import(file)
        self.assertTrue(all([True for i in {"independent", "exp_dependant", "lin_dependant"} if i in set(data.collection_dictionary.keys())]))

    def test_create_empty_collection(self):
        data.create_empty_collection("test_empty_collection")
        self.assertIn("test_empty_collection", data.collection_dictionary.keys())
        self.assertIsInstance(data.collection_dictionary["test_empty_collection"], cl.Collection)
        with self.assertRaises(IndexError):
            data.collection_dictionary["test_empty_collection"].data[0]

    def test_add_collection(self):
        new_collection = cl.Collection("Added_Collection")
        data.add_collection(new_collection)
        self.assertIn("Added_Collection", data.collection_dictionary.keys())


class TestCollection(TestCase):
    TestMasterData().test_auto_import()

    def test_round_all(self):
        test_collection = data.collection_dictionary["exp_dependant"]
        test_collection.round_all()
        self.assertEqual(test_collection.data[1], 5.526)


class TestUnit(TestCase):

    def test_prefixes(self):
        u = cl.Unit('mA')
        self.assertSetEqual(set(u.prefixes.keys()), {'m', 'c', 'd', 'de', 'h', 'k'})
        self.assertEqual(str(u), 'mA')


class TestCartPlot(TestCase):

    def test_swap_axis(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [6, 7, 8, 9, 10]
        p = cl.CartPlot(cl1, cl2)
        p.swap_axis()
        self.assertEqual(p.x, [6, 7, 8, 9, 10])
        self.assertEqual(p.y, [1, 2, 3, 4, 5])


class TestLinReg(TestCase):
    TestMasterData().test_auto_import()

    def test_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [3, 5, 7, 9, 11]

        reg = cl.LinReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.func(1), 3)

    def test_lower_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [3, 5, 7, 9, 11]

        reg = cl.LinReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.func(3), reg.lower_func(3))

    def test_upper_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [3, 5, 7, 9, 11]

        reg = cl.LinReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.func(3), reg.upper_func(3))

    def test_round_all(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1.152725153, 2.251621798]
        cl2 = cl.Collection("cl2")
        cl2.data = [3.7656734890234, 5.54767983897]
        reg = cl.LinReg(cl1, cl2)
        reg.round_all()
        self.assertEqual(reg.x[0], 1.153)
        self.assertEqual(reg.y[0], 3.766)

    def test_usr_reg(self):
        # Does not test the input, only the calculated error
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [3, 5, 7, 9, 11]
        reg = cl.LinReg(cl1, cl2)
        reg.calc_reg()
        reg.usr_m = 2
        reg.usr_b = 1
        self.assertEqual(reg.usr_func(1), reg.func(1))

    def test_MSE_to_usr_def(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1.152725153, 2.251621798]
        cl2 = cl.Collection("cl2")
        cl2.data = [3.7656734890234, 5.54767983897]
        reg = cl.LinReg(cl1, cl2)
        reg.calc_reg()
        reg.usr_m = 2
        reg.usr_b = 1
        reg.MSE_to_usr_def()
        self.assertEqual(reg.MSE, 0)


class TestExpReg(TestCase):

    def test_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [8.2436063535, 13.5914091423, 22.4084453517, 36.9452804947, 60.9124698035]

        reg = cl.ExpReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.func(2), 13.5914091423)

    def test_lower_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [8.2436063535, 13.5914091423, 22.4084453517, 36.9452804947, 60.9124698035]

        reg = cl.ExpReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.lower_func(1), 6.5948850828)

    def test_upper_func(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [8.2436063535, 13.5914091423, 22.4084453517, 36.9452804947, 60.9124698035]

        reg = cl.ExpReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.upper_func(1), 9.8923276242)

    def test_calc_reg(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [8.2436063535, 13.5914091423, 22.4084453517, 36.9452804947, 60.9124698035]

        reg = cl.ExpReg(cl1, cl2)
        reg.calc_reg()
        self.assertAlmostEqual(reg.m, 0.5, places=4)
        self.assertAlmostEqual(reg.b, 5)

    def MSE_to_usr_def(self):
        cl1 = cl.Collection("cl1")
        cl1.data = [1, 2, 3, 4, 5]
        cl2 = cl.Collection("cl2")
        cl2.data = [8.2436063535, 13.5914091423, 22.4084453517, 36.9452804947, 60.9124698035]

        reg = cl.ExpReg(cl1, cl2)
        reg.calc_reg()
        reg.usr_m = 0.5
        reg.usr_b = 5
        reg.MSE_to_usr_def()
        self.assertEqual(reg.MSE, 0)
