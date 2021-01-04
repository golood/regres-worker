import unittest
import Models


class TestTaskDTO(unittest.TestCase):
    method_data = {'freeChlen': False,
                   'x': [[2, 9, 6, 8, 1, 5], [5, 4, 1, 3, 7, 8]],
                   'y': [7, 9, 1, 6, 4, 5],
                   'h1': [0, 1, 2],
                   'h2': [3, 4, 5]}

    @classmethod
    def setUpClass(cls):
        cls.taskDTO = Models.TaskDTO(cls.method_data)

        cls.taskDTO.run()

    def setUp(self):
        self.exprTaskDTO = Models.TaskDTO(self.method_data)
        self.exprTaskDTO.method[0].a = [1.6785714, 0.0, 0.60714286, 0.0, 0.0, 0.0]
        self.exprTaskDTO.method[0].e = 3.544973556324568e-07
        self.exprTaskDTO.method[0].eps = [0.0, 0.0]
        self.exprTaskDTO.method[1].a = [0.0, 0.0, 0.0, 0.2244898, 0.0, 1.0408163]
        self.exprTaskDTO.method[1].e = 6.084656122866471e-07
        self.exprTaskDTO.method[1].eps = [0.0, 0.0]

    def test_run(self):
        self.assertEqual(self.exprTaskDTO, self.taskDTO)

    def test__calculate_bias_criterion(self):
        expr = 66.66666666666666

        self.assertEqual(expr, self.taskDTO._calculate_bias_criterion())

    def test_get_results(self):
        self.assertEqual(self.exprTaskDTO.get_results(), self.taskDTO.get_results())


if __name__ == '__main__':
    unittest.main()
