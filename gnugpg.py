#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# using python-gnupg
# https://pypi.python.org/pypi/python-gnupg
# https://pythonhosted.org/python-gnupg/
import gnupg
from os.path import expanduser, join, isdir, exists
from os import access, W_OK, X_OK

def main():
    # set the home directory to ~/.gnupg
    dir = join(expanduser('~'), '.gnupg')

    # check if gnupg directory is writeable/executable
    if (access(dir, W_OK | X_OK)):

        # check for existence of GnuPG on local system
        # check: without binary -> gpg2 -> gpg
        try:
            gpg = gnupg.GPG(gnupghome=dir, verbose=True)
            # debug
            print(gpg.gpgbinary)
        except OSError as err:
            try:
                gpg = gnupg.GPG(gnupghome=dir, gpgbinary='/usr/local/bin/gpg2', verbose=True)
                # debug
                print(gpg.gpgbinary)
            except OSError as err:
                try:
                    gpg = gnupg.GPG(gnupghome=dir, gpgbinary='/usr/local/bin/gpg', verbose=True)
                    # debug
                    print(gpg.gpgbinary)
                except RuntimeError as err:
                    print(err)
                    print("You need to download and install GnuPG before "
                          "you can run this programm. \n"
                          "See https://www.gnupg.org/download/ for more information.")
                    exit(1)
    else:
        print("Sorry, but the directory provided for "
              "GnuPG keyrings is not writeable.")


if __name__ == "__main__":
    main()
