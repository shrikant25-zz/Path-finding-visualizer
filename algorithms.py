import math


class Graph(object):

    def __init__(self, grid):
        self.grid = grid  # list to store graph
        self.visitednodes = []  # list to store visited nodes
        self.shortestpath = []  # list to store the shortest path

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
        currentnode = self.getfinishnode()  # sets the finish node as current node
        while currentnode:  # loop will continue until there is a node
            self.shortestpath.insert(0, currentnode)  # current-node is inserted at the beginning of the list
            currentnode = currentnode.previousnode  # previous node of current node is set as current node
            # the last node i.e the starting node wont't have any previous node, so it will return none
            # which will terminate the loop

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
        return filter(lambda x: (x.isvisited is False and x.iswall is False), neighbours)


class Dijkstra(Graph):
    def __init__(self, grid):
        super().__init__(grid)

    def dijkstra(self):
        graph = self.getallnodes()  # gets nodes in the form of one-D list
        startnode = self.getstartnode()  # gets the start node
        startnode.distance = 0  # set start node distance to zero
        while len(graph):  # loop until the list is empty
            graph.sort(key=lambda x: x.distance)  # sort the list according to distance
            nearest_node = graph.pop(0)  # pops the first node from list
            if nearest_node.distance == math.inf:
                # if distance of nearest node is sys.maxsize
                # it means the node was not modifies for distance
                # this case happens when the node is wall
                # it means we are trapped, time to stop entire process
                return
            nearest_node.isvisited = True  # sets the node as visited
            self.visitednodes.append(nearest_node)  # add the node in the list of visited nodes
            if nearest_node.isfinishnode:
                # if the node is finish node
                # it means the finish has been discovered and time to return the list of visited nodes
                return
            self.updateunvisitedneighbour(nearest_node)  # updates the list of neighbours which are not visited

    def updateunvisitedneighbour(self, nearest_node):
        unvisitedneighbours = self.getunvisitednodes(nearest_node)  # gets all the unvisited neighbours
        for neighbour in unvisitedneighbours:
            # if the neighbour is unvisited, set the distance as
            # total distance of current node + 1
            # each node as value of one
            # if isweight parameter is set to true then value of that node becomes 2
            if neighbour.isweight is True:
                if neighbour.distance > nearest_node.distance + 3:
                    neighbour.distance = nearest_node.distance + 3
                    neighbour.previousnode = nearest_node  # set current node as previous node of neighbour
            else:
                if neighbour.distance > nearest_node.distance + 1:
                    neighbour.distance = nearest_node.distance + 1
                    neighbour.previousnode = nearest_node  # set current node as previous node of neighbour



class Bfs(Graph):
    def __init__(self, grid):
        super().__init__(grid)
        self.nodesqueue = []

    def bfs(self):
        startnode = self.getstartnode()
        startnode.isvisited = True
        self.nodesqueue.append(startnode)
        while len(self.nodesqueue):
            current_node = self.nodesqueue.pop(0)
            self.visitednodes.append(current_node)
            if current_node.isfinishnode:
                return
            self.updateunvisitedneighbour(current_node)

    def updateunvisitedneighbour(self, current_node):
        unvisitedneighbours = self.getunvisitednodes(current_node)  # gets all the unvisited neighbours
        for neighbour in unvisitedneighbours:
            neighbour.previousnode = current_node  # set current node as previous node of neighbour
            neighbour.isvisited = True
            self.nodesqueue.append(neighbour)


class Dfs(Graph):
    def __init__(self, grid):
        super().__init__(grid)
        self.nodesstack = []

    def dfs(self):
        startnode = self.getstartnode()
        self.nodesstack.append(startnode)
        while len(self.nodesstack):
            current_node = self.nodesstack.pop()
            if current_node.isfinishnode:
                return
            if current_node.isvisited is False:
                current_node.isvisited = True
                self.visitednodes.append(current_node)
                self.updateunvisitedneighbour(current_node)

    def updateunvisitedneighbour(self, current_node):
        unvisitedneighbours = self.getunvisitednodes(current_node)  # gets all the unvisited neighbours
        for neighbour in unvisitedneighbours:
            neighbour.previousnode = current_node  # set current node as previous node of neighbour
            self.nodesstack.append(neighbour)
