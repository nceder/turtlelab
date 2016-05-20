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
