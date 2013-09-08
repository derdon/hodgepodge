#!/usr/bin/env python
import sys
import subprocess
from StringIO import StringIO

import tex2pix


def main():
    pngfile = sys.argv[1]
    tex2pix.Renderer(StringIO(sys.stdin.read())).mkpng(pngfile)
    return subprocess.call(['mogrify', '-trim', pngfile])


if __name__ == '__main__':
    sys.exit(main())
