import unittest
import Main


class Test(unittest.TestCase):
    def setUp(self):
        self.date = {
            'id': 1,
            'x': [[2, 9, 6, 8, 1, 5], [5, 4, 1, 3, 7, 8]],
            'y': [7, 9, 1, 6, 4, 5],
            'freeChlen': False,
            'list_h': [{"h1": [0, 1, 2], "h2": [3, 4, 5]}]
        }

    def test_start_solution(self):
        expr = [[[1.68, 0.0, 0.61, 0.0, 0.0, 0.0],
                 [0.0, 0.0], 0.0, 66.67, [1, 2, 3], [4, 5, 6]]]

        self.assertEqual(expr, Main.start_solution(self.date))


if __name__ == '__main__':
    unittest.main()
