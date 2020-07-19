import pygame
import math
import node
import algorithms

pygame.init()  # creates pygame instance
screen = pygame.display.set_mode((800, 600))  # sets the size of window
pygame.display.set_caption("Path Visualizer")  # sets the title

# following is the dictionary containing colors
color = {1: [0, 128, 0],  # green
         2: [255, 0, 0],  # red
         3: [0, 0, 0],  # black
         4: [250, 250, 250],  # white
         5: [0, 0, 128],  # blue
         6: [42, 53, 61],  # dark-gray
         7: [200, 200, 200],  # silver
         8: [255, 255, 0],  # yellow
         9: [255, 192, 203]}  # pink

# following are global variables used to create rectangular objects
width = 20
height = 20
margin = 5

screen.fill(color[4])  # fills the screen background with color from dictionary
legend = pygame.image.load('legend.png')
screen.blit(legend, (530, 50))


class Game:
    def __init__(self):
        self.startnoderow = node.start_node_row
        self.startnodecolumn = node.start_node_column
        self.finishnoderow = node.finish_node_row
        self.finishnodecolumn = node.finish_node_column
        self.dijkstrabutton = Button(265, 550, 65, 30, 'arial', 20, 'Dijkstra', 6, 7)
        self.bfsbutton = Button(215, 550, 30, 30, 'arial', 20, 'bfs', 6, 7)
        self.dfsbutton = Button(165, 550, 30, 30, 'arial', 20, 'dfs', 6, 7)
        self.astarbutton = Button(115, 550, 30, 30, 'arial', 20, 'A*', 6, 7)
        self.resetbutton = Button(350, 550, 65, 30, 'arial', 20, 'Reset', 6, 7)
        self.flag = 0
        # creates the button instance
        # accepts x,y coords, width, height, fontname, fontsize, buttontext, backgroundcolor,
        # text color accordingly as parameter
        self.grid = []  # array to hold rectangles/nodes

    def creategrid(self):
        for row in range(20):  # loop creating nodes
            rows = []
            for column in range(20):
                flag = 3
                # checks the row and column matches the variables
                if row == self.startnoderow and column == self.startnodecolumn:
                    flag = 1  # if it matches then sets the flag accordingly
                elif row == self.finishnoderow and column == self.finishnodecolumn:
                    flag = 2
                    # calls the draw rect function
                self.drawrect(flag, (margin + width) * row + margin, (margin + height) * column + margin)
                newnode = node.createnode(row, column)
                if flag == 1:
                    newnode.isstartnode = True
                elif flag == 2:
                    newnode.isfinishnode = True
                rows.append(newnode)  # appends the node in row
            self.grid.append(rows)  # appends the row in grid

    def cleargrid(self):
        for nodelist in self.grid:  # check the list match the row and column with the values in list
            for cnode in nodelist:
                cnode.isvisited = False
                cnode.previousnode = False
                cnode.distance = math.inf
                if cnode.iswall is True:
                    continue
                elif cnode.isweight is True:
                    self.drawrect(9, (margin + width) * cnode.row + margin, (margin + height) * cnode.column + margin)
                elif cnode.isstartnode is True:
                    self.drawrect(1, (margin + width) * cnode.row + margin, (margin + height) * cnode.column + margin)
                elif cnode.isfinishnode is True:
                    self.drawrect(2, (margin + width) * cnode.row + margin, (margin + height) * cnode.column + margin)
                else:
                    self.drawrect(3, (margin + width) * cnode.row + margin, (margin + height) * cnode.column + margin)
        pygame.display.flip()

    # this function contains main while loop to run the game
    def rungame(self):
        self.creategrid()
        running = True  # variable is use to keep loop running
        # following variables will used in program for different purposes
        currentx = 0
        currenty = 0
        while running:
            for event in pygame.event.get():  # checks for the event
                if event.type == pygame.QUIT:  # if event type is quit, then proceed to quit the window
                    pygame.quit()  # end the pygame instance
                    quit()  # closes the window

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # checks if mouse button is pressed
                    if self.dijkstrabutton.chechkifclicked():  # checks if the dijkstra button is pressed
                        self.cleargrid()
                        g = algorithms.Dijkstra(self.grid)  # creates an instance of class graph from dijkstra  module
                        g.dijkstra()  # gets the list of all visited nodes
                        # this function accepts the color-code, list of nodes and changes the color of visited nodes
                        self.pathprint(7, g.visitednodes)
                        g.getshortestpath()  # gets the list of nodes leading to shortest path
                        self.pathprint(5, g.shortestpath)
                        pygame.event.clear()  # clears the event queue
                        # if any button is pressed during the execution of algorithm
                        # that event will be removed from event queue
                        # this avoids arbitrary functioning after the algorithm completes its process

                    elif self.bfsbutton.chechkifclicked():  # checks if the bfs button is pressed
                        self.cleargrid()
                        b = algorithms.Bfs(self.grid)
                        b.bfs()
                        self.pathprint(7, b.visitednodes)
                        b.getshortestpath()  # gets the list of nodes leading to shortest path
                        self.pathprint(5, b.shortestpath)  # '''
                        pygame.event.clear()  # clears the event queue

                    elif self.dfsbutton.chechkifclicked():  # checks if the bfs button is pressed
                        self.cleargrid()
                        d = algorithms.Dfs(self.grid)
                        d.dfs()
                        self.pathprint(7, d.visitednodes)
                        d.getshortestpath()  # gets the list of nodes leading to shortest path
                        self.pathprint(5, d.shortestpath)  # '''
                        pygame.event.clear()  # clears the event queue

                    elif self.astarbutton.chechkifclicked():  # checks if the bfs button is pressed
                        self.cleargrid()
                        d = algorithms.Astar(self.grid)
                        d.astar()
                        self.pathprint(7, d.visitednodes)
                        d.getshortestpath()  # gets the list of nodes leading to shortest path
                        self.pathprint(5, d.shortestpath)  # '''
                        pygame.event.clear()  # clears the event queue

                    elif self.resetbutton.chechkifclicked():
                        pygame.display.flip()
                        pygame.time.wait(100)  # add time delay
                        self.startnoderow = node.start_node_row
                        self.startnodecolumn = node.start_node_column
                        self.finishnoderow = node.finish_node_row
                        self.finishnodecolumn = node.finish_node_column
                        self.flag = 0
                        self.grid = []
                        self.creategrid()

                    else:
                        mousex, mousey = pygame.mouse.get_pos()  # gets the current coordinates of mouse
                        # by using mouse coordinates, it can be determined if any of the rectangle on screen is clicked
                        # the following function also returns the starting coordinates of particular rectangle
                        # if no rectangle is clicked it returns -1
                        currentx, currenty = self.get_rectanglepos(mousex, mousey)
                        # by using rectangle coordinates,
                        # the type of rectangle/node can be determined start-node, finish-node, normal nodes etc
                        # according to type of rectangle/node the flag value is set
                        self.flag = self.checknode(currentx, currenty)
                        if self.flag == 3:
                            cnode = self.getnode(currentx, currenty)  # gets the node related to rectangle
                            cnode.iswall = True  # sets the iswall attribute to true
                            self.drawrect(8, currentx, currenty)  # changes the color of rectangle

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and (self.flag == 1 or self.flag == 2):
                    # checks if mouse button is released
                    mousex, mousey = pygame.mouse.get_pos()  # gets the coordinates where mouse was released
                    newx, newy = self.get_rectanglepos(mousex, mousey)  # gets the coordinates of rectangle
                    if self.checknode(newx, newy) == 3:  # checks the type of node
                        self.setpos(newx, newy, currentx, currenty)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mousex, mousey = pygame.mouse.get_pos()
                    currentx, currenty = self.get_rectanglepos(mousex, mousey)
                    self.flag = self.checknode(currentx, currenty)
                    if self.flag == 3:
                        cnode = self.getnode(currentx, currenty)
                        cnode.isweight = True
                        self.drawrect(9, currentx, currenty)

    # setpos function accepts the following parameters
    # flag : type of node where mouse button was clicked
    # newx : x-coordinate of rectangle where mouse button was released
    # newy : y-coordinate of rectangle where mouse button was released
    # currentx : x-coordinate of rectangle where mouse button was pushed
    # currenty : y-coordinate of rectangle where mouse button was pushed
    # grid : grid of nodes/rectangles
    def setpos(self, newx, newy, currentx, currenty):
        self.drawrect(3, currentx, currenty)
        currentnode = self.getnode(currentx, currenty)
        self.drawrect(self.flag, newx, newy)
        newnode = self.getnode(newx, newy)
        row, column = self.getrowcolumn(newx, newy)
        if self.flag == 1:
            newnode.isstartnode = True  # sets the attributes accordingly
            currentnode.isstartnode = False
            self.startnoderow = row
            self.startnodecolumn = column

        elif self.flag == 2:
            newnode.isfinishnode = True
            currentnode.isfinishnode = False
            self.finishnoderow = row
            self.finishnodecolumn = column
        pygame.display.flip()

    # this function checks the type of node
    # the function accepts the x-coord and y-coord of rectangle/node and the grid
    def checknode(self, x, y):
        if x == -1 or y == -1:  # if  any of the value is -1, it returns 0
            return 0
        else:
            currentnode = self.getnode(x, y)  # gets the node
            if currentnode.isstartnode is True:  # if is is startnode return 1
                return 1
            elif currentnode.isfinishnode is True:  # is it is finishnode return 2
                return 2
            elif currentnode.isweight is False and currentnode.iswall is False:  # if it is normal node return 3
                return 3

    def getnode(self, x, y):  # function returns the node related to the rectangle, accepts x,y coord of rect and grid
        # by using coordinated derive the current row and column of node in grid
        currentrow, currentcolumn = self.getrowcolumn(x, y)
        for nodelist in self.grid:  # check the list match the row and column with the values in list
            for cnode in nodelist:
                if cnode.row == currentrow and cnode.column == currentcolumn:
                    return cnode

    def getrowcolumn(self, x, y):  # returns the row and column of rectangle, accepts x,y coordinate of rectangle
        # dimensions of rectangle are measured as follows
        # xcoordinate = (margin + width) * row + margin
        # ycoordinate = (margin + width) * column + margin
        # above formula can be tweaked to get row and column
        row = int((x - margin) / (margin + width))
        column = int((y - margin) / (margin + height))
        return row, column

    # function accepts the x,y coordinates of mouse and returns coordinates of rectangle
    def get_rectanglepos(self, mousex, mousey):
        # loop will check all possibilities of rectangle coordinates
        # if mouse coordinates lie between the rectangle coordinates
        # then those rectangle coordinates will be return
        # if none matches then -1 will be return
        for row in range(20):
            for column in range(20):
                rectx = (margin + width) * row + margin
                recty = (margin + height) * column + margin
                if rectx <= mousex <= rectx + width and recty <= mousey <= recty + height:
                    return rectx, recty
        return -1, -1

    # function checks the type of node and calls the function to draw rectangle
    def pathprint(self, flag, path):
        for rect in path:
            pygame.time.wait(10)
            if rect.isstartnode:
                cflag = 1
            elif rect.isfinishnode:
                cflag = 2
            else:
                cflag = flag
            self.drawrect(cflag, (margin + width) * rect.row + margin, (margin + height) * rect.column + margin)

    def drawrect(self, flag, x, y):  # function to draw rectangle, excepts color-code, x-coordinate and y-coordinate
        pygame.draw.rect(screen, color[flag], [x, y, width, height])  # inbuilt pygame function to create rectangles
        pygame.display.flip()  # updates the screen


class Button:  # class use to create buttons
    def __init__(self, bxcoord, bycoord, bwidth, bheight, bfontname, bfontsize, btext, bcolorcode, btextcolor):
        self.bxcoord = bxcoord  # x-coordinate
        self.bycoord = bycoord  # y-coordinate
        self.bwidth = bwidth  # width
        self.bheight = bheight  # height
        self.bfontname = bfontname  # fontname
        self.bfontsize = bfontsize  # fontsize
        self.btext = btext  # text on button
        self.bcolorcode = bcolorcode  # backgroundcolor
        self.btextcolor = btextcolor  # text color
        self.createbutton()  # calls the create button function

    def createbutton(self):  # function to create button
        pygame.draw.rect(screen, color[self.bcolorcode], [self.bxcoord, self.bycoord, self.bwidth, self.bheight])
        # create an instance for font object
        smalltext = pygame.font.SysFont(self.bfontname, self.bfontsize)
        # get the surface and and rectangle to store the text
        textsurf, textrect = self.text_objects(self.btext, smalltext)
        # align the rectangle
        textrect.center = (int(self.bxcoord + (self.bwidth / 2)), int(self.bycoord + (self.bheight / 2)))
        # blit draws one thing on another
        # here it draws the textsurface on textrect
        screen.blit(textsurf, textrect)

    # this function returns the surface fo text and a rectangle to hold text on surface
    def text_objects(self, text, font):
        # renders text on surface and returns the surface
        # the returned surface will be the dimensions required to hold the surface
        textsurface = font.render(text, True, color[self.btextcolor])
        # textsurface provides the dimensions
        # while textsurface.get_rect() provides the rectangle to store
        # finally returns the surface (variable = textsurface)
        # textsurface.get_rect() creates returns a new rectangle covering the surface
        return textsurface, textsurface.get_rect()

    def chechkifclicked(self):  # checks if the button is clicked
        mousex, mousey = pygame.mouse.get_pos()  # gets the x and y coordinates of mouse's current position
        # if the position of mouse is within the button does the stuff and returns 1 else returns 0
        if self.bxcoord <= mousex <= self.bxcoord + self.bwidth and self.bycoord <= mousey <= self.bycoord + self.bheight:
            self.bcolorcode = 1  # colorcode is changed
            self.createbutton()  # button is recreated with new color
            pygame.display.flip()
            pygame.time.wait(50)
            self.bcolorcode = 6  # colorcode is changed
            self.createbutton()  # button is recreated with new color
            return 1
        return 0


if __name__ == '__main__':
    game = Game()
    game.rungame()
