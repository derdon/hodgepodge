# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


import sys
if sys.version_info <= (3,):
    from itertools import imap as map


def main(x):
    return sum(map(int, str(2 ** x)))


if __name__ == '__main__':
    try:
        x = int(sys.argv[1])
    except (IndexError, ValueError):
        x = 1000
    print(main(x))
