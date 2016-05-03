#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script for sending e-mail.
#
# Depends on: sendmail_config.py
# where variables for server, sender, recipient
# and message to be sent are stored.

import sendmail_config as config
import getpass
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL, SMTPAuthenticationError, \
    SMTPNotSupportedError, SMTPConnectError
from ssl import SSLError


def main():
    """
    Main function.
    """
    # ---VARS---
    timeout = 10
    recipient = ''

    # read message data from file
    msg_file = config.MSG
    with open(msg_file, mode='r') as m:
        read_msg = m.read()
        full_msg = read_msg.split('\n', 1)

    subject = full_msg[0]
    content = full_msg[1]
    # debug
    # print("Subject: {}".format(subject))
    # print("Content: {}".format(content))

    text_type = "plain"

    # define parts of the e-mail to be sent
    msg = MIMEText(content, text_type)
    msg['Subject'] = subject
    msg['From'] = config.SENDER

    # try to establish connection to server
    server = config.SERVER
    port = config.PORT
    # debug
    print(server)

    if config.PASS:
        userpass = config.PASS
    else:
        userpass = getpass.getpass()

    if config.RECIPIENT:
        recipient = config.RECIPIENT
    else:
        recipient = input("Who do you want to send your e-mail to? ")

    # debug
    print("Recipient: {}".format(recipient))

    try:
        if config.SEC == 'STARTTLS':
            # debug
            # print("with STARTTLS")
            conn = SMTP(server, port, timeout=timeout)
            # conn.set_debuglevel(True)
            conn.set_debuglevel(False)
            conn.starttls()
        elif config.SEC == 'SSL':
            # debug
            # print("with SSL")
            conn = SMTP_SSL(server, port, timeout=timeout)

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

    try:
        conn.login(config.USER, userpass)
        print("Login successful!")
    except Exception as err:
        print("Could not log in.")
        print(err)
        exit(1)

    try:
        conn.sendmail(config.SENDER, recipient, msg.as_string())
        print("Email sent!")
    except Exception as err:
        print("Could not send e-mail.")
        print(err)
        exit(1)

    conn.quit()


if __name__ == "__main__":
    main()
