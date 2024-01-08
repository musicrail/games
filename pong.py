import turtle
import os

## sound from https://bigsoundbank.com/sound-1825-balloon-against-wall-1.html

class GameComponent(turtle.Turtle):
  def __init__(self, function):
    super().__init__()

    if function in ["paddle_left", "paddle_right"]:
      self.paddle(function.removeprefix("paddle_"))
    elif function == "ball":
      self.ball()
  
  def paddle(self, position):
    self.speed(0)
    self.shape("square")
    self.color("white")
    self.shapesize(stretch_wid=5, stretch_len=1)
    self.penup()
    if position == "left":
      self.goto(- (screen_width//2 - 50), 0)
    elif position == "right":
      self.goto(screen_width//2 - 50, 0)
    else:
      print("not a valid position")

  def ball(self):
    speed = 0.02
    self.speed(0)
    self.shape("square")
    self.color("white")
    self.penup()
    self.goto(0,0)
    self.dx = speed
    self.dy = speed

  def paddle_up(self):
    y = self.ycor()
    y += 20
    self.sety(y)

  def paddle_down(self):
    y = self.ycor()
    y -= 20
    self.sety(y)

screen_width = 700
screen_height = 500

# score
score_a = 0
score_b = 0

# pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, screen_height // 2 - 40)
pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 20, "normal"))

paddle_left = GameComponent("paddle_left")
paddle_right = GameComponent("paddle_right")
ball = GameComponent("ball")

window = turtle.Screen()
window.title("Pong game")
window.bgcolor("black")
window.setup(width=screen_width, height=screen_height)
window.tracer(0)

window.listen()
window.onkeypress(paddle_left.paddle_up, "w")
window.onkeypress(paddle_left.paddle_down, "s")
window.onkeypress(paddle_right.paddle_up, "Up")
window.onkeypress(paddle_right.paddle_down, "Down")

# game loop
while True:
  window.update()

  # move the ball
  ball.setx(ball.xcor() + ball.dx)
  ball.sety(ball.ycor() + ball.dy)

  # border check
  y_border = screen_height // 2 - 10
  outfield = screen_width // 2 
  if ball.ycor() > y_border:
    os.system("aplay bounce.wav&")
    ball.sety(y_border)
    ball.dy *= -1
  
  if ball.ycor() < -y_border:
    os.system("aplay bounce.wav&")
    ball.sety(-y_border)
    ball.dy *= -1

  if ball.xcor() > outfield:
    ball.goto(0,0)
    ball.dx *= -1
    score_a += 1
    pen.clear()
    pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 20, "normal"))
  
  if ball.xcor() < -outfield:
    ball.goto(0,0)
    ball.dx *= -1
    score_b += 1
    pen.clear()
    pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 20, "normal"))

  # make the ball bounce of the paddles
  paddle_right_x = screen_width // 2 - 50
  if (ball.xcor() > paddle_right_x - 10 and ball.xcor() < paddle_right_x) and (ball.ycor() < paddle_right.ycor() + 50 and ball.ycor() > paddle_right.ycor() - 50):
    os.system("aplay bounce.wav&")
    ball.setx(paddle_right_x - 10)
    ball.dx *= -1

  paddle_left_x = - (screen_width // 2 - 50)
  if (ball.xcor() < paddle_left_x + 10 and ball.xcor() > paddle_left_x) and (ball.ycor() < paddle_left.ycor() + 50 and ball.ycor() > paddle_left.ycor() - 50):
    os.system("aplay bounce.wav&")
    ball.setx(paddle_left_x + 10)
    ball.dx *= -1
  



  

