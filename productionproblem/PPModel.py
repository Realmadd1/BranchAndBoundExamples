from gurobipy import *


class PPModel:
    def __init__(self):
        self.model = Model()
        self.x1 = None
        self.x2 = None
        self.nonContinuousVars = []

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
        for var in self.model.getVars():
            if var.vtype != GRB.CONTINUOUS:
                self.nonContinuousVars.append(var)
                var.vtype = GRB.CONTINUOUS
                var.lb = 0
                var.ub = GRB.INFINITY

    def getModel(self):
        return self.model

    def solve(self):
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            print("目标函数值：", self.model.objVal)
            print("x1的值：", self.x1.x)
            print("x2的值：", self.x2.x)
        else:
            print("无解")

