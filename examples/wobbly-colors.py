# TurtleLab example by sruiz
# Set up the screen
setup(1.0,1.0)
update()
width = window_width()
height = window_height()
penup()
delay(0)
tracer(0)
color("black")
dot(3000)
penup()

LARGEST_RADIUS = 200

def rainbow_spike():
    radius = LARGEST_RADIUS
    while radius > 0:
        for c in ('red','orange','yellow','green','blue','purple'):
            color(c)
            forward(5)
            dot(radius)
            radius = radius - 1
            if radius < 1:
                break

x = LARGEST_RADIUS * 5 / 2

setheading(0)
for y in range(height/2,-height/2-LARGEST_RADIUS,-LARGEST_RADIUS):
    goto(-x,y)
    rainbow_spike()

setheading(180)
for y in range(height/2+LARGEST_RADIUS/2,-height/2-LARGEST_RADIUS/2,-LARGEST_RADIUS):
    goto(x,y)
    rainbow_spike()
