__author__ = 'fatih'


class Commands(list):
    """
        Commands object class
    """
    command = None
    param = None

    def setCommand(self, command):
        self.command = command

    def getCommand(self):
        return self.command

    def setParam(self, param):
        self.param = param

    def getCommand(self):
        return self.param

