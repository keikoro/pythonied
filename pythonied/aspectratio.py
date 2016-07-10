#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aspectratio

A program to (re)calculate an image's dimensions
when one of its sides gets changed in size.

Copyright (c) 2015 K Kollmann <code∆k.kollmann·moe>
"""


# TODO make sure entered values are numbers (floats)


def newdimensions(width, height):
    """
    Calculate new width or height of an image.

    The new dimensions are based on one of the new
    values being provided by the user. The image's
    aspect ratio is kept intact.
    """
    w = None
    h = None
    # prompt for desired new width / height
    w = input("New w: ")
    h = input("New h: ")

    # convert str input to floats
    if w:
        w = float(w)
    if h:
        h = float(h)

    # print out warning if user provided no values
    if w == '' and h == '':
        print("You didn't provide any new values! Please try again.")
    elif w == '':
        w = (h * width) / height
        print("The new width of your image is {}, rounded: {}".format(
            round(w, 2), round(w)))
    elif h == '':
        h = (w * height) / width
        print("The new height of your image is {}, rounded: {}".format(
            round(h, 2), round(h)))
    # print out warning if user provided both new width and height
    else:
        print("You provided two new values instead of one! Please try again.")
    return w, h


def main():
    """
    Main function.
    """

    # prompt for current width and height of image
    print("Please enter the dimensions of your image:")
    width = float(input("w: "))
    height = float(input("h: "))

    print("Leave one of the following values blank (simply press enter)")

    # run the function once
    new_w, new_h = newdimensions(width, height)

    # run the function until only one new value was entered
    while (new_w == None or new_w == '') and (new_h == None or new_h == ''):
        new_w, new_h = newdimensions(width, height)


if __name__ == "__main__":
    main()
