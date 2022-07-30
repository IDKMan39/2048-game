# Notes
# [[a],[b],[c]]
# on screen it will look like :
#   A -->
#   B -->
#   C --

### Self.x == number of rows (down)
### Self.y == number of columbs (across)


import pygame
import keyboard
import random
import time
import turtle
import random
from pygame import mixer
import copy
pygame.init()

def is_integer(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True


def compilelistofzeros(matrix):
    possiblelist = []
    x = len(matrix)
    y = len(matrix[1])
    for i in range(x):
        for b in range(y):
            if matrix[i][b] == 0:
                possiblelist.append([i,b])
    print(possiblelist)
    if len(possiblelist) == 0:
        if checkpossibles(matrix,possiblelist) == 0:
            return "finish"
        else :
            return possiblelist
    else:
        return possiblelist

def checkpossibles(matrix,possiblelist):
    x = len(matrix)
    y = len(matrix[1])
    possibles = 0
    if len(possiblelist) == 0 :
        print("InLoop")
        for i in range(x):
            for b in range(y):
                if i == x-1 and b == y-1 :
                    pass
                elif i == x-1 :
                    if matrix[i][b] == matrix[i][b+1] :
                        possibles +=1
                elif b == y-1 :
                    if matrix[i][b] == matrix[i+1][b] :
                        possibles +=1
                elif matrix[i][b] == matrix[i][b+1] or matrix[i][b] == matrix[i+1][b] :
                    possibles +=1
    return possibles

class Matrix:
    def __init__(self,screen,x=4,y=4,):
        self.x = x
        self.y = y
        self.matrix = []
        self.screen = screen
        for item in range(x):
            self.matrix.append([0]*y)
        self.state = "On"
    def startup(self) :
        Draw(self.matrix,self.screen).drawgrid()
        self.add2or4()
        self.add2or4()

        Draw(self.matrix,self.screen).reloadsquares()

    def move(self,identifier) :
        if self.state == "On" :

            justskipped = False
            checkmatrix = copy.deepcopy(self.matrix)
            # Code taking direction and assigning variables
            if identifier == "down" or  identifier == "up":
                rangeforb = self.y
                whatminuszero = self.x
            elif identifier == "left" or  identifier == "right" :
                rangeforb = self.x
                whatminuszero = self.y

            if identifier == "down":
                rangeforix = self.x-1
                rangeforiy = -1
                rangeforiz = -1
            elif identifier == "up" :
                rangeforix = 0
                rangeforiy = self.x
                rangeforiz = 1
            elif identifier == "left" :
                rangeforix = 0
                rangeforiy = self.y
                rangeforiz = 1
            elif identifier == "right" :
                rangeforix = self.y-1
                rangeforiy = -1
                rangeforiz = -1

            #-------
            #code creates a list (present) that will at the end have the numbers from top to bottom
            for b in range(rangeforb):
                present = []
                justskipped = False
                for i in range(rangeforix,rangeforiy,rangeforiz):
                    if identifier == "up" or  identifier == "down" :
                        currentindex = self.matrix[i][b] # << Something about this
                    elif identifier == "left" or  identifier == "right" :
                        currentindex = self.matrix[b][i] # << Something about this

                    # so it will go 1,1 2,1, 3,1
                    # 3,1 2,1 1,1
                    if currentindex != 0:
                        if present == [] :
                            present.append(currentindex)
                        else :
                            if present[-1]== currentindex:
                                if justskipped == False :
                                    justskipped = True
                                    present[-1] = 2*present[-1]
                                else :
                                    justskipped = False
                                    present.append(currentindex)

                            elif present[-1] != currentindex :
                                present.append(currentindex)
                amountofzeros = whatminuszero - len(present)
                for i in range(amountofzeros) :
                    present.append(0)

                for i in range(rangeforix,rangeforiy,rangeforiz) :
                    if identifier == "up":
                        self.matrix[i][b] = present[i] # << Something about this
                    elif identifier == "down":
                        self.matrix[i][b] = present[-1*abs(i+1)] # << Something about this
                    elif identifier == "left":
                        self.matrix[b][i] = present[i]
                    elif identifier == "right":
                        self.matrix[b][i] = present[-1*abs(i+1)]
            Draw(self.matrix,self.screen).reloadsquares()
            pygame.display.update()
            time.sleep(.15)
            #present lists are for each column -- formatted with only numbers ex. [2,4] goes bottom up
            #below i must reinput the numbers for each columb after it has been gravitied

            if self.add2or4(checkmatrix) != "finish" :
                Draw(self.matrix,self.screen).reloadsquares()
            else :
                self.state = "off"
                Draw(self.matrix,self.screen).finish()


            pygame.display.update()


    def add2or4(self,checkmatrix=1):
        #Possible amount of combines on the board rn
        possibles = 0
        #Zeros
        possiblelist = compilelistofzeros(self.matrix)
        if possiblelist != "finish" and self.matrix != checkmatrix :
            if len(possiblelist) != 0:
                b = random.randint(0,len(possiblelist)-1)
                i = random.randint(1,4)

                if i == 1 or i == 2 or i == 3 :
                    self.matrix[possiblelist[b][0]][possiblelist[b][1]] = 2
                else :
                    self.matrix[possiblelist[b][0]][possiblelist[b][1]] = 4
                pygame.display.update()

        elif possiblelist == "finish":
            return "finish"




class Draw:
    def __init__(self,matrix,screen) :
        self.color = (210,0,225)
        self.matrix = matrix
        self.x = len(matrix)
        self.y = len(matrix[0])
        self.screen = screen
        self.colordict = {
        0 : (205, 193, 180),
        2 : (238, 228, 218),
        4 : (238, 225, 201),
        8 : (243, 178, 122),
        16 : (246, 150, 100),
        32 : (247, 124, 95),
        64 : (247, 95, 59),
        128 : (237, 208, 115)
        }

        self.font = pygame.font.SysFont(None, 70)

    def drawgrid(self) :
        #First I have to draw a square
        pygame.draw.rect(self.screen, (0,0,0), (40,40,600,600),1)
        pygame.display.update()

        # top left corner
        pygame.draw.circle(self.screen, (187, 173, 160), (40,40),4)

        # top right
        pygame.draw.circle(self.screen, (187, 173, 160), (640,40),4)

        # bottom left
        pygame.draw.circle(self.screen, (187, 173, 160), (40,640),4)

        # bottom right
        pygame.draw.circle(self.screen, (187, 173, 160), (640,640),4)

        pygame.display.update()

        #40 - 640
        for i in range(1,self.y+1):
            #pygame.draw.rect(self.screen, (187, 173, 160), (i*colspaces+40,40,10,600))
            pygame.draw.rect(self.screen, (187, 173, 160), (40,40,i*(600/self.y),600),10)
        for i in range(1,self.x+1):
            #pygame.draw.rect(self.screen, (187, 173, 160), (i*colspaces+40,40,10,600))
            pygame.draw.rect(self.screen, (187, 173, 160), (40,40,600,i*(600/self.x)),10)
        pygame.display.update()

    def reloadsquares(self):
        #startsquare = 45,45
        x = 0
        y = 0
        for i in range(self.y):
            if i != 0 :
                x += (600/self.y)
            y = 0
            for b in range(self.x):
                pygame.draw.rect(self.screen,(0,0,0),(45+x,45+y,(600/self.y),(600/self.x)))
                currentindex = self.matrix[b][i]
                try:
                    colorofbox = self.colordict[currentindex]
                except Exception as e:
                    colorofbox = (10,10,10)


                pygame.draw.rect(self.screen,colorofbox,(45+x,45+y,(600/self.y)-10,(600/self.x)-10))

                if currentindex == 2 or currentindex == 4 :
                    text = self.font.render(str(currentindex), 1,(119, 110, 101))
                elif currentindex == 0 :
                    text = self.font.render("", 1,(119, 110, 101))
                else :
                    text = self.font.render(str(currentindex), 1,(255,255,255))
                self.screen.blit(text, (45+x+(.5*600/self.y)-20,45+y+(.5*600/self.x)-20))
                pygame.display.update()
                y += (600/self.x)

    def finish(self) :
        screen.fill((255,255,255))
        text = self.font.render("You Lost", 1, (0,0,0))
        self.screen.blit(text, (200,300))

global running
running = True
key = ""
screen = pygame.display.set_mode((900,800))
pygame.display.set_caption("Something")
screen.fill((255,255,255))
pygame.display.update()


x = input("x integer \n\t> ")
y = int(input("y integer \n\t> "))
if is_integer(x) and is_integer(y):
    arrayobj = Matrix(screen,int(x),int(y))
    arrayobj.startup()
else :
    print("sus")

while running:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                print(mouse_x,mouse_y)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key = "left"
                arrayobj.move("left")
            elif event.key == pygame.K_RIGHT:
                key = "right"
                arrayobj.move("right")
            elif event.key == pygame.K_UP:
                key = "up"
                arrayobj.move("up")

            elif event.key == pygame.K_DOWN:
                key = "down"
                arrayobj.move("down")
            else :
                key = ""
            if key != "" :
                print(key)


    pygame.display.update()
