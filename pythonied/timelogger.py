#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>


import timelogger_config as tlconf
import logging
import time
from os.path import expanduser
from sys import path
from os.path import join
import subprocess

rn = time.strftime("%Y-%m-%d %H:%M")
home = expanduser("~")

try:
    this_file = open(join(tlconf.user_dir, tlconf.log_file), 'a')
    this_file.write("logged: " + rn + " (home: " + home + ")\n")
except Exception as err:
    # create error log in directory containing the script
    logging.basicConfig(filename=join(path[0],tlconf.error_log), level=logging.DEBUG,
                    format=tlconf.error_format)
    logger = logging.getLogger(__name__)
    subprocess.call('osascript -e "display notification '
                    '\\\"$(date)\n' + str(err) + '\\\" '
                    'with title \\\"Timelogger script failed!\\\" "',
                    shell=True)
    logger.error(err)
    exit(1)
