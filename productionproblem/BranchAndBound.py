import numpy as np

from productionproblem.PPModel import PPModel


class BrandAndBound:
    def __init__(self, modelClass):
        self.modelClass = modelClass        # 初始化模型类
        self.nodeModel = None               # 根节点模型
        self.global_UB = np.inf             # 全局上界
        self.global_LB = 0                  # 全局下界
        self.eps = 1e-3                     # 误差精度
        self.incumbentNode = None           # 当前节点
        self.gap = np.inf                   # 当前全局上下界误差

    def run(self):
        # 初始化模型
        self.__establishModel()
        # 求解模型
        PPModel.solveModel(self.nodeModel)
        self.global_UB = PPModel.getObjective(self.nodeModel)       # 最大化问题，线性松弛时的解为全局上界

    def __establishModel(self):
        """
        初始化并线性化模型。

        该方法用于内部模型的建立过程，首先通过调用modelClass的initModel方法来初始化模型，
        然后通过调用linearizeModel方法来线性化模型。这两个步骤是模型建立过程中的关键步骤，
        它们为后续的模型使用和操作提供了基础。
        """
        # 初始化模型
        self.modelClass.initModel()
        # 线性化模型
        self.modelClass.linearizeModel()
        # 获得根节点模型
        self.nodeModel = self.modelClass.getModel()







