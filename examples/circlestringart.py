# Circular String Art
# TurtleLab example by sruiz
import time
from turtle import * # <- so it can be run outside TurtleLab
RADIUS = 300

for NUM_POINTS in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
    reset()
    pensize(3)
    hideturtle()
    speed("fastest")
    tracer(0) # Change this to tracer(0) to turn off animations completely
    penup()
    # Collect points to use
    goto(0,-RADIUS)
    pos_list = list()
    for i in range(NUM_POINTS):
        circle(RADIUS,360.0/NUM_POINTS)
        pos_list.append(position())

    linecount = 0
    # Draw lines between the points
    for i in range(1,NUM_POINTS/2+1):
        x = (i*2)/float(NUM_POINTS)
        color(x,x,x)
        for j in range(NUM_POINTS):
            goto(pos_list[j])
            pendown()
            goto(pos_list[(j+i)%NUM_POINTS])
            penup()
            linecount += 1

    goto(0,-7)
    color("black")
    write("%d vertices\n%d lines drawn"% (NUM_POINTS, linecount), align="center")
    time.sleep(2)
exitonclick()
