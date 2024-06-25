import numpy as np

from productionproblem.Node import Node
from productionproblem.PPModel import PPModel


class BrandAndBound:        # MAX问题
    def __init__(self, modelClass):
        self.modelClass = modelClass            # 初始化模型类
        self.nodeModel = None                   # 根节点模型
        self.nonContinuousVars = []             # 非连续变量列表
        self.global_UB = np.inf                 # 全局上界（线性松弛后的解）
        self.global_LB = 0                      # 全局下界（任意满足整数要求的可行解）
        self.eps = 1e-3                         # 误差精度
        self.incumbentNode = None               # 当前节点
        self.gap = np.inf                       # 当前全局上下界误差
        self.Queue = []                         # 待处理队列
        self.globalUBChang = []                 # 全局上界变化记录
        self.globalLBChang = []                 # 全局下界变化记录

    def run(self):
        # 初始化模型
        self.__establishModel()
        # 求解模型
        PPModel.solveModel(self.nodeModel)
        self.global_UB = PPModel.getObjective(self.nodeModel)  # 最大化问题，线性松弛时的解为全局上界
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
        self.nonContinuousVars = PPModel.nonContinuousVars
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
            current_node = self.Queue.pop(0)
            cnt += 1

            # 求解当前节点的模型
            PPModel.solveModel(current_node.model)
            solutionStatus = current_node.model.Status
            """
            OPTIMAL = 2
            INFEASIBLE = 3
            UNBOUNDED = 5
            """

            # ----------------------------------------------
            # 注意剪枝规则
            # 1. 最优性剪枝
            #       即为整数解
            #       对于最小化问题来说，任意可行整数解为全局上界
            #       对于最大化问题来说，任意可行整数解为全局下界  √
            # 2. 界限剪枝
            #       对于最小化问题，节点下界大于全局上界
            #       对于最大化问题，节点上界小于全局下界  √
            # 3. 不可行性剪枝
            #
            # 可行的时候需要判断1和2
            # 不可行直接默认剪枝
            # ----------------------------------------------

            isInteger = True  # 是否为整数解
            isPrune = False  # 是否需要剪枝

            if solutionStatus == 2:
                current_node.x_sol = PPModel.getVarsValues(current_node.model)
                current_node.x_int_sol = PPModel.getRoundedVarsValues(current_node.model)

                """
                整数解的相关判断
                """
                # 判断是否为整数解
                for varName in self.nonContinuousVars:
                    if current_node.x_sol[varName] - current_node.x_int_sol[varName] > self.eps:
                        isInteger = False

                if isInteger:   # 为整数解
                    current_node.isInteger = True
                    # 更新当前节点的上下界
                    # 当为整数解时，上下界都为当前节点的线性松弛解，即找到当前节点的最优解
                    current_node.local_UB = PPModel.getObjective(current_node.model)
                    current_node.local_LB = PPModel.getObjective(current_node.model)
                    # 对于最大化问题来说，任意可行整数解为全局下界
                    # 判断是否需要更新全局下界
                    if current_node.local_LB > self.global_LB:
                        self.global_LB = current_node.local_LB
                        self.incumbentNode = Node.deepcopyNode(current_node)
                else:           # 非整数解
                    current_node.isInteger = False
                    # 更新当前节点的上下界
                    # 对于最大化问题来说，当前节点的线性松弛解为当前节点的本地上界
                    # 下界即为任意一个可行的整数解
                    current_node.local_UB = PPModel.getObjective(current_node.model)
                    current_node.local_LB = 0
                    for varName, value in current_node.x_int_sol.items():
                        var = current_node.model.getVarByName(varName)
                        current_node.local_LB += value * var.getAttr('Obj')
                    # 判断是否需要更新全局下界
                    if current_node.local_LB > self.global_LB:
                        self.global_LB = current_node.local_LB
                        # 这里的意义？？
                        self.incumbentNode = Node.deepcopyNode(current_node)
                        self.incumbentNode.local_LB = current_node.local_LB
                        self.incumbentNode.local_UB = current_node.local_UB

                """
                剪枝的相关判断
                """
                if isInteger:   # 最优性剪枝
                    isPrune = True
                else:
                    if current_node.local_UB - current_node.local_LB < self.eps:  # 界限剪枝
                        isPrune = True
                self.gap = round((self.global_UB - self.global_LB) * 100 / self.global_LB, 2)

            else:   # 不可行剪枝
                isInteger = False
                isPrune = True

            if isPrune:
                continue

            """
            剪枝操作
            """
            if not isPrune:
                pass

            break




















