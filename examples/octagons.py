from random import *
tracer(False)
width(3)

sides = int(raw_input("Enter sides: "))
figures =  int(raw_input("Number of times to repeat the figure: "))
size = int(raw_input("Size in pixes of one side: "))

for i in range(figures):
    color(random(), random(), random())
    for x in range(sides):
        forward(size)
        right(360.0/sides)
    right (360.0/figures)
update()
