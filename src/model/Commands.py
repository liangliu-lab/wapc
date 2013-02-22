__author__ = 'fatih'


class Commands(list):
    """
        Commands object class
    """
    command = None
    param = None

    def setCommand(self, command):
        """

        :param command:
        """
        self.command = command

    def getCommand(self):
        """

        :return:
        """
        return self.command

    def setParam(self, param):
        """

        :param param:
        """
        self.param = param

    def getCommand(self):
        """

        :return:
        """
        return self.param

