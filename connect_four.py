import pygame

"""
TODO: a way to check for wins is missing

and there isn't yet a good way to play (choose players, name them, show the winner, etc.)
"""

class Player:
  def __init__(self, color, name) -> None:
    self.color = color
    self.name = name

class Coin:
  def __init__(self, width, rows, position, player: Player) -> None:
    self.columnWidth = width // rows
    self.radius = self.columnWidth // 2
    self.x = self.columnWidth * position[0] + self.radius
    self.y = self.columnWidth * (rows - 1 - position[1]) + self.radius
    self.coords = (self.x, self.y)
    self.player = player

  def draw(self, surface):
    pygame.draw.circle(surface, self.player.color, self.coords, self.radius-4)

class Window:
  def __init__(self, players: list[Player]) -> None:
    self.rows = 5
    self.coin_matrix: list[list[Coin]] = [[None for _ in range(self.rows)] for _ in range(self.rows)]  # coin-matrix represents the window
    self.width = 600
    self.height = self.width
    self.surface = pygame.display.set_mode((self.width, self.height))
    self.players = players
    self.active_player, self.inactive_player = self.players

  def draw_grid(self):
    rectSize = self.width // self.rows
    x, y = 0, 0
    for row in range(self.rows):
      x += rectSize
      y += rectSize
      pygame.draw.line(self.surface, (0,0,0), (x, 0), (x, self.width))
      pygame.draw.line(self.surface, (0,0,0), (0, y), (self.width, y))

  def draw_matrix(self):
    for column in self.coin_matrix:
      for coin in column:
        if coin is not None:
          coin.draw(self.surface)

  def draw(self):
    self.surface.fill((255,255,255))
    self.draw_grid()
    self.draw_matrix()
    pygame.display.update()

  def listen_for_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    buttons = pygame.mouse.get_pressed()
    if any(buttons):
      x, _ = pygame.mouse.get_pos()
      columnWidth = self.width // self.rows
      column = x // columnWidth
      if None not in self.coin_matrix[column]:
        print("column is full")
      for index, row in enumerate(self.coin_matrix[column]):
        if row is None:
          self.coin_matrix[column][index] = Coin(self.width, self.rows, (column, index), self.active_player)
          self.active_player, self.inactive_player = self.inactive_player, self.active_player
          break

  def check_for_win(self):
    coin_matrix = [map(lambda z: True if z.player == self.active_player else None, column) for column in self.coin_matrix]
    transposed_matrix = 0

    # quick reminder: the inner lists are the columns, i.e. coin_matrix[0][3] gets the 4th entry in the 1th column
    for column in self.coin_matrix:  # checks the columns for a winner
      last_coin_owner = None
      num = 0
      for index, coin_field in enumerate(column):
        if index > self.rows - 4 and not last_coin_owner:
          continue
        elif coin_field is None:
          last_coin_owner = None
          num = 0
        elif coin_field and last_coin_owner is None:
          last_coin_owner = coin_field.player
          num = 1
        elif coin_field and last_coin_owner == coin_field.player:
          num += 1
        elif coin_field and last_coin_owner != coin_field.player:
          last_coin_owner = None
          num = 0
        if num == 4:
          return last_coin_owner.name
    for r in range(self.rows):  # checks the rows for a winner
      last_coin_owner = None
      num = 0
      for c in range(self.rows):
        coin_field = self.coin_matrix[c][r]
        if c > self.rows - 4 and not last_coin_owner:
          continue
        elif coin_field is None:
          last_coin_owner = None
          num = 0
        elif coin_field and last_coin_owner is None:
          last_coin_owner = coin_field.player
          num = 1
        elif coin_field and last_coin_owner == coin_field.player:
          num += 1
        elif coin_field and last_coin_owner != coin_field.player:
          last_coin_owner = None
          num = 0
        if num == 4:
          return last_coin_owner.name
    
    # check for winner and show winner and return True
    if all([all(column) for column in self.coin_matrix]):
      print("game over")
      return True
  
  def reset(self):
    self.coin_matrix: list[list[Coin]] = [[None for _ in range(self.rows)] for _ in range(self.rows)]  # coin-matrix represents the window


def main():
  clock = pygame.time.Clock()
  player1 = Player((255,0,0), "amy")
  player2 = Player((0,255,0), "steve")
  window = Window([player1, player2])
  while True:
    pygame.time.delay(50)
    clock.tick(10)
    # TODO: make some kind of pause after a mouseclick. otherwise the game maybe take
    window.listen_for_input()
    window.draw()
    gameover = window.check_for_win()
    if gameover:
      print(gameover)
      pygame.time.delay(2000)
      window.reset()




if __name__ == "__main__":
  main()