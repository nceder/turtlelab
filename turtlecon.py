#!/bin/env python

""" Toolbar to "drive" the Python turtle

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
import os
from os.path import join, expanduser
import code
from idlelib.CallTipWindow import *

color_list = ["'white'", "'gray'", "'yellow'", "'orange'", "'red'", "'purple'", "'blue'", "'green'", "'brown'", "'black'", "random_color()"]
command_dict = {'forward':'forward(<distance?>)',
                'back': 'back(<distance?>)',
                'left': 'left(<Degrees?>)',
                'right': 'right(<Degrees?>)',
                'speed':'speed(<"slow"-"normal"-"fast"-"fastest">)\n',
                'circle':'circle(<radius>)\n',
                'dot':'dot(<size>)\n',
                'begin_fill':'begin_fill()\n',
                'end_fill':'end_fill()\n',
                'goto': 'goto(<x, y>)',
                'pendown':'pendown()\n',
                'penup':'penup()\n',
                'show turtle':'showturtle()\n',
                'hide turtle':'hideturtle()\n',
                'setheading':'setheading(<Degrees?>',
                'towards':'towards(<location (x,y)>)',
                'if...':'if <what?>:\n# commands go here\n',
                'repeat...':'for i in range(<how many times?>):\n# commands go here\n',
                'while...':'while <what?>:\n# commands go here\n',
                'rand. loc.':'random_location()',
                'rand. color':'random_color()',
                'rand. direction':'random_direction()',
                'rand. size':'random_size(<max_size>)',
                'undo':'undo()\n',
                'full screen':'hide_grid()\nsetup(width=1.0, height=1.0)\n',
                'exitonclick':'exitonclick()\n',
                '':''
                }
command_list = ['forward',
                'back',
                'left',
                'right',
                'speed',
                'circle',
                'dot',
                'begin_fill',
                'end_fill',
                'goto',
                'pendown',
                'penup',
                'show turtle',
                'hide turtle',
                'setheading',
                'towards',
                'if...',
                'repeat...',
                'while...',
                'rand. loc.',
                'rand. color',
                'rand. direction',
                'rand. size',
                'undo',
                'full screen',
                'exitonclick',
                ''
                ]

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
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.at_exit)
        self.indent_level = 0
        Frame.__init__(self, master)
        self.master.title("Turtle Control")
        self.grid()
        self.filename = ""
        if sys.platform == 'win32':
            self.filename = join(os.environ.get('HOMEDRIVE', ""),
                                 os.environ.get('HOMEPATH', ""))
        else:
            self.filename = os.environ.get('HOME', "")
        self.filename = join(self.filename, "turtlefile.py")
        self.edit_window = EditorWindow(root=master, filename=self.filename)
        self.max_width =  master.winfo_screenwidth()
        self.max_height =  master.winfo_screenheight()
        self.tools_x = int(self.max_width * .6)+6
        self.tools_y = 0
        self.create_code_box()
        self.code_frame.update()
        self.tools_w = self.master.winfo_width()
        self.tools_h = self.master.winfo_height()
        self.master.geometry("%sx%s+%s+%s" % (self.tools_w, self.tools_h,
                                              self.tools_x, self.tools_y))

        self.edit_x = self.tools_x + self.tools_w+ 6
        self.edit_y = 0
        self.edit_w = self.max_width - (self.tools_x + self.tools_w+16)
        self.edit_h = int(self.max_height * .70)

        self.edit_window.top.geometry("%sx%s+%s+%s" % (self.edit_w, self.edit_h,
                                                       self.edit_x, self.edit_y))
        self.edit_window.text_frame.update()
        
        self.errors_x = self.tools_x + self.tools_w+ 6
        self.errors_y = self.edit_window.top.winfo_height()+80
        self.create_error_box()
        self.error_frame.update()
        self.errors_w = self.edit_window.top.winfo_width()
        self.errors_h = self.toplevel.winfo_height()
        self.toplevel.geometry("%sx%s+%s+%s" % (self.errors_w, self.errors_h,
                                                self.errors_x, self.errors_y))
        self.error_box.update()
        self.interp = newInterp(None, window=self.error_box)

        self.run_code(
        """from turtle import *
from turtle import _CFG
_CFG['using_IDLE'] = True
_CFG['width'] = .6
_CFG['height'] = .75
_CFG['topbottom'] = 0
_CFG['leftright'] = True
_CFG['shape'] = 'turtle'
_CFG['pencolor'] = 'red'
_CFG['fillcolor'] = 'red'
_CFG['pensize'] = 5
_CFG['turtlesize'] = 2
_CFG['resizemode'] = 'user'
""")

        self.load_gridline_functs()
        self.show_grid()
##         self.load_random_functs()
        self.run_code("""resizemode('user')
print _CFG.items()
## pensize(5)
## shape('turtle')
## color('red')
## turtlesize(2)
""")

        self.edit_window.text.focus_set()

    def create_code_box(self):

        self.code_frame = Frame(self.master)
        self.code_frame.grid(row=0, column=0)
        self.tools_label = Label(self.code_frame, text="Tools")
        self.tools_label.grid(row=0, column=0, sticky=E+W)
        self.tools_frame = Frame(self.code_frame, borderwidth=2,
                                 relief='sunken')
        self.tools_frame.grid(row=1, column=0, sticky=W+N+S)

        self.color_frame = Frame(self.tools_frame)
        self.color_frame.grid(row=0, column=0,sticky=W+E)
        self.color_label = Label(self.color_frame, text="Color", anchor=W)
        self.color_label.grid(row=0, column=0, sticky=W)
        self.color_v = StringVar()
        self.color_v.set("'red'")
        self.colors = OptionMenu(self.color_frame, self.color_v,
                                 command=self.set_color, *color_list )
        self.colors.grid(row=0, column=1, sticky=E)
        
        self.size_frame = Frame(self.tools_frame)
        self.size_frame.grid(row=1, column=0,sticky=W+E)
        self.sizes_label = Label(self.size_frame, text="Size", anchor=W)
        self.sizes_label.grid(row=0, column=0, sticky=W+E)
        self.size_v = IntVar()
        self.size_v.set(2)
        self.sizes = OptionMenu(self.size_frame, self.size_v,
                                command=self.set_size, *list(range(5)))
        self.sizes.grid(row=0, column=1,sticky=E)

        self.pen_frame = Frame(self.tools_frame)
        self.pen_frame.grid(row=2, column=0,sticky=W+E)
        self.pen_label = Label(self.pen_frame, text="Pen size", anchor=W)
        self.pen_label.grid(row=0, column=0)
        self.pen_v = IntVar()
        self.pen_v.set(3)
        self.pens = OptionMenu(self.pen_frame, self.pen_v,
                               command=self.set_pen, *list(range(7)))
        self.pens.grid(row=0, column=1)

        self.command_frame = Frame(self.tools_frame)
        self.command_frame.grid(row=6, column=0, sticky=E+W)
        self.command_label = Label(self.command_frame, text="Commands",
                                   anchor=W)
        self.command_label.grid(row=0, column=0, sticky=W)
        self.command_v = StringVar()
        self.command_v.set("")
        self.commands = OptionMenu(self.command_frame, self.command_v,
                                   command=self.set_command,
                                   *command_list)
        self.commands.grid(row=0, column=1, sticky=W)
            
            
        self.go_btn = Button(self.tools_frame, text="Go!", command=self.go)
        self.go_btn.grid(row=8, column=0, columnspan=2, sticky=E+W+S, pady=10)
        self.go_tip = ToolTip(self.go_btn, "Run the code")
        self.code_clear_btn = Button(self.tools_frame, text="Clear code",
                                     command=self.code_clear)
        self.code_clear_btn.grid(row=10, column=0, sticky=E+W+S)
        self.hide_grid_btn = Button(self.tools_frame, text="Hide Grid",
                                    command=self.hide_grid, width=10)
        self.hide_grid_btn.grid(row=11, column=0, sticky=E+W+S)
        self.reset_screen_btn = Button(self.tools_frame, text="Reset Turtle",
                                       command=self.reset_screen, width=10)
        self.reset_screen_btn.grid(row=12, column=0, sticky=E+W+S)
        self.close_screen_btn = Button(self.tools_frame, text="Close Screen",
                                       command=self.close_screen, width=10)
        self.close_screen_btn.grid(row=13, column=0, sticky=E+W+S)
        self.quit_btn = Button(self.tools_frame, text="Quit",
                               command=self.at_exit, width=10)
        self.quit_btn.grid(row=14, column=0, sticky=E+W+S)

                                 
    def create_error_box(self):
        self.toplevel = Toplevel()
        self.error_frame = Frame(self.toplevel)
        self.toplevel.title("Errors")
        self.error_frame.grid()
        self.error_box = Text(self.error_frame, height=8, width=60)
        self.error_box.grid(row=0, column=0, sticky=E+W)
 
    def go(self, event=None):
        """ compile code to code object and run """
        code_text = self.edit_window.text.get(0.0,END)
        self.error_clear()
        open(self.filename, "w").write(code_text)
#        self.edit_window.text.event_generate("<<save-window>>")
        self.run_code(code_text)
        # need to grab output and display
        
    def run_code(self, code_text):
        result = self.interp.runcode(code_text)
        if result:
            self.interp.showsyntaxerror()

    def reset_screen(self):
        self.run_code("""
reset()
hide_grid()
show_grid()
resizemode('user')
pensize(5)
shape('turtle')
color('red')
turtlesize(2)
tracer(1)
delay(10)
""")
    def close_screen(self):
        self.run_code('bye()')

    def error_clear(self):
        """  clear error box """
        self.error_box.delete(0.0, END)

    def code_clear(self):
        """ clear code box """
        self.edit_window.text.delete(0.0, END)
        
    def set_color(self, value=None):
        color_str  = """color(%s)""" % (value)
        self.edit_window.text.insert(INSERT, color_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")

    def set_size(self, value=None):
        size_str  = """turtlesize(%s)""" % (value)
        self.edit_window.text.insert(INSERT, size_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")

    def set_pen(self, value=None):
        size_str  = """pensize(%s)""" % (value)
        self.edit_window.text.insert(INSERT, size_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")

    def set_command(self, key=None):
        command_strings = command_dict[key].split("\n")
        for command_str in command_strings:
            startpos = len(command_str) - command_str.rfind("<")
            endpos = len(command_str) - (command_str.rfind(">") + 1)
            
            self.edit_window.text.insert(INSERT, command_str)
            if startpos <= len(command_str) and endpos < startpos:
                self.edit_window.text.tag_add("replace", "%s-%sc" %
                                              (INSERT, startpos),
                                              "%s-%sc" % (INSERT, endpos))
                self.edit_window.text.tag_config("replace",foreground="red",
                                                 background="lightpink",
                                                 underline=1)
            if command_str.strip():
                self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.edit_window.text.focus_set()
        self.command_v.set("")


    def at_exit(self):
        self.run_code("bye()")
        try:
            self.edit_window.close()
        except:
            self.edit_window.text_frame.destroy()
        self.destroy()

    def hide_grid(self):
        self.run_code("""hide_grid()""")
        self.hide_grid_btn.config(command=self.show_grid, text="Show Grid")
    def show_grid(self):
        self.run_code("""show_grid()""")
        self.hide_grid_btn.config(command=self.hide_grid, text="Hide Grid")

    def load_gridline_functs(self):
        self.run_code("""
grids = []
def show_grid():
    global grids
    cv = getcanvas()
    line = cv.create_line(0, window_height()/2, 0, -window_height()/2, width=2,
                          tags="gridline", fill="gray75")
    grids.append(line)

    line = cv.create_line(window_width()/2, 0, -window_width()/2, 0,
                          width=2, fill="gray75", tags="gridline")
    grids.append(line)
    for x in range(100, window_width()/2, 100):
        line = cv.create_line(x, window_height()/2, x, -window_height()/2,
                              width=1, fill="gray75",tags="gridline")
        grids.append(line)
        text = cv.create_text(x+20, 10, fill="gray75", text=str(x),
                              tags="gridline")
        grids.append(text)

    for x in range(-100, -window_width()/2, -100):
        line = cv.create_line(x, window_height()/2, x, -window_height()/2,
                              width=1, fill="gray75",tags="gridline")
        grids.append(line)
        text = cv.create_text(x+20, 10, fill="gray75", text=str(x),
                              tags="gridline")
        grids.append(text)

    for y in range(100, window_height()/2, 100):
        line = cv.create_line(window_width()/2, y, -window_width()/2, y,
                              width=1, fill="gray75",tags="gridline")
        grids.append(line)
        text = cv.create_text(20, y+10, fill="gray75", text=str(-y),
                              tags="gridline")
        grids.append(text)

    for y in range(-100, -window_height()/2, -100):
        line = cv.create_line(window_width()/2, y, -window_width()/2, y,
                              width=1, fill="gray75",tags="gridline")
        grids.append(line)
        text = cv.create_text(20, y+10, fill="gray75", text=str(-y),
                              tags="gridline")
        grids.append(text)

def hide_grid():
    cv = getcanvas()
    for item in grids:
        cv.delete(item)
        cv.update()""")
    def load_random_functs(self):
        self.run_code('''
from random import randint, random
def random_size(max_size=100):
    """returns a random size between 1 and size)"""
    return randint(1, max_size)

def random_location():
    """ returns a random location on screen"""
    return randint(-window_width()/2, window_width()/2), randint(-window_height()/2, window_height()/2)

def random_direction():
    return randint(0, 359)

def random_color():
    """ returns a random color """
    if colormode() == 255:
        return randint(0,255), randint(0,255), randint(0,255)
    else:
        return random(), random(), random()
''') 
    
#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized

if __name__ == '__main__':

    app = TurtleConGUI()
    app.mainloop()
