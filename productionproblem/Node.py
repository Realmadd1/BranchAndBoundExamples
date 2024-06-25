import copy
import numpy as np


class Node:
    def __init__(self):
        self.cnt = None
        self.model = None
        self.isInteger = False
        self.local_LB = 0
        self.local_UB = np.inf
        self.x_sol = {}
        self.x_int_sol = {}
        self.branch_var_list = []

    @staticmethod
    def deepcopyNode(node: "Node"):
        new_node = Node()
        new_node.cnt = node.cnt
        new_node.model = node.model.copy()
        new_node.isInteger = node.isInteger
        new_node.local_LB = 0
        new_node.local_UB = np.inf
        new_node.x_sol = copy.deepcopy(node.x_sol)
        new_node.x_int_sol = copy.deepcopy(node.x_int_sol)
        new_node.branch_var_list = []
        return new_node
