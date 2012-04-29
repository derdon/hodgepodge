# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.

import sys
if sys.version_info <= (3,):
    from itertools import imap as map
import string


def letter2number(letter):
    normalized_letter = letter.lower()
    return string.ascii_lowercase.find(normalized_letter) + 1


def score_name(name, pos):
    return sum(map(letter2number, name)) * pos


def parse_file(f):
    first_line = f.readline()
    assert f.read() == ''
    return sorted(word.replace('"', '') for word in first_line.split(','))


def score_all_names(f):
    names = parse_file(f)
    return sum(score_name(name, pos + 1) for pos, name in enumerate(names))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'names.txt'
    with open(filename) as f:
        total_scoring = score_all_names(f)
    return total_scoring

if __name__ == '__main__':
    print(main())
