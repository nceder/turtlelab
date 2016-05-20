"""
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
