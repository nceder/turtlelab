import random
from turtle import *
delay(0)
tracer(False)
h= window_height()
w = window_width()
x1 = w/4
x2 = -x1
y1 = h/4
y2 = -y1

for x in range(120):
    up()
    goto(x1,y1)
    down()
    color(random.random(), random.random(), random.random()) 
    circle(140)
    up()
    goto(x2,y1)
    down()
    color(random.random(), random.random(), random.random()) 
    circle(140)
    up()
    setx(x2)
    sety(y2)
    down()
    color(random.random(), random.random(), random.random()) 
    circle(140)
    up()
    setx(x1)
    sety(y2)
    down()
    color(random.random(), random.random(), random.random()) 
    circle(140)
    right(360/120)
