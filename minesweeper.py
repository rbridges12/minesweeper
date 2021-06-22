import  sys, pygame, random

# game constants
WIDTH = 10
HEIGHT = 10
SQUARE_SIZE = 30
NUM_MINES = 20
BLACK = 0, 0, 0
WHITE = 255, 255, 255

def get_rect(i, j):
  return pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

def draw_tile()

# setup pygame window
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('')
size = WIDTH * SQUARE_SIZE, HEIGHT * SQUARE_SIZE
screen = pygame.display.set_mode(size)
screen.fill(WHITE)

# init board
board = [['0' for i in range(WIDTH)] for j in range(HEIGHT)]

# add mines randomly
mines = NUM_MINES
while mines > 0:
  x = random.randrange(0, WIDTH)
  y = random.randrange(0, HEIGHT)
  if board[x][y] != 'x':
    board[x][y] = 'x'
    mines -= 1

# draw tiles
for i in range(len(board)):
  for j in range(len(board[0])):
    pygame.draw.rect(screen, BLACK, get_rect(i, j), 1)

pygame.display.flip()

# game event loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

    elif event.type == pygame.MOUSEBUTTONUP:
      mouse_location = pygame.mouse.get_pos()
      
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
              # reveal
              pass

            

  