#!/bin/env python

""" Console to "drive" the turtle

    VLC, 12/10/2009

"""

from turtle import *
from Tkinter import *
#from pmw import *
import sys
color_list = ["red", "green", "blue", "brown"]
def go(event=None):
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
def set_color():
#    print dir(colors)
#    print colors.selection_get(ACTIVE)
    color_str  = """color('%s')""" % (color_list[colors.index(ACTIVE)])
    codebox.insert(END, color_str)
    go()
#    print colors.keys()
                                     
def popup():
    colors.post(color_btn.winfo_rootx(), color_btn.winfo_rooty())

def click(event=None, event2=None):
    print event, event2
    pencolor('black')
    width(width()+2)


#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized
#TODO: colorize code - keywords, strings, comment
#TODO: add turtle color, size and image manipulation
#TODO: reset screen or even close screen
#TODO: help?

root = Tk()
root.title("Turtle Control Window")
history_label = Label(root, text="History")
history_label.pack()
history_box = Text(root, height=15, width=80)
history_box.pack()
history_controls = Frame(root, borderwidth=2, relief='sunken')
history_save_btn = Button(history_controls, text="Save", command=history_save)
history_save_btn.pack(side=LEFT)
history_clear_btn = Button(history_controls, text="Clear", command=history_clear)
history_clear_btn.pack(side=LEFT)
history_controls.pack(fill=X)
code_label = Label(root, text="Code")
code_label.pack()
codebox = Text(root, height=15, width=80)
## codebox.bind("<Return>", go)
codebox.pack()
code_controls = Frame(root, borderwidth=2, relief='sunken')
go_btn = Button(code_controls, text="Go!", command=go)
code_clear_btn = Button(code_controls, text="Clear", command=code_clear)
go_btn.pack(side=LEFT)
code_clear_btn.pack(side=LEFT)
color_btn = Button(code_controls, text="Colors", command=popup)
color_btn.pack(side=LEFT)
code_controls.pack(fill=X)
colors = Menu(code_controls, tearoff=0)
for color_name in color_list:
    colors.add_command(label=color_name, command=set_color)
#colors.pack(side=LEFT)
onclick(click)
root.mainloop()
