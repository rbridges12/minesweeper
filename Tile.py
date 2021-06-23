
class Tile:
  def __init__(self):
      self.value = ' '
      self.flagged = False
      self.revealed = False

  def is_mine(self):
     return self.value == 'x'
