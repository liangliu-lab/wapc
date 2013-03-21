__author__ = 'fatih'


class Commands(list):
    """
        Commands object class
    """
    command = None
    param = None

    def set_command(self, command):
        """

        :param command:
        """
        self.command = command

    def get_command(self):
        """

        :return:
        """
        return self.command

    def set_param(self, param):
        """

        :param param:
        """
        self.param = param

    def get_param(self):
        """

        :return:
        """
        return self.param