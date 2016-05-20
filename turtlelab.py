#!/usr/bin/env python

""" Toolbar to "drive" the Python turtle 

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
from turtle import *
from Tkinter import *
from idlelib.ToolTip import ToolTip
from idlelib.EditorWindow import EditorWindow
import tkColorChooser
import tkMessageBox
import traceback
import sys
import os
from os.path import join, expanduser
import code

# force UTF-8 encoding...
reload(sys)                              # restore module sys from disk
sys.setdefaultencoding('utf-8')          # or whatever codec you need
del sys.setdefaultencoding               # ensure against later accidents



command_dict = {'forward':'forward(<distance?>)',
                'back': 'back(<distance?>)',
                'left': 'left(<degrees?>)',
                'right': 'right(<degrees?>)',
                'setheading':'setheading(<degrees?>)',
                'towards':'towards(<location(x,y)?>)',
                'goto': 'goto(<location(x,y)?>)',
                'circle':'circle(<radius?>)\n',
                'dot':'dot(<radius?>)\n',
                'speed':'speed(<"slow"-"normal"-"fast"-"fastest"?>)\n',
                'pensize':'pensize(<width?>)\n',
                'penup':'penup()\n',
                'pendown':'pendown()\n',
                'pencolor':'pencolor(<color?>)\n',
                'fillcolor':'fillcolor(<color?>)\n',
                'begin_fill':'begin_fill()\n',
                'end_fill':'end_fill()\n',
                'turtlesize':'turtlesize(<how_big?>)\n',
                'hideturtle':'hideturtle()\n',
                'showturtle':'showturtle()\n',
                'if...':'if <what?>:\n# commands go here\n',
                'repeat...':'for i in range(<how many times?>):\n# commands go here\n',
                'while...':'while <what?>:\n# commands go here\n',
                'repeat forever':'while True:\n# commands go here\n',
                'Full Screen':'setup(width=1.0, height=1.0)\n',
                'exitonclick':'exitonclick()\n',
                '':''
                }

value_list = ["'white'", "'gray'", "'yellow'", "'orange'", "'red'", "'purple'",
              "'blue'", "'green'", "'brown'", "'black'", "random_color()", "HexColorPicker",
              '', 'random_location()','random_direction()',
              'random_size(<max_size?>)']
move_list = ['forward', 'back', 'left', 'right', '', 'circle', 'dot', '',
             'goto', 'setheading', 'towards']
pen_list = ['pencolor', 'pensize', 'penup', 'pendown', '', 'fillcolor',
            'begin_fill', 'end_fill', '', 'showturtle', 'hideturtle',
            'turtlesize', 'speed']
extra_list = ['if...', 'repeat...', 'repeat forever', 'while...',
              '', 'Full Screen', 'exitonclick']
turtle_speed_list = ['slowest','slow','normal','fast','fastest','*instant*']

local_dict = locals()


class newInterp(code.InteractiveInterpreter):
#    def __init__(self, locals=None, window=None):
#        code.InteractiveInterpreter.__init__(self, locals)
#        self.window = window
   def showtraceback(self):
        """Ripped out of code.py, and tweaked slightly"""
        try:
            etype, value, tb = sys.exc_info()
            sys.last_type = etype
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            elist = traceback.format_list(tblist)
            if elist:
                elist.insert(0, "Traceback (most recent call last):\n")
            elist[len(elist):] = traceback.format_exception_only(etype, value)
        finally:
            tblist = tb = None
        tkMessageBox.showwarning("Code Error", "".join(elist))

class TurtleConGUI(Frame):
    def __init__(self, master=None):
        if not master:
            master = Tk()
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.at_exit)
        self.indent_level = 0
        Frame.__init__(self, master)
        self.master.title("TurtleLab")
        self.grid()
        self.filename = ""
        if sys.platform == 'win32':
            try:
                # Find the "My Documents" folder.
                shell_folders_key = '"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"'
                shell_folders = os.popen('reg QUERY %s' % shell_folders_key).readlines()
                my_docs = [i for i in shell_folders if "Personal" in i][0]
                my_docs = my_docs.split("REG_SZ")[1].strip()
                self.filename = my_docs
            except:
                # If any of the above fails, assume "My Documents" is in the default location.
                self.filename = join(os.environ.get('HOMEDRIVE', ""),
                                     os.environ.get('HOMEPATH', ""),
                                     "My Documents")
        else:
            self.filename = os.environ.get('HOME', "")
        self.go_filename = join(self.filename, "turtlefile-go.py")
        self.filename = join(self.filename, "turtlefile.py")
        self.edit_window = EditorWindow(root=master, filename=self.filename)
        self.max_width =  master.winfo_screenwidth()
        self.max_height =  master.winfo_screenheight()
        #     Ubuntu reports these figures in such a way that all the windows'
        # area is visible. Windows XP reports them in such a way that the
        # Windows are behind the taskbar. Stupid solution:
        if sys.platform == 'win32':
            self.max_height = self.max_height - 70
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
        self.edit_h = int(self.max_height)

        self.edit_window.top.geometry("%sx%s+%s+%s" % (self.edit_w, self.edit_h,
                                                       self.edit_x, self.edit_y))
        self.edit_window.text_frame.update()
        
        #self.errors_x = self.tools_x + self.tools_w+ 6
        #self.errors_y = self.edit_window.top.winfo_height()+80
        #self.create_error_box()
        #self.error_frame.update()
        #self.errors_w = self.edit_window.top.winfo_width()
        #self.errors_h = self.toplevel.winfo_height()
        #self.toplevel.geometry("%sx%s+%s+%s" % (self.errors_w, self.errors_h,
        #                                        self.errors_x, self.errors_y))
        #self.error_box.update()
        self.interp = newInterp({'status_dict':{'x':self.status_x,
                                                'y':self.status_y,
                                                'heading':self.status_h,
                                                'penrgb':self.status_penrgb,
                                                'fillrgb':self.status_fillrgb}})#,
                                                #window=self.error_box)
        self.load_gridline_functs()
        self.setup_graphics_window()
        self.load_random_functs()
        self.edit_window.text.focus_set()

    def setup_graphics_window(self):
        self.run_code(
        """from turtle import *

from turtle import _CFG
_CFG['using_IDLE'] = True
_CFG['width'] = .6
_CFG['height'] = 1.0
_CFG['topbottom'] = 0
_CFG['leftright'] = True
_CFG['shape'] = 'turtle'
_CFG['pencolor'] = 'red'
_CFG['fillcolor'] = 'red'
_CFG['pensize'] = 5
_CFG['turtlesize'] = 2
_CFG['resizemode'] = 'user'
""")
        self.run_code("""
clearscreen()
""")
        if not self.hide_grid_check.get():
            self.show_grid()
        self.run_code("""resizemode('user')
## print _CFG.items()

pensize(_CFG['pensize'])
shape(_CFG['shape'])

color(_CFG['pencolor'])
turtlesize(_CFG['turtlesize'])
""")
        self.run_code("speed('%s')\n" % self.turtle_speed.get())

    def create_code_box(self):
        # MASTER FRAME
        self.code_frame = Frame(self.master)
        self.code_frame.grid(row=0)

        # - COMMANDS FRAME
        self.command_v = StringVar()
        Label(self.code_frame, text="Insert Code").grid(row=0, sticky=E+W+S,pady=5)
        self.tools_frame = Frame(self.code_frame, borderwidth=2, relief='sunken')
        self.tools_frame.grid(row=1, sticky=E+W, ipadx=5, ipady=5)
        self.tools_frame.columnconfigure(0,minsize=150,weight=1)   # <----- This determines the minimum size of the window

        Label(self.tools_frame, text="Commands").grid(row=0, sticky=E+W, pady=5)
        Label(self.tools_frame, text="Move Control", anchor=W).grid(row=1, sticky=W)
        OptionMenu(self.tools_frame, self.command_v, command=self.set_command, *move_list).grid(row=1, sticky=E)
        Label(self.tools_frame, text="Pen Control", anchor=W).grid(row=2, sticky=W)
        OptionMenu(self.tools_frame, self.command_v, command=self.set_command, *pen_list).grid(row=2, sticky=E)
        Label(self.tools_frame, text="Extra", anchor=W).grid(row=3, sticky=W)
        OptionMenu(self.tools_frame, self.command_v, command=self.set_command, *extra_list).grid(row=3, sticky=E)
        Label(self.tools_frame, text="Values").grid(row=4, sticky=E+W, pady=5)
        Label(self.tools_frame, text="Colors, etc.", anchor=W).grid(row=5, sticky=W)
        OptionMenu(self.tools_frame, self.command_v, command=self.insert_value, *value_list ).grid(row=5, sticky=E)

        #Label(self.tools_frame, text="Commands", anchor=W).grid(row=4, sticky=W)
        #OptionMenu(self.tools_frame, self.command_v, command=self.set_command, *command_list).grid(row=4, sticky=E)
        
        # - GRAPHICS WINDOW FRAME
        Label(self.code_frame, text="Graphics Window").grid(row=2, sticky=E+W, pady=5)
        self.graphics_window_frame = Frame(self.code_frame, borderwidth=2, relief='sunken')
        self.graphics_window_frame.grid(row=3,sticky=E+W)
        self.graphics_window_frame.columnconfigure(0,weight=1)
        # - - BUTTONS IN GRAPHICS WINDOW FRAME
        #self.hide_grid_btn = Button(self.graphics_window_frame, text="Hide Grid", command=self.hide_grid)
        #self.hide_grid_btn.grid(row=0, sticky=N+S+E+W, pady=5, padx=5)
        #Button(self.graphics_window_frame, text="Reset Turtle & Screen", command=self.reset_screen, background="orange3", activebackground="orange").grid(row=1, sticky=N+S+E+W, padx=5)
        # - Speed List
        self.turtle_speed = StringVar()
        Label(self.graphics_window_frame, text="Speed:", anchor=W).grid(row=0, stick=W)
        OptionMenu(self.graphics_window_frame, self.turtle_speed, *turtle_speed_list).grid(row=0, sticky=N+S+E)
        self.turtle_speed.set("normal")
        # - Grid checkbox
        self.hide_grid_check = IntVar()
        Checkbutton(self.graphics_window_frame, text="Hide Grid", variable=self.hide_grid_check).grid(row=1, sticky=N+S+E+W)
        # - Buttons
        Button(self.graphics_window_frame, text="Go!", command=self.go, background="green3", activebackground="green").grid(row=2, sticky=N+S+E+W)
        Button(self.graphics_window_frame, text="Close Screen", command=self.close_screen, background="orange3", activebackground="orange").grid(row=3, sticky=N+S+E+W)
        
        # - STATUS FRAME
        Label(self.code_frame, text="Current Turtle Status").grid(row=4, sticky=E+W+S, pady=5)
        self.status_frame = Frame(self.code_frame, borderwidth=2, relief='sunken', background="white")
        self.status_frame.grid(row=5, sticky=E+W)
        self.status_frame.columnconfigure(0,weight=1)
        # - - TEXT IN STATUS FRAME
        self.status_x = StringVar(value="0")
        self.status_y = StringVar(value="0")
        self.status_h = StringVar(value="0")
        self.status_penrgb = StringVar(value="0,  0,  0")
        self.status_fillrgb = StringVar(value="0,  0,  0")
        Label(self.status_frame, text="x:", background="white").grid(row=1, sticky=W)
        Label(self.status_frame, textvar=self.status_x, background="white").grid(row=1, sticky=E)
        Label(self.status_frame, text="y:", background="white").grid(row=2, sticky=W)
        Label(self.status_frame, textvar=self.status_y, background="white").grid(row=2, sticky=E)
        Label(self.status_frame, text="heading:", background="white").grid(row=3, sticky=W)
        Label(self.status_frame, textvar=self.status_h, background="white").grid(row=3, sticky=E)
        Label(self.status_frame, text="pencolor:", background="white").grid(row=4, sticky=W)
        Label(self.status_frame, textvar=self.status_penrgb, background="white").grid(row=4, sticky=E)
        Label(self.status_frame, text="fillcolor:", background="white").grid(row=5, sticky=W)
        Label(self.status_frame, textvar=self.status_fillrgb, background="white").grid(row=5, sticky=E)

        # - CODE WINDOW FRAME
        #Label(self.code_frame, text="Code Window").grid(row=6, sticky=E+W+S, pady=5)
        #self.code_window_frame = Frame(self.code_frame, borderwidth=2, relief='sunken')
        #self.code_window_frame.grid(row=7, sticky=N+S+E+W)
        #self.code_window_frame.columnconfigure(0,weight=1)
        # - - BUTTONS IN CODE WINDOW FRAME
        #Button(self.code_window_frame, text="Go!", command=self.go, background="green3", activebackground="green").grid(row=0, sticky=N+S+E+W)
        #Button(self.code_window_frame, text="Clear code", command=self.code_clear, background="orange3", activebackground="orange").grid(row=1, sticky=N+S+E+W)
        # - BACK IN MASTER FRAME
        Button(self.code_frame, text="X - Quit - X", command=self.at_exit, width=10, background="red3",activebackground="red").grid(row=6, sticky=N+S+E+W,padx=5, pady=5)

                                 
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
        #self.error_clear()
        open(self.go_filename, "w").write(code_text)
        self.setup_graphics_window()
        if self.turtle_speed.get() == "*instant*":
            self.run_code("tracer(0)\n")
        self.run_code(code_text)
        if self.turtle_speed.get() == "*instant*":
            self.run_code("update()\n")
        # need to grab output and display
        
    def run_code(self, code_text):
        result = self.interp.runcode(code_text)
        if result:
            self.interp.showsyntaxerror()

#    def reset_screen(self):
#        self.run_code("""
#reset()
#hide_grid()
#show_grid()
#resizemode('user')
#pensize(5)
#shape('turtle')
#color('red')
#turtlesize(2)
#tracer(1)
#delay(10)
#""")
    def close_screen(self):
        self.run_code('bye()')

#    def error_clear(self):
#        """  clear error box """
#        self.error_box.delete(0.0, END)

    def code_clear(self):
        """ clear code box """
        self.edit_window.text.delete(0.0, END)
        
    def insert_value(self, value=None):
	self.command_v.set("")
        if value == "HexColorPicker":
            value = "'" + tkColorChooser.askcolor("black")[1] + "'"
        value_str  = """%s""" % (value)
        self.edit_window.text.insert(INSERT, value_str)

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
        #self.hide_grid_btn.config(command=self.show_grid, text="Re-draw Grid")
    def show_grid(self):
        self.run_code("""show_grid()""")
        #self.hide_grid_btn.config(command=self.hide_grid, text="Hide Grid")

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
def status():
    t = getturtle()
        
    status_dict['x'].set("%4.0f" % t.position()[0])
    status_dict['y'].set("%4.0f" % t.position()[1])
    status_dict['heading'].set("%3d" % (t.heading()))

    for item in ('pen','fill'):
        colorstr = t._colorstr(t.pen()[item+'color'])
        if not colorstr.startswith("#"):
            try:
                rgblist = [c/256 for c in t.screen.cv.winfo_rgb(colorstr)]
            except TK.TclError:
                raise Exception("bad colorstring: %s" % colorstr)
        elif len(colorstr) == 7:
            rgblist = [int(colorstr[i:i+2], 16) for i in (1, 3, 5)]
        elif len(colorstr) == 4:
            rgblist = [16*int(colorstr[h], 16) for h in colorstr[1:]]
        else:
            raise Exception("bad colorstring: %s" % colorstr)
        colorstatus = "%3.0f,%3.0f,%3.0f" % tuple(rgblist)
        status_dict[item+'rgb'].set(colorstatus)

def new_update(self):
    if Turtle._pen is not None:
        status()
    self.cv.update()

old_update = TurtleScreen._update
TurtleScreen._update = new_update

maze_data = (( 110.85445804 , 44.9444101085 ),( 14.0362434679 , 37.1079506306 ),
( 316.636577042 , 49.5176736125 ),( 266.268603001 , 46.0977222864 ),
( 197.744671625 , 52.4976189937 ),( 141.666659891 , 54.8178802946 ),
( 90.0 , 31.0 ),( 156.801409486 , 22.8473193176 ),( 270.0 , 43.0 ),
( 305.942111871 , 49.4064773081 ),( 348.340707346 , 64.3272881443 ),
( 278.746162262 , 26.305892876 ),( 168.550662012 , 80.6039701255 ),
( 118.810793743 , 45.6508488421 ),( 104.215853474 , 77.3692445355 ),
( 38.3674853848 , 61.2209114601 ),( 354.289406863 , 60.2992537267 ),
( 328.815025341 , 44.418464629 ),( 289.230672376 , 45.5411901469 ),
( 14.6208739886 , 23.769728648 ),( 109.983106522 , 46.8187996429 ),
( 12.8042660653 , 22.5610283454 ),( 277.431407971 , 69.5844810285 ),
( 241.189206257 , 45.6508488421 ),( 343.300755766 , 31.3209195267 ),
( 73.2442510708 , 97.1236325515 ),( 115.866356794 , 73.3484832836 ),
( 162.570137182 , 90.1387818866 ),( 182.290610043 , 75.0599760192 ),
( 285.945395901 , 21.8403296678 ),( 353.088772881 , 66.4830805544 ),
( 348.503436982 , 60.207972894 ),( 211.607502246 , 30.528675045 ),
( 166.390268104 , 97.7445650663 ),( 208.739795292 , 70.7106781186 ),
( 246.250505507 , 54.626001135 ),( 295.559965172 , 50.9901951359 ),
( 306.15818544 , 64.4049687524 ),( 346.37300514 , 101.867561078 ),
( 12.8750015597 , 35.902646142 ),( 114.943905263 , 47.4236228055 ),
( 154.358994176 , 27.7308492477 ),( 33.690067526 , 57.6888204074 ),
( 252.552811577 , 36.6878726557 ),( 330.945395901 , 51.4781507049 ),
( 22.2490236572 , 47.539457296 ),( 78.9964591483 , 110.022724925 ),
( 128.585398193 , 120.253898066 ),( 173.088772881 , 132.966161109 ),
( 219.255841676 , 120.104121495 ),( 258.190117043 , 112.378823628 ),
( 310.544397167 , 109.224539367 ),( 341.565051177 , 98.0306074652 ))

def maze(username = ''):
    username = username.lower()
    ascii_total = 0
    for c in username:
        ascii_total += ord(c)
    tr = tracer()
    pc = pencolor()
    ps = pensize()
    tracer(0)
    pencolor("black")
    pensize(5)
    penup()
    right(ascii_total)
    left(45)
    back(45)
    left(90)
    pendown()
    for h,d in maze_data:
        setheading(h + ascii_total)
        forward(d*2)
    penup()
    home()
    pendown()
    tracer(tr)
    pencolor(pc)
    pensize(ps)
''') 
    
#TODO: make control window stay on top unless minimized
#TODO: make turtle window stay on top unless minimized

if __name__ == '__main__':

    app = TurtleConGUI()
    app.mainloop()
