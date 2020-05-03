import datetime

import numpy as np
from functools import reduce
from pulp import LpVariable, LpMinimize, LpProblem
import regres.rrrr as rrr
import sys
import math
from itertools import combinations
import threading
from queue import Queue


sys.setrecursionlimit(1000000000)

# x = np.array([[2., 5.],
#           [9., 4.],
#           [6., 1.],
#           [8., 3.],
#           [1., 7.],
#           [5., 8.]])
#
# y = np.array([7., 9., 1., 6., 4., 5.])
#
#
# h1 = [0, 1, 2]
#
# h2 = [3, 4, 5]
#
# y1 = np.array([7, 9, 1])
# y2 = np.array([6, 4, 5])


class Method:

    def __init__(self, x, y):
        self.y = np.array(y)
        self.x = np.array(x)
        self.a = []
        self.eps = []
        self.e = 0
        self.nz = None

    def _y(self, alfa):
        A = list(map(lambda item:
                     list(map(lambda x, a: x * a, item,
                              alfa)),
                     self.x))
        A = list(map(lambda item:
                     reduce(lambda x, y: x + y, item), A))

        return A

    def epselon(self, alfa):
        return list(
            map(lambda x, y: y - x, self._y(alfa), self.y))

    def Epselon(self, alfa):
        mod = lambda x: x if (x > 0) else x * -1

        E = 1 / len(self.y) * reduce(
            lambda x, y: x + y,
            list(map(lambda x, y: mod((y - x) / y),
                     self._y(alfa), self.y))) * 100

        return E

    def getResaul(self):
        return self.a, self.eps, self.e

    def getSmeshenir(self):
        sum = 0
        m = len(self.x)
        try:
          for item in self.x:
            x = math.fsum(item) / len(item)
            sum += math.fabs((self._minusAlfa() * x) / (self.a[0] * x)) / m

          return sum * 100
        except ZeroDivisionError:
          return 'Infinity'

    def _minusAlfa(self):
        a = self.a[0]
        for i in range(1, len(self.a)):
            a -= self.a[i]
        return a

class MNK(Method):

    def __init__(self, x, y):
        super().__init__(x, y)

    def find_a(self):
        return np.dot(
            np.dot(
                np.linalg.inv(np.dot(self.x.T, self.x)),
                self.x.T),
            self.y)

    def run(self):
        a = self.find_a()
        for item in a:
            self.a.append(item)
        eps = self.epselon(self.a)
        for item in eps:
            self.eps.append(item)
        self.e = self.Epselon(self.a)

    def getResaul(self):
        return 'МНК', super().getResaul()


class MNM(Method):

    def __init__(self, x, y):
        super().__init__(x, y)

    def find_a(self):
        pass

    def run(self):
        task = rrr.LpSolve_MNM(self.x, self.y)
        task.run()
        self.a, self.eps = task.getResault()
        self.e = self.Epselon(self.a)

    def getResaul(self):
        return 'МНМ', super().getResaul()


class MAO(Method):

    def __init__(self, x, y):
        super().__init__(x, y)

    def find_a(self):
        pass

    def run(self):
        task = rrr.LpSolve_MAO(self.x, self.y)
        task.run()
        self.a, self.eps = task.getResault()
        self.e = self.Epselon(self.a)

    def getResaul(self):
        return 'МАО', super().getResaul()


class MCO(Method):

    def __init__(self, x, y, h1, h2):
        super().__init__(x, y)
        self.h1 = h1
        self.h2 = h2

    def find_a(self):
        pass

    def run(self):
        task = rrr.LpSolve_MCO(self.x, self.y, self.h1, self.h2)
        task.run()
        self.a, self.eps = task.getResault()
        self.e = self.Epselon(self.a)

    def getResaul(self):
        return 'МСО', super().getResaul()


class Task:

    def __init__(self, tasks, x, y, h1=None, h2=None):
        self.methods = []
        if (tasks[0]):
          self.methods.append(MNK(x, y))
        if (tasks[1]):
          self.methods.append(MNM(x, y))
        if (tasks[2]):
          self.methods.append(MAO(x, y))
        if (tasks[3]):
          self.methods.append(MCO(x, y, h1, h2))

    def run(self):

        for item in self.methods:
            item.run()

    def getResaults(self):
        resaults = []

        for item in self.methods:
            resaults.append(item.getResaul())

        return resaults


class TaskMCO:

    def __init__(self, x, y, h1=None, h2=None):
        self.methods = []
        self.methods.append(MCO(x, y, h1, h2))

    def run(self):

        for item in self.methods:
            item.run()

    def getResaults(self):
        resaults = []

        for item in self.methods:
            resaults.append(item.getResaul())
            resaults.append(item.getSmeshenir())
            resaults.append(item.h1)
            resaults.append(item.h2)

        return resaults
