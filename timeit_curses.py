#!/usr/bin/env python

import curses
from datetime import datetime

def main(func):
    # initializing curses
    stdscr = curses.initscr()

    # make the cursor invisible
    curses.curs_set(0)

    stdscr.addstr(0, 0, "Start time: ")
    stdscr.addstr(1, 0, "End time: ")
    stdscr.addstr(3, 0, "Difference: ")

    # a counter to track the number of pressing <SPACE>
    space_pressed = 0

    while True:
        # wait for a keypress
        c = stdscr.getch()

        # if <SPACE> is pressed...
        if c == ord(" "):
            space_pressed += 1

            # print the start time
            if space_pressed == 1:
                start_time = datetime.now()
                stdscr.addstr(0, 12, start_time.strftime("%H:%M:%S"))

            # show end time and difference
            elif space_pressed == 2:
                end_time = datetime.now()
                stdscr.addstr(1, 10, end_time.strftime("%H:%M:%S"))

                difference = end_time - start_time
                minutes, seconds = divmod(difference.seconds, 60)
                hours, minutes = divmod(minutes, 60)

                # format the output
                seconds = "%02d" % seconds if seconds < 10 else seconds
                minutes = "%02d" % minutes if minutes < 10 else minutes
                hours = "%02d" % hours if hours < 10 else hours

                stdscr.addstr(3, 12, "%s:%s:%s" % (hours, minutes, seconds))

            # delete the calculated data and start again
            elif space_pressed == 3:
                # delete start time
                for col in xrange(12, 25):
                    stdscr.delch(0, 12)

                # delete end time
                for col in xrange(10, 25):
                    stdscr.delch(1, 10)

                # delete difference time
                for col in xrange(12, 25):
                    stdscr.delch(3, 12)

                # reset the counter and restart
                space_pressed = 0

        # quit the app if `q` is pressed
        elif c == ord("q"):
            return

if __name__ == "__main__":
    curses.wrapper(main)
