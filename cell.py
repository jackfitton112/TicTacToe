import pygame as pg
from config import config


class cell:

    # Constructor
    def __init__(self, row, col, color, margin, marginColor, width, height):
        self.row = row
        self.col = col
        self.color = color
        self.margin = margin
        self.marginColor = marginColor
        self.width = width
        self.height = height
        self.x = False
        self.o = False
        self.score = 0



    # Getters
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def getColor(self):
        return self.color
    
    def getMargin(self):
        return self.margin
    
    def getMarginColor(self):
        return self.marginColor
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    # Setters
    def setRow(self, row):
        self.row = row

    def setCol(self, col):
        self.col = col

    def setColor(self, color):
        self.color = color

    def setMargin(self, margin):
        self.margin = margin

    def setMarginColor(self, marginColor):
        self.marginColor = marginColor

    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height

    # Functions

    # Draw the cell
    def draw(self, screen):
        #draw cell with cell color and margin color
        pg.draw.rect(screen, self.color, [(self.margin + self.width) * self.col + self.margin, (self.margin + self.height) * self.row + self.margin, self.width, self.height])
        #draw margin
        pg.draw.rect(screen, self.marginColor, [(self.margin + self.width) * self.col + self.margin, (self.margin + self.height) * self.row + self.margin, self.width, self.height], self.margin)

        if self.x == True:
            pg.draw.line(screen, config.RED, [(self.margin + self.width) * self.col + self.margin, (self.margin + self.height) * self.row + self.margin], [(self.margin + self.width) * self.col + self.margin + self.width, (self.margin + self.height) * self.row + self.margin + self.height], 5)
            pg.draw.line(screen, config.RED, [(self.margin + self.width) * self.col + self.margin, (self.margin + self.height) * self.row + self.margin + self.height], [(self.margin + self.width) * self.col + self.margin + self.width, (self.margin + self.height) * self.row + self.margin], 5)
            self.score = 1

        if self.o == True:
            pg.draw.circle(screen, config.RED, [(self.margin + self.width) * self.col + self.margin + self.width // 2, (self.margin + self.height) * self.row + self.margin + self.height // 2], self.width // 2, 5)
            self.score = -1

    def toggleColor(self, screen):

        return

        #TODO: Implement this function

        # Set the colors
        BLACK = config.BLACK
        WHITE = config.WHITE
        RED = config.RED

        if self.color == WHITE:
            self.color = RED
        elif self.color == RED:
            self.color = BLACK
        elif self.color == BLACK:
            self.color = WHITE

        #if black, make margin white
        if self.color == BLACK:
            self.marginColor = WHITE


        self.draw(screen)

    

        
