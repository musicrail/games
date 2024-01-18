import random
import pygame

class Cube:
  def __init__(self, position, color) -> None:
    self.position = position
    self.color = color

  def draw(self, surface, cube_size):
    pygame.draw.rect(surface, self.color, ((self.position[0]*cube_size, self.position[-1]*cube_size), (cube_size-2, cube_size-2)))

class Figure:
  def __init__(self, matrix: list[list[bool]], spawn_middle, color) -> None:
    self.moving = True
    self.color = color
    self.cube_matrix = self._create_cube_matrix(matrix, spawn_middle)
    self.four_sites = self._create_four_sites(matrix, spawn_middle)

    
  def _create_cube_matrix(self, matrix, spawn_middle) -> list[list[Cube]]:
    figure_middle = len(matrix[-1]) // 2
    if len(matrix) > 1:
      top_right = (spawn_middle[0] - 1, spawn_middle[1] - figure_middle)
    else:
      top_right = (spawn_middle[0], spawn_middle[1] - figure_middle)
    for row in range(len(matrix)):
      for field in range(len(matrix[-1])):
        if matrix[row][field]:
          position = (top_right[0] + field, top_right[1] + row)
          matrix[row][field] = Cube(position, self.color)
    return matrix

  def _create_four_sites(self, matrix, spawn_middle) -> dict[int, list[list[Cube]]]:
    rotate180 = lambda matrix: [[field for field in reversed(row)] for row in reversed(matrix)]
    def rotate90(matrix: list[list]):
      rotated_matrix = list()
      for column in range(len(matrix[-1])):
        rotated_matrix_row = list()
        for row in range(len(matrix)):
          cube = matrix[row][column]
          rotated_matrix_row.append(cube)
        rotated_matrix.append(list(reversed(rotated_matrix_row)))
      return rotated_matrix
    
    return {0: self._create_cube_matrix(matrix, spawn_middle),
            1: self._create_cube_matrix(rotate90(matrix), spawn_middle),
            2: self._create_cube_matrix(rotate180(matrix), spawn_middle),
            3: self._create_cube_matrix(rotate180(rotate90(matrix)), spawn_middle)}

  def move(self):
    pass

  def draw(self):
    pass


class Game_Window:
  # andere idee: statt game_matrix, einfach eine liste von cubes, die gerade zu sehen sind 
  # (denn ein cube hat schließlich bereits eine position)
  def __init__(self, width, height, cube_size) -> None:
    # 1111
    line = [[True, True, True, True]]
    # 111
    # 100
    letter_l = [[True, True, True],[True, False, False]]

    self.figures = {1: line, 2: letter_l}
    self.figure = None

    self.width = width
    self.height = height
    self.cube_size = cube_size
    self.row = [None for i in range(self.width)]
    self.game_matrix = [self.row[:] for i in range(self.height)]
  
  def spawn(self):
    figure_index, figure = random.choice(list(self.figures.items()))
    x = self.width // 2
    y = 1
    spawn_middle = (x, y)
    self.figure = Figure(figure, spawn_middle, (255,0,0))
    # write the coordinates of the figure onto the game_matrix
    cubes: list[Cube] = list()
    for row in self.figure.cube_matrix:
      cubes.extend([field for field in row if field])
    for cube in cubes:
      x, y = cube.position
      self.game_matrix[y][x] = cube


  def check_lines(self):
    for index, row in enumerate(self.game_matrix):
      if all(row):
        self.game_matrix.pop(index)
        self.game_matrix.append(self.row[:])

  def draw(self, surface):
    for i in self.game_matrix:
      for j in i:
        if j:
          j.draw(surface, self.cube_size)
  

class Window:
  def __init__(self) -> None:
    self.cube_size = 20
    self.main_game_width = 10
    self.main_game_height = 20
    self.main_game = Game_Window(self.main_game_width, self.main_game_height, self.cube_size)
    self.window = pygame.display.set_mode((200,400))

  def run(self):
    running = True
    while running:
      if self.main_game.figure and self.main_game.figure.moving:
        self.main_game.figure.move()
      else:
        self.main_game.spawn()
      self.main_game.draw(self.window)
      self.window.fill((255,255,255))
      pygame.display.update()

def figure_test():
  f = Figure([[1,1,1],[0,0,1]], ((10,1)), (255,0,0))
  print(f.cube_matrix)
  translation_f = lambda x: [list(map(lambda c: c.position if c else 0, row)) for row in x]
  print(translation_f(f.cube_matrix))
  fours = [translation_f(i) for i in f.four_sites.values()]
  print(fours)

if __name__ == "__main__":
  Window().run()