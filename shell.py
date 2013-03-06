# coding=utf-8
"""
    Commandline interface to handle user interaction commands between WAP
"""
from src.cli.ConsoleInterface import ConsoleInterface
from src.language.language import Language

__author__ = 'fatih'


def __main__():
    try:
        print Language.MSG_APP_WELCOME
        print Language.MSG_APP_CMD_INIT
        ConsoleInterface().cmdloop()
    except Exception as e:
        print e.message
        pass
    finally:
        pass


if __name__ == "__main__":
    __main__()