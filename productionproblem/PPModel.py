from gurobipy import *


class PPModel:

    nonContinuousVars = []

    def __init__(self):
        self.model = Model()
        self.x1 = None
        self.x2 = None

    def initModel(self):
        """建立决策变量"""
        self.x1 = self.model.addVar(vtype=GRB.INTEGER, name="x1")
        self.x2 = self.model.addVar(vtype=GRB.INTEGER, name="x2")
        """建立目标函数"""
        self.model.setObjective(100 * self.x1 + 150 * self.x2, GRB.MAXIMIZE)
        """建立约束条件"""
        self.model.addConstr(2 * self.x1 + self.x2 <= 10, "c1")
        self.model.addConstr(3 * self.x1 + 6 * self.x2 <= 40, "c2")
        self.model.update()

    def linearizeModel(self):
        """
        将模型中的所有非连续变量转换为连续变量。

        该方法遍历模型中的所有变量，如果发现变量类型不是连续的（例如，整数或二进制变量），
        则将其转换为连续变量，并设置其下界为0，上界为无穷大。这样做的目的是为了线性化模型，
        使得模型更适合使用线性规划算法进行求解。

        注意：这个方法会修改原始模型的变量类型，因此应在调用此方法前后对模型的状态进行适当管理。
        """

        # 遍历模型中的所有变量
        for var in self.model.getVars():
            # 检查变量类型是否为非连续类型
            if var.vtype != GRB.CONTINUOUS:
                # 将非连续变量添加到非连续变量列表中
                PPModel.nonContinuousVars.append(var.varName)
                # 将变量类型强制转换为连续型
                var.vtype = GRB.CONTINUOUS
                # 设置变量的下界为0
                var.lb = 0
                # 设置变量的上界为无穷大
                var.ub = GRB.INFINITY
        self.model.update()

    def getModel(self):
        return self.model

    @staticmethod
    def solveModel(model):
        model.optimize()
        varsValues = PPModel.getVarsValues(model)
        for varName, value in varsValues.items():
            print(f"{varName} = {value}")

    @staticmethod
    def getObjective(model):
        return model.objVal

    @staticmethod
    def getVarsValues(model):
        return {var.varName: var.x for var in model.getVars()}

    @staticmethod
    def getRoundedVarsValues(model):
        return {var.varName: (int(var.x) if var.varName not in PPModel.nonContinuousVars else var.x) for var in model.getVars()}



