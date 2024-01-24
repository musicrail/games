import random
import pygame
import pprint
import sys     #test
from decorators import *

class Cube:
  def __init__(self, position, color) -> None:
    self.position = position  # position := (x, y)
    self.color = color
    self.active = True
  
  def __str__(self) -> str:
    if self.active == False:
      return "0"
    else:
      return "1"

  def draw(self, surface, cube_size):
    pygame.draw.rect(surface, self.color, ((self.position[0]*cube_size+1, self.position[-1]*cube_size+1), (cube_size-2, cube_size-2)))

class Figure:
  def __init__(self, matrix: list[list[bool]], pivot:tuple[int,int], color, mapping, has_x_sides=4) -> None:
    self.matrix = matrix
    self.color = color
    self.pivot = pivot
    self.mapping = mapping
    if has_x_sides == 1:
      self.restrict_rotation = {"restrict_rotation": True, "turns": 0}
    elif has_x_sides == 2:
      self.restrict_rotation = {"restrict_rotation": True, "turns": 3}
    else:
      self.restrict_rotation = {"restrict_rotation": False}

  def init(self, spawn):
    self.cube_matrix = self._create_cube_matrix(self.matrix, spawn)
  
  def rotate_90(self):
    x_pivot, y_pivot = self.cube_matrix[self.pivot[1]][self.pivot[0]].position
    for x in range(len(self.cube_matrix[0])):
      for y in range(len(self.cube_matrix)):
        if self.cube_matrix[y][x]:
          x_cube, y_cube = self.cube_matrix[y][x].position
          #print("x,y", x, y)
          #print(x_cube-x_pivot, y_cube-y_pivot)
          direction_x, direction_y = self.mapping[(x_cube - x_pivot, y_cube - y_pivot)]
          #print(direction_x, direction_y)
          #print("alte position", x_cube, y_cube)
          #print("neue position", x_cube + direction_x, y_cube + direction_y)
          #print("...")
          self.cube_matrix[y][x].position = (x_cube + direction_x, y_cube + direction_y)

  @property
  def cubes(self) -> list[Cube]:
    flattened_cube_matrix = list()
    for row in self.cube_matrix:
      flattened_cube_matrix.extend(row)
    flattened_cube_matrix = [field for field in flattened_cube_matrix if field]
    return flattened_cube_matrix

  def _create_cube_matrix(self, matrix, spawn) -> list[list[Cube]]:  #spawn_middle := (x, y) , e.g. (10, 1)
    figure_middle = len(matrix[-1]) // 2
    if len(matrix) > 1:
      top_right = (spawn[0] - figure_middle, spawn[1] - 1)
    else:
      top_right = (spawn[0] - figure_middle, spawn[1])
    for row in range(len(matrix)):
      for field in range(len(matrix[-1])):
        if matrix[row][field]:
          position = (top_right[0] + field, top_right[1] + row)
          matrix[row][field] = Cube(position, self.color)
    return matrix

  def update(self, directionX=0, directionY=0, rotate=False):
    if rotate:
      if self.restrict_rotation["restrict_rotation"] and self.restrict_rotation["turns"] == 0:
        pass
      elif self.restrict_rotation["restrict_rotation"] and self.restrict_rotation["turns"] == 1:
        self.rotate_90()
        self.restrict_rotation["turns"] = 3
      elif self.restrict_rotation["restrict_rotation"] and self.restrict_rotation["turns"] == 3:
        for _ in range(3):
          self.rotate_90()
        self.restrict_rotation["turns"] = 1
      else:
        self.rotate_90()

    for row in self.cube_matrix:
      for field in row:
        if field:
          field.position = (field.position[0] + directionX, field.position[1] + directionY)

  @classmethod
  def l(cls):
    """predefined L-figure"""
    matrix = [[1,1,1],[1,0,0]]
    pivot = (1,0)  # marks the pivot-position in the matrix
    color = (30,120,30)
    mapping = {(0,0):(0,0), (-1,1):(0,-2), (-1,0):(1,-1), (1,0):(-1,1), (0,1):(-1,-1), (0,-1):(1,1), (-1,-1):(2,0), (1,-1):(0,2), (1,1):(-2,0)}
    return cls(matrix, pivot, color, mapping)
  
  @classmethod
  def l_r(cls):
    matrix = [[1,1,1],[0,0,1]]
    pivot = (1,0)
    color = (120,120,30)
    mapping = {(0,0):(0,0), (-1,0):(1,-1), (0,-1):(1,1), (1,0):(-1,1), (0,1):(-1,-1), (1,1):(-2,0), (-1,1):(0,-2), (1,-1):(0,2), (-1,-1):(2,0)}
    return cls(matrix, pivot, color, mapping)
  
  @classmethod
  def halv_cross(cls):
    matrix = [[1,1,1],[0,1,0]]
    pivot = (1,0)
    color = (30,120,120)
    mapping = {(0,0):(0,0), (0,1):(-1,-1), (1,0):(-1,1), (-1,0):(1,-1), (0,-1):(1,1)}
    return cls(matrix, pivot, color, mapping)
  
  @classmethod
  def z(cls):
    matrix = [[0,1,1],[1,1,0]]
    pivot = (1,0)
    color = (30,30,120)
    mapping = {(0,0):(0,0), (0,1):(-1,-1), (-1,1):(0,-2), (1,0):(-1,1), (-1,0):(1,-1), (-1,-1):(2,0), (0,-1):(1,1), (1,-1):(0,2), (1,1):(-2,0)}
    return cls(matrix, pivot, color, mapping, has_x_sides=2)
  
  @classmethod
  def z_r(cls):
    matrix = [[1,1,0],[0,1,1]]
    pivot = (1,0)
    color = (30,30,30)
    mapping = {(-1,-1):(2,0), (-1,0):(1,-1), (-1,1):(0,-2), (0,-1):(1,1), (0,0):(0,0), (0,1):(-1,-1), (1,-1):(0,2), (1,0):(-1,1), (1,1):(-2,0)}
    # mapping = {(0,0):(0,0), (-1,0):(1,1), (0,1):(1,-1), (1,1):(0,-2), (1,-1):(0,2), (1,0):(-1,1), (0,1):(-1,-1)}
    return cls(matrix, pivot, color, mapping, has_x_sides=2)
  
  @classmethod
  def i(cls):
    matrix = [[1,1,1,1]]
    pivot = (1,0)
    color = (120,30,30)
    mapping={(0,0):(0,0), (-1,0):(1,-1), (1,0):(-1,1), (2,0):(-2,2), (0,-1):(-1,1), (0,1):(1,-1), (0,2):(2,-2)}
    return cls(matrix, pivot, color, mapping)
  
  @classmethod
  def o(cls):
    matrix = [[1,1],[1,1]]
    pivot = tuple()
    color = (120,120,120)
    mapping = dict()
    return cls(matrix, pivot, color, mapping, has_x_sides=1)

class Game_Window:
  # mapping: key   = the position of a cube relativ to the pivot
  #          value = the distance, that the cube moves (dx, dy)
  figures = [Figure.z(), Figure.z_r(), Figure.l(), Figure.l_r(), Figure.i(), Figure.o(), Figure.halv_cross()]

  def __init__(self, width, height, cube_size, surface) -> None:
    self.surface = surface
    self.active_figure = None
    self.move = 7
    self.speed = 8
    self.width = width
    self.height = height
    self.cube_size = cube_size
    self.spawn_point = (self.width//2, 1)
    self.game_row = [None for field in range(self.width)]
    self.cutline_at = 2
    self.init_game_matrix()
  
  def init_game_matrix(self):
    # [
    #  [X X X ...],
    #  [X X X ...],
    #  ...
    # ] 
    self.game_matrix: list[list[Cube]] = [self.game_row.copy() for _ in range(self.height)]

  def spawn(self):
    self.active_figure = random.choice(self.figures)
    self.active_figure.init(self.spawn_point)

  def check_lines(self):
    up = 0
    to_pop = list()
    for index, row in reversed(list(enumerate(self.game_matrix))):
      if up > 0:
        for field in row:
          if field and not field.active:
            field.position = (field.position[0], field.position[1] + up)
      row_copy = map(lambda c: not c.active if c else False, row.copy())
      if all(row_copy):
        to_pop.append(index)
        up += 1
    for pop in to_pop:
      self.game_matrix.pop(pop)
    for _ in range(len(to_pop)):
      self.game_matrix.insert(0, self.game_row.copy())

  def check_end(self):
    cut_line = map(lambda field: True if field and not field.active else False, self.game_matrix[self.cutline_at])
    if any(cut_line):
      self.game_over()

  @sleeper(sec=2)
  def game_over(self):
    # TODO: add some window or so to pop up
    self.init_game_matrix()

  def collide(self) -> (bool, bool):
    cube_positions = [cube.position for cube in self.active_figure.cubes]
    x_collide = y_collide = None
    for x, y in cube_positions:
      if y > self.height-1:
        y_collide = True
        return (x_collide, y_collide) 
      # if I turn the figure right after the spawn, I get a e.g. y=-1
      #   which means I have a valid index for the game_matrix, but I don't get the behavior I want
      if x > self.width-1 or x < 0 or y < 0:
        x_collide = True
        return (x_collide, False)
      
      if not x_collide and self.game_matrix[y][x] and not self.game_matrix[y][x].active:
        x_collide = True
        y_collide = True
        return (x_collide, y_collide)
    return (False, False)

  def settle(self):
    self.map()
    for row in self.active_figure.cube_matrix:
      for field in row:
        if field:
          field.active = False
    
    self.spawn()

  def map(self):
    """maps active_figure onto the game_matrix"""
    for y in range(self.height):
      for x in range(self.width):
        if self.game_matrix[y][x] and self.game_matrix[y][x].active:
          self.game_matrix[y][x] = None
        for cube in self.active_figure.cubes:
          if (x, y) == cube.position:
            self.game_matrix[y][x] = cube

  def update(self):
    """spawns new figures and controls keyboard input"""
    if not self.active_figure:
      self.spawn()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
      self.active_figure.update(rotate=True)
      x_collide, y_collide = self.collide()
      if x_collide or y_collide:
        for _ in range(3):
          self.active_figure.update(rotate=True)
      if y_collide:
        self.settle()
    x_collide = y_collide = False
    if keys[pygame.K_LEFT]:
      self.active_figure.update(directionX=-1)
      x_collide, _ = self.collide()
      if x_collide:
        self.active_figure.update(directionX=1)
    x_collide = y_collide = False
    if keys[pygame.K_RIGHT]:
      self.active_figure.update(directionX=1)
      x_collide, _ = self.collide()
      if x_collide:
        self.active_figure.update(directionX=-1)
    x_collide = y_collide = False
    if keys[pygame.K_DOWN]:
      self.active_figure.update(directionY=1)
      self.move = 0
      _, y_collide = self.collide()
      if y_collide:
        self.active_figure.update(directionY=-1)
        self.settle()
    x_collide = y_collide = False

    if self.move > self.speed:
      self.active_figure.update(directionY=1)
      _, y_collide = self.collide()
      if y_collide:
        self.active_figure.update(directionY=-1)
        self.settle()
      self.move = 0
    else:
      self.move += 1

    self.map()
    
    pp = pprint.PrettyPrinter(width=160)
    for row in self.game_matrix:
      row2 = row.copy()
      row2 = list(map(lambda x: str(x) if x != None else " ", row2))
      pp.pprint(row2)
    # pp.pprint([[str(j) for j in i] for i in self.game_matrix])
    print("-"*30)

    self.check_lines()
    self.check_end()
    self.draw()
    


  def draw(self):
    """just draws the game_matrix"""
    for row in self.game_matrix:
      for field in row:
        if field:
          field.draw(self.surface, self.cube_size)
  

class Window:
  def __init__(self) -> None:
    self.cube_size = 20
    self.main_game_width = 10
    self.main_game_height = 20
    self.window = pygame.display.set_mode((200,400))
    self.main_game = Game_Window(self.main_game_width, self.main_game_height, self.cube_size, self.window)
  
  def run(self):
    running = True
    clock = pygame.time.Clock()
    fps = 10

    while running:
      self.window.fill((0,0,0))
      clock.tick(fps)
      self.main_game.update()
      pygame.display.update()

      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
      

def figure_test():
  f = Figure([[True,True,True],[True, False, False]], ((10,1)), (255,0,0))
  print(f.cube_matrix)
  translation_f = lambda x: [list(map(lambda c: c.position if c else 0, row)) for row in x]
  print(translation_f(f.cube_matrix))
  fours = [translation_f(i) for i in f.four_sites.values()]
  print(fours)

if __name__ == "__main__":
  w = Window()
  w.run()
  # figure_test()