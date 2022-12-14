from turtle import update
import pygame as pg
import random as rd
import time
from dataclasses import dataclass

pg.init()  # initialize all imported pygame modules
width, columns, rows, add = 390, 15, 30, 6
distance = width // columns  # size image squares = 26
height = distance * rows  # 780
grid = [0]*columns*rows
speed, score, level = 800, 0, 0

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
level_up = pg.mixer.Sound('sound-game/level-up.mp3')
increaseScore = pg.mixer.Sound('sound-game/increase-score.mp3')
game_Over = pg.mixer.Sound('sound-game/game-over.mp3')


# load image
picture = []
# for i in range(8):
#     picture.append(pg.transform.scale(
#         pg.image.load(f'image/T{i}.jpg'), (distance, distance)))

picture = [(pg.transform.scale(pg.image.load(
    f'image/T{i}.jpg'), (distance, distance))) for i in range(8)]   # use list comprehension

screen = pg.display.set_mode([width+(add*26), height])
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

    # rotate the tetrominos blocks.
    def rotate(self):
        clonetetro = self.tetro.copy()
        for n, color in enumerate(clonetetro):
            self.tetro[(2-(n % 4))*4+(n//4)] = color
        if not self.check(self.row, self.column):
            self.tetro = clonetetro.copy()


# draw the frame
def drawFrame():
    for i in range(rows):
        screen.blit(picture[0], (columns*distance, i*distance))


# draw the next tetromino
def drawNextTetromino(next_tetromino):
    for n, color in enumerate(next_tetromino):
        if color > 0:
            x = ((columns + 1) + n % 4) * distance  # column = 31
            y = (1 + n//4) * distance   # row = 0
            screen.blit(picture[color], (x, y))


# Save square block on grid
def OjectOnGridLine():
    for n, color in enumerate(character.tetro):
        if color > 0:
            grid[(character.row + n//4)*columns +
                 (character.column + n % 4)] = color


# Calculate the score received
def scoreCalculate(scoreX2):
    # If you delete 2 lines or more, your score will increase to an exponential 2 times.
    if scoreX2 > 1:
        global score
        score += scoreX2 ** 2 * 100
        print(score)
    elif scoreX2 == 1:
        score += scoreX2 * 100
        print(score)


# Check if there are enough score to level up
def levelUp():
    global score
    global level
    global speed
    if (score // 500) != level:
        # [This is not a bug, it's a feature :) ]if you delete more and more rows at once the speed will increase slower.
        speed = int(speed * 0.7)
        pg.time.set_timer(tetromino_down, speed)
        level = score // 500
        pg.mixer.Sound.play(level_up)


# Delete all filled rows
def DeleteOnRow():
    scoreX2 = 0
    for row in range(rows):
        for column in range(columns):
            if grid[row * columns + column] == 0:
                break
        else:
            del grid[row * columns: row * columns + column + 1]
            grid[0:0] = [0]*columns
            scoreX2 += 1
            pg.mixer.Sound.play(increaseScore)

    scoreCalculate(scoreX2)


# Write to file txt
def writeFile():
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
                if event.key == pg.K_q:  # if you exit the game when you pause the game, the system will automatically check the score with the highest score to save in the file highest-score.txt
                    writeFile()
                    pg.quit()
                    quit()
        textsurface = pg.font.SysFont(f'consolas', 40).render(
            'PAUSE GAME', True, (255, 255, 255))
        screen.blit(textsurface, (width // 2 -
                    textsurface.get_width() // 2, 300))
        textsurface = pg.font.SysFont(f'consolas', 20).render(
            'press P to play or press Q to quit', False, (255, 255, 255))
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
                writeFile()

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
                textsurface = pg.font.SysFont(f'consolas', 30).render(
                    f'Highest score: {highestScore}', False, (255, 255, 255))
                screen.blit(textsurface, (width // 2 -
                            textsurface.get_width() // 2, 450))
                pg.display.update()


character = tetromino(rd.choice(tetrominos))
next_tetromino = (rd.choice(tetrominos)).copy()
print(type(next_tetromino))

status = True
while status:
    # pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        if event.type == tetromino_down:
            if not character.update(1, 0):
                OjectOnGridLine()
                character = tetromino(next_tetromino)
                next_tetromino = rd.choice(tetrominos)
                DeleteOnRow()
                levelUp()
                gameOver()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                character.update(0, -1)
            if event.key == pg.K_RIGHT:
                character.update(0, 1)
            if event.key == pg.K_UP:
                while(1):
                    if not character.update(1, 0):
                        break
            if event.key == pg.K_DOWN:
                character.update(1, 0)
            if event.key == pg.K_SPACE:
                character.rotate()
            if event.key == pg.K_p:
                pauseGame()

    screen.fill((128, 128, 128))  # background color
    drawFrame()
    drawNextTetromino(next_tetromino)
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
