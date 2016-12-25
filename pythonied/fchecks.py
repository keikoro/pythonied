#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check if a file exists and is writeable.

Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>

Depends on:
- logconf.json for logging configuration
"""

import sys
from log import log
from os import W_OK, access, makedirs
from os.path import basename, dirname, exists, join

from log import log


def file_is(fpath, c=False, ftype='f', fname=None):
    """
    Check if a file exists (and try to create it if it does not).

    :param fpath: full path to a file
    :param c: if set to True, create file if it does not exist yet
    :param ftype: type; defaults to file
    :param fname: file name; used for recursive use of the function
           (when directory creation has to precede file creation)
    :return return file path if file/dir exists, otherwise return None
    """
    fp = None

    # if path name ends in / it is a directory
    if fpath[-1] == '/' or ftype == 'd' or ftype == 'dir':
        this_type = 'directory'
    else:
        this_type = 'file'

    # check if file exists
    if exists(fpath):
        # check if file is writeable
        if not access(fpath, W_OK):
            log.warning("{} {} exists but is not writeable."
                        .format(this_type.title(), fpath))
        else:
            log.info("{} {} exists and is writeable."
                     .format(this_type.title(), fpath))
            fp = fpath
    else:
        if not c:
            log.error("{} {} does not exist."
                      .format(this_type.title(), fpath))
        else:
            # try to create a file or directory (depending)
            try:
                if this_type == 'file':
                    open(fpath, 'w')
                    fp = fpath
                    log.info("File created.")
                else:
                    makedirs(fpath, mode=0o777)
                    fp = fpath
                    log.info("Successfully created directory.")
                    # if the intention was to create a file as well as
                    # its containing directory (indicated by setting the
                    # ftype flag to 'd' or 'dir' as well as providing fname
                    # for the actual file name), call the function again
                    if fname and (ftype == 'd' or ftype == 'dir'):
                        file_is(join(fpath, fname))
            except PermissionError:
                log.error("Permission Error: {} {} does not exist or "
                          "cannot be accessed.".format(this_type.title(),
                                                       fpath))
            except FileNotFoundError:
                if this_type == 'file':
                    file_dir = dirname(fpath)
                    log.error("File not found. Checking for existence "
                              "of parent directory {}.".format(file_dir))
                    file_is(file_dir, ftype='d', fname=basename(fpath))
            except NotADirectoryError:
                log.error("File {} exists but is not a directory "
                          "(leave off trailing slash).".format(fpath))
            # unforeseen exception
            except Exception as e:
                line_no = sys.exc_info()[2].tb_lineno
                log.exception("An unexpected error occurred on line {} while "
                              "checking for existance of file {}: {}"
                              .format(fpath, line_no, e))

    return fp


def main():
    """Main function."""

    # ---USER INPUT---
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="")
    parser.add_argument('-f', '--file',
                        help="File to look for")
    args = parser.parse_args()

    if args.file:
        fname = args.file
    else:
        log.error("No file provided!")
        fname = input("Path to file: ")

    file_is(fname, c=False)


if __name__ == "__main__":
    # imports only relevant for main
    import argparse

    main()
