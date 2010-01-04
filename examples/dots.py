import random
from turtle import *
delay(0)
tracer(False)
h= window_height()
w = window_width()


for x in range (1000):
    r = random.randrange(100)
    x = random.randrange(-h/2, h/2)
    y = random.randrange(-w/2, w/2)-r
    c = random.random(), random.random(), random.random()
    up()
    goto(x,y)
    down()
    color(c)
    fill(1)
    circle(r)
    fill(0)
