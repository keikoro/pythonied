#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
#
# Search a dictionary for occurrences of (parts of) words.
#
# Depends on: config.py
# (variables for dictionary file(s) and words to search)


import re
import config as conf


def main():
    """
    Main function.
    """
    # ---VARS---
    dicts = conf.DICTS
    words = conf.WORDS
    countw = len(words)
    matches_single = []
    matches_all = []


    for match in matches_single:
        print(match)


if __name__ == "__main__":
    main()
