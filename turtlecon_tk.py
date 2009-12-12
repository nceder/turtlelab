#!/bin/env python

""" Console to "drive" the turtle

    VLC, 12/10/2009

"""

from turtle import *
from Tkinter import *
import sys

root = Tk()
root.title("Turtle Control Window")
textbox = Text(root, height=20, width=100)
textbox.pack()
def go():
    a = textbox.dump(0.0,99.99, text=True)
    com_text_list = [x[1] for x in a]
    com_text = "".join(com_text_list)

    print com_text
    code = compile(com_text, "-", 'exec')
    eval(code)
    ## for line in com_text_list:
    ##     eval(line)
go_btn = Button(root, text="Go!", command=go)
go_btn.pack()

## command = ""
## command_hist = []

## while command != 'exit':
##     command = raw_input(">>> ").strip()
##     try:
##         eval(command)
##         command_hist.append(command)
##     except BaseException, e:
##         print e

## print command_hist

root.mainloop()
