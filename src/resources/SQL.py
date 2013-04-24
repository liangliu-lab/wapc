# coding=utf-8
"""
Copyright 2013 Labris Technology.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

__sql__ class aims to provide required SQL statements to requester metdhos

@package config
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""


class SQL(object):
    """
        This class includes all using database commands such as insert, remove,
        select etc.

        Only need to do is you will write your sql command and format it into
        running command by given values
    """

    # =============================
    # select queries
    # =============================
    #select device records
    SQL_SELECT_DEVICE = "SELECT ad.id, " \
                        "ad.name, " \
                        "ad.description, " \
                        "ad.ip, " \
                        "ad.username, " \
                        "ad.password," \
                        "ad.brand," \
                        "ad.model," \
                        "ad.firmware," \
                        "ad.relation," \
                        "ac.radius," \
                        "ac.ssid," \
                        "ac.vlan," \
                        "ac.channel," \
                        "ac.frequency," \
                        "ac.maxclients," \
                        "ac.id AS \"Configuration\", " \
                        "ad.date_added \"Add Date\", " \
                        "ad.date_modified AS \"Last Modified\" " \
                        "FROM apc_device AS ad " \
                        "INNER JOIN apc_config AS ac ON ad.config_id = ac.id " \
                        "WHERE ad.name IS NOT NULL AND ad.id = %(id)d" \
                        "ORDER BY DATE(ad.date_added);"

    SQL_SELECT_DEVICE_CONFIG = "SELECT * " \
                               "FROM apc_device d " \
                               "LEFT JOIN apc_config c ON d.config_id = c.id " \
                               "WHERE d.id = {0};"

    SQL_SELECT_BY_KEY = "SELECT %(key)s " \
                        "FROM %(table)s ad " \
                        "LEFT JOIN apc_config ac " \
                        "ON ad.config_id = ac.id " \
                        "WHERE ad.id = %(id)d;"

    SQL_SELECT_DEVICE_ALL = "SELECT ad.id, " \
                            "ad.name, " \
                            "ad.description, " \
                            "ad.ip, " \
                            "ad.username, " \
                            "ad.password," \
                            "ad.brand," \
                            "ad.model," \
                            "ad.firmware," \
                            "ad.relation," \
                            "ac.radius," \
                            "ac.ssid," \
                            "ac.vlan," \
                            "ac.channel," \
                            "ac.frequency," \
                            "ac.maxclients," \
                            "ad.date_added \"Add Date\", " \
                            "ad.date_modified AS \"Last Modified\" " \
                            "FROM apc_device AS ad " \
                            "INNER JOIN apc_config AS ac ON " \
                            "ad.config_id = ac.id " \
                            "WHERE ad.name IS NOT NULL " \
                            "ORDER BY DATE(ad.date_added);"

    SQL_SELECT_DEVICE_FROM_GROUP = "SELECT " \
                                   "ad.id , " \
                                   "ad.name, " \
                                   "ad. description, " \
                                   "ad.ip, " \
                                   "ad.username, " \
                                   "ad.password, " \
                                   "ad.brand," \
                                   "ad.model," \
                                   "ad.firmware," \
                                   "ad.relation," \
                                   "ad.config_id AS \"Configuration\"," \
                                   "ad.date_added \"Add Date\", " \
                                   "ad.date_modified AS \"Last Modified\" " \
                                   "FROM apc_device AS ad " \
                                   "LEFT JOIN apc_device_group AS adg ON " \
                                   "ad.id = adg.device_id " \
                                   "RIGHT JOIN apc_groups AS ag ON " \
                                   "ag.id = adg.group_id " \
                                   "WHERE ag.id = %(group_id)d;"

    # select config records
    SQL_SELECT_CONFIG = "SELECT ac.id AS \"ID\"," \
                        "ac.name AS \"Name\", " \
                        "ac.description," \
                        "ac.ip, " \
                        "ac.radius," \
                        "ac.ssid," \
                        "ac.vlan," \
                        "ac.channel," \
                        "ac.frequency," \
                        "ac.maxclients," \
                        "ac.username," \
                        "ac.password," \
                        "ac.enable_password," \
                        "ac.transport_protocol," \
                        "ac.personality," \
                        "ac.date_added AS \"Add Date\"," \
                        "ac.date_modified AS \"Last Modified\"" \
                        "FROM apc_config AS ac " \
                        "WHERE ac.name IS NOT NULL ORDER BY date_added ASC;"

    SQL_SELECT_CONFIG_DETAIL = "SELECT ac.id AS \"ID\"," \
                               "ac.name AS \"Name\", " \
                               "ac.description," \
                               "ac.ip, " \
                               "ac.radius," \
                               "ac.ssid," \
                               "ac.vlan," \
                               "ac.channel," \
                               "ac.frequency," \
                               "ac.maxclients," \
                               "ac.username," \
                               "ac.password," \
                               "ac.enable_password," \
                               "ac.transport_protocol," \
                               "ac.personality," \
                               "ac.date_added AS \"Add Date\"," \
                               "ac.date_modified AS \"Last Modified\"" \
                               "FROM apc_config AS ac " \
                               "WHERE ac.name IS NOT NULL AND ac.id = %(id)d;"

    #select group queries
    SQL_SELECT_GROUP_DETAIL = "SELECT id AS ID, " \
                              "name, " \
                              "description, " \
                              "config_id AS \"Configuration\", " \
                              "date_added AS \"Add Date\", " \
                              "date_modified AS \"Last Modified\"" \
                              "FROM apc_groups g " \
                              "WHERE g.name IS NOT NULL AND g.id = {0} " \
                              "ORDER BY date_added ASC;"

    SQL_SELECT_GROUP_ALL = "SELECT id AS ID, " \
                           "name, " \
                           "description, " \
                           "config_id AS \"Configuration\", " \
                           "date_added AS \"Add Date\", " \
                           "date_modified AS \"Last Modified\"" \
                           "FROM apc_groups d " \
                           "WHERE d.name IS NOT NULL " \
                           "ORDER BY date_added ASC;"

    SQL_SELECT_GROUP_CONFIG = "SELECT ac.id AS \"Config\"," \
                              "ad.id AS \"Device\"," \
                              "ad.name AS \"Device Name\"," \
                              "ac.name AS \"Config Name\", " \
                              "ac.description," \
                              "ac.ip, " \
                              "ac.radius," \
                              "ac.ssid," \
                              "ac.vlan," \
                              "ac.channel," \
                              "ac.frequency," \
                              "ac.maxclients," \
                              "ac.username," \
                              "ac.password," \
                              "ac.enable_password," \
                              "ac.transport_protocol," \
                              "ac.personality," \
                              "ac.date_added AS \"Add Date\"," \
                              "ac.date_modified AS \"Last Modified\"" \
                              "FROM apc_config AS ac " \
                              "LEFT JOIN apc_device AS ad ON " \
                              "ad.config_id = ac.id " \
                              "LEFT JOIN apc_device_group AS adg ON " \
                              "ad.id = adg.device_id " \
                              "RIGHT JOIN apc_groups AS ag ON " \
                              "ag.id = adg.group_id " \
                              "WHERE ag.id = %(group_id)d;"

    SQL_SELECT_GROUP_DEVICE = "SELECT * FROM apc_device d " \
                              "LEFT JOIN apc_group g ON " \
                              "d.config_id = g.id WHERE d.id = {0};"

    SQL_SELECT_VLAN = "SELECT * FROM apc_vlan v " \
                      "WHERE v.id IS NOT NULL " \
                      "ORDER BY date_added ASC;"
    SQL_SELECT_VLAN_DETAIL = "SELECT * FROM apc_config AS c " \
                             "WHERE c.name IS NOT NULL AND c.id = '%(id)d';"

    # =============================
    # insert queries
    # =============================
    #insert new config
    SQL_INSERT_CONFIG = "INSERT INTO " \
                        "apc_config(" \
                        "name, " \
                        "description, " \
                        "radius, " \
                        "ssid, " \
                        "vlan, " \
                        "channel, " \
                        "maxclients," \
                        "username," \
                        "password," \
                        "enable_password," \
                        "transport_protocol," \
                        "personality," \
                        "date_added, " \
                        "date_modified) " \
                        "VALUES(" \
                        "'%(name)s', " \
                        "'%(description)s', " \
                        "'%(ip)s', " \
                        "'%(radius_config_id)s', " \
                        "'%(ssid)s', " \
                        "'%(vlan_id)s', " \
                        "'%(channel)s', " \
                        "'%(maxclients)s', " \
                        "'%(username)s', " \
                        "'%(password)s', " \
                        "'%(enable_password)s', " \
                        "'%(transport_protocol)s', " \
                        "'%(personality)s', " \
                        "'%(date_added)s', " \
                        "'%(date_modified)s') RETURNING id;"

    # =============================
    #insert new device
    SQL_INSERT_DEVICE = "INSERT INTO " \
                        "apc_device(" \
                        "name, " \
                        "username," \
                        "password," \
                        "description, " \
                        "ip, " \
                        "config_id, " \
                        "brand, " \
                        "model, " \
                        "firmware, " \
                        "relation, " \
                        "date_added, " \
                        "date_modified) " \
                        "VALUES(" \
                        "'%(name)s', " \
                        "'%(username)s', " \
                        "'%(password)s', " \
                        "'%(desc)s', " \
                        "'%(ip)s', " \
                        "'%(config)d', " \
                        "'%(brand)s', " \
                        "'%(model)s', " \
                        "'%(firmware)s', " \
                        "'%(relation)s'," \
                        "'%(date_added)s', " \
                        "'%(date_modified)s'" \
                        ") RETURNING id;"

    # =============================
    #insert group to the database
    SQL_INSERT_DEVICE_TO_GROUP = "INSERT INTO " \
                                 "apc_device_group(" \
                                 "group_id, " \
                                 "device_id, " \
                                 "date_added, " \
                                 "date_modified) " \
                                 "VALUES(" \
                                 "'%(group_id)d'," \
                                 "'%(device_id)d', " \
                                 "'%(added)s', " \
                                 "'%(modified)s') " \
                                 "RETURNING id;"

    #insert device to the group then the database
    SQL_INSERT_GROUP = "INSERT INTO " \
                       "apc_groups(" \
                       "name, " \
                       "description, " \
                       "config_id, " \
                       "date_added, " \
                       "date_modified) " \
                       "VALUES(" \
                       "'{0}'," \
                       "'{1}', " \
                       "'{2}', " \
                       "'{3}', " \
                       "'{4}') " \
                       "RETURNING id;"

    # =============================
    #insert vlan config values to the database
    SQL_INSERT_VLAN_CONFIG = "INSERT INTO " \
                             "apc_vlan(" \
                             "name, " \
                             "ip, " \
                             "subnet, " \
                             "number, " \
                             "interface, " \
                             "date_added, " \
                             "date_modified) " \
                             "VALUES(" \
                             "'{0}'," \
                             "'{1}'," \
                             "'{2}'," \
                             "'{3}'," \
                             "'{4}'," \
                             "'{5}'," \
                             "'{6}')"

    # =============================
    # update queries
    # =============================
    #update device group
    SQL_UPDATE_DEVICE_CONFIG = "UPDATE apc_config " \
                               "SET %(key)s = '%(value)s', " \
                               "date_modified='%(modified)s' " \
                               "WHERE id IN (" \
                               "SELECT ac.id FROM apc_config AS ac " \
                               "INNER JOIN apc_device AS ad ON " \
                               "ad.config_id = ac.id " \
                               "WHERE ad.id=%(id)d);"

    #update config
    SQL_UPDATE_CONFIG = "UPDATE apc_config " \
                        "SET %(key)s = '%(value)s', " \
                        "date_modified='%(modified)s'" \
                        "WHERE id=%(id)d"
    # =============================
    #update group
    SQL_UPDATE_GROUP = "UPDATE apc_groups " \
                       "SET %(key)s='%(value)s', " \
                       "date_modified='%(modified)s'" \
                       "WHERE id=%(id)d"
    # =============================
    #update device
    SQL_UPDATE_DEVICE = "UPDATE apc_device " \
                        "SET %(key)s='%(value)s', " \
                        "date_modified='%(modified)s'" \
                        "WHERE id=%(id)d"

    SQL_UPDATE_GROUP_CONFIG = "UPDATE apc_config SET %(key)s = '%(value)s' " \
                              "WHERE id IN " \
                              "(" \
                              "SELECT ac.id FROM apc_config AS ac " \
                              "INNER JOIN apc_device AS ad ON " \
                              "ad.config_id = ac.id " \
                              "INNER JOIN apc_device_group AS adg ON " \
                              "ad.id = adg.device_id " \
                              "INNER JOIN apc_groups AS ag ON " \
                              "ag.id = adg.group_id " \
                              "WHERE ag.id = %(group_id)d" \
                              ");"

    #update vlan

    # =============================
    # remove queries
    # =============================
    #remove commands
    SQL_REMOVE_CONFIG = "DELETE FROM apc_config WHERE id = %(id)d;"
    SQL_REMOVE_DEVICE = "DELETE FROM apc_device WHERE id = %(id)d;"
    SQL_REMOVE_GROUP = "DELETE FROM apc_groups WHERE id = %(id)d;"
    SQL_REMOVE_VLAN = "DELETE FROM apc_vlan WHERE id = %(id)d;"
    SQL_REMOVE_DEVICE_FROM_GROUP = "DELETE FROM apc_device_group " \
                                   "WHERE device_id = %(device)d " \
                                   "AND group_id = %(group)d;"