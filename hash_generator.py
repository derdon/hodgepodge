#!/usr/bin/env python

import sys
import random
from string import letters, digits
from os import linesep

def generate_hash(length=8, include=letters + digits, exclude="1Il0O"):
    chars = list(set(include) ^ set(exclude))
    return "".join(random.sample(chars, length))

def main(num):
    """ return passwords with a number of num.
    useful for writing in files
    `python pw_generator.py 100 > 100_passwords` writes 100 generated passwords
    into the file 100_passwords (only possible on POSIX compatible systems)
    >>> print pw_generator.main(2)
    Kjeh0kA7UbFs
    cWwitUDzs7Jf
    """
    return linesep.join(generate_hash() for password in xrange(num))

if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
    except IndexError:
        num = 1
    print main(num)
