from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

X_POS_RIGHT = 350
X_POS_LEFT = -350
Y_POS = 0
score_left = 0
score_right = 0

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

paddle_right = Paddle((X_POS_RIGHT, Y_POS))
paddle_left = Paddle((X_POS_LEFT, Y_POS))
ball = Ball()
screen.listen()
score = Scoreboard()

screen.onkey(key= "Up", fun = paddle_right.up)
screen.onkey(key= "Down", fun = paddle_right.down)
screen.onkey(key= "w", fun = paddle_left.up)
screen.onkey(key= "s", fun = paddle_left.down)

game_is_on=True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    #Collision with all
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    #Detect Collision with paddle
    if (ball.distance(paddle_right) < 50 and ball.xcor()) > 320 or (ball.distance(paddle_left) < 50 and ball.xcor() < -320):
        ball.move_speed *= 0.9
        ball.bounce_x()

    #Detect Points
    if ball.xcor() > 380:
        score_left += 1
        ball.reset_position()
        score.l_point()

    elif ball.xcor() < -380:
        score_right +=1
        ball.reset_position()
        score.r_point()

screen.exitonclick()