"""An info module

This is a module which gives you some info

Here is an example::

  print(info.info())
"""
import os, sys
import time

def info():
    """Produce some useful info

    Time: what time it is
    Executable: where Python is
    """
    print("Time:", time.asctime())
    print("Executable:", sys.executable)

def a(): pass

def b(): pass

def c(): pass
