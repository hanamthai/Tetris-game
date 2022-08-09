from turtle import Screen
import pygame as pg
import random as rd
import time
from dataclasses import dataclass

pg.init()  # initialize all imported pygame modules
width, columns, rows = 400, 15, 30
distance = width // columns  # size image squares
height = distance * rows
grild = [0]*columns*rows

# load image
picture = []
for i in range(8):
    picture.append(pg.transform.scale(
        pg.image.load(f'T{i}.jpg'), (distance, distance)))

screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')

# tetromino for letters O,I,J,L,S,Z,T (https://en.wikipedia.org/wiki/Tetromino)
tetrominos = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # O
              [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # I
              [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # J
              [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # L
              [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # S
              [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Z
              [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]]  # T

# create class and define function


@dataclass
class tetromino():
    tetro: list
    row: int = 0    # create coordinates that start to fall
    column: int = 5

    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n % 4) * distance
                y = (self.column + n//4) * distance
                screen.blit(picture[color], (x, y))


character = tetromino(tetrominos[6])

status = True
while status:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
    screen.fill((128, 128, 128))  # background color
    character.show()
    for i, color in enumerate(grild):
        if color > 0:
            x = i % columns * distance  # coordinates of the square
            y = i // columns * distance
            # used to draw one surface onto another surface
            screen.blit(picture[color], (x, y))
    pg.display.flip()   # update all screen (pg.display.update())
pg.quit()
