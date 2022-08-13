from turtle import Screen, speed, update
import pygame as pg
import random as rd
import time
from dataclasses import dataclass

pg.init()  # initialize all imported pygame modules
width, columns, rows = 400, 15, 30
distance = width // columns  # size image squares
height = distance * rows
grild = [0]*columns*rows
speed = 1000

# load image
picture = []
for i in range(8):
    picture.append(pg.transform.scale(
        pg.image.load(f'T{i}.jpg'), (distance, distance)))

screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')

# create event
tetromino_down = pg.USEREVENT + 1
speed_up = pg.USEREVENT + 2

# repeatedly create an event on the event queue
pg.time.set_timer(tetromino_down, speed)
pg.time.set_timer(speed_up, 30000)
pg.key.set_repeat(200, 100)   # control how held keys are repeated

# tetromino for letters O,I,J,L,S,Z,T (https://en.wikipedia.org/wiki/Tetromino)
tetrominos = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # O
              [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # I
              [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0],  # J
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
                y = (self.row + n//4) * distance
                screen.blit(picture[color], (x, y))

    def check(self, r, c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                rs = r + n//4
                cs = c + n % 4
                if cs < 0 or rs >= rows or cs >= columns or grild[rs * columns + cs] > 0:
                    return False
        return True

    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c
            return True
        return False

    def rotate(self):
        clonetetro = self.tetro.copy()
        for n, color in enumerate(clonetetro):
            self.tetro[(2-(n % 4))*4+(n//4)] = color
        if not self.check(self.row, self.column):
            self.tetro = clonetetro.copy()


character = tetromino(tetrominos[2])

status = True
while status:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        if event.type == tetromino_down:
            character.update(1, 0)
        if event.type == speed_up:
            speed = int(speed * 0.7)
            pg.time.set_timer(tetromino_down, speed)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                character.update(0, -1)
            if event.key == pg.K_RIGHT:
                character.update(0, 1)
            if event.key == pg.K_DOWN:
                character.update(1, 0)
            if event.key == pg.K_SPACE:
                character.rotate()

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
