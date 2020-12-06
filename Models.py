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
        self.avg_x = self.__get_avg_x(method_data['x'])

    @staticmethod
    def _decode_method(method_data):
        return [MCO(method_data['x'], method_data['y'], method_data['h1'], method_data['h2']),
                MCO(method_data['x'], method_data['y'], method_data['h2'], method_data['h1'])]

    def run(self):
        for item in self.method:
            item.run()

    def __get_avg_x(self, x):
        avg_x = []
        if self.freeChlen == 'True':
            for i in range(1, self.m):
                accumulator = 0
                for j in range(self.n):
                    accumulator += x[j][i]
                avg_x.append(accumulator / self.n)
        else:
            for i in range(self.m):
                accumulator = 0
                for j in range(self.n):
                    accumulator += x[j][i]
                avg_x.append(accumulator / self.n)
        return avg_x

    def _calculate_bias_criterion(self):
        accumulator = 0
        if self.freeChlen == 'True':
            for i in range(1, self.m):
                accumulator += (math.fabs(self.method[0].a[i] - self.method[1].a[i]) / self.avg_x[i-1])
            accumulator /= self.m
            accumulator *= 100
        else:
            for i in range(self.m):
                accumulator += (math.fabs(self.method[0].a[i] - self.method[1].a[i]) / self.avg_x[i])
            accumulator /= self.m
            accumulator *= 100

        return accumulator

    def get_results(self):
        return [self.method[0].getResaul(),
                self._calculate_bias_criterion(),
                self.h1,
                self.h2]
