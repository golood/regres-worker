from regres.regr import MCO


class TaskDTO:
    def __init__(self, method_data):
        self.method = self._decode_method(method_data)

    @staticmethod
    def _decode_method(method_data):
        return MCO(method_data['x'], method_data['y'], method_data['h1'], method_data['h2'])

    def run(self):
        self.method.run()

    def get_results(self):
        return [self.method.getResaul(),
                self.method.getSmeshenir(),
                self.method.h1,
                self.method.h2]
