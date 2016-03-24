#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tl_config as tlconf
import logging
import time
from os.path import expanduser

rn = time.strftime("%Y-%m-%d %H:%M")
home = expanduser("~")

logging.basicConfig(filename='error.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

try:
    thisfile = open(tlconf.user_dir + "logger.txt", 'a')
    thisfile.write("logged: " + rn + " (home: " + home + ")\n")
except Exception as err:
    logger.error(err)
