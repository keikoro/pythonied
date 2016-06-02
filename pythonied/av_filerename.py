#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
#
# Rename video and audio files.


import av_filerename_config as config
import os


def find_files_bytype(this_dir, filetypes):
    file_list = []
    for startdir, subdirs, filenames in os.walk(this_dir):
        for file in filenames:
            if file.endswith(filetypes):
                file_list.append(file)
    return file_list

def main():
    """
    Main function.
    """
    # ---VARS---
    filetypes = config.FTYPES # list
    search_dirs = config.DIRS # list

    files = []

    for this_dir in search_dirs:
        files.extend(find_files_bytype(this_dir, tuple(filetypes)))

    print(files)

if __name__ == "__main__":
    main()
