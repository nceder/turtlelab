# TurtleLab example by sruiz
speed("fastest")
setup(width=1.0, height=1.0)
hideturtle()
delay(0)
penup()

# Define some values
stemthickness = 25
petals = 180
petalringradius = 150
petalseparation = 9.14159
seedrings = 72
seedringradius = 160

# Describe how to draw a single petal
def drawAPetal(degreesout = 10):
    circle(-5,90 - degreesout/2)
    begin_fill()
    circle(-250,degreesout)
    circle(-5, (180 - degreesout))
    circle(-250,degreesout)
    circle(-5, (90 - degreesout/2))
    end_fill()
    right(90)
    forward(75)
    back(75)
    left(90)

# Draw a sunset-ish sky
goto(200,-200)
color("red")
dot(4000)
for x in range(80):
    color((1,x*.01,0))
    dot(1800 - x*20)

# Draw the stem
goto(0,0)
pendown()
color("black")
pensize(stemthickness)
right(115)
circle(500,90)
color("green")
pensize(stemthickness-4)
circle(500,-90)
color("black")
pensize(1)
left(115)
penup()

# Draw a circle of petals
goto(0,-petalringradius)
pencolor("black")
fillcolor("yellow")
d = 40.
pendown()
for i in range(petals):
    circle(petalringradius,petalseparation)
    x = d-(5./petals)*i
    drawAPetal(x)
penup()

# Draw the seed ring
goto(0,-seedringradius)
setheading(0)
pendown()
fillcolor("brown")
begin_fill()
circle(seedringradius)
end_fill()
for i in range(seedrings):
    circle(seedringradius,360/seedrings)
    circle(seedringradius/2)
exitonclick()
