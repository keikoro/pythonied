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
            p = '[\w]*{}[\w]*'.format(w)
            pfull = '[^;]*{}[^;]*'.format(w)
            p_obj = re.compile(p, flags=re.IGNORECASE)
            pfull_obj = re.compile(pfull, flags=re.IGNORECASE)
            patterns.append([p_obj, pfull_obj])

        # check each line of the dict file for the words to look for
        for d in dicts:
            dict_loc = join(ext_files, d)
            print("Searching dictionary {}".format(d))
            with open(dict_loc, mode='r') as file:
                for line in file.read().splitlines():
                    # ignore comments in dictionary files
                    if not line.startswith("#"):
                        for w, p in zip(words, patterns):
                            # match result is a list
                            this_match = re.findall(p[0], line)
                            this_match_full = re.findall(p[1], line)
                            # put all matches for a word
                            # into a dictionary named after the word
                            if this_match:
                                # initial creation of the dict
                                if w not in matches:
                                    matches[w] = {}
                                # enter keys and values
                                for m, mf in zip(this_match, this_match_full):
                                    # initial creation of dict entries
                                    matches[w][m] = ''
                                    # + add full matches if they differ
                                    if m != mf:
                                        if not matches[w][m]:
                                            matches[w][m] = mf

            file.close()

        # only create dir/files for results if there are matches
        if len(matches):

            # save output files in /var/ directory
            output_dir = join(dirname(this_dir), 'var')

            # create output directory if it does not exist yet
            if not isdir(output_dir):
                try:
                    makedirs(output_dir)
                # TODO narrow exception clause
                except Exception as err:
                    print("Couldn't create directory for "
                          "saving files. Exiting.")
                    print(err)
                    exit(1)

            # write results into files (one for each word)
            for m, words in matches.items():
                # file name pattern: results_WORD.txt
                filename = join(output_dir, 'results_' + m + '.txt')
                file = open(filename, 'w')
                # create headline from word
                file.write(m + '\n' + '-' * len(m) + '\n')
                # print no. of matches
                print("Search for '{}' finished: {} "
                      "matches!".format(m, len(words)))

                # write matches into results file
                for key, value in sorted(words.items()):
                    file.write(key)
                    if value:
                        file.write('\t[' + value + ']')
                    file.write('\n')
                    # debug
                    # print(key,end='')
                    # if value:
                    #     print('\t[' + value + ']', end='')
                    # print()

                file.close()
        else:
            print("No matches.")

    # print msg if dict/word files were not provided
    else:
        print("ATTN: You seem to not have provided any dictionary files\n"
              "and/or words or word parts to search for. Please try again.")


if __name__ == "__main__":
    main()
