#!/bin/env python

""" Console to "drive" the Python turtle

    Copyright 2009, Vern Ceder, vceder@gmail.com
   
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
from turtle import *
from Tkinter import *
import sys
import code

from tk_colors import tk_colors
color_list = ["red", "green", "blue", "brown"]
local_dict = locals()


class newInterp(code.InteractiveInterpreter):
    def write(self,data):
        if data != 'None\n':
            self.window.insert(END,data)

class TurtleConGUI(Frame):
    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master.title("Turtle Control")
        self.grid()
        self.create_code_box()
        self.create_history_box()

        self.interp = newInterp(local_dict )
        self.interp.window = self.history_box
        onclick(self.click)
        self.grids = []
        self.grid_lines()

    def create_code_box(self):

        self.code_frame = Frame(self)
        self.code_frame.grid(row=0, column=0)
        self.tools_label = Label(self.code_frame, text="Tools")
        self.tools_label.grid(row=0, column=0, sticky=E+W)
        self.code_label = Label(self.code_frame, text="Code")
        self.code_label.grid(row=0, column=1,  sticky=E+W)
        self.tools_frame = Frame(self.code_frame, borderwidth=2, relief='sunken')
        self.tools_frame.grid(row=1, column=0, rowspan=4, sticky=W+N+S)
        self.color_btn = Button(self.tools_frame, text="Colors", command=self.popup)
        self.color_btn.grid(row=0, column=0,sticky=W+E)
        self.repeat_btn = Button(self.tools_frame, text="repeat", command=self.popup)
        self.repeat_btn.grid(row=1, column=0,sticky=W+E)
        self.while_btn = Button(self.tools_frame, text="while...", command=self.popup)
        self.while_btn.grid(row=2, column=0,sticky=W+E)
        self.if_btn = Button(self.tools_frame, text="if...", command=self.popup)
        self.if_btn.grid(row=3, column=0,sticky=W+E)
        self.go_btn = Button(self.tools_frame, text="Go!", command=self.go)
        self.go_btn.grid(row=4, column=0, sticky=E+W+S, rowspan=2)
        self.code_clear_btn = Button(self.tools_frame, text="Clear", command=self.code_clear)
        self.code_clear_btn.grid(row=6, column=0, sticky=E+W+S)
        self.hide_grid_btn = Button(self.tools_frame, text="Hide Grid", command=self.hide_grid, width=10)
        self.hide_grid_btn.grid(row=7, column=0, sticky=E+W+S)

        self.codebox = Text(self.code_frame, height=18, width=80)
        ## codebox.bind("<Return>", go)
        self.codebox.grid(row=1, column=1, sticky=W)
        self.code_controls = Frame(self.code_frame, borderwidth=2, relief='sunken', height=30)
        self.code_controls.grid(row=2, column=1, sticky=W+E)

        self.colors = Menu(self.code_controls, tearoff=0)
        for color_name in color_list:
            self.colors.add_command(label=color_name, command=self.set_color)
                                 
    def create_history_box(self):
        self.history_label = Label(self.code_frame, text="History")
        self.history_label.grid(row=3, column=1, sticky=E+W)
        self.history_box = Text(self.code_frame, height=5, width=80)
        self.history_box.grid(row=4, column=1, sticky=E+W)
 
    def go(self, event=None):
        """ compile code to code object and run """
        ## print getturtle().position()
        code_text = self.codebox.get(0.0,END)
        self.history_box.delete(1.0, END)
        result = self.interp.runcode(code_text)
        if not result:
            self.interp.showsyntaxerror()
        # need to grab output and display


    def history_save(self):
        """ save selection or all, if no selection """
        pass
    def history_clear(self):
        """  clear history box """
        self.history_box.delete(1.0, END)
    def code_clear(self):
        """ clear code box """
        self.codebox.delete(1.0, END)
    def set_color(self):
    #    print dir(colors)
    #    print colors.selection_get(ACTIVE)
        color_str  = """color('%s')\n""" % (color_list[self.colors.index(ACTIVE)])
        self.codebox.insert(END, color_str)
        self.go()
    #    print colors.keys()

    def popup(self):
        self.colors.post(self.color_btn.winfo_rootx(), self.color_btn.winfo_rooty())

    def click(self,event=None, event2=None):
#        print event, event2
        pencolor('black')
        width(width()+2)

    def grid_lines(self):
        cv = getcanvas()
        line = cv.create_line(0, window_height()/2, 0, -window_height()/2, width=2, tags="gridline", fill="gray75")
        self.grids.append(line)

        line = cv.create_line(window_width()/2, 0, -window_width()/2, 0, width=2, fill="gray75", tags="gridline")
        self.grids.append(line)
        for x in range(100, window_width()/2, 100):
            line = cv.create_line(x, window_height()/2, x, -window_height()/2, width=1,
                                  fill="gray75",tags="gridline")
            self.grids.append(line)
            text = cv.create_text(x+20, 10, fill="gray75", text=str(x),tags="gridline")
            self.grids.append(text)
            
        for x in range(-100, -window_width()/2, -100):
            line = cv.create_line(x, window_height()/2, x, -window_height()/2, width=1,
                                  fill="gray75",tags="gridline")
            self.grids.append(line)
            text = cv.create_text(x+20, 10, fill="gray75", text=str(x),tags="gridline")
            self.grids.append(text)
            

        for y in range(100, window_height()/2, 100):
            line = cv.create_line(window_width()/2, y, -window_width()/2, y, width=1,
                                  fill="gray75",tags="gridline")
            self.grids.append(line)
            text = cv.create_text(20, y+10, fill="gray75", text=str(y),tags="gridline")
            self.grids.append(text)
            
        for y in range(-100, -window_height()/2, -100):
            line = cv.create_line(window_width()/2, y, -window_width()/2, y, width=1,
                                  fill="gray75",tags="gridline")
            self.grids.append(line)
            text = cv.create_text(20, y+10, fill="gray75", text=str(y),tags="gridline")
            self.grids.append(text)
            self.hide_grid_btn.config(command=self.hide_grid, text="Hide Grid")
        ## gl = cv.find_withtag("gridline")
        ##cv.lower(gl)
        ## cv.lower("gridline")
        ## for item in self.grids:
        ##     cv.lower(item)
    def hide_grid(self):
        cv = getcanvas()
        for item in self.grids:
            cv.itemconfig(item, fill="White")
#            cv.delete(item)
        cv.update()
        self.hide_grid_btn.config(command=self.grid_lines, text="Show Grid")
    def show_grid(self):
        cv = getcanvas()
        for item in self.grids:
            cv.itemconfig(item, fill="gray75")
#            cv.delete(item)
        cv.update()
        self.hide_grid_btn.config(command=self.grid_lines, text="Hide Grid")

#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized
#TODO: colorize code - keywords, strings, comment
#TODO: add turtle color, size and image manipulation
#TODO: reset screen or even close screen
#TODO: help?

#root = Tk()
#root.title("Turtle Control Window")
    #colors.pack(side=LEFT)
app = TurtleConGUI()
app.mainloop()
