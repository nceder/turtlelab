#!/bin/env python

""" Console to "drive" the turtle

    VLC, 12/10/2009

"""

from turtle import *
command = ""
command_hist = []

while command != 'exit':
    command = raw_input(">>> ").strip()
    try:
        eval(command)
        command_hist.append(command)
    except BaseException, e:
        print e

print command_hist
