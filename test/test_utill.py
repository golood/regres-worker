import unittest
import utill


class MyTestCase(unittest.TestCase):
    def test_get_value_checkbox(self):
        self.assertTrue(utill.get_value_checkbox('on'))
        self.assertFalse(utill.get_value_checkbox('off'))

    def test_format_numbers(self):
        values = [0.1131234, 1.2321213]
        expr = [0.11, 1.23]
        self.assertEqual(expr, utill.format_numbers(values))

        values = [1, 2]
        expr = [1.00, 2.00]
        self.assertEqual(expr, utill.format_numbers(values))

        values = [-1, -2.9111111]
        expr = [-1.00, -2.91]
        self.assertEqual(expr, utill.format_numbers(values))

        values = ['-1', '-2.11313442']
        expr = [-1.00, -2.11]
        self.assertEqual(expr, utill.format_numbers(values))

    def test_format_number(self):
        value = 0.1111
        expr = 0.11
        self.assertEqual(expr, utill.format_number(value))

        value = -1
        expr = -1.00
        self.assertEqual(expr, utill.format_number(value))

        value = '0.1111'
        expr = 0.11
        self.assertEqual(expr, utill.format_number(value))

        value = 'Infinity'
        expr = 'Infinity'
        self.assertEqual(expr, utill.format_number(value))

        value = 0.1234567
        expr = 0.12346
        self.assertEqual(expr, utill.format_number(value, 5))

        value = 0.1234567
        expr = 0.12346
        self.assertEqual(expr, utill.format_number(value, precision=5))

        value = 0.1234567
        expr = 0.12
        self.assertEqual(expr, utill.format_number(value, validator=utill.find_min_float))

        value = 0.00001
        expr = 0.00001
        self.assertEqual(expr, utill.format_number(value, validator=utill.find_min_float))

        value = 'Infinity'
        expr = 'Infinity'
        self.assertEqual(expr, utill.format_number(value, validator=utill.find_min_float))

    def test_format_to_int(self):
        values = [0.11, '21.23242', -2.32, 0, '-3', 0.9, '-1.9']
        expr = [0, 21, -2, 0, -3, 0, -1]
        self.assertEqual(expr, utill.format_to_int(values))

    def test_append_one_for_number(self):
        values = [1, 2, 3.00, 4.56, -2]
        expr = [2, 3, 4.00, 5.56, -1]
        self.assertEqual(expr, utill.append_one_for_number(values))

    def test_find_min_float(self):
        a = [56, 1, 2]
        b = [0.00001, 2, 3]
        expr = 5
        self.assertEqual(expr, utill.find_min_float(a, b))

        self.assertEqual(expr, utill.find_min_float(b))

        self.assertEqual(2, utill.find_min_float([0, 1]))

        self.assertEqual(2, utill.find_min_float([0.01]))


if __name__ == '__main__':
    unittest.main()
