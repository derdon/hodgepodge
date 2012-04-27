# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


import sys


def sum_of_squares(n):
    return n * (n + 1) * (2 * n + 1) / 6


def square_of_sums(n):
    return (x * (x + 1) / 2) ** 2


def main(x):
    return square_of_sums(x) - sum_of_squares(x)


if __name__ == '__main__':
    try:
        x = int(sys.argv[1])
    except (IndexError, ValueError):
        x = 100
    print(main(x))
