from pprint import pformat

from OPTIONS import DEBUG_MODE

GRAY = '\33[90m'
BLUE = '\33[94m'
GREEN = '\33[92m'
YELLOW = '\33[93m'
RED = '\33[31m'

DEBUG_PRINTS = False


def printdebug(*text):
    if DEBUG_MODE:
        printColor(printFormat(*text), GRAY)


def print_verbose(*msg):
    from OPTIONS import VERBOSE_MODE
    if not VERBOSE_MODE:
        return
    printMessage(*msg)


def setDebugPrints(option):
    global DEBUG_PRINTS
    DEBUG_PRINTS = option


def printColor(text, color, e='\n'):
    print(color + text + '\33[0m', end=e)


def printFormat(*text):
    if len(text) == 1 and type(*text) is dict:
        r = pformat(*text)
        return r
    else:
        r = ''
        for i in text:
            r += str(i) + ' '

        return r.replace('\'', '')  # remove quotes


def printinfo(*text):
    printColor(printFormat(*text), BLUE)


def printProgress(*text, end='\n'):
    printColor(printFormat(*text), GREEN, end)


def printMessage(*text, end='\n'):
    printColor(printFormat(*text), YELLOW, end)
