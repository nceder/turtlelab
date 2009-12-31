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
        self.pack()
        self.create_history_box()
        self.create_code_box()

        self.interp = newInterp(local_dict )
        self.interp.window = self.history_box
        onclick(self.click)
        self.grids = []
        self.grid_lines()

    def create_history_box(self):
        self.history_label = Label(self, text="History")
        self.history_label.pack()
        self.history_box = Text(self, height=15, width=80)
        self.history_box.pack()
        self.history_controls = Frame(self, borderwidth=2, relief='sunken')
        self.history_save_btn = Button(self.history_controls, text="Save", command=self.history_save)
        self.history_save_btn.pack(side=LEFT)
        self.history_clear_btn = Button(self.history_controls, text="Clear", command=self.history_clear)
        self.history_clear_btn.pack(side=LEFT)
        self.history_controls.pack(fill=X)

    def create_code_box(self):

        self.code_label = Label(self, text="Code")
        self.code_label.pack()
        self.codebox = Text(self, height=15, width=80)
        ## codebox.bind("<Return>", go)
        self.codebox.pack()
        self.code_controls = Frame(self, borderwidth=2, relief='sunken')
        self.go_btn = Button(self.code_controls, text="Go!", command=self.go)
        self.code_clear_btn = Button(self.code_controls, text="Clear", command=self.code_clear)
        self.go_btn.pack(side=LEFT)
        self.code_clear_btn.pack(side=LEFT)
        self.color_btn = Button(self.code_controls, text="Colors", command=self.popup)
        self.color_btn.pack(side=LEFT)
        self.code_controls.pack(fill=X)
        self.colors = Menu(self.code_controls, tearoff=0)
        for color_name in color_list:
            self.colors.add_command(label=color_name, command=self.set_color)
        self.hide_grid_btn = Button(self.code_controls, text="Hide Grid", command=self.hide_grid)
        self.hide_grid_btn.pack(side=LEFT)
    def go(self, event=None):
        """ compile code to code object and run """
        print getturtle().position()
        code_text = self.codebox.get(0.0,END)
        print code_text
        ## code = self.interp.runsource(code_text)
        ## code = compile(code_text, "-", 'exec')
        ## eval(code)
        result = self.interp.runcode(code_text)
        if result:
            print "... "
        else:
            self.interp.showsyntaxerror()
#            self.codebox.delete(1.0, END)
#            self.history_box.insert(END, code_text)
            print getturtle().position()
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
        print event, event2
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
