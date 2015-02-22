#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A Python3 program to (re)calculate an image's dimensions
when one of its sides is changed in size.

Copyright (c) 2015 K Kollmann <code∆k.kollmann·moe>
Licence: http://opensource.org/licenses/MIT The MIT License (MIT)
'''

import math
import sys

def recalculate_dimensions(old_w, old_h, w=0, h=0):
    new_w = w
    new_h = h

    try:
        float(new_w)
    except TypeError:
        # height provided, calculate new width
        new_w = (old_w * float(new_h)) / old_h
    else:
        # width provided, calculate new height
        new_h = (old_h * float(new_w)) / old_w

    return new_w, new_h

def provide_dimensions(w,h):
    ''' recalculate_dimensions the dimensions of an image based on
        current width, current height, and either a new width or height.
    '''
    global old_w
    global old_h
    try:
        float(w)
        float(h)
    except ValueError:
        if not old_w and not old_h:
            print("You entered at least one invalid value - try again.")
            return None, None
        else:
            # analyse new value(s) provided
            try:
                float(w)
            except ValueError:
                if w == '':
                    try:
                        float(h)
                    except ValueError:
                        pass
                    except KeyboardInterrupt:
                        sys.exit("\nProgram aborted by user.")
                    # try-except-else
                    else:
                        # width is empty
                        new_w, new_h = recalculate_dimensions(old_w, old_h, None, float(h))
                        return new_w, new_h
            except KeyboardInterrupt:
                sys.exit("\nProgram aborted by user.")
            # try-except-else
            else:
                try:
                    float(h)
                except ValueError:
                    if h == '':
                        # height is empty
                        new_w, new_h = recalculate_dimensions(old_w, old_h, float(w), None)
                        return new_w, new_h
                except KeyboardInterrupt:
                    sys.exit("\nProgram aborted by user.")
    except KeyboardInterrupt:
        sys.exit("\nProgram aborted by user.")
    # try-except-else
    else:
        # set variables for original width and height
        if not old_w and not old_h:
            old_w = float(w)
            old_h = float(h)

    while True:
        print("Input new value of (only) one of the dimensions:")
        new_w, new_h = provide_dimensions(input("new w: "), input("new h: "))
        return new_w, new_h
        break

    return new_w, new_h

old_w = None
old_h = None
new_w = None
new_h = None

if __name__ == "__main__":
    try:
        while True:
            print("Current dimensions of your image:")
            new_w, new_h = provide_dimensions(input("w: "), input("h: "))
            if new_w is not None:
                print("-----")
                print("new width: {}\nnew height: {}" .format(new_w, new_h))
                break
    except KeyboardInterrupt:
        sys.exit("\nProgram aborted by user.")

