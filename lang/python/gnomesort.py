import sys


def gnomesort(l):
    n = len(l)
    if not n > 2:
        return l
    i = 0
    while True:
        current_item = l[i]
        try:
            next_item = l[i + 1]
        except IndexError:
            break
        if next_item < current_item:
            l[i], l[i + 1] = l[i + 1], l[i]
            if i == 0:
                i += 1
            else:
                i -= 1
        else:
            i += 1
    return l


def main(stdin=sys.stdin):
    elements = stdin.readline()
    l = list(map(lambda num: int(num.strip()), elements.strip().split(',')))
    return gnomesort(l)


if __name__ == '__main__':
    print(main())
