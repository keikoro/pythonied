#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script for
# - creating a local directory for storing/managing GPG keys
# - creating new GPG keys (using a name and e-mail address)
#
# Depends on: gpg_config.py
# where variables for the directory path, the encryption algorithm
# and the key strenght are stored.

import gpg_config as config
# using python-gnupg
# https://pypi.python.org/pypi/python-gnupg
# https://pythonhosted.org/python-gnupg/
from os.path import exists
from os import access, W_OK, X_OK, makedirs
import gnupg
import argparse


def dir_checkmake(thisdir, permission=0o755):
    """
    Check for the existence of a directory.

    Try to create the directory if it doesn't exist.
    Use permission setting 755 if no other value is provided.
    """
    if not exists(thisdir):
        try:
            makedirs(thisdir, mode=permission)
            print("Directory {} created, continuing program.".format(thisdir))
        except PermissionError as err:
            print("Directory {} does not exit "
                  "and cannot be created either.\n"
                  "Make sure the necessary permissions are set "
                  "for the provided path.".format(thisdir))
            exit(1)
    # if it exists, check if it can be written to
    elif not access(thisdir, W_OK | X_OK):
        print("Directory {} exists but cannot be written to.\n"
              "Make sure the necessary permissions are set "
              "for the provided path.".format(thisdir))
        exit(1)
    else:
        print("Directory {} exists and can be written to.".format(thisdir))


def gnupg_check(thisdir):
    """
    Check for existence of GnuPG on the local system.

    Check for gpg binaries in the following order:
        - link to gpg in $PATH
        - gpg2 in /usr/local/bin/gpg2
        - gpg in /usr/local/bin/gpg
    """
    binary1 = "/usr/local/bin/gpg2"
    binary2 = "/usr/local/bin/gpg"
    verbosity = False
    try:
        gpg = gnupg.GPG(gnupghome=thisdir, verbose=verbosity)
        # debug
        print("GPG binary used: {}".format(gpg.gpgbinary))
        return gpg
    except OSError as err:
        try:
            gpg = gnupg.GPG(gnupghome=thisdir,
                            gpgbinary=binary1,
                            verbose=verbosity)
            # debug
            print("GPG binary used: {}".format(gpg.gpgbinary))
            return gpg
        except OSError as err:
            try:
                gpg = gnupg.GPG(gnupghome=thisdir,
                                gpgbinary=binary2,
                                verbose=verbosity)
                # debug
                print("GPG binary used: {}".format(gpg.gpgbinary))
                return gpg
            except RuntimeError as err:
                print(err)
                print("You need to download and install GnuPG before "
                      "you can run this programm. \n"
                      "See https://www.gnupg.org/download/ "
                      "for more information.")
                exit(1)


def main():
    """
    Main function.
    """
    # ---VARS---
    gpgdir = config.GPGDIR
    alg = config.GPGTYPE
    keylength = config.GPGKEYLENGTH
    keylist = False
    new = False

    # HANDLE USER INPUT
    # user can list all available keys on the system
    # and create new keys using RSA with a key length of 4096
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Sign e-mail messages using GnuPG.",
        epilog="For more entropy during key creation, make sure to e.g. \n"
               "move around your mouse pointer or perform some other action\n"
               "on your machine.")
    parser.add_argument('-n', '--new', nargs=2, metavar=('NAME', 'EMAIL'),
                        help="Create a new GPG key using type RSA and "
                             "key length\n"
                             "of 4096. You will have to provide a name "
                             "and e-mail\n"
                             "address for which this key should be created.")
    parser.add_argument('-l', '--list', action='store_true',
                        help="list all known GPG keys.")
    args = parser.parse_args()

    if args.list:
        keylist = True
    if args.new:
        new = True
        key_name = args.new[0]
        key_email = args.new[1]

    # create .gpgdir with correct permissions if it doesn't exist
    dir_checkmake(gpgdir, permission=0o700)

    # look for gpg on the system
    gpg = gnupg_check(gpgdir)

    # list all existing keys
    if keylist:
        print("List of all GPG keys:")
        print(gpg.list_keys())

    if new:
        # create a new GPG key
        try:
            input_data = gpg.gen_key_input(key_type=alg,
                                           key_length=keylength,
                                           name_real=key_name,
                                           name_email=key_email)
            key = gpg.gen_key(input_data)
            # debug
            print("The newly created GPG key is:")
            print(key)
        except Exception as err:
            print("An unexpected error occurred while trying"
                  "to create a new GPG key:")
            print(err)
            exit(1)


if __name__ == "__main__":
    main()
