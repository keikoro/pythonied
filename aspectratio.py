#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A program to (re)calculate an image's dimensions
when one of its sides is changed in size.

Copyright (c) 2015 K Kollmann <code∆k.kollmann·moe>
License: http://opensource.org/licenses/MIT The MIT License (MIT)
'''

import math
import sys

def calculate_newdimension(w,h):
    ''' Calculate the missing dimension of an image based on its current
        width, height and new measurement for a third dimension.
    '''
    global old_w
    global old_h
    try:
        float(w)
        float(h)
    except ValueError:
        if not old_w and not old_h:
            print("There was at least one invalid value.")
            return None, None
        else:
            print("2nd loop -- do stuff here ") #debug
            return w, h
    else:
        if not old_w and not old_h:
            old_w = w
            old_h = h

    while True:
        print("Input new value of (only) one of the dimensions:")
        new_w, new_h = calculate_newdimension(input("new w: "), input("new h: "))
        return new_w, new_h
        break

old_w = None
old_h = None

if __name__ == "__main__":
    while True:
        print("Current dimensions of your image:")
        new_w, new_h = calculate_newdimension(input("w: "), input("h: "))
        print("new width: {}\nnew height: {}" .format(new_w, new_h))
        break
