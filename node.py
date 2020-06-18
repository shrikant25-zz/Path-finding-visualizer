import sys

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
        self.isstartnode = row == start_node_row and column == start_node_column
        self.isfinishnode = row == finish_node_row and column == finish_node_column
        self.distance = sys.maxsize
        self.isvisited = False
        self.previousnode = None


def createnode(row, column):
    newnode = Node(row, column)  # creates instance for Node class
    return newnode
