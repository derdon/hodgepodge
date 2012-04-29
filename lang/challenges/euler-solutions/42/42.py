# (c) Simon Liedtke <liedtke.simon@googlemail.com> under the ISC license.
# See COPYING for more details.


from itertools import imap, izip, count, tee
import string
import sys


# copied from http://docs.python.org/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def f(x):
    return 0.5 * x * (x + 1)


def letter2number(letter):
    normalized_letter = letter.lower()
    return string.ascii_lowercase.find(normalized_letter) + 1


def word2number(word):
    return sum(imap(letter2number, word))


def word_is_triangle_word(word):
    num = word2number(word)
    for current_number, next_number in pairwise(count(1)):
        if f(current_number) == num:
            return True
        elif f(current_number) < num < f(next_number):
            return False


def parse_file(f):
    first_line = f.readline()
    assert f.read() == ''
    return (word.replace('"', '') for word in first_line.split(','))


def get_triangle_words(f):
    words = parse_file(f)
    return filter(word_is_triangle_word, words)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'words.txt'
    with open(filename) as f:
        triangle_words = get_triangle_words(f)
    return len(triangle_words)

if __name__ == '__main__':
    print main()
