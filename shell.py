import time
from src.cli.ConsoleInterface import ConsoleInterface

__author__ = 'fatih'


def __main__():
    try:
        print "Welcome to Labris Wireless Access Point Controller"
        time.sleep(1)
        print "Command Line Tool initializing..."
        time.sleep(3)
        ConsoleInterface().cmdloop()
    except Exception as e:
        print e.message
        pass

if __name__ == "__main__":
    __main__()