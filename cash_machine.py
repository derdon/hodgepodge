#!/usr/bin/env python
import sys

from texttable import Texttable

def cash_machine(req_money, debug=False):
    possible_bills = [5, 10, 20, 50, 100, 200, 500]
    output = list()
    money_out = 0
    while money_out != req_money >= 5:
        for bill in reversed(possible_bills):
            num, rest = divmod(req_money, bill)
            if num:
                output.append((num, bill))
                possible_bills.pop()
                req_money = rest
                break
    if debug:
        if req_money in xrange(1, 5):
            sys.stderr.write(
                'ERROR:You requested an amount of %d but it is'
                ' not possible to give it out.\n' % req_money
            )
    return output

def table_output(output):
    table = Texttable()
    table.header(('Note', 'Number of Notes'))
    for row in output:
        table.add_row(row)
    return table.draw()

if __name__ == '__main__':
    try:
        req_money = int(sys.argv[1])
    except IndexError:
        req_money = int(raw_input('Enter the requested money: '))
    output = cash_machine(req_money, debug=True)
    print table_output(output)
