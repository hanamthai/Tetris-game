from distutils.ccompiler import show_compilers
import pygame as pg
import random as rd
import time
from dataclasses import dataclass

pg.init()  # initialize all imported pygame modules
width, columns, rows = 400, 15, 30
distance = width // columns  # size image squares
height = distance * rows
grid = [0]*columns*rows
speed, score, level = 1000, 0, 0

# read file highest-score
try:
    file1 = open("highest-score.txt", "r")
except:
    print("File don't exist!!")
    pg.quit()
    quit()
highestScore = int(file1.read())
file1.close()

# add background music
backgroundMusic = pg.mixer.music.load("sound-game/soundtrack.mp3")
# start music and The -1 value tells Pygame to loop the music file infinitely.
pg.mixer.music.play(-1)
# add other musics
levelUp = pg.mixer.Sound('sound-game/level-up.mp3')
increaseScore = pg.mixer.Sound('sound-game/increase-score.mp3')
game_Over = pg.mixer.Sound('sound-game/game-over.mp3')


# load image
picture = []
for i in range(8):
    picture.append(pg.transform.scale(
        pg.image.load(f'image/T{i}.jpg'), (distance, distance)))

screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')
pygame_icon = pg.image.load('image/tetris-icon.png')
pg.display.set_icon(pygame_icon)

# create event
tetromino_down = pg.USEREVENT + 1

# repeatedly create an event on the event queue
pg.time.set_timer(tetromino_down, speed)
pg.key.set_repeat(300, 100)   # control how held keys are repeated

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

    # create a frame that limits the movement of square.
    def check(self, r, c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                cs = c + n % 4
                rs = r + n//4
                if cs < 0 or rs >= rows or cs >= columns or grid[rs * columns + cs] > 0:
                    return False
        return True

    # move the square block to the right, left or down
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


# save square block on grid
def OjectOnGridLine():
    for n, color in enumerate(character.tetro):
        if color > 0:
            grid[(character.row + n//4)*columns +
                 (character.column + n % 4)] = color


def DeleteOnRow():
    scoreX2 = 0
    for row in range(rows):
        for column in range(columns):
            if grid[row * columns + column] == 0:
                break
        else:
            del grid[row * columns: row * columns + column]
            grid[0:0] = [0]*columns
            scoreX2 += 1
            pg.mixer.Sound.play(increaseScore)
    # If you delete 2 lines or more, your score will increase to an exponential 2 times.
    if scoreX2 > 1:
        global score
        score += scoreX2 ** 2 * 100
        print(score)
    elif scoreX2 == 1:
        score += scoreX2 * 100
        print(score)


# Pause Game
def pauseGame():
    pause = True
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        textsurface = pg.font.SysFont(f'consolas', 40).render(
            'PAUSE GAME', True, (255, 255, 255))
        screen.blit(textsurface, (width // 2 -
                    textsurface.get_width() // 2, 300))
        textsurface = pg.font.SysFont(f'consolas', 20).render(
            'press P to play', False, (255, 255, 255))
        screen.blit(textsurface, (width // 2 -
                    textsurface.get_width() // 2, 350))
        pg.display.update()  # it allows only a portion of the screen to updated


# Game Over
def gameOver():
    for column in range(columns):
        if grid[column] != 0:
            endGame = True
            pg.mixer.music.stop()
            pg.mixer.Sound.play(game_Over)
            while endGame:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_q:
                            endGame = False
                            pg.quit()
                            quit()
                global score
                global highestScore
                if score > highestScore:
                    try:
                        file1 = open("highest-score.txt", "w")
                    except:
                        print("File don't exist!!")
                        pg.quit()
                        quit()
                    highestScore = score
                    file1.write(str(highestScore))
                    file1.close()
                screen.fill((128, 128, 128))  # background color
                textsurface = pg.font.SysFont(f'consolas', 50).render(
                    'GAME OVER', True, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 250))
                textsurface = pg.font.SysFont(f'consolas', 30).render(
                    f'Your score: {score}', False, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 300))
                textsurface = pg.font.SysFont(f'consolas', 30).render(
                    f'Your level: {level}', False, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 350))
                textsurface = pg.font.SysFont(f'consolas', 20).render(
                    'press Q to quit', False, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 400))
                textsurface = pg.font.SysFont(f'consolas', 40).render(
                    f'Highest score: {highestScore}', False, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 500))
                pg.display.update()


character = tetromino(rd.choice(tetrominos))

status = True
while status:
    # pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        if event.type == tetromino_down:
            if not character.update(1, 0):
                OjectOnGridLine()
                character = tetromino(rd.choice(tetrominos))
                DeleteOnRow()
                if (score // 500) != level:
                    # [This is not a bug, it's a feature :) ]if you delete more and more rows at once the speed will increase slower.
                    speed = int(speed * 0.7)
                    pg.time.set_timer(tetromino_down, speed)
                    level = score // 500
                    pg.mixer.Sound.play(levelUp)
                gameOver()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                character.update(0, -1)
            if event.key == pg.K_RIGHT:
                character.update(0, 1)
            if event.key == pg.K_DOWN:
                character.update(1, 0)
            if event.key == pg.K_SPACE:
                character.rotate()
            if event.key == pg.K_p:
                pauseGame()

    screen.fill((128, 128, 128))  # background color
    character.show()
    textsurface = pg.font.SysFont(f'consolas', 40).render(
        f'{score:,}', False, (255, 255, 255))
    screen.blit(textsurface, (width // 2 - textsurface.get_width() // 2, 5))
    textsurface = pg.font.SysFont(f'consolas', 20).render(
        f'Level: {level}', False, (255, 255, 255))
    screen.blit(textsurface, (width // 2 - textsurface.get_width() // 2, 55))
    for i, color in enumerate(grid):
        if color > 0:
            x = i % columns * distance  # coordinates of the square
            y = i // columns * distance
            # used to draw one surface onto another surface
            screen.blit(picture[color], (x, y))
    pg.display.flip()   # update all screen (pg.display.update())
pg.quit()
