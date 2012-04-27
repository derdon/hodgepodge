# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.

from math import log10


def fib():
    i = 1
    a, b = 0, 1
    while True:
        a, b = b, a + b
        i += 1
        if log10(b) >= 999:
            return i

if __name__ == '__main__':
    print(fib())
