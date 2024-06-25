import numpy as np

from productionproblem.Node import Node
from productionproblem.PPModel import PPModel


class BrandAndBound:
    def __init__(self, modelClass):
        self.modelClass = modelClass        # 初始化模型类
        self.nodeModel = None               # 根节点模型
        self.nonContinuousVars = []         # 非连续变量列表
        self.global_UB = np.inf             # 全局上界（线性松弛后的解）
        self.global_LB = 0                  # 全局下界（任意满足整数要求的可行解）
        self.eps = 1e-3                     # 误差精度
        self.incumbentNode = None           # 当前节点
        self.gap = np.inf                   # 当前全局上下界误差
        self.Queue = []                     # 待处理队列
        self.globalUBChang = []             # 全局上界变化记录
        self.globalLBChang = []             # 全局下界变化记录

    def run(self):
        # 初始化模型
        self.__establishModel()
        # 求解模型
        PPModel.solveModel(self.nodeModel)
        self.global_UB = PPModel.getObjective(self.nodeModel)       # 最大化问题，线性松弛时的解为全局上界
        # 创建初始节点
        self.__createRootNode()
        # 开始分支定界
        self.__branchAndBound()

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
        self.nonContinuousVars = self.modelClass.nonContinuousVars
        # 获得根节点模型
        self.nodeModel = self.modelClass.getModel()

    def __createRootNode(self):
        """
        创建根节点。

        该方法用于在划分空间之前初始化算法的根节点。根节点的本地下界设置为0，
        本地上界设置为全局上界，模型初始化为节点模型的副本，并且输出标志设置为0，
        表示在优化过程中不会输出该节点的模型。节点的计数器初始化为0，然后将节点
        添加到处理队列中。

        """
        # 创建一个新的节点实例
        node = Node()
        # 初始化节点的本地下界为0
        node.local_LB = 0
        # 初始化节点的本地上界为全局上界
        node.local_UB = self.global_UB
        # 复制节点模型，并设置模型的输出标志为0
        node.model = self.nodeModel.copy()
        node.model.setParam('OutputFlag', 0)
        # 初始化节点的计数器为0
        node.cnt = 0
        # 将新创建的节点添加到处理队列中
        self.Queue.append(node)

    def __branchAndBound(self):
        cnt = 0
        while len(self.Queue) > 0 and self.global_UB - self.global_LB > self.eps:
            # 从队列中取出一个节点
            node = self.Queue.pop(0)
            cnt += 1








