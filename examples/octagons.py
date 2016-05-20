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
