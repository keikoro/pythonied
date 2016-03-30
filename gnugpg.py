#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gnupg

# check for existence of GnuPG on local system
try:
    # gpg = gnupg.GPG(homedir='/Users/Kay/.gnupg', verbose='True')
    gpg = gnupg.GPG(verbose='True')
    gpg.encoding = 'ascii'
    print(gpg)
    # input_data = gpg.gen_key_input(key_type='RSA',
    #                               key_length=1024, name_real='Test name')
    # key = gpg.gen_key(input_data)
    # print(key)
    public_keys = gpg.list_keys()
    print(public_keys)

except RuntimeError as err:
    print(err)
    print("You need to download and install GnuPG before "
          "you can run this programm. \n"
          "See https://www.gnupg.org/download/ for more information.")
    exit(1)

