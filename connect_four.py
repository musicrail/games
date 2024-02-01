from itertools import chain

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
    """
    
    position: (column, index)  # both are in range(Window.rows)
    """
    self.columnWidth = width // rows
    self.radius = self.columnWidth // 2
    self.x = self.columnWidth * position[0] + self.radius
    self.y = self.columnWidth * (rows - 1 - position[1]) + self.radius
    self.coords = (self.x, self.y)
    self.player = player
    self.position = position

  def draw(self, surface, color=None, shade=1):
    if color is None:
      color = self.player.color
    pygame.draw.circle(surface, tuple(map(lambda x: int(x*shade), color)), self.coords, self.radius-4)

class Window:
  """"""
  def __init__(self, players: list[Player]) -> None:
    self.rows = 5
    self.coin_matrix: list[list[Coin]] = [[None for _ in range(self.rows)] for _ in range(self.rows)]  # coin-matrix represents the window
    self.width = 600
    self.height = self.width
    self.surface = pygame.display.set_mode((self.width, self.height))
    self.players = players
    self.active_player, self.inactive_player = self.players
    self.winner = None
    self.winning_positions = None

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

  def update(self):
    self.surface.fill((255,255,255))
    self.draw_grid()
    self.draw_matrix()
    if self.winning_positions is not None:
      for coin in self.winning_positions:
        coin.draw(self.surface, shade=0.5)
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
 
  def check_for_gameover(self):
    """Check for a winner or a full coin_matrix."""
    self._check_for_win()
    if self.winner is not None:
      return self.winner.name
    if all([all(column) for column in self.coin_matrix]):
      return "game over"
    return None

  def _check_for_win(self) -> Player:
    """Calls self._check on every Coin in the coin_matrix."""
    for field in chain.from_iterable(self.coin_matrix):
      if field is not None:
        self._check(field, list(), self.coin_matrix)
    return None
  
  def _check(self, coin_field: Coin, store: list[Coin], matrix: list[list[Coin]], direction: tuple[int, int] = (0,0)):
    """Checks for a winning line and sets self.winner."""
    store = store.copy()
    store.append(coin_field)
    if len(store) >= 4:
      self.winning_positions = store.copy()
      self.winner = coin_field.player
    valid_range = range(len(matrix))
    x_coin_field = coin_field.position[0]
    y_coin_field = coin_field.position[1]
    if direction == (0,0):
      for x in range(-1,2):
        for y in range(-1,2):
          x_neighbor = x_coin_field + x
          y_neighbor = y_coin_field + y
          if x == 0 and y == 0:
            continue
          if x_neighbor not in valid_range or y_neighbor not in valid_range:
            continue
          neighbor = matrix[x_neighbor][y_neighbor]
          if neighbor is None or neighbor.player != coin_field.player:
            continue
          self._check(neighbor, store, matrix, direction=(x,y))
    else:
      x_neighbor = x_coin_field + direction[0]
      y_neighbor = y_coin_field + direction[1]
      if x_neighbor not in valid_range or y_neighbor not in valid_range:
        return None
      neighbor = matrix[x_neighbor][y_neighbor]
      if neighbor is None or neighbor.player != store[-1].player:
        return None
      self._check(neighbor, store, matrix, direction=direction)
    return None

  def reset(self):
    self.winning_positions = None
    self.winner = None
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
    gameover = window.check_for_gameover()
    window.update()
    if gameover is not None:
      print(gameover)
      pygame.time.delay(2000)
      window.reset()




if __name__ == "__main__":
  main()