#!/usr/bin/python3
# encoding: utf-8

import timeit
from time import sleep

def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        print('%s 耗时 [%0.8fs]' % (name, elapsed))
        return result
    return clocked
