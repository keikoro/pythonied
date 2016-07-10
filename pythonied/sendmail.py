#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for sending e-mail.

Copyright (c) 2016 K Kollmann <code∆k.kollmann·moe>

Sends an e-mail message to a specified recipient
from a specified e-mail address using SMTP login data.

Depends on: config.py
(variables for server, sender, recipient, message to be sent)
"""


import config as conf
import getpass
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL, SMTPAuthenticationError, \
    SMTPNotSupportedError, SMTPConnectError
from ssl import SSLError
from sys import path
from os.path import join


def main():
    """
    Main function.
    """
    # ---VARS---
    timeout = 10
    recipient = ''
    text_type = conf.TTYPE

    # read message data from file
    msg_file = conf.MSG
    with open(join(path[0], msg_file), mode='r') as m:
        read_msg = m.read()
        full_msg = read_msg.split('\n', 1)

    subject = full_msg[0]
    content = full_msg[1]
    # debug
    # print("Subject: {}".format(subject))
    # print("Content: {}".format(content))

    # define parts of the e-mail to be sent
    msg = MIMEText(content, text_type)
    msg['Subject'] = subject
    msg['From'] = conf.SENDER

    # try to establish connection to server
    server = conf.SERVER
    port = conf.PORT
    # debug
    print(server)

    # use variables from config file if provided,
    # otherwise prompt the user to input
    # - the password for the e-mail account
    # - the recipient's e-mail address
    if conf.PASS:
        userpass = conf.PASS
    else:
        userpass = getpass.getpass()

    if conf.RECIPIENT:
        recipient = conf.RECIPIENT
    else:
        recipient = input("Who do you want to send your e-mail to? ")

    # debug
    print("Recipient: {}".format(recipient))

    # pick encryption method based on config file
    try:
        if conf.SEC == 'STARTTLS':
            # debug
            # print("with STARTTLS")
            conn = SMTP(server, port, timeout=timeout)
            # conn.set_debuglevel(True)
            conn.set_debuglevel(False)
            conn.starttls()
        elif conf.SEC == 'SSL':
            # debug
            # print("with SSL")
            conn = SMTP_SSL(server, port, timeout=timeout)

    # check for various errors on trying to connect
    except SMTPConnectError as err:
        print("SMTPConnectError")
        print(err)
        exit(1)

    except SMTPAuthenticationError as err:
        print("SMTPAuthenticationError")
        print(err)
        exit(1)

    except SMTPNotSupportedError as err:
        print("SMTPNotSupportedError")
        print(err)
        exit(1)

    except SSLError as err:
        print("An SSL error occured. Stopping program.")
        print(err)
        exit(1)

    except Exception as err:
        print("An unexpected exception occured. Stopping program.")
        print(err)
        exit(1)

    ehlo = conn.ehlo()
    # debug
    print(ehlo)

    # smtp login
    try:
        conn.login(conf.USER, userpass)
        print("Login successful!")
    except Exception as err:
        print("Could not log in.")
        print(err)
        exit(1)

    # sending of e-mail
    try:
        conn.sendmail(conf.SENDER, recipient, msg.as_string())
        print("Email sent!")
    except Exception as err:
        print("Could not send e-mail.")
        print(err)
        exit(1)

    conn.quit()


if __name__ == "__main__":
    main()
