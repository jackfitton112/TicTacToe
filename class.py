import pygame as pg
from config import config
from cell import cell
from random import randint
import time

config = config()


def algorithm(grid: list) -> None:

    rows = config.ROWS
    cols = config.COLS


    scoreCard = []
    score = 0
    for row in range(0, rows):
        for col in range(0, cols):
            score += grid[row][col].score

        #ALL ROWS
        scoreCard.append(score)
        score = 0

    for col in range(0, cols):
        for row in range(0, rows):
            score += grid[row][col].score

        #ALL COLUMNS
        scoreCard.append(score)
        score = 0

    #DIAGONAL 1
    for row in range(0, rows):
        score += grid[row][row].score

    scoreCard.append(score)
    score = 0

    #DIAGONAL 2
    for row in range(0, rows):
        score += grid[row][rows - row - 1].score
    
    scoreCard.append(score)
    score = 0


    if rows in scoreCard:
        print("X wins")
        return True
    
    elif -rows in scoreCard:
        print("O wins")
        return True

    #check if there are any empty cells
    elif not(checkEmptyCells()):
        print("Tie")
        return True
    
    else:
        return False

def isCellEmpty(row: int, col: int) -> bool:
    #check if cell is empty
    if grid[row][col].x or grid[row][col].o:
        return False
    return True

def drawX(row: int, col: int) -> None:
    #draw an X on the cell
    grid[row][col].x = True
    grid[row][col].draw(screen)

def drawO(row: int, col: int) -> None:
    #draw an O on the cell
    grid[row][col].o = True
    grid[row][col].draw(screen)

def computerPlayerTurn() -> None:
    #picks random cell, if cell is already taken, pick another cell

    #pick a random cell
    row = randint(0, config.ROWS - 1)
    col = randint(0, config.COLS - 1)

    if not(isCellEmpty(row, col)):
        computerPlayerTurn()
        return


    if config.player == "X":
        #computer is O
        drawO(row, col)

    if config.player == "O":
        #computer is X
        drawX(row, col)

    return 

def playerTurn() -> None:

    #check cell is empty
    pos = pg.mouse.get_pos()
    col = pos[0] // (grid[0][0].getWidth() + grid[0][0].getMargin())
    row = pos[1] // (grid[0][0].getHeight() + grid[0][0].getMargin())

    if config.player == "X" and isCellEmpty(row, col):
        drawX(row, col)
        return True

    elif config.player == "O" and isCellEmpty(row, col):
        drawO(row, col)
        return True
    
    else:
        return False

def generateGrid() -> list:

    # number of rows and columns
    ROWS = config.ROWS
    COLS = config.COLS

    WIDTH = config.WINDOW_SIZE[0] // ROWS
    HEIGHT = config.WINDOW_SIZE[1] // COLS

    # Set the margin between each cell
    MARGIN = config.MARGIN

    # Set the colors
    BLACK = config.BLACK
    WHITE = config.WHITE


    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    grid = []

    # Loop for each row and create an object for each cell
    for row in range(ROWS):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(COLS):
            grid[row].append(cell(row, column, WHITE, MARGIN, BLACK, WIDTH, HEIGHT))

    #draw the grid
    for row in range(ROWS):
        for column in range(COLS):
            grid[row][column].draw(screen)

    

    return grid

def toggleCell() -> None:
    pos = pg.mouse.get_pos()
    col = pos[0] // (grid[0][0].getWidth() + grid[0][0].getMargin())
    row = pos[1] // (grid[0][0].getHeight() + grid[0][0].getMargin())

    current = [row, col]

    if not(current in PreviousCells):
        PreviousCells.append(current)
        toggleCell([row, col])


    grid[row][col].toggleColor(screen)

def checkEmptyCells() -> bool:

    #check if there are any empty cells
    for row in range(config.ROWS):
        for col in range(config.COLS):
            if not(grid[row][col].x or grid[row][col].o):
                return True
    
    return False

def setup() -> object:
    #setup pygame
    pg.init()

    #set the window size
    screen = pg.display.set_mode(config.WINDOW_SIZE)

    #set the window title
    pg.display.set_caption("Tic Tac Toe")

    return screen

screen = setup()
grid = generateGrid()


IS_RUNNING = True
mousePrevState = False
PreviousCells = []
gameScore = []
turn = True

#update the screen
pg.display.update()
pg.display.flip()

# Loop until the user clicks the close button.
while IS_RUNNING:

    #if x is pressed or the user clicks the close button or esc is pressed
    for event in pg.event.get():

        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            IS_RUNNING = False

    
    #check if the mouse is pressed down and if the mouse was not pressed down in the previous frame
    if pg.mouse.get_pressed()[0] and not(mousePrevState):

        if playerTurn():
            mousePrevState = True
            turn = False
        else:
            print("Cell is already taken")
            mousePrevState = True


    
    #if mouse is not pressed down
    if not(pg.mouse.get_pressed()[0]):
        mousePrevState = False

        if not(turn):
            computerPlayerTurn()
            turn = True
            
            continue
            

    




    if algorithm(grid):
        IS_RUNNING = False

    #update the screen
    pg.display.update()

  