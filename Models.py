import json
from regres.regr import MCO

class TaskDTO:
    def __init__(self, methodData):
        self.method = self._decodeMethod(methodData)

    def _decodeMethod(self, methodData):
        data = json.loads(methodData)

        return MCO(data['x'], data['y'], data['h1'], data['h2'])

    def run(self):
        self.method.run()

    def getResaults(self):
        resaults = []

        resaults.append(self.method.getResaul())
        resaults.append(self.method.getSmeshenir())
        resaults.append(self.method.h1)
        resaults.append(self.method.h2)

        return resaults


