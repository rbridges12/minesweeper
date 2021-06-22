from os import write
import sys
import random
import pygame
import pygame.freetype

# game constants
WIDTH = 10
HEIGHT = 10
SQUARE_SIZE = 30
NUM_MINES = 20
FONT_SIZE = 30
BLACK = 0, 0, 0
RED = 255, 0, 0
BACKGROUND = 200, 200, 200


# setup pygame window
pygame.init()
size = WIDTH * SQUARE_SIZE, HEIGHT * SQUARE_SIZE
screen = pygame.display.set_mode(size)
screen.fill(BACKGROUND)

GAME_FONT = pygame.freetype.SysFont('ubuntu', FONT_SIZE)

# init board
board = [[' ' for i in range(WIDTH)] for j in range(HEIGHT)]


def get_rect(i, j):
    return pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)


def write_to_tile(i, j, text, color):
    text_rect = GAME_FONT.get_rect(text)
    text_rect.center = get_rect(i, j).center
    GAME_FONT.render_to(screen, text_rect, text, color)


def on_board(i, j):
    return i in range(len(board)) and j in range(len(board[0]))


def get_surrounding_tiles(i, j):
    coords = [
        (i-1, j-1),
        (i-1, j),
        (i-1, j+1),
        (i, j-1),
        (i, j+1),
        (i+1, j-1),
        (i+1, j),
        (i+1, j+1)]

    return [board[row][col] for row, col in coords if on_board(row, col)]


def fill_board():
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 'x':
                count = 0
                for tile in get_surrounding_tiles(i, j):
                    if tile == 'x':
                        count += 1

                if count != 0:
                    board[i][j] = str(count)

# TODO: make colors constants
def draw_tile(i, j):
    mines = board[i][j]
    if mines == '1':
        color = (0, 0, 255)

    elif mines == '2':
        color = (0, 255, 0)

    elif mines == '3':
        color = (255, 255, 0)

    elif mines == '4':
        color = (255, 0, 255)

    elif mines == '5':
        color = (255, 0, 0)

    elif mines == '6':
        color = (0, 255, 255)

    elif mines == '7':
        color = (0, 0, 0)

    else:
        color = (128, 128, 128)

    write_to_tile(i, j, mines, color)


def mark_mine(i, j):
  pygame.draw.rect(screen, RED, get_rect(i, j))

# add mines randomly
mines = NUM_MINES
while mines > 0:
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    if board[x][y] != 'x':
        board[x][y] = 'x'
        mines -= 1

fill_board()

# draw board
for i in range(len(board)):
    for j in range(len(board[0])):
        pygame.draw.rect(screen, BLACK, get_rect(i, j), 1)


# GAME_FONT.render_to(screen, (0, 0), 'test', (0, 0, 0))
# write_to_tile(3, 4, "X", (0, 100, 0))

pygame.display.flip()

# game event loop
while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_location = pygame.mouse.get_pos()
            button = event.button

            # left click
            if button == 1:
              for i, row in enumerate(board):
                  for j, square_contents in enumerate(row):
                      square = get_rect(i, j)
                      if square.collidepoint(mouse_location):

                          # mine
                          if square_contents == 'x':
                              print('you clicked on a mine, you lose')
                              sys.exit()

                          # empty space
                          elif square_contents == '0':
                              # reveal then check surrounding tiles to see if they need to be revealed
                              pass

                          # space next to mine
                          else:
                              draw_tile(i, j)
            
            # right click
            elif button == 3:


