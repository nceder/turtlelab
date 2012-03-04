# TurtleLab example by sruiz

penup()

#This next line makes the program run faster
delay(0)

##############
# First let's create a background for our flower.
###
# A clear blue sky.
pencolor("sky blue")
dot(2000)
###
# A sun way off in space.
goto(-200,300)
pencolor("orange")
for i in range(18):
    pensize(10)
    pendown()
    forward(50)
    pensize(6)
    forward(30)
    pensize(3)
    forward(20)
    penup()
    backward(100)
    right(20)
pencolor("yellow")
dot(80)
###
# A mountain in the distance.
pencolor("black")
fillcolor("brown")
goto(-100,-10)
setheading(30)
pendown()
begin_fill()
forward(500)
right(90)
forward(300)
end_fill()
penup()
backward(200)
fillcolor("white")
begin_fill()
backward(100)
left(90)
backward(100)
right(90)
forward(50)
left(120)
forward(30)
right(120)
forward(50)
left(100)
forward(50)
right(100)
forward(30)
end_fill()


###
# Green ground.
pensize(10)
pencolor("green")
fillcolor("light green")
goto(-500,0)
pendown()
begin_fill()
goto(500,0)
goto(500,-400)
goto(-500,-400)
goto(-500,0)
end_fill()
penup()
###
# How about some nice grass?
goto(-400,-20)
setheading(90)
pensize(2)
for i in range(100):
    pendown()
    forward(75)
    penup()
    backward(60)
    right(90)
    forward(5)
    left(90)
    pendown()
    forward(75)
    penup()
    backward(90)
    right(90)
    forward(3)
    left(90)


######################################
# And now the centerpiece: our flower.
# Set up drawing the stem.
penup()
home()
pensize(5)
setheading(90)
pencolor("dark green")
fillcolor("green")

# Start drawing the main stem.
pendown()
forward(50)
left(36)
forward(20)
# First leaf
pensize(2)
begin_fill()
left(20)
forward(50)
right(40)
forward(50)
right(140)
forward(50)
right(40)
forward(50)
right(160)
end_fill()
forward(30)
backward(30)
pensize(5)
# Back to the stem
backward(20)
right(36)
forward(50)
right(53)
forward(30)
# Another leaf
pensize(2)
begin_fill()
left(20)
forward(50)
right(40)
forward(50)
right(140)
forward(50)
right(40)
forward(50)
right(160)
end_fill()
forward(30)
backward(30)
pensize(5)
# Finish stem
backward(30)
left(53)
forward(100)


# Petals...
pencolor("purple")
fillcolor("violet")
pensize(4)
for i in range(12): # Do this next part 10 times.
    left(20)
    begin_fill()
    forward(50)
    right(40)
    forward(50)
    right(140)
    forward(50)
    right(40)
    forward(50)
    end_fill()
    right(130)
penup()

# The center of our flower.
color("dark orange")
dot(80)
color("orange")
dot(60)
color("yellow")
dot(40)
