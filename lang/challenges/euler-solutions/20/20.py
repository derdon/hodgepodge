# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


import sys
if sys.version_info <= (3,):
    from itertools import imap as map
import math


def main():
    return sum(map(int, str(math.factorial(100))))


if __name__ == '__main__':
    print(main())
