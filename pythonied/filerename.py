#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
#
# Rename video and audio files.


import filerename_config as config
import os


def find_files_bytype(this_dir, filetypes):
    """
    Find files of a certain file type in a given directory
    (and its subdirectories).

    :param this_dir: the directory to start the search at
    :param filetypes: a tuple of allowed file extensions
    :return: a list of all file names
    """
    file_list = []
    for directory, subdir, filename in os.walk(this_dir):
        for file in filename:
            if file.endswith(filetypes):
                file_list.append(file)
    return file_list


def main():
    """
    Main function.
    """
    # ---VARS---
    filetypes = config.FTYPES  # list
    search_dirs = config.DIRS  # list

    files = []

    for this_dir in search_dirs:
        files.extend(find_files_bytype(this_dir, tuple(filetypes)))

    # debug
    print(files)

if __name__ == "__main__":
    main()
