import pygame as pg
import re
import random
import tkinter as tk
from tkinter import messagebox


class Cube:
  def __init__(self, start, rows, width, directionX=0, directionY=1, color=(255,0,0)):
    self.rows = rows
    self.width = width
    self.position = start
    self.directionX = directionX
    self.directionY = directionY
    self.color = color

  def move(self, directionX, directionY):
    self.directionX = directionX
    self.directionY = directionY
    self.position = self.position[0]+self.directionX, self.position[1]+self.directionY

  def draw(self, surface, eyes=False):
    cubeSize = self.width // self.rows
    rowIndex, columnIndex = self.position

    if eyes:
      self.color = (255,255,0)
    pg.draw.rect(surface, self.color, (rowIndex*cubeSize+1, columnIndex*cubeSize+1, cubeSize-2, cubeSize-2))



class Snake:
  body = list()
  turns = dict()

  def __init__(self, color, position, rows, width):
    self.rows = rows
    self.width = width
    self.color = color
    self.head = Cube(position, rows, width)
    self.body.append(self.head)
    self.directionX = 0
    self.directionY = 1

  def move(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
      
      keys = pg.key.get_pressed()  # gets all the keys that were pressed
      for key in keys:
        if keys[pg.K_LEFT]:
          self.directionX = -1
          self.directionY = 0
          self.turns[self.head.position[:]] = [self.directionX, self.directionY]  # TODO: try it without "[:]"
        elif keys[pg.K_RIGHT]:
          self.directionX = 1
          self.directionY = 0
          self.turns[self.head.position[:]] = [self.directionX, self.directionY]  
        elif keys[pg.K_UP]:
          self.directionX = 0
          self.directionY = -1
          self.turns[self.head.position[:]] = [self.directionX, self.directionY]  
        elif keys[pg.K_DOWN]:
          self.directionX = 0
          self.directionY = 1
          self.turns[self.head.position[:]] = [self.directionX, self.directionY]  

    for index, cube in enumerate(self.body):
      position = cube.position[:]
      if position in self.turns:
        directionX, directionY = self.turns[position]
        cube.move(directionX, directionY)
        if index == len(self.body) - 1:
          self.turns.pop(position)
      else:
        if cube.directionX == -1 and cube.position[0] <= 0: cube.position = (cube.rows-1, cube.position[1])
        elif cube.directionX == 1 and cube.position[0] >= cube.rows-1: cube.position = (0, cube.position[1])
        elif cube.directionY == 1 and cube.position[1] >= cube.rows-1: cube.position = (cube.position[0], 0)
        elif cube.directionY == -1 and cube.position[1] <= 0: cube.position = (cube.position[0], cube.rows-1)
        else: cube.move(cube.directionX, cube.directionY)

  def reset(self, position):
    self.body = list()
    self.turns = dict()
    self.head = Cube(position, self.rows, self.width)
    self.body.append(self.head)

  def addCube(self, rows, width):
    tail = self.body[-1]
    directionX = tail.directionX
    directionY = tail.directionY
    x, y = tail.position
    newPosition = x - directionX, y - directionY

    newCube = Cube(newPosition, rows, width, directionX=directionX, directionY=directionY)
    self.body.append(newCube)

  def draw(self, surface):
    for index, cube in enumerate(self.body):
      if index == 0:
        cube.draw(surface, True)
      else:
        cube.draw(surface)


def drawGrid(surface, rows, width):
  cubeSize = width // rows

  x, y = 0, 0
  for i in range(rows):
    x += cubeSize
    y += cubeSize
    pg.draw.line(surface, (255,255,255), (x, 0), (x, width))
    pg.draw.line(surface, (255,255,255), (0, y), (width, y))

def redrawWindow(surface, snake, snack, rows, width):
  surface.fill((20,20,20))
  drawGrid(surface, rows, width)
  snake.draw(surface)
  snack.draw(surface)
  pg.display.update()

def randomSnack(rows, snake):
  positions = snake.body

  while True:
    x, y = random.randrange(rows), random.randrange(rows)
    if len(list(filter(lambda z: z.position == (x,y), positions))) == 0:
      break
  return (x,y)

def messageBox():
  root = tk.Tk()
  root.attributes("-topmost", True)
  root.withdraw()
  messagebox.showinfo("Lost", "again!")
  try:
    root.destroy()
  except:
    pass


def main():
  width = 500
  height = width * 1
  rows = 20
  user_input = False  # TODO: set to True for production
  while user_input:
    rows = input(f"Tip in the number of rows (must divide {width} evenly): ")
    if rows == "":
      print("Please input a number.")
      continue
    check_input = re.match(r"\d*", rows).group()
    rows = rows.replace(check_input, "")
    if rows != "":
      print("Please input a valid number.")
      continue
    rows = int(check_input)
    if width % rows != 0:
      print(f"Number must divide {width} evenly.")
      continue
    user_input = False
  
  window = pg.display.set_mode((width, height))

  snake = Snake((255,0,0), (10,10), rows, width)
  snack = Cube(randomSnack(rows, snake), rows, width, color=(0,255,0))

  clock = pg.time.Clock()

  while True:
    pg.time.delay(60)  # pauses the program for XX milliseconds
    clock.tick(8)     # to control the Frames-per-Second
    snake.move()
    if snake.body[0].position == snack.position:
      snake.addCube(rows, width)
      snack = Cube(randomSnack(rows, snake), rows, width, color=(0,255,0))
    if len(list(filter(lambda x: x.position == snake.body[0].position, snake.body[1:]))) > 0:
      print("score: ", len(snake.body))
      messageBox()
      snake.reset((rows // 2, rows // 2))
    # can't see any difference between the above to lines and the below four lines
    # for x in range(len(snake.body)):
      # if snake.body[x].position in list(map(lambda z: z.position, snake.body[x+1:])):
        # snake.reset((rows//2, rows//2))
        # break
    redrawWindow(window, snake, snack, rows, width)



if __name__ == "__main__":
  main()

    
  




    
