# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


def main():
    return sum(num for num in range(1000) if any(not num % x for x in [3, 5]))


if __name__ == '__main__':
    print(main())
