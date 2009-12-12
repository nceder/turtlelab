#!/bin/env python

""" Console to "drive" the turtle

    VLC, 12/10/2009

"""

from turtle import *
from Tkinter import *
import sys

def go():
    """ compile code to code object and run """
    code_text = codebox.get(0.0,END)
    print code_text
    code = compile(code_text, "-", 'exec')
    eval(code)
    codebox.delete(1.0, END)
    history_box.insert(END, code_text)
    # need to grab output and display
def history_save():
    """ save selection or all, if no selection """
    pass
def history_clear():
    """  clear history box """
    history_box.delete(1.0, END)
def code_clear():
    """ clear code box """
    codebox.delete(1.0, END)

#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized
#TODO: colorize code - keywords, strings, comments
#TODO: add turtle color, size and image manipulation
#TODO: reset screen or even close screen
#TODO: help?

root = Tk()
root.title("Turtle Control Window")
history_label = Label(root, text="History")
history_label.pack()
history_box = Text(root, height=15, width=80)
history_box.pack()
history_save_btn = Button(root, text="Save", command=history_save)
history_save_btn.pack()
history_clear_btn = Button(root, text="Clear", command=history_clear)
history_clear_btn.pack()
code_label = Label(root, text="Code")
code_label.pack()
codebox = Text(root, height=15, width=80)
codebox.pack()

go_btn = Button(root, text="Go!", command=go)
code_clear_btn = Button(root, text="Clear", command=code_clear)
go_btn.pack()
code_clear_btn.pack()
root.mainloop()
