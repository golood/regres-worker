import math

from regres.regr import MCO


class TaskDTO:
    def __init__(self, method_data):
        self.method = self._decode_method(method_data)
        self.h1 = method_data['h1']
        self.h2 = method_data['h2']
        self.n = len(method_data['x'])
        self.m = len(method_data['x'][0])

    @staticmethod
    def _decode_method(method_data):
        return [MCO(method_data['x'], method_data['y'], method_data['h1'], method_data['h2']),
                MCO(method_data['x'], method_data['y'], method_data['h2'], method_data['h1'])]

    def run(self):
        for item in self.method:
            item.run()

    def _calculate_bias_criterion(self):
        accumulator = 0
        for i in range(self.m):
            accumulator += math.fabs(self.method[0].a[i] - self.method[1].a[i]) \
                           / max(math.fabs(self.method[0].a[i]), math.fabs(self.method[1].a[i]))
        accumulator *= (1 / self.m)
        accumulator *= 100

        return accumulator

    def get_results(self):
        return [self.method[0].getResaul(),
                self._calculate_bias_criterion(),
                self.h1,
                self.h2]
