
import sys
import random
import pygame
from pygame import draw, init
import pygame.freetype
from Tile import Tile

# TODO: mine generation at first click to make sure you start on an empty space
#       - record tile that was clicked on
#       - generate random position of mines
#       - regenerate position if it lands on a previous mine
#         or in a 3x3 box around the tile that was clicked
# TODO: buttons to start/new game instead of quitting the whole program
# TODO: display flag counter on screen
# TODO: adjust board size and mine density in game
# TODO: make it prettier
# TODO: you lose/you win message on screen instead of print
# TODO: time to completion
# TODO: time leaderboard
# TODO: make it less CPU intense?


class Minesweeper:

  def __init__(self):

    # game constants
    self.WIDTH = 20
    self.HEIGHT = 10
    self.SQUARE_SIZE = 30
    self.NUM_MINES = 30
    self.FONT_SIZE = 30
    self.BLACK = 0, 0, 0
    self.RED = 255, 0, 0
    self.WHITE = 255, 255, 255
    self.BACKGROUND = 200, 200, 200

    # setup pygame
    pygame.init()
    self.game_font = pygame.freetype.SysFont('ubuntu', self.FONT_SIZE)
    size = self.WIDTH * self.SQUARE_SIZE, self.HEIGHT * self.SQUARE_SIZE
    self.screen = pygame.display.set_mode(size)
    self.screen.fill(self.BACKGROUND)

    # init board
    self.board = [[Tile() for i in range(self.HEIGHT)]
                  for j in range(self.WIDTH)]

    # counters
    self.flags_used = 0
    self.revealed_tiles = 0

  def get_rect(self, i, j):
    return pygame.Rect(i*self.SQUARE_SIZE, j*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)

  def write_to_tile(self, i, j, text, color):
    text_rect = self.game_font.get_rect(text)
    text_rect.center = self.get_rect(i, j).center
    self.game_font.render_to(self.screen, text_rect, text, color)

  def on_board(self, i, j):
    return i in range(len(self.board)) and j in range(len(self.board[0]))

  def get_surrounding_tiles(self, i, j):
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
    return [coord for coord in coords if self.on_board(*coord)]

  def fill_tile_values(self):
    for i in range(len(self.board)):
      for j in range(len(self.board[0])):
        if not self.board[i][j].is_mine():
          count = 0
          for r, c in self.get_surrounding_tiles(i, j):
            if self.board[r][c].is_mine():
              count += 1

          if count != 0:
            self.board[i][j].value = str(count)

  # TODO: make colors constants

  def draw_hidden_tile(self, i, j):
    pygame.draw.rect(self.screen, self.BACKGROUND, self.get_rect(i, j))
    pygame.draw.rect(self.screen, self.BLACK, self.get_rect(i, j), 1)

  # TODO: store color in class and compute it in prepare board

  def draw_revealed_tile(self, i, j):
    mines = self.board[i][j].value
    if mines == '1':
      color = (0, 0, 255)

    elif mines == '2':
      color = (0, 255, 0)

    elif mines == '3':
      color = (200, 200, 0)

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
    pygame.draw.rect(self.screen, self.WHITE, self.get_rect(i, j))
    pygame.draw.rect(self.screen, self.BLACK, self.get_rect(i, j), 1)
    self.write_to_tile(i, j, mines, color)
    self.board[i][j].revealed = True

  def reveal_tile(self, i, j):
    self.draw_revealed_tile(i, j)
    self.revealed_tiles += 1

    # if an empty space was revealed, recursively reveal all surrounding tiles
    # do not reveal flagged tiles
    if self.board[i][j].value == ' ':
      for r, c in self.get_surrounding_tiles(i, j):
        if not self.board[r][c].revealed and not self.board[r][c].flagged:
          self.reveal_tile(r, c)

  def draw_flagged_tile(self, i, j):
    pygame.draw.rect(self.screen, self.RED, self.get_rect(i, j))
    pygame.draw.rect(self.screen, self.BLACK, self.get_rect(i, j), 1)

  def place_mines(self, initial_i, initial_j):
    # add mines randomly, avoiding the 3x3 area around where the player first clicked
    starting_tiles = self.get_surrounding_tiles(initial_i, initial_j)

    mines = self.NUM_MINES
    while mines > 0:
      x = random.randrange(0, self.WIDTH)
      y = random.randrange(0, self.HEIGHT)
      if not self.board[x][y].is_mine() and not (x, y) in starting_tiles:
        self.board[x][y].value = 'x'
        mines -= 1


  def run_game(self):
    mines_placed = False
    
    # draw board
    for i in range(len(self.board)):
      for j in range(len(self.board[0])):
        pygame.draw.rect(self.screen, self.BLACK, self.get_rect(i, j), 1)
        
    # game event loop
    while True:
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
          mouse_location = pygame.mouse.get_pos()
          button = event.button

          # find the tile that was clicked on
          for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
              square = self.get_rect(i, j)
              if square.collidepoint(mouse_location):

                # left click
                if button == 1:

                  # left clicking on a flagged tile does nothing
                  if tile.flagged:
                    continue

                  # game over if a mine is clicked
                  if tile.is_mine():
                    print('you clicked on a mine, you lose')
                    sys.exit()

                  else:
                    # when the player reveals the first tile, place mines
                    if not mines_placed:
                      self.place_mines(i, j)
                      self.fill_tile_values()
                      mines_placed = True
                      
                    self.reveal_tile(i, j)

                # right click
                elif button == 3:

                  # you can only flag tiles that arent revealed
                  if not tile.revealed:

                    # right clicking on an already flagged tile unflags it
                    if tile.flagged:
                      tile.flagged = False
                      self.flags_used -= 1
                      self.draw_hidden_tile(i, j)

                    else:
                      tile.flagged = True
                      self.flags_used += 1
                      self.draw_flagged_tile(i, j)

          # print(f"revealed tiles: {self.revealed_tiles}")
          print(f"flags used: {self.flags_used}")

          # if all possible tiles have been revealed, you win
          if self.revealed_tiles == (self.WIDTH * self.HEIGHT) - self.NUM_MINES:
            print('you win!')
            sys.exit()


game = Minesweeper()
game.run_game()
