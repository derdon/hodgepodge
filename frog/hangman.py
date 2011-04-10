#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from string import letters
import sys
import os
import random
import codecs

from frog import Pool, Frog

# set this constant only for debugging reasons to True
# (or any value which converts to True)!
SHOW_SOLUTION = False

class Hangman(object):
    """ The logic stuff """
    def __init__(self):
        self.word = new_word()
        self.attempts = set()
        self.right_attempts = set()
        self.wrong_attempts = set()

    def guess(self, guessed_char):
        """ works not case-sensitive """
        # only accept an attempt if the pressed key is a letter
        if guessed_char in letters:
            self.attempts.add(guessed_char.lower())
            if guessed_char.lower() in self.word.lower():
                self.right_attempts.add(guessed_char)
            else:
                self.wrong_attempts.add(guessed_char)
            return ' '.join(
                char if char.lower() in self.attempts else '_' for char in self.word
            )
        else:
            raise ValueError('You can guess only letters!')

class HangmanWidget(object):
    """ The GUI stuff """
    def __init__(self, window):
        self.hangman = Hangman()
        self.window = window

        # create a new pen to write the dashes
        self.pen = Frog(self.window)
        self.pen.visible = False
        self.pen.write(' '.join('_' for char in self.hangman.word))

        if SHOW_SOLUTION:
            # show the solution
            solution = Frog(self.window)
            solution.visible = False
            solution.jumpto(0, 50)
            solution.write(' '.join(char for char in self.hangman.word))

        # prepare a pen for writing the gallow
        self.gallow_writer = Frog(self.window)
        self.gallow_writer.visible = False
        self.gallow_writer.jump(-150)

    def reset(self):
        """ clear the whole window and restart the game """
        # delete the 'frogs'
        self.pen.exit()
        self.gallow_writer.exit()
        self.__init__(self.window)

    def attempt(self, event):
        guessed_char = event['name']

        # lock the pen if it is just writing
        if self.gallow_writer.active:
            return

        self.gallow_writer.speed = 'max'

        # TODO: write a list of all guessed letters

        # right attempt
        if guessed_char.lower() in self.hangman.word:
            self.pen.write(self.hangman.guess(guessed_char))
            if len(self.hangman.right_attempts) == len(set(self.hangman.word)):
                self.gallow_writer.message(
                    'info',
                    'Congratulation! You guessed the word correctly!'
                )
                # start a new game
                self.reset()

        # wrong attempt
        else:
            # the number of mistakes
            num_mistakes = len(self.hangman.wrong_attempts)

            figures = [
                self.hill,
                self.first_beam,
                self.second_beam,
                self.bracket,
                self.rope,
                self.head,
                self.body,    
                self.first_leg,
                self.second_leg,
                self.first_arm,
                self.second_arm,
            ]

            # only draw a figure if the guessed
            # letter was not already guessed earlier
            if guessed_char not in self.hangman.attempts:
                figures[num_mistakes]()

            self.hangman.guess(guessed_char)

    def hill(self):
        self.gallow_writer.turnto(90)
        self.gallow_writer.circle(50, 180)

    def first_beam(self):
        self.gallow_writer.circle(50, -90, draw = False)
        self.gallow_writer.turnto(90)
        self.gallow_writer.move(100)

    def second_beam(self):
        self.gallow_writer.turnto(0)
        self.gallow_writer.move(100)

    def bracket(self):
        # move back and build the supporting beam (and yes, the strange
        # number 36 is necessary because the gallow must be hit exactly
        # on the right place)
        self.gallow_writer.jump(-75)
        self.gallow_writer.turnto(225)
        self.gallow_writer.move(36)

        # don't forget to to move to the place where the man will be hung
        self.gallow_writer.jump(-36)
        self.gallow_writer.turnto(0)
        self.gallow_writer.jump(75)

    def rope(self):
        self.gallow_writer.turnto(270)
        self.gallow_writer.move(25)

    def head(self):
        self.gallow_writer.turnto(0)
        self.gallow_writer.circle(-15)

    def body(self):
        self.gallow_writer.turnto(270)
        self.gallow_writer.jump(30)
        self.gallow_writer.move(50)

    def first_leg(self):
        self.gallow_writer.turnto(225)
        self.gallow_writer.move(25)

    def second_leg(self):
        self.gallow_writer.jump(-25)
        self.gallow_writer.turnto(315)
        self.gallow_writer.move(25)

    def first_arm(self):
        self.gallow_writer.jump(-25)
        self.gallow_writer.turnto(90)
        self.gallow_writer.jump(25)
        self.gallow_writer.turnto(135)
        self.gallow_writer.move(25)

    def second_arm(self):
        """ last figure -> user lost! """
        self.gallow_writer.jump(-25)
        self.gallow_writer.turnto(45)
        self.gallow_writer.move(25)
        self.gallow_writer.message(
            'Info',
            'You lost! Shame on you! The word was: ' + self.hangman.word
        )
        # start a new game
        self.reset()

def new_word():
    """ reurn a word randomly chosen from a dictionary """
    dic_file = os.path.join(os.sep, 'usr', 'share', 'dict', 'words')

    # use a randomized chosen word from the dictionary
    try:
        with codecs.open(dic_file, encoding = 'utf-8', errors = 'ignore') as f:
            random_word = random.choice(f.readlines())
    except IOError, error:
        random_word = ''
        sys.stderr.write(str(error))
    return random_word.strip()

def main():
    """ The main application """
    gallows_hill = Pool(width = 800, height = 600)
    widget = HangmanWidget(gallows_hill)

    # check if the generated word contains the
    # guessed letter if any key was pressed
    gallows_hill.listen('<Key>', widget.attempt)

    # you can quit the game by clicking Ctrl+q or [Esc]
    gallows_hill.listen('<Key-Escape>', lambda e: gallows_hill.quit())
    gallows_hill.listen('<Control-Key-q>', lambda e: gallows_hill.quit())

    # start the mainloop
    gallows_hill.ready()

if __name__ == '__main__':
    main()
