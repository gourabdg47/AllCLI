import sys
import os
import time
from copy import deepcopy

from rich import print
from rich.panel import Panel

try:
    import curses
except ImportError:
    if sys.platform.startswith('win'):
        try:
            os.system('pip install windows-curses')
            import curses
        except Exception as e:
            print("Failed to install windows-curses:", e)
            sys.exit(1)

def engine(stdscr):
    print("----->")


def engine_start():
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(engine)