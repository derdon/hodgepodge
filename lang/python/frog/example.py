#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial

from frog import Pool, Frog

def move(event, frog, max_width, max_height, step=100, turnonly=False, draw=False):
    degrees = {
        'Up': 90,
        'Right': 0,
        'Down': 270,
        'Left': 180
    }
    frog.turnto(degrees.get(event['name']))
    if not turnonly:
        # FIXME: check the frog's position and move
        # only if the frog is in the allowed area
        x_pos, y_pos = tuple(abs(round(num)) for num in frog.pos)

        print '(x_pos + step, y_pos + step) = %r, (max_width / 2, max_height / 2) = %r' % (
            (x_pos + step, y_pos + step), (max_width / 2, max_height / 2)
        )

        #if x_pos + step <= (max_width / 2) and y_pos + step <= (max_height / 2):
        frog.move(step) if draw else frog.jump(step)

def remote_control(window, frog):
    """ control the frog via some buttons. """
    pass

def main(window):
    # shortcuts for callbacks
    jump_callback = lambda event: move(event, frog, window.width, window.height)
    move_callback = lambda event: move(event, frog, window.width, window.height, draw=True)
    turn_callback = lambda event: move(event, frog, window.width, window.height, turnonly=True)

    # create a new frog
    frog = Frog(window)
    frog.shape = 'frog'
    frog.bodycolor = 'green'

    # let the frog jump and turn it, if necessary
    window.listen('<Key-Up>', jump_callback)
    window.listen('<Key-Down>', jump_callback)
    window.listen('<Key-Left>', jump_callback)
    window.listen('<Key-Right>', jump_callback)

    # move the frog and turn it, if necessary
    window.listen('<Shift-Key-Up>', move_callback)
    window.listen('<Shift-Key-Down>', move_callback)
    window.listen('<Shift-Key-Left>', move_callback)
    window.listen('<Shift-Key-Right>', move_callback)

    # turn the frog without moving it
    window.listen('<Control-Key-Up>', turn_callback)
    window.listen('<Control-Key-Down>', turn_callback)
    window.listen('<Control-Key-Left>', turn_callback)
    window.listen('<Control-Key-Right>', turn_callback)

    # "write" a dot with space
    window.listen('<space>', lambda event: frog.dot())

    # you can quit the game by clicking `q` or [Esc]
    window.listen('<Key-Escape>', lambda e: window.quit())
    window.listen('<Key-q>', lambda e: window.quit())


if __name__ == '__main__':
    # create a new field (the main window)
    window = Pool(width=800, height=600)

    main(window)
    #remote_control(window)

    # start the mainloop
    window.ready()
