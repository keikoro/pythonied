#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import timelogger_config as tlconf
import logging
import time
from os.path import expanduser
import subprocess

rn = time.strftime("%Y-%m-%d %H:%M")
home = expanduser("~")

logging.basicConfig(filename='error.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

try:
    this_file = open(tlconf.user_dir + tlconf.log_file, 'a')
    this_file.write("logged: " + rn + " (home: " + home + ")\n")
except Exception as err:
    subprocess.call('osascript -e "display notification '
                    '\\\"$(date)\n' + str(err) + '\\\" '
                    'with title \\\"Timelogger script failed!\\\" "',
                    shell=True)
    logger.error(err)
    exit(1)
