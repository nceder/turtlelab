"""
based on logo program - creates "webs"

    Copyright 2009, Naomi Ceder, naomi.ceder@gmail.com  
   
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.  

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

# imports turtle library in Tkinter dialogs
from turtle import *
from tkSimpleDialog import askinteger
from tkSimpleDialog import askfloat
from tkSimpleDialog import askstring

# creates turtles for drawing
t1 = Turtle()
t1.tracer(False)
# comment out this line to get main lines
#t1.up()
t2 = Turtle()
t2.tracer(False)
t2.up()
t3 = Turtle()
t3.tracer(False)
t3.delay(0)
t3.up()

# gets values from user
lines = askfloat("","Number of lines: ")
strands = askfloat("","Number of strands: ")
gap = askinteger ("","Number of lines to skip from center :")
size = distance = askinteger("","Diameter :")
color = askstring("", "Color :")
step = size/float(strands)
t1.color(color)
t3.color(color)

# t1 moves to outside of one line
t1.forward(distance)

# draws the figure by connecting different points on two adjacent lines
for x in range(lines):
    t2.right(360.0/lines)
    t2.forward(step * gap)
    for x in range(strands-gap):
        t2.forward(step)
        t3.goto(t1.position())
        t3.down()
        t3.goto(t2.position())
        t3.up()
        t3.goto(t1.position())
        t1.backward(step)
    t1.backward(step * gap)
    t1.right(360.0/lines)
    t1.forward(distance)
   
    t2.backward(distance)
    
t1.backward(distance)


