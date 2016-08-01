#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get HTML.

Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>

Connect to a website (or open an HTML file)
and get back its HTML contents.

Depends on:
- logging configuration values in JSON format (default: logconf.json)
- HTTP(S) request header values in JSON format (default: requestheaders.json)
"""

import json
import random
import sys
import urllib.error
from platform import system
from time import strftime
from urllib.request import urlopen

import requests

from fchecks import file_is
from log import log


def custom_headers(fpath='requestheaders.json', seed=strftime("%Y-%m-%d %H"),
                   use_os=True):
    """
    Custom headers for http(s) request.

    Create headers using common user agents as found on e.g.
    https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    to make requests look less bot-like.

    :param fpath: file path to JSON file containing possible header values
    :param seed: seed to use to randomise headers; defaults to hourly change,
                 can also be set to None (headers will then always change)
    :param use_os: if True, tries to only use headers applicable to the
                   operating system running the script
    """
    random.seed(a=seed)

    # try opening the JSON file containing possible header values
    try:
        with open(fpath, 'r') as f:
            json_content = json.load(f)

        moz = json_content['mozilla']
        platform = random.sample(tuple(json_content['platforms']), 1)[0]

        # if the executing machine's OS matches any of the OS
        # listed in the JSON, use that OS for headers
        if use_os:
            this_os = system()
            if this_os in json_content['platforms']:
                platform = this_os
                log.debug("OS detected: {}".format(platform))

        p_vers = random.sample(tuple(json_content['platforms']
                                     [platform]['versions']), 1)[0]
        browser = random.sample(tuple(json_content['platforms']
                                      [platform]['browsers']), 1)[0]
        b_vers = random.sample(tuple(json_content['browsers']
                                     [browser]['versions']), 1)[0]
        b_app = random.sample(tuple(json_content['browsers']
                                    [browser]['appnames']), 1)[0]

        user_agent = "{} ({}) {} {}".format(moz, p_vers, b_vers, b_app)

        accept = json_content['browsers'][browser]['accept']
        accept_encoding = json_content['accept-encoding']
        accept_lang = random.sample(tuple(json_content['accept-lang']), 1)[0]

    # fall back on one set of headers in case the JSON file cannot be opened
    except (FileNotFoundError, PermissionError):
        log.error("Cannot read header data from JSON file {}. ".format(fpath))
        sys.exit(1)

    headers = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept-Encoding": accept_encoding,
        "Accept-Language": accept_lang
    }

    for k, v in sorted(headers.items()):
        log.debug("{}: {}".format(k, v))

    return headers


def open_website(url):
    """
    Open a website or local HTML file
    and return its HTML contents.

    :param url: the website/file to be opened
    :return: an HTML object, or None
    """
    session = requests.Session()
    headers = custom_headers()

    # connect to the (assumed) website
    try:
        r = session.get(url, headers=headers, verify=True, timeout=5)
        # check the status code returned by the web request
        # only status 200 (OK) signifies the request was successful
        if not r.status_code // 100 == 2:
            # output a separate message for 404 errors
            if r.status_code == 404:
                log.error("404 – page not found: {}".format(url))
            # output for all errors that are not 404
            log.error("Unexpected response {}".format(r))
        else:
            log.info("Opening {}".format(url))
            r.encoding = r.apparent_encoding
            html = r.text
            return html
    # connection timeout
    except requests.exceptions.ConnectTimeout:
        log.error("The connection timed out.")
    # ambiguous exceptions on trying to connect to website
    except requests.exceptions.RequestException as e:
        # when there is a problem with reading the file
        # check if it's a local file (requests lib does not work with those)
        if "No connection adapters were found for" not in str(e):
            fpath = "file:///{}".format(url)
            log.info("URL seems to be pointing to a local file. "
                     "Trying to open...".format(fpath))
            if file_is(url):
                # check if url is actually a local file
                try:
                    # make sure the file can be read
                    f = urlopen(fpath)
                    html = f.read()
                    return html
                # if the local file cannot be opened/does not exist
                except urllib.error.URLError:
                    log.error("Not a valid file: {}".format(url))
                # unforeseen exception
                except Exception as e:
                    log.error("An unexpected error occurred on line {}."
                              .format(sys.exc_info()[2].tb_lineno))
                    log.error(e)
        # if the url is NOT a local file, sth. else went wrong
        # with the request
        else:
            log.error("Invalid request. Cannot open website: {}".format(url))
    # unforeseen exception
    except Exception as e:
        log.error("An unexpected error occurred on line {}."
                  .format(sys.exc_info()[2].tb_lineno))
        log.error(e)

    return None


def main():
    """Main function."""

    # ---USER INPUT---
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="")
    parser.add_argument('-u', '--url',
                        help="URL to get HTML from")
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        log.error("No URL provided!")
        url = input("URL: ")

    html = open_website(url)
    if html:
        log.info(html)


if __name__ == "__main__":
    # imports only relevant for main
    import argparse

    main()
