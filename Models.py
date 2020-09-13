import json
from regres.regr import MCO


class TaskDTO:
    def __init__(self, methodData):
        self.method = self._decodeMethod(methodData)

    def _decodeMethod(self, methodData):
        return MCO(methodData['x'], methodData['y'], methodData['h1'], methodData['h2'])

    def run(self):
        self.method.run()

    def getResaults(self):
        resaults = []

        resaults.append(self.method.getResaul())
        resaults.append(self.method.getSmeshenir())
        resaults.append(self.method.h1)
        resaults.append(self.method.h2)

        return resaults


