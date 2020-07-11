import math

# variables to hold values for row and column of start node and finish node
start_node_row = 0
start_node_column = 0
finish_node_row = 19
finish_node_column = 19


class Node:  # node class holds all the attributes related to node
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.iswall = False
        self.isstartnode = False
        self.isfinishnode = False
        self.distance = math.inf
        self.isvisited = False
        self.previousnode = None
        self.isweight = False


def createnode(row, column):
    newnode = Node(row, column)  # creates instance for Node class
    return newnode
