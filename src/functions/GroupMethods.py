# coding=utf-8
from Queue import Empty
from time import strftime, gmtime
from src.config.__sql__ import SQL
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language
from src.model.Group import Group
from src.resources.resources import Resources

__author__ = 'fatih'


class GroupMethods(object):
    """
        GroupMethods
    """

    def __init__(self):
        self.utils = Utils()
        self.now = strftime(Resources.time_format, gmtime())
        self.db = Database()

    def create(self, params):
        """
            add new group with params
        :rtype : object
        :param params:
        """
        group = Group()
        try:
            #check namespace variables if set
            if params.name:
                group.setName(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('group')

            if params.description:
                group.setDescription(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('group')

            if params.config:
                group.setConfig(params.config)
            else:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')

            cmd = SQL.SQL_INSERT_GROUP.format(
                group.getName(),
                group.getDescription(),
                group.getConfig(),
                self.now,
                self.now
            )
            id = self.db.insert(cmd)
            if id is Empty:
                print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'inserting new group', id)
            else:
                print Language.MSG_ADD_NEW.format('group', id[0], group.getName())
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def read(self, id):
        """

        :param id:
        """
        cmd = None
        flag = False

        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_GROUP_DETAIL.format(id)
            fields, results = self.db.select(cmd)
            if fields and results:
                try:
                    rset = {"fields": fields, "results": [list(f) for f in results][0]}
                    return rset
                except Exception as e:
                    print e.message
                    pass
            else:
                raise Exception(
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no group record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def update(self, params):
        """
        :param params:
        """
        group = Group()
        try:
            if params.id:
                did = params.id.rstrip().lstrip()
                rset = self.read(did)
                data = dict(map(list, zip(rset['fields'], rset['results'])))

                if params.name:
                    group.setName(params.name.rstrip().lstrip())
                else:
                    group.setName(data["name"])
                if params.description:
                    group.setDescription(params.description.rstrip().lstrip())
                else:
                    group.setDescription(data["description"])
                if params.config:
                    group.setConfig(params.config.rstrip().lstrip())
                else:
                    group.setConfig(data["config"])

                group.setModified(self.now)

                cmd = SQL.SQL_UPDATE_GROUP % \
                      {
                          "name": group.getName(),
                          "description": group.getDescription(),
                          "config_id": int(group.getConfig()),
                          "modified": self.now,
                          "id": int(did)
                      }

                if self.db.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format('group', params.id, group.getName())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                print Language.MSG_ERR_EMPTY_ID
        except Exception as e:
            print e.message


def delete(self, params):
    """

        :param params:
        """