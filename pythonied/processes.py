#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processes - demo of process pool.

Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>
"""

import random
import time
from multiprocessing.dummy import Pool

from log import log


def url_name(url):
    sleep_time = random.choice(range(0, 10))
    time.sleep(sleep_time)
    return sleep_time, url


def main():
    urls = [
      'http://www.python.org',
      'https://stackoverflow.com/',
      'https://css-tricks.com/',
      'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
      'https://dev.twitter.com/',
      'https://d3js.org/',
      'https://www.heroku.com/',
      'https://docs.pytest.org/en/latest/',
      'https://www.djangoproject.com/',
      'https://pudding.cool/',
      'https://caniuse.com/',
      'http://svgpocketguide.com/book/',
      'https://www.w3.org/TR/SVG/intro.html',
      ]

    pool = Pool()
    start = time.time()
    for x, y in pool.imap_unordered(url_name, urls):
        index = urls.index(y)
        log.info("{}s (sleep: {}) (#{} in array) for {})"
                 .format(int(time.time() - start), x, index, y))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
