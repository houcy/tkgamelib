# Copyright 2014, Eric Clack, eric@bn7.net
# This program is distributed under the terms of the GNU General Public License

"""A set of 5 sprites that follow each other with acceleration and pens"""

from tkinter import *
import random
from geekclub.pyscratch import *

create_canvas()

ball_img = PhotoImage(file='geekclub/images/ball.gif')
bat_img = PhotoImage(file='geekclub/images/bat.gif')
brick_img = PhotoImage(file='geekclub/images/brick.gif')

ball = Sprite(ball_img)
ball.speed_x = random.randint(-4,4) * 2
ball.speed_y = random.randint(-4,4) * 2
ball.max_speed = 10

bat = Sprite(bat_img)

bricks = []
for x in range(10):
    brick = Sprite(brick_img)
    brick.move_to_random_pos()
    bricks.append(brick)
    

def bat_follows_mouse():
    bat.move_to(mousex(), mousey())

def bounce_ball():
    ball.move_with_speed()
    ball.if_on_edge_bounce()
    if ball.touching(bat):
        ball.speed_y = -abs(ball.speed_y)
        ball.accelerate(1.05)
    brick = ball.touching_any(bricks)
    if brick:
        if brick.below(ball):
            ball.speed_y = abs(ball.speed_y)            
        else:
            ball.speed_y = -abs(ball.speed_y)
        bricks.remove(brick)
        brick.delete()

    
forever(bat_follows_mouse, 20)
forever(bounce_ball, 20)
mainloop()
