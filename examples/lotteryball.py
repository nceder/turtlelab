#!/usr/bin/python
# Lotteryball Generator
#  TurtleLab example by sruiz
#   After running, click on screen to generate lottery numbers.
import random
from turtle import * # <- so it can run outside TurtleLab
delay(0)
hideturtle()
if "hide_grid" in dir(): # <- so it can run outside TurtleLab
    hide_grid()

CIRCLERADIUS = 25
FONTSIZE = 12

def lotteryball(x,y):
    numbers = []
    for i in range(5):
        numbers.append(random.randrange(1,60))
    numbers.append(random.randrange(1,40))

    clear()
    pencolor("black")
    fillcolor("white")
    penup()
    goto(-CIRCLERADIUS*5,0)
    pendown()
    for n in range(len(numbers)):
        if n == len(numbers)-1:
            fillcolor("red")
        begin_fill()
        circle(CIRCLERADIUS)
        end_fill()
        penup()
        left(90)
        forward(CIRCLERADIUS - FONTSIZE/2)
        write(numbers[n],align="center",font=("Arial",FONTSIZE,"bold"))
        backward(CIRCLERADIUS - FONTSIZE/2)
        right(90)
        forward(CIRCLERADIUS * 2)
        pendown()

onscreenclick(lotteryball)

mainloop()
