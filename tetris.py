from turtle import Screen
import pygame as pg
import random as rd
import time

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
grild[0] = 2
grild[1] = 2

status = True
while status:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
    screen.fill((128, 128, 128))  # background color
    for i, color in enumerate(grild):
        if color > 0:
            x = i % columns * distance  # coordinates of the square
            y = i // columns * distance
            # used to draw one surface onto another surface
            screen.blit(picture[color], (x, y))
    pg.display.flip()   # update all screen (pg.display.update())
pg.quit()
