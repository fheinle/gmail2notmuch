#!/usr/bin/env python2

"""add notmuch tags to maildir w/ X-Keywords header in mails"""
import os
import sys
import ConfigParser
import logging

import notmuch

def get_notmuch_config():
    """get notmuch config

    order of precedence:
        1. given on sys.argv[1] or
        2. environment variable NOTMUCH_CONFIG
        3. from ~/.notmuch-config
        4. fail"""
    if len(sys.argv) > 1:
        if os.path.isdir(
                os.path.join(sys.argv[1]),
                '.notmuch'
        ):
            logging.debug('Using notmuch config from command line')
            notmuch_config_fname = sys.argv[1]
    elif os.getenv('NOTMUCH_CONFIG'):
        notmuch_config_fname = os.getenv('NOTMUCH_CONFIG')
        logging.debug('Using notmuch config from env variable')
        notmuch_config_fname = os.getenv('NOTMUCH_CONFIG')
    else:
        notmuch_config_fname = os.path.join(os.path.expanduser('~'), '.notmuch-config')
    try:
        notmuch_config = ConfigParser.SafeConfigParser()
        notmuch_config.read(os.path.join(
            os.path.expanduser('~'),
            notmuch_config_fname
        ))
        logging.debug('Using notmuch config from config file')
        return notmuch_config.get('database', 'path')
    except:
        logging.error('No usable notmuch config')
        raise RuntimeError('No notmuch config found')

def add_tags(notmuch_db, add_gmail=False):
    """loop through all the messages and tags from X-Keywords header to
    notmuch. This obviously might take a while

    @param notmuch_db: notmuch db instance
    @param add_gmail: wether to add tags like Sent, Important, etc"""
    all_messages = notmuch.Query(notmuch_db, '').search_messages()
    for message in all_messages:
        message_tags = message.get_header('X-Keywords')
        if message_tags:
            for tag in message_tags.split(','):
                if tag.startswith('\\'):
                    if add_gmail:
                        message.add_tag(tag)
                else:
                    logging.debug('Adding tag %s to msg <%s>', tag, message.get_message_id())
                    message.add_tag(tag)

def main(add_gmail=False):
    """run it all"""
    notmuch_config = get_notmuch_config()
    logging.info("Notmuch config used: %s", notmuch_config)
    logging.info("Setting up notmuch database")
    notmuch_database = notmuch.Database(path=notmuch_config, create=False,
                                        mode=notmuch.Database.MODE.READ_WRITE)
    add_tags(notmuch_database, add_gmail)

if __name__ == '__main__':
    if len(sys.argv == 1) or sys.argv[1] in ('-h', '--help'):
        print '''Usage: %s [config_path] [--add-gmail-tags]

              config_path (optional): specify path to notmuch config file
              --add-gmail-tags (optional): add internal gmail tags like Sent, Important, etc, too 

              This script will try config filenames in the following order:
              1. [config_path] from commandline
              2. NOTMUCH_CONFIG environment variable
              3. ~/.notmuch-config
              
              You may also set an environment variable LOGLEVEL to your desired loglevel,
              e.g. ERROR, INFO or DEBUG''' % sys.argv[0]
    LOG_FNAME = os.path.join(
        os.path.expanduser('~'),
        "addtags.log"
    )
    logging.basicConfig(filename=LOG_FNAME, level=os.environ.get('LOGLEVEL') or logging.ERROR)
    ADD_GMAIL = '--add-gmail' in sys.argv
    main(add_gmail=ADD_GMAIL)
