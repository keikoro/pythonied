#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>

import av_filerename_config as config
import os


def main():
    """
    Main function.
    """
    # ---VARS---
    filetypes = ('mpg', 'mpeg', 'avi', 'mkv', 'mp4', 'srt', 'idx', 'sub')
    search_dirs = config.DIRS

    files = []

    for this_dir in search_dirs:
        for startdir, subdirs, filenames in os.walk(this_dir):
            for file in filenames:
                if file.endswith(filetypes):
                    files.append(file)

    print(files)

if __name__ == "__main__":
    main()
