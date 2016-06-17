#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
#
# Search a dictionary for occurrences of (parts of) words.
#
# Depends on: config.py
# (variables for dictionary file(s) and words to search)


import config as conf
from os.path import dirname, realpath, join, isdir
from os import makedirs
import sys
import re
import argparse


def main():
    """
    Main function.
    """
    # ---VARS---
    dicts = conf.DICTS
    words = conf.WORDS
    matches = {}
    patterns = []
    this_dir = dirname(realpath(sys.argv[0]))  # cwd
    ext_files = join(dirname(this_dir), 'etc')  # dir for input files

    # HANDLE USER INPUT
    # users can input words or word parts to search for manually
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Search a dictionary for "
                    "occurrences of (parts of) words.")
    parser.add_argument('-w', '--words', nargs='+', metavar='WORD',
                        help="The words or word parts you want to\n"
                             "search the dictionary file(s) for.")
    args = parser.parse_args()

    if args.words:
        words = args.words

    # only continue program if dict(s) and word(s) were provided
    if dicts is not None and len(words) and words[0]:
        # create a pattern (object) based on each word
        for w in words:
            matches[w] = {}
            p = '[\w]*{}[\w]*'.format(w)
            p_obj = re.compile(p, flags=re.IGNORECASE)
            patterns.append(p_obj)

        # check each line of the dict file for the words to look for
        for d in dicts:
            dict_loc = join(ext_files, d)
            print("Searching dictionary {}".format(d))
            with open(dict_loc, mode='r') as file:
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

        # save output files in /var/ directory
        output_dir = join(dirname(this_dir), 'var')

        # TODO only create dir & safe files if there are actual results
        # create output directory if it does not exist yet
        if not isdir(output_dir):
            try:
                makedirs(output_dir)
            # TODO narrow exception clause
            except Exception as err:
                print("Couldn't create directory for saving files. Exiting.")
                print(err)
                exit(1)

        # write all results into files based on the words
        # (pattern: results_WORD.txt)
        for m, words in matches.items():
            result = open(join(output_dir, 'results_' + m + '.txt'), 'w')
            result.write('---\n' + m + '\n---\n')
            print("Search for '{}' finished!".format(m))
            for w in words:
                result.write(w + '\n')
                # debug
                # print(w)

    # print msg if dict/word files were not provided
    else:
        print("ATTN: You seem to not have provided any dictionary files\n"
              "and/or words or word parts to search for. Please try again.")


if __name__ == "__main__":
    main()
