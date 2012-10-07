import re
import sys
import string
from functools import partial
from collections import defaultdict

eliminate_punctuation = partial(re.sub, '[{0}]'.format(string.punctuation), '')


def index_file(file_name):
    d = defaultdict(list)
    with open(file_name) as f:
        for lineno, line in enumerate(f, 1):
            # ignore empty lines
            if line.strip():
                for word in line.split():
                    plain_word = eliminate_punctuation(word.lower())
                    d[plain_word].append(lineno)
    return dict(d)


def main(argv=sys.argv):
    return index_file(argv[1])

if __name__ == '__main__':
    print main()
