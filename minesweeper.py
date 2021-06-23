from os import write
import sys
import random
import pygame
from pygame import draw
import pygame.freetype
from Tile import Tile

# game constants
WIDTH = 10
HEIGHT = 10
SQUARE_SIZE = 30
NUM_MINES = 20
FONT_SIZE = 30
BLACK = 0, 0, 0
RED = 255, 0, 0
WHITE = 255, 255, 255
BACKGROUND = 200, 200, 200


# setup pygame window
pygame.init()
size = WIDTH * SQUARE_SIZE, HEIGHT * SQUARE_SIZE
screen = pygame.display.set_mode(size)
screen.fill(BACKGROUND)

GAME_FONT = pygame.freetype.SysFont('ubuntu', FONT_SIZE)

# init board
board = [[Tile() for i in range(WIDTH)] for j in range(HEIGHT)]


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

  # return [board[row][col] for row, col in coords if on_board(row, col)]
  return [coord for coord in coords if on_board(*coord)]


def fill_board():
  for i in range(len(board)):
    for j in range(len(board[0])):
      if not board[i][j].is_mine():
        count = 0
        for r, c in get_surrounding_tiles(i, j):
          if board[r][c].is_mine():
            count += 1

        if count != 0:
          board[i][j].value = str(count)

# TODO: make colors constants


def draw_hidden_tile(i, j):
  pygame.draw.rect(screen, BACKGROUND, get_rect(i, j))
  pygame.draw.rect(screen, BLACK, get_rect(i, j), 1)


# TODO: store color in class and compute it in prepare board
def draw_revealed_tile(i, j):
  mines = board[i][j].value
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

  # make tile white, then write number to it
  pygame.draw.rect(screen, WHITE, get_rect(i, j))
  pygame.draw.rect(screen, BLACK, get_rect(i, j), 1)
  write_to_tile(i, j, mines, color)
  board[i][j].revealed = True


def reveal_tile(i, j):
  print(i, j)
  print(board[i][j].value)
  draw_revealed_tile(i, j)
  if board[i][j].value == ' ':
    for r, c in get_surrounding_tiles(i,j):
      if not board[r][c].revealed:
        reveal_tile(r, c)
    
    

def mark_mine(i, j):
  pygame.draw.rect(screen, RED, get_rect(i, j))


# add mines randomly
mines = NUM_MINES
while mines > 0:
  x = random.randrange(0, WIDTH)
  y = random.randrange(0, HEIGHT)
  if not board[x][y].is_mine():
    board[x][y].value = 'x'
    mines -= 1

fill_board()

# draw board
for i in range(len(board)):
  for j in range(len(board[0])):
    pygame.draw.rect(screen, BLACK, get_rect(i, j), 1)


# GAME_FONT.render_to(screen, (0, 0), 'test', (0, 0, 0))
# write_to_tile(3, 4, "X", (0, 100, 0))
# mark_mine(4, 7)

# pygame.display.flip()

# game event loop
while True:
  pygame.display.flip()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    elif event.type == pygame.MOUSEBUTTONUP:
      mouse_location = pygame.mouse.get_pos()
      button = event.button

      for i, row in enumerate(board):
        for j, tile in enumerate(row):
          square = get_rect(i, j)
          if square.collidepoint(mouse_location):

            # left click
            if button == 1:
              
              # left clicking on a flagged tile does nothing
              if tile.flagged:
                continue

              # game over if mine is clicked
              if tile.is_mine():
                print('you clicked on a mine, you lose')
                sys.exit()

              # # TODO: empty space
              # elif tile.value == '0':
              #   # reveal then check surrounding tiles to see if they need to be revealed
              #   pass

              # space next to mine
              else:
                reveal_tile(i, j)

            # right click
            elif button == 3:
              
              # you can only flag tiles that arent revealed
              if not tile.revealed:
                
                # right clicking on an already flagged tile unflags it
                if tile.flagged:
                  tile.flagged = False
                  draw_hidden_tile(i, j)
                  
                else:
                  tile.flagged = True
                  mark_mine(i, j)
