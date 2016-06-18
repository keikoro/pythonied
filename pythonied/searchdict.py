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


def intersect_matches(matches):
    """
    Intersect all existing result sets for words.

    :param matches: dictionary of dictionaries of matches
    :return:
    """
    intersect = {}
    word_list = []
    results_list = []
    for word, results in matches.items():
        word_list.append(word)
        results_list.append(results)

    # debug
    print(word_list)
    print(results_list)


def save_matches(output_dir, word, matches):
    """
    Save found matches into text files.

    :param output_dir: directory to save files in
    :param word: the word which was searched for
    :param matches: a dictionary of matches
    """
    # file name pattern: results_WORD.txt
    filename = join(output_dir, 'results_' + word + '.txt')
    file = open(filename, 'w')
    # create headline from word
    file.write(word + '\n' + '-' * len(word) + '\n')
    # print no. of matches
    print("Search for '{}' finished: {} "
          "matches!".format(word, len(matches)))

    # write alphabetically sorted matches into results file
    for key, value in sorted(matches.items()):
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


def search_single_words(dictionary, words, patterns, matches):
    """
    Search for words or words parts in a dictionary file.
    Search the file line by line, looking for particular patterns.

    :param dictionary: path to the dictionary file to search in
    :param words: list of words/word parts to search for
    :param patterns: patterns to search for
    :param matches: dictionary of dictionaries to save matches in
    :return: dictionary of dictionaries of matches
    """
    with open(dictionary, mode='r') as file:
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
    return matches


def create_patterns(words, patterns):
    """
    Create lists of pattern objects
    based on words/word parts to search for.

    :param words: words to search for
    :param patterns: a list to save all search patterns in
    :return: list of search patterns
    """
    # create a pattern (object) based on each word
    for w in words:
        p = '[\w]*{}[\w]*'.format(w)
        pfull = '[^;]*{}[^;]*'.format(w)
        p_obj = re.compile(p, flags=re.IGNORECASE)
        pfull_obj = re.compile(pfull, flags=re.IGNORECASE)
        patterns.append([p_obj, pfull_obj])

    return patterns


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
    input_dir = join(dirname(this_dir), 'etc')  # dir for input files

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

        # create patterns to search for based on words
        patterns = create_patterns(words, patterns)

        # search dict files
        for d in dicts:
            dict_loc = join(input_dir, d)
            print("Searching dictionary {}".format(d))
            search_single_words(dict_loc, words, patterns, matches)

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


            # write results into files (one file per word)
            for word, results in matches.items():
                # save_matches(output_dir, word, results)
                pass

            intersect_matches(matches)



        else:
            print("No matches.")

    # print msg if dict/word files were not provided
    else:
        print("ATTN: You seem to not have provided any dictionary files\n"
              "and/or words or word parts to search for. Please try again.")


if __name__ == "__main__":
    main()
