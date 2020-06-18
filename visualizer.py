import pygame
import node
import djikstra

pygame.init()  # creates pygame instance
screen = pygame.display.set_mode((510, 600))  # sets the size of window
pygame.display.set_caption("Path Visualizer")  # sets the title

# following is the dictionary containing colors
color = {1: [0, 128, 0],  # green
         2: [128, 0, 0],  # red
         3: [0, 0, 0],  # black
         4: [255, 255, 255],  # white
         5: [0, 0, 128],  # blue
         6: [42, 53, 61],  # darkgrayblack
         7: [200, 200, 200],  # silver
         8: [255, 255, 0]}  # yellow

# following are global variables used to create rectanlugar objects
width = 20
height = 20
margin = 5

screen.fill(color[4])  # fills the screen background with color from dictionary


def drawrect(flag, x, y):  # function to draw rectangle, excpts colorcode, x-coordinate and y-coordinate
    pygame.draw.rect(screen, color[flag], [x, y, width, height])  # inbuilt pygame function to create rectangles
    pygame.display.flip()  # updates the screen


def main():  # function to create basic structre of window
    grid = []  # array to hold rectangles
    for row in range(20):  # loop creating reactangles
        rows = []
        for column in range(20):
            flag = 3
            # checks the row and column matches the variables
            if row == node.start_node_row and column == node.start_node_column:
                flag = 1  # if it matches then sets the flag accordingly
            elif row == node.finish_node_row and column == node.finish_node_column:
                flag = 2
                # calls the draw rect function
            drawrect(flag, (margin + width) * row + margin, (margin + height) * column + margin)
            rows.append(node.createnode(row, column))  # appends the reactangle in row
        grid.append(rows)  # appends the row in grid

    djikstrabutton = Button(250, 550, 65, 30, 'arial', 20, 'Djikstra', 6, 7)
    # creates the button instance djikstra"s algorithm
    # accepts x,y coords, width, height, fontname, fontsize, buttontext, backgroundcolor,
    # text color accordingly as parameter
    resetbutton = Button(350, 550, 65, 30, 'arial', 20, 'Reset', 6, 7)  # creates the  button instance for reset button
    pygame.display.flip()
    rungame(djikstrabutton, resetbutton, grid)  # calls the rungame function


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
        # get the surface and and rectangle to store the surface
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
        # while textsurface.get_rect() provides the rectagnle to store
        # finally returns the surface (variable = textsurface)
        # textsurface.get_rect() creates returns a new rectangle covering the surface
        return textsurface, textsurface.get_rect()

    def chechkifclicked(self):  # checks if the button is clicked
        mousex, mousey = pygame.mouse.get_pos()  # gets the x and y coordinates of mouse's current position
        # if the position of mouse is within the button does the stuff and returns 1 else returns 0
        if self.bxcoord <= mousex <= self.bxcoord + self.bwidth and self.bycoord <= mousey <= self.bycoord + self.bheight:
            self.bcolorcode = 1  # colorcode is changed
            self.createbutton()  # button is recreated with new color
            return 1
        return 0


def rungame(dijkstrabutton, resetbutton, grid):  # this function contains main while loop to run the game
    running = True  # variable is use to keep loop running
    # following variables will used in program for different purposes
    flag = 0
    currentx = 0
    currenty = 0
    while running:
        for event in pygame.event.get():  # checks for the evnet
            if event.type == pygame.QUIT:  # if evnet type is quit, then proceed to quit the window
                pygame.quit()  # end the pygame instance
                quit()  # closes the window

            if event.type == pygame.MOUSEBUTTONDOWN:  # checks if mouse button is pressed
                if dijkstrabutton.chechkifclicked():  # checks if the djikstra button is pressed
                    g = djikstra.Graph(400)  # creates an instance of class graph from djikstra  module
                    g.grid = grid.copy()  # copies the grid into graph instance
                    path = g.dijkstra()  # gets the list of all visited nodes
                    # this function accepts the colorcode, list of nodes and changes the color of visited nodes
                    pathprint(7, path)
                    path = g.getshortestpath()  # gets the list of nodes leading to shortest path
                    pathprint(5, path)  #
                    pygame.event.clear()  # clears the event queue
                    # if any button is pressed during the execution of algorithm
                    # that event will be removed from event queue
                    # this avoids arbitrary functioning after the algorithm completes its process

                elif resetbutton.chechkifclicked():  # checks if reset button is clicked
                    pygame.display.flip()
                    pygame.time.wait(100)  # add time delay
                    main()  # calls the main function

                else:
                    mousex, mousey = pygame.mouse.get_pos()  # gets the current coordinates of mouse
                    # by using mouse coordinates, it can be determined if any of the rectangle on screen is clicked
                    # the following function also returns the starting coordinates of particular rectangle
                    # if no rectangle is clicked it returns -1
                    currentx, currenty = get_rectanglepos(mousex, mousey)
                    # by using rectangle coordinates,
                    # the type of rectangle/node can be determined startnode, finishnode, normal nodes etc
                    # according to type of rectangle/node the flag value is set
                    flag = checknode(currentx, currenty, grid)

            if flag == 3:
                cnode = getnode(currentx, currenty, grid)  # gets the node related to rectangle
                cnode.iswall = True  # sets the iswall attribute to true
                drawrect(8, currentx, currenty)  # changes the color of rectangle

            elif flag == 1 or flag == 2:
                if event.type == pygame.MOUSEBUTTONUP:  # checks if mouse button is released
                    mousex, mousey = pygame.mouse.get_pos()  # gets the coordinates where mouse was released
                    newx, newy = get_rectanglepos(mousex, mousey)  # gets the coordinates of rectangle
                    if checknode(newx, newy, grid) == 3:  # checks the type of node
                        setpos(flag, newx, newy, currentx, currenty, grid)


# setpos function accepts the following parameters
# flag : type of node where mouse button was clicked
# newx : x-coordinate of rectangle where mouse button was released
# newy : y-coordinate of rectangle where mouse button was released
# currentx : x-coordinate of rectangle where mouse button was pushed
# currenty : y-coordinate of rectangle where mouse button was pushed
# grid : grid of nodes/rectangles
def setpos(flag, newx, newy, currentx, currenty, grid):
    drawrect(3, currentx, currenty)
    currentnode = getnode(currentx, currenty, grid)
    drawrect(flag, newx, newy)
    newnode = getnode(newx, newy, grid)
    if flag == 1:
        newnode.isstartnode = True  # sets the attributes accordingly
        currentnode.isstartnode = False
    elif flag == 2:
        newnode.isfinishnode = True
        currentnode.isfinishnode = False
    pygame.display.flip()


# this function checks the type of node
# the function accepts the x-coord and y-coord of rectangle/node and the grid
def checknode(x, y, grid):
    if x == -1 or y == -1:  # if  any of the value is -1, it returns 0
        return 0
    else:
        currentnode = getnode(x, y, grid)  # gets the node
        if currentnode.isstartnode:  # if is is staratnode return 1
            return 1
        elif currentnode.isfinishnode:  # is it is finishnode return 2
            return 2
        else:  # if it is normal node return 3
            return 3


def getnode(x, y, grid):  # function returns the node related to the rectangle, accepts x,y coord of rectangle and grid
    # by using coordinated derive the current row and column of node in grid
    currentrow, currentcolumn = getrowcolumn(x, y)
    for nodelist in grid:  # check the list match the row and column with the values in list
        for cnode in nodelist:
            if cnode.row == currentrow and cnode.column == currentcolumn:
                return cnode


def getrowcolumn(x, y):  # returns the row and column of rectangle, accepts x,y coordinate of rectangle
    # dimensions of rectangle are measured as follows
    # xcoordinate = (margin + width) * row + margin
    # ycoordinate = (margin + width) * column + margin
    # above formula can be tweaked to get row and column
    row = int((x - margin) / (margin + width))
    column = int((y - margin) / (margin + height))
    return row, column


# function accepts the x,y coordinates of mouse and returns coordinates of rectangle
def get_rectanglepos(mousex, mousey):
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


# function checks the type of node and calls the fucntion to draw rectangle
def pathprint(flag, path):
    for rect in path:
        pygame.time.wait(10)
        if rect.isstartnode:
            cflag = 1
        elif rect.isfinishnode:
            cflag = 2
        else:
            cflag = flag
        drawrect(cflag, (margin + width) * rect.row + margin, (margin + height) * rect.column + margin)


if __name__ == '__main__':
    main()
