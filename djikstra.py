# dijkstra's Algorithm
import sys


class Graph:

    def __init__(self, vertices):
        self.grid = [0 for _ in range(vertices)]

    def dijkstra(self):
        graph = self.getallnodes()  # gets nodes in the form of one-D list
        startnode = self.getstartnode()  # gets the start node
        startnode.distance = 0   # set start node distance to zero
        visitednodes = []   # list to store visited nodes
        while len(graph):  # loop until the list is empty
            graph.sort(key=lambda x: x.distance)  # sort the list according to distance
            nearest_node = graph.pop(0)  # pops the first node from list
            if nearest_node.iswall:   # checks if the node is wall
                continue              # is it is wall then skip the process
            if nearest_node.distance == sys.maxsize:
                # if distance of nearest node is sys.maxsize
                # it means the node was not modifies for distance
                # this case happens when the node is wall
                # it means we are trapped, time to stop entire process
                return visitednodes
            nearest_node.isvisited = True  # sets the node as visited
            visitednodes.append(nearest_node)  # add the node in the list of visited nodes
            if nearest_node.isfinishnode:
                # if the node is finish node
                # it means the finish has been discovered and time to return the list of visited nodes
                return visitednodes
            self.updateunvisitedneighbour(nearest_node)  # updates the list of neighbours which are not visited

    def updateunvisitedneighbour(self, nearest_node):
        unvisitedneighbours = self.getunvisitednodes(nearest_node) # gets all the unvisited neighbours
        for neighbour in unvisitedneighbours:
            # if the neighbour is unvisited, set the distance as
            # total distance of current node + 1
            # each node as weight of one
            neighbour.distance = nearest_node.distance + 1
            neighbour.previousnode = nearest_node  # set current node as previous node of neighbour

    def getunvisitednodes(self, currentnode):  # gets the list of unvisited neighbours
        neighbours = []  # list to store neighbours
        row = currentnode.row
        column = currentnode.column
        #
        #   [x][N][x]
        #   [N][C][N]
        #   [x][N][x]
        #  C:   Current node
        #  N:   Neighbours
        #  X:   Non-Neighbours
        # following conditions check the possibles neighbours and appends them into list
        if row > 0:
            neighbours.append(self.grid[row - 1][column])
        if row < len(self.grid) - 1:
            neighbours.append(self.grid[row + 1][column])
        if column > 0:
            neighbours.append(self.grid[row][column - 1])
        if column < len(self.grid[0]) - 1:
            neighbours.append(self.grid[row][column + 1])
            # neighbours list is filtered and only unvisited neighbours are kept
        return filter(lambda x: (x.isvisited == False), neighbours)

    def getallnodes(self):
        # converts 2d list in 1d list of nodes
        nodes = []
        for row in self.grid:
            for node in row:
                nodes.append(node)
        return nodes

    def getstartnode(self):
        # checks for start node
        for row in self.grid:
            for curnode in row:
                if curnode.isstartnode:
                    return curnode

    def getfinishnode(self):
        # checks fro finish node
        for row in self.grid:
            for curnode in row:
                if curnode.isfinishnode:
                    return curnode

    def getshortestpath(self):
        # function gets shortest path by backtracking the list
        shortestpath = []  # list to store the shortest path
        currentnode = self.getfinishnode()  # sets the finish node as current node
        while currentnode:  # loop will continue until there is a node
            shortestpath.insert(0, currentnode)  # current-node is inserted at the beginning of the list
            currentnode = currentnode.previousnode  # previous node of current node is set as current node
            # the last node i.e the starting node wont't have any previous node, so it will return none
            # which will terminate the loop
            # finally the shortest path is returned
        return shortestpath
