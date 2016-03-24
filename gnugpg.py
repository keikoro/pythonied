#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gnupg as gnupg

gpg = gnupg.GPG()
print(gpg)

# check for existence of GnuPG on local system
try:
    gpg = gnupg.GPG()
    print(gpg)
except RuntimeError as err:
    print(err)
    print("You need to download and install GnuPG before "
          "you can run this programm. \n"
          "See https://www.gnupg.org/download/ for more information.")

