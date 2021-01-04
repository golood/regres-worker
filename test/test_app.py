import unittest
import app


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_api(self):
        expr = b'{"answer":[[[1.68,0.0,0.61,0.0,0.0,0.0],[0.0,0.0],0.0,66.67,[1,2,3],[4,5,6]]'b'],"id":1}\n'
        rv = self.app.post('/api',
                           json={'index': '1',
                                 'x': '[[2, 9, 6, 8, 1, 5], [5, 4, 1, 3, 7, 8]]',
                                 'y': '[7, 9, 1, 6, 4, 5]',
                                 'freeChlen': 'False',
                                 'list_h': '[{"h1": [0, 1, 2],"h2": [3, 4, 5]}]'
                                 })

        self.assertEqual(201, rv.status_code)
        self.assertEqual(expr, rv.data)

    def tearDown(self):
        del self.app


if __name__ == '__main__':
    unittest.main()
