#!/usr/bin/env python

import sys
import random

def ai_guesser(number, min_num, max_num):
    """number must be higher than the highest value from the set
    "too small" and lower than the smallest value from the set "too high"

    """
    too_high = set([max_num])
    too_small = set([min_num])
    attempt = (min_num + max_num) / 2
    yield attempt
    while attempt != number:
        if attempt < number:
            too_small.add(attempt)
        elif attempt > number:
            too_high.add(attempt)
        attempt = round((max(too_small) + min(too_high)) / 2)
        yield attempt

def ai_main(min_num=1, max_num=100):
    num = random.randint(min_num, max_num)
    for num_of_attempts, attempt in enumerate(ai_guesser(num, min_num, max_num)):
        print 'Guess a number: %d' % attempt
    print 'Number of attempts: %d' % (num_of_attempts + 1)

def main(min_num=1, max_num=100):
    attempt = None
    attempts = 0
    num = random.randint(min_num, max_num)
    while attempt != num:
        while True:
            try:
                attempt = float(raw_input('Guess a number: '))
            except ValueError:
                pass
            except KeyboardInterrupt:
                sys.exit(1)
            else:
                if attempt:
                    break
        if attempt < num:
            print 'Too small'
        elif attempt > num:
            print 'Too big!'
        attempts += 1
    print 'Congratulation! You guessed the number!'
    print 'Number of attempts: %d' % attempts

if __name__ == '__main__':
    #main()
    ai_main()
