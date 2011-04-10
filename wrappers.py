#!/usr/bin/env python

from time import ctime
from itertools import izip

def log_function(func):
    def decorate(foo):
        print 'function %s called at %s' % (func.__name__, ctime())
        return func(foo)
    return decorate

def parameter_types(*types):
    def decorate(f):
        def check_parameters(*args):
            for type, arg in izip(types, args):
                if not isinstance(arg, type):
                    raise TypeError('%s must be of type %s' % (arg, type))
                    return None
            return f(*args)
        return check_parameters
    return decorate

@log_function
def main(foo):
    return 'I am main() and was called with the parameter %s' % foo

@parameter_types(int, str, float)
def foo(age, name, weight):
    return 'age: %s; name: %s; weight: %s' % (age, name, weight)

if __name__ == '__main__':
    #print main('spam')
    #print foo(42, 'Max', 98.4)
    print foo(42, 'Max', 98)
