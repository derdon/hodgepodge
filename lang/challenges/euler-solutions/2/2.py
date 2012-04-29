# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


def main():
    i = 0
    a, b = 0, 1
    while True:
        a, b = b, a + b
        if a % 2 == 0:
            i += a
        elif a > 4e6:
            break
    return i

if __name__ == '__main__':
    print(main())
