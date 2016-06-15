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
    matches = {}
    patterns = []

    # create a pattern (object) based on each word
    for w in words:
        matches[w] = {}
        p = '[\w]*{}[\w]*'.format(w)
        p_obj = re.compile(p, flags=re.IGNORECASE)
        patterns.append(p_obj)

    for d in dicts:
        print("Searching dictionary {}".format(d))
        with open(d, mode='r') as file:
            # iterate over all lines, stripping newlines
            for line in file.read().splitlines():
                # ignore comments in dictionary files
                if not line.startswith("#"):
                    for w, p in zip(words, patterns):
                        this_match = p.search(line)
                        # put all matches for a word into
                        # the dictionary named after the word
                        if this_match:
                            matches[w][this_match.group(0)] = ''
        file.close()

    for m, words in matches.items():
        # write all results into a file based on the word
        result = open('results_' + m + '.txt', 'w')
        result.write('---\n' + m + '\n---\n')
        # debug
        # print(m)
        # print('---')
        for w in words:
            result.write(w + '\n')
            # debug
            # print(w)


if __name__ == "__main__":
    main()
