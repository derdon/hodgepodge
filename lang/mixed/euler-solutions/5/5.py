# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


import sys
try:
    reduce = reduce
except NameError:
    from functools import reduce
from fractions import gcd


def lcm(a, b):
    return int(a * b / gcd(a, b))


def main():
    return reduce(lcm, range(2, 21))


if __name__ == '__main__':
    print(main())
