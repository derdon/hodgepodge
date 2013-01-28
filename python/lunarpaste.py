#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import io
import sys
import getpass

import requests
import argparse

URL = 'http://devnull.lunar-linux.org/p/'
DEFAULT_LANG = 'text'
DEFAULT_EXPIRY = 'm'


def paste(text, name, lang=DEFAULT_LANG, expiry=DEFAULT_EXPIRY):
    d = {
        'parent_pid': '',
        'format': lang,
        'code2': text,
        'challenge': str(int('101010', base=2)),
        'paste': 'Send',
        'poster': name,
        'remember': '',
        'expiry': expiry}
    r = requests.post(URL, data=d)
    return r.url


def parse_args(argv):
    descr = 'Upload the content of a file to the paste service of Lunar Linux'
    parser = argparse.ArgumentParser(description=descr, prog='p')
    add_arg = parser.add_argument
    add_arg('file', help='path to the file that will be uploaded')
    add_arg(
        '-l', '--language', default=DEFAULT_LANG,
        help=(
            'the programming language used in the paste'
            '(for syntax highlighting)'))
    add_arg('-n', '--name', help='your name', default=getpass.getuser())
    add_arg(
        '-e', '--expiry', choices='dmf', default=DEFAULT_EXPIRY,
        help=(
            'How long should your post be retained? '
            'Select d for one day, m for one month or f for forever'))
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    with io.open(args.file, encoding='utf8') as f:
        text = f.read()
    url = paste(text, args.name, args.language, args.expiry)
    return 'The file {} was successfully pasted at {}.'.format(args.file, url)

if __name__ == '__main__':
    print(main())
