#!/usr/bin/python3
# encoding: utf-8

import timeit
from time import sleep
from ChineseChess.loggerPrint import LoggerPrint
from ChineseChess.settings import Settings

logg = LoggerPrint(Settings()).printLogToSystem()

def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        logg.info('%s 耗时 [%0.8fs]' % (name, elapsed))
        return result
    return clocked
