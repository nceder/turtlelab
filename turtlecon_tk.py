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
command_list = [('forward', 'How far?'), ('right', 'Degrees?'), ('left', 'Degrees?'),
                ('back', 'How far?'), ('undo', 'Undo last command'),
                ('dot', '[size],[color]'), ('circle', 'Size [,extent, steps]'),
                ('penup()',''), ('pendown()',''), ('goto', ''), ('setheading','')]

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
        self.edit_window = EditorWindow(root=master)
        self.max_width =  master.winfo_screenwidth()
        self.max_height =  master.winfo_screenheight()
        self.tools_x = int(self.max_width * .5)+6
        self.tools_y = 0
        self.create_code_box()
        self.code_frame.update()
        self.tools_w = self.master.winfo_width()
        self.tools_h = self.master.winfo_height()
        self.master.geometry("%sx%s+%s+%s" % (self.tools_w, self.tools_h,self.tools_x, self.tools_y))

        self.edit_x = self.tools_x + self.tools_w+ 6
        self.edit_y = 0
        self.edit_w = self.max_width - (self.tools_x + self.tools_w+16)
        self.edit_h = int(self.max_height * .70)
        ## print "%sx%s+%s+%s" % (self.edit_w, self.edit_h,self.edit_x, self.edit_y)
        self.edit_window.top.geometry("%sx%s+%s+%s" % (self.edit_w, self.edit_h,self.edit_x, self.edit_y))
        self.edit_window.text_frame.update()
        
        self.errors_x = self.tools_x + self.tools_w+ 6
        self.errors_y = self.edit_window.top.winfo_height()+80
        self.create_error_box()
        self.error_frame.update()
        self.errors_w = self.edit_window.top.winfo_width()
        self.errors_h = self.toplevel.winfo_height()
        self.toplevel.geometry("%sx%s+%s+%s" % (self.errors_w, self.errors_h,self.errors_x, self.errors_y))
        self.error_box.update()
        self.screen = Screen()
        setup(width=.5, height=.75, startx=0, starty=0)
        onclick(self.click)
        self.grids = []
        self.grid_lines()
        resizemode('user')
        pensize(5)
        shape('turtle')
        color('red')
        turtlesize(2)
        self.interp = newInterp(local_dict, self. error_box)
        ## self.run_code("""resizemode('auto')\npensize(5)\nshape('turtle')\ncolor('red')""")
        self.tips = dict(command_list)

        self.edit_window.text.focus_set()

    def at_exit(self):
        bye()
        self.edit_window.close()
        sys.exit()
        
    def create_code_box(self):

        self.code_frame = Frame(self.master)
        self.code_frame.grid(row=0, column=0)
        self.tools_label = Label(self.code_frame, text="Tools")
        self.tools_label.grid(row=0, column=0, sticky=E+W)
        self.tools_frame = Frame(self.code_frame, borderwidth=2, relief='sunken')
        self.tools_frame.grid(row=1, column=0, sticky=W+N+S)
        self.color_btn = Button(self.tools_frame, text="Colors", command=self.popup)
        self.color_btn.grid(row=0, column=0,sticky=W+E)
        self.size_btn = Button(self.tools_frame, text="Size", command=self.popup_sizes)
        self.size_btn.grid(row=1, column=0,sticky=W+E)
        self.pen_btn = Button(self.tools_frame, text="Pen width", command=self.popup_pens)
        self.pen_btn.grid(row=2, column=0,sticky=W+E)
        self.code_clear_btn = Button(self.tools_frame, text="Clear code", command=self.code_clear)
        self.code_clear_btn.grid(row=6, column=0, sticky=E+W+S)
        self.hide_grid_btn = Button(self.tools_frame, text="Hide Grid", command=self.hide_grid, width=10)
        self.hide_grid_btn.grid(row=7, column=0, sticky=E+W+S)
        self.reset_screen_btn = Button(self.tools_frame, text="Reset Turtle", command=self.reset_screen, width=10)
        self.reset_screen_btn.grid(row=8, column=0, sticky=E+W+S)
        ## self.close_screen_btn = Button(self.tools_frame, text="Close Screen", command=self.close_screen, width=10)
        ## self.close_screen_btn.grid(row=9, column=0, sticky=E+W+S)
        self.repeat_btn = Button(self.tools_frame, text="repeat...", command=self.add_for)
        self.repeat_btn.grid(row=0, column=1,sticky=W+E)
        self.while_btn = Button(self.tools_frame, text="while...", command=self.add_while)
        self.while_btn.grid(row=1, column=1,sticky=W+E)
        self.if_btn = Button(self.tools_frame, text="if...", command=self.add_if)
        self.if_btn.grid(row=2, column=1,sticky=W+E)
        self.commands_btn = Button(self.tools_frame, text="Commands", command=self.popup_command)
        self.commands_btn.grid(row=3, column=1, sticky=E+W+S)
        self.go_btn = Button(self.tools_frame, text="Go!", command=self.go)
        self.go_btn.grid(row=10, column=0, columnspan=2, sticky=E+W+S)
        self.go_tip = ToolTip(self.go_btn, "Run the code")

        self.colors = Menu(self.tools_frame, tearoff=0)
        for color_name in color_list:
            self.colors.add_command(label=color_name, command=self.set_color)
        self.sizes = Menu(self.tools_frame, tearoff=0)
        for size in range(5):
            self.sizes.add_command(label=str(size), command=self.set_size)
            
        self.pens = Menu(self.tools_frame, tearoff=0)
        for size in range(10):
            self.pens.add_command(label=str(size), command=self.set_pen)
            
        self.commands = Menu(self.tools_frame, tearoff=0)
        for command_name, tip in command_list:
            self.commands.add_command(label=command_name, command=self.set_command)
                                 
    def create_error_box(self):
        self.toplevel = Toplevel()
        self.error_frame = Frame(self.toplevel)
        self.toplevel.title("Errors")
        self.error_frame.grid()
        ## self.history_label = Label(self.error_frame, text="Errors")
        ## self.history_label.grid(row=0, column=0, sticky=E+W)
        self.error_box = Text(self.error_frame, height=8, width=60)
        self.error_box.grid(row=0, column=0, sticky=E+W)
 
    def go(self, event=None):
        """ compile code to code object and run """
        ## print getturtle().position()
        code_text = self.edit_window.text.get(0.0,END)
        self.error_box.delete(1.0, END)
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
        turtlesize(2)
        color('red')

    def close_screen(self):
        bye()

    def error_clear(self):
        """  clear error box """
        self.error_box.delete(0.0, END)

    def code_clear(self):
        """ clear code box """
        self.edit_window.text.delete(0.0, END)
        
    def set_color(self):
        color_str  = """color('%s')""" % (color_list[self.colors.index(ACTIVE)])
        self.edit_window.text.insert(END, color_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.run_code(color_str)

    def set_size(self):
        size_str  = """turtlesize(%s)""" % (self.sizes.index(ACTIVE))
        self.edit_window.text.insert(END, size_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.run_code(size_str)

    def set_pen(self):
        size_str  = """width(%s)""" % (self.pens.index(ACTIVE))
        self.edit_window.text.insert(END, size_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.run_code(size_str)

    def set_command(self):
        command_str  = """%s""" % (command_list[self.commands.index(ACTIVE)][0])
        
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.focus_set()

    def add_if(self):
        command_str  = """if <what?>:"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.tag_add("replace", str(INSERT) + "-8c", str(INSERT)+ "-1c")
        self.edit_window.text.tag_config("replace",foreground="red", background="pink", underline=1)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        command_str  = """# commands go here"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.edit_window.text.focus_set()
        
    def add_for(self):
        command_str  = """for i in range(<how many times?>):"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.tag_add("replace", str(INSERT) + "-19c", str(INSERT)+ "-2c")
        self.edit_window.text.tag_config("replace",foreground="red", relief="raised", underline=1)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        command_str  = """# commands go here"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.edit_window.text.focus_set()


    def add_while(self):
        command_str  = """while <what?>:"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.tag_add("replace", str(INSERT) + "-8c", str(INSERT)+ "-1c")
        self.edit_window.text.tag_config("replace",foreground="red", background="pink", underline=1)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        command_str  = """# commands go here"""
        self.edit_window.text.insert(INSERT, command_str)
        self.edit_window.text.event_generate("<<newline-and-indent>>")
        self.edit_window.text.focus_set()

    def popup(self):
        self.colors.post(self.color_btn.winfo_rootx(), self.color_btn.winfo_rooty())

    def popup_sizes(self):
        self.sizes.post(self.size_btn.winfo_rootx(), self.size_btn.winfo_rooty())

    def popup_pens(self):
        self.pens.post(self.pen_btn.winfo_rootx(), self.pen_btn.winfo_rooty())
        
    def popup_command(self):
        self.commands.post(self.commands_btn.winfo_rootx()+50, self.commands_btn.winfo_rooty())

    def click(self,event=None, event2=None):
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
            text = cv.create_text(20, y+10, fill="gray75", text=str(-y),tags="gridline")
            self.grids.append(text)
            
        for y in range(-100, -window_height()/2, -100):
            line = cv.create_line(window_width()/2, y, -window_width()/2, y, width=1,
                                  fill="gray75",tags="gridline")
            self.grids.append(line)
            text = cv.create_text(20, y+10, fill="gray75", text=str(-y),tags="gridline")
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

    def random_size(self):
        pass

    def random_location(self):
        pass

    def random_direction(self):
        pass
    
#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized

#TODO: add turtle color, size and image manipulation

app = TurtleConGUI()
app.mainloop()
