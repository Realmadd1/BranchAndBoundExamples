

class BrandAndBound:
    def __init__(self, modelClass):
        self.modelClass = modelClass

    def run(self):
        self.__establishModel()
        self.__solveModel()

    def __establishModel(self):
        self.modelClass.initModel()
        self.modelClass.linearizeModel()

    def __solveModel(self):
        self.modelClass.solve()


