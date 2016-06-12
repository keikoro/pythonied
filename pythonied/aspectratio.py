#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A program to (re)calculate an image's dimensions
# when one of its sides is changed in size.
#
# Copyright (c) 2015 K Kollmann <code∆k.kollmann·moe>

# TODO make sure entered values are numbers (floats)


def newdimensions():
    """ Calculate new width / height of an image based on
        its current width and height, and one new value
        (keeping intact its aspect ratio). """
    # prompt for desired new width / height
    w = input("New w: ")
    h = input("New h: ")
    # convert str input to floats
    if w:
        w = float(w)
    if h:
        h = float(h)

    """ calculate new width or height depending on which
        new dimension was provided by the user """

    # print out warning if user provided no values
    if w == "" and h == "":
        print("You didn't provide any new values! Please try again.")
    elif w == "":
        w = (h * width) / height
        print("The new width of your image is {}, rounded: {}".format(
            round(w, 2), round(w)))
    elif h == "":
        h = (w * height) / width
        print("The new height of your image is {}, rounded: {}".format(
            round(h, 2), round(h)))
    # print out warning if user provided both new width and height
    else:
        print("You provided two new values instead of one! Please try again.")
        w = ""
        h = ""
    return w, h


# prompt for current width and height of image
print("Please enter the dimensions of your image:")
width = float(input("w: "))
height = float(input("h: "))

print("Leave one of the following values blank (simply press enter)")

# run the function once
new_w, new_h = newdimensions()

# run the function again for as long as only one new value was entered
while new_w == "" and new_h == "":
    new_w, new_h = newdimensions()
