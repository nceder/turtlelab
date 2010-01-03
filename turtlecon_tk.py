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
from idlelib.ToolTip import ToolTip
from idlelib.EditorWindow import EditorWindow
import sys
import code
from idlelib.CallTipWindow import *
CHECKHIDE_TIME = 1000
from time import sleep

from tk_colors import tk_colors
color_list = ['white', 'gray', 'yellow', 'orange', "red", 'purple', "blue", "green", "brown", 'black']
command_list = [('forward', 'How far?'), ('right', 'Degrees?')]

local_dict = locals()


class newInterp(code.InteractiveInterpreter):
    def __init__(self, locals=None, window=None):
        code.InteractiveInterpreter.__init__(self, locals)
        self.window = window
    def write(self,data):
        if data != 'None\n':
            self.window.insert(END,data)

class TurtleConGUI(Frame):
    def __init__(self, master=None):
        if not master:
            master = Tk()
        self.master = master.protocol("WM_DELETE_WINDOW", self.exit)

        Frame.__init__(self, master)
        self.master.title("Turtle Control")
        self.grid()
        self.create_code_box()
        self.create_history_box()
        self.screen = Screen()
        onclick(self.click)
        self.grids = []
        self.grid_lines()
#        turtlesize=2
        print dir()
        self.interp = newInterp(local_dict, self. history_box)
        self.run_code("""resizemode('auto')\npensize(5)\nshape('turtle')\ncolor('red')""")
        self.tips = dict(command_list)

        self.calltip = CallTip(self.code_box)

        self.code_box.event_add("<<calltip-show>>", "(")
        self.code_box.event_add("<<calltip-hide>>", ")")
        self.code_box.bind("<<calltip-show>>", self.calltip_show)
        self.code_box.bind("<<calltip-hide>>", self.calltip_hide)

   
    def calltip_show(self, event=None):
        key = self.calltip.widget.get(str(CURRENT)+'-2c wordstart', str(CURRENT)+ '-2c wordend')
        self.calltip.showtip(self.tips[key], CURRENT, END)
        print key

    def calltip_hide(self, event=None):
        self.calltip.hidetip()
        
    def exit(self):
        bye()
        sys.exit()
        
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
        self.commands_btn = Button(self.tools_frame, text="commands", command=self.popup_command)
        self.commands_btn.grid(row=4, column=0, sticky=E+W+S)
        self.go_btn = Button(self.tools_frame, text="Go!", command=self.go)
        self.go_btn.grid(row=5, column=0, sticky=E+W+S)
        self.go_tip = ToolTip(self.go_btn, "Run the code")
        self.code_clear_btn = Button(self.tools_frame, text="Clear", command=self.code_clear)
        self.code_clear_btn.grid(row=6, column=0, sticky=E+W+S)
        self.hide_grid_btn = Button(self.tools_frame, text="Hide Grid", command=self.hide_grid, width=10)
        self.hide_grid_btn.grid(row=7, column=0, sticky=E+W+S)
        self.reset_screen_btn = Button(self.tools_frame, text="Reset Screen", command=self.reset_screen, width=10)
        self.reset_screen_btn.grid(row=8, column=0, sticky=E+W+S)
        self.close_screen_btn = Button(self.tools_frame, text="Close Screen", command=self.close_screen, width=10)
        self.close_screen_btn.grid(row=9, column=0, sticky=E+W+S)

        self.code_box = Text(self.code_frame, height=18, width=80)
        ## code_box.bind("<Return>", go)
        self.code_box.grid(row=1, column=1, sticky=W)
        self.code_controls = Frame(self.code_frame, borderwidth=2, relief='sunken', height=30)
        self.code_controls.grid(row=2, column=1, sticky=W+E)

        self.colors = Menu(self.code_controls, tearoff=0)
        for color_name in color_list:
            self.colors.add_command(label=color_name, command=self.set_color)
        self.commands = Menu(self.code_controls, tearoff=0)
        for command_name, tip in command_list:
            self.commands.add_command(label=command_name, command=self.set_command)
                                 
    def create_history_box(self):
        self.history_label = Label(self.code_frame, text="History")
        self.history_label.grid(row=3, column=1, sticky=E+W)
        self.history_box = Text(self.code_frame, height=5, width=80)
        self.history_box.grid(row=4, column=1, sticky=E+W)
 
    def go(self, event=None):
        """ compile code to code object and run """
        ## print getturtle().position()
        code_text = self.code_box.get(0.0,END)
        self.history_box.delete(1.0, END)
        self.run_code(code_text)
        # need to grab output and display
        
    def run_code(self, code_text):
        result = self.interp.runcode(code_text)
        if not result:
            self.interp.showsyntaxerror()
        

    def reset_screen(self):
        reset()
        pensize(6)
        shape('turtle')
        ## turtlesize=2

    def close_screen(self):
        bye()

    def history_save(self):
        """ save selection or all, if no selection """
        pass
    def history_clear(self):
        """  clear history box """
        self.history_box.delete(1.0, END)
    def code_clear(self):
        """ clear code box """
        self.code_box.delete(1.0, END)
    def set_color(self):
        color_str  = """color('%s')\n""" % (color_list[self.colors.index(ACTIVE)])
        self.code_box.insert(END, color_str)
        self.run_code(color_str)

    def set_command(self):
        command_str  = """%s""" % (command_list[self.commands.index(ACTIVE)][0])
        self.code_box.insert(END, command_str)
#        self.code_box.update()
        self.code_box.insert(CURRENT, "(")
        self.code_box.focus_set()
        self.code_box.event_generate("<<calltip-show>>")
        
#        self.calltip_show()
        ## self.go()

    def popup(self):
        self.colors.post(self.color_btn.winfo_rootx(), self.color_btn.winfo_rooty())

    def popup_command(self):
        self.commands.post(self.commands_btn.winfo_rootx(), self.commands_btn.winfo_rooty())

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
        for t in turtles():
            t.update()
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
