import math

from regres.regr import MCO


class TaskDTO:
    def __init__(self, method_data):
        self.freeChlen = method_data['freeChlen']
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
        if self.freeChlen == 'True':
            for i in range(1, self.m):
                try:
                    accumulator += math.fabs(self.method[0].a[i] - self.method[1].a[i]) \
                                    / max(math.fabs(self.method[0].a[i]), math.fabs(self.method[1].a[i]))
                except ZeroDivisionError:
                    accumulator += 0
            accumulator *= (1 / self.m)
            accumulator *= 100
        else:
            for i in range(self.m):
                try:
                    accumulator += math.fabs(self.method[0].a[i] - self.method[1].a[i]) \
                                    / max(math.fabs(self.method[0].a[i]), math.fabs(self.method[1].a[i]))
                except ZeroDivisionError:
                    accumulator += 0
            accumulator *= (1 / self.m)
            accumulator *= 100

        return accumulator

    def get_results(self):
        return [self.method[0].getResaul(),
                self._calculate_bias_criterion(),
                self.h1,
                self.h2]

    def __eq__(self, other):
        return (isinstance(other, TaskDTO) and
                self.freeChlen == other.freeChlen and
                self.h1 == other.h1 and
                self.h2 == other.h2 and
                self.m == other.m and
                self.n == other.n and
                self.method[0].__eq__(other.method[0]) and
                self.method[1].__eq__(other.method[1]))
