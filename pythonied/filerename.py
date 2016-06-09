#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
#
# Rename video and audio files.


import config as conf
import os
import re


def find_patterns(oldpath):
    """
    Look for patterns in all old file names and create
    new file names based on these patterns.

    :param oldpath: the original path to the file
    :return: the new file name
    """
    dirpath, file = os.path.split(oldpath)
    fname, ext = os.path.splitext(file)

    # remove full stops, hyphens, underscores right between characters,
    # replace with spaces
    # !! leaves the last full stop for file ending intact!
    # p = '(\w+)\.+|\-+|\_+(\w)'
    p = '(\S)[_.-](\S)'
    r = '\g<1> \g<2>'
    new_fname = re.sub(p, r, fname) + ext

    # debug
    # print(oldpath)
    print(new_fname)

    return new_fname


def find_files_bytype(this_dir, filetypes):
    """
    Find files of a certain file type in a given directory
    (and its subdirectories).

    :param this_dir: the directory to start the search at
    :param filetypes: a tuple of allowed file extensions
    :return: a dictionary with paths, old file names, new file names
    """
    paths = {}
    for directory, subdir, filename in os.walk(this_dir):
        root = directory
        for file in filename:
            if file.endswith(filetypes):
                path = os.path.join(root, directory)
                paths[path, file] = find_patterns(os.path.join(path, file))
    return paths


def main():
    """
    Main function.
    """
    # ---VARS---
    filetypes = conf.FTYPES  # list
    search_dirs = conf.DIRS  # list

    files = {}

    for this_dir in search_dirs:
        files.update(find_files_bytype(this_dir, tuple(filetypes)))

    # debug
    print(files)

if __name__ == "__main__":
    main()
