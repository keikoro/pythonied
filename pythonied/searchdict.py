#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search a dictionary for occurrences of (parts of) words.

Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>

Depends on: config.py
(variables for dictionary file(s) and words to search)
"""


import config as conf
from os.path import dirname, realpath, join, isdir
from os import makedirs
import sys
import re
import argparse
from itertools import combinations
from locale import setlocale, getlocale, strxfrm, LC_ALL

# strxfrm apparently broken for several German locales on OS X, like UTF-8
# -> umlauts currently get sorted after words starting with z!
setlocale(LC_ALL, 'de_AT.UTF-8')

# debug
# print(getlocale(LC_ALL))


def print_results(word, match_dict):
    """
    Print all matches found for a word to stdout.

    :param word: a word that was looked for
    :param match_dict: dictionary of matches for that word
    """
    # create 'headline'
    sep = '-' * len(word)
    print(sep)
    print(str(word))
    print(sep)

    # account for intersected word sets
    if isinstance(match_dict, set):
        matches = {str(match_dict): ''}
    else:
        matches = dict(match_dict)

    # use lambda for sorting the matches lowercased
    # (otherwise matches starting with a capital letter get sorted first)
    # ATTN not working!
    # strxfrm for umlaut sorting broken in several German locales on OS X
    for word, suppl in sorted(matches.items(),
                              key=lambda w: strxfrm(w[0].lower())):
        print(word, end=' ')
    print()


def intersect_matches(match_dict):
    """
    Intersect all existing result sets for words.

    :param match_dict: dictionary of dictionaries of matches
    :return: a dictionary of dictionaries containing matches
    """
    shared = {}

    matches = dict(match_dict.items())
    words = list(sorted(match_dict.keys(), key=str.lower))

    for i in range(2, len(words) + 1):
        for elems in combinations(words, i):

            # list of sets of matches
            match_sets = [set(list(matches[elems[j]])) for j in
                          range(len(elems))]
            # intersect available match sets to find common words
            # and add them to the 'shared' dictionary
            shared_matches = set.intersection(*match_sets)
            if shared_matches:
                shared[elems] = shared_matches
    # debug
    # print(shared)

    return shared


def save_single(output_dir, word, match_dict):
    """
    Save found matches into text files.

    :param output_dir: directory to save files in
    :param word: the word which was searched for
    :param match_dict: a dictionary of matches
    """
    # file name pattern results_WORD.txt
    filename = join(output_dir, 'results_' + word + '.txt')

    # create 'headline'
    sep = '-' * len(word)
    file = open(filename, 'w')
    file.write(word + '\n')
    file.write(sep + '\n')

    matches = dict(match_dict)

    # use lambda for sorting the matches lowercased
    # (otherwise matches starting with a capital letter get sorted first)
    # ATTN not working!
    # strxfrm for umlaut sorting broken in several German locales on OS X?
    for word, suppl in sorted(matches.items(),
                              key=lambda w: (
                                      strxfrm(w[0].lower()),
                                      strxfrm(w[1].lower()))):
        file.write(word)
        if suppl:
            file.write('\t[' + suppl + ']')
        file.write('\n')
        # debug
        # print(word, end=' ')
        # if value:
        #     print('\t[' + value + ']', end='')
    # print()

    file.close()


def save_intersecting(output_dir, words, match_dict):
    """
     Save intersectnig matches into one single text file.

    :param output_dir: directory to save file in
    :param words: the word combinations which were searched for
    :param match_dict: a dictionary of matches
    """
    filename = join(output_dir, 'shared_' + '+'.join(
        sorted(words, key=str.lower)) + '.txt')

    file = open(filename, 'w')

    # use lambda for sorting the matches lowercased
    # (otherwise matches starting with a capital letter get sorted first)
    # ATTN not working!
    # strxfrm for umlaut sorting broken in several German locales on OS X?
    matches = dict(match_dict)
    for combo, results in sorted(matches.items(),
                                 key=lambda w: (
                                         strxfrm(''.join(w[0]).lower()),
                                         strxfrm(''.join(w[1]).lower()))):

        # separator
        combo_combined = '+'.join(combo)
        sep = '-' * len(combo_combined)
        file.write(combo_combined + '\n')
        file.write(sep + '\n')

        for res in results:
            file.write(res + '\n')
        file.write('\n')

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


def create_dir(output_dir):
    try:
        makedirs(output_dir)
    # TODO narrow exception clause
    except Exception as err:
        print("Couldn't create directory for "
              "saving files. Exiting.")
        print(err)
        exit(1)


def main():
    """
    Main function.
    """
    # ---VARS---
    dicts = conf.DICTS
    words = conf.WORDS
    matches = {}
    patterns = []
    intersect = None
    save = None
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
    parser.add_argument('-i', '--intersect', action='store_true',
                        help="Intersect the words you are looking for\n"
                             "to find only results that match them all.")
    parser.add_argument('-s', '--save', action='store_true',
                        help="Save all results to text files,\n"
                             "otherwise only display the results.")
    args = parser.parse_args()

    if args.words:
        words = args.words
    if args.intersect:
        intersect = 1
    if args.save:
        save = 1
        # save output files in /var/ directory
        output_dir = join(dirname(this_dir), 'var')
        # create output directory if it does not exist yet
        if not isdir(output_dir):
            create_dir(output_dir)

    # only continue program if dict(s) and word(s) were provided
    if dicts is not None and len(words) and words[0]:

        # create patterns to search for based on words
        patterns = create_patterns(words, patterns)

        # search dict files
        for d in dicts:
            dict_loc = join(input_dir, d)
            print("Searching dictionary {}".format(d))
            search_single_words(dict_loc, words, patterns, matches)

        # print results
        # or create dir/files for results if there are matches + save flag
        if len(matches):
            # function call per word
            for word, results in matches.items():
                if save:
                    save_single(output_dir, word, results)
                    print("Search for '{}' saved: {} "
                          "matches!".format(word, len(results)))
                else:
                    print_results(word, results)

            # intersect matches to find words that match sets have in common
            if intersect:
                print("Looking for shared words in all matches...")
                shared_matches = intersect_matches(matches)
                if shared_matches:
                    if save:
                        save_intersecting(output_dir, words, shared_matches)
                        print("Shared words saved.")
                    else:
                        for word_combo, results in sorted(
                                shared_matches.items(),
                                key=lambda w: (strxfrm(
                                            ''.join(list(w[0])).lower()))):
                            print_results('+'.join(word_combo), results)
                else:
                    print("No intersections found.")
        else:
            print("No matches.")

    # print msg if dict/word files were not provided
    else:
        print("ATTN: You seem to not have provided any dictionary files\n"
              "and/or words or word parts to search for. Please try again.")


if __name__ == "__main__":
    main()
