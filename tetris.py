from turtle import Screen
import pygame as pg
import random as rd
import time

pg.init()  # initialize all imported pygame modules
width, columns, rows = 400, 15, 30
distance = width // columns  # size image squares
height = distance * rows

screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')

status = True
while status:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False

pg.quit()
