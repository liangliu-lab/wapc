#coding=utf-8
"""
    SQL object covers all sql scripts
"""

__author__ = 'fatih'


class SQL(object):
    """
        This class includes all using database commands such as insert, remove, select etc.
        Only need to do is you will write your sql command and format it into running command by given values
    """

    # =============================
    # select queries
    # =============================
    #select device records
    SQL_SELECT_DEVICE = "SELECT id AS ID, " \
                        "name, " \
                        "description, " \
                        "ip, " \
                        "username, " \
                        "password," \
                        "config_id AS config, " \
                        "date_added AS Added, " \
                        "date_modified AS Modified " \
                        "FROM apc_device d " \
                        "WHERE d.name IS NOT NULL AND d.id = %(id)d;"

    SQL_SELECT_DEVICE_CONFIG = "SELECT * " \
                               "FROM apc_device d " \
                               "LEFT JOIN apc_config c ON d.config_id = c.id " \
                               "WHERE d.id = {0};"

    SQL_SELECT_DEVICE_ALL = "SELECT id AS ID, " \
                            "name, " \
                            "description, " \
                            "ip, " \
                            "username, " \
                            "password, " \
                            "config_id AS Configuration, " \
                            "date_added AS Added, " \
                            "date_modified AS Modified " \
                            "FROM apc_device AS d " \
                            "WHERE d.name IS NOT NULL " \
                            "ORDER BY DATE(date_added) ASC;"

    SQL_SELECT_DEVICE_FROM_GROUP = "SELECT " \
                                   "ad.id , " \
                                   "ad.name, " \
                                   "ad. description, " \
                                   "ad.ip, " \
                                   "ad.username, " \
                                   "ad.password, " \
                                   "ad.config_id AS config," \
                                   "ad.date_added AS Added, " \
                                   "ad.date_modified AS Modified " \
                                   "FROM apc_device AS ad " \
                                   "LEFT JOIN apc_device_group AS adg ON ad.id = adg.device_id " \
                                   "RIGHT JOIN apc_groups AS ag ON ag.id = adg.group_id " \
                                   "WHERE ag.id = %(group_id)d;"

    # select config records
    SQL_SELECT_CONFIG = "SELECT * FROM apc_config c WHERE c.name IS NOT NULL ORDER BY date_added ASC;"
    SQL_SELECT_CONFIG_DETAIL = "SELECT * FROM apc_config AS c WHERE c.name IS NOT NULL AND c.id = %(id)d;"

    #select group queries
    SQL_SELECT_GROUP_DETAIL = "SELECT id AS ID, " \
                              "name, " \
                              "description, " \
                              "config_id AS config, " \
                              "date_added AS Added, " \
                              "date_modified AS Modified " \
                              "FROM apc_groups g " \
                              "WHERE g.name IS NOT NULL AND g.id = {0} " \
                              "ORDER BY date_added ASC;"

    SQL_SELECT_GROUP_ALL = "SELECT id AS ID, " \
                           "name, " \
                           "description, " \
                           "config_id AS Configuration, " \
                           "date_added AS Added, " \
                           "date_modified AS Modified " \
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
                              "ac.date_added," \
                              "ac.date_modified " \
                              "FROM apc_config AS ac " \
                              "LEFT JOIN apc_device AS ad ON ad.config_id = ac.id " \
                              "LEFT JOIN apc_device_group AS adg ON ad.id = adg.device_id " \
                              "RIGHT JOIN apc_groups AS ag ON ag.id = adg.group_id " \
                              "WHERE ag.id = %(group_id)d;"

    SQL_SELECT_GROUP_DEVICE = "SELECT * FROM apc_device d LEFT JOIN apc_group g ON d.config_id = g.id WHERE d.id = {0};"

    SQL_SELECT_VLAN = "SELECT * FROM apc_vlan v WHERE v.id IS NOT NULL ORDER BY date_added ASC;"
    SQL_SELECT_VLAN_DETAIL = "SELECT * FROM apc_config AS c WHERE c.name IS NOT NULL AND c.id = '%(id)d';"

    # =============================
    # insert queries
    # =============================
    #insert new config
    SQL_INSERT_CONFIG = "INSERT INTO " \
                        "apc_config(" \
                        "name, " \
                        "description, " \
                        "ip, " \
                        "radius, " \
                        "ssid, " \
                        "vlan, " \
                        "channel, " \
                        "frequency, " \
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
                        "'%(channel_freq)s', " \
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
                        "'%(date_modified)s', " \
                        ") RETURNING id;"

    # =============================
    #insert group to the database
    SQL_INSERT_DEVICE_TO_GROUP = "INSERT INTO apc_device_group(group_id, device_id, date_added, date_modified) " \
                                 "VALUES('%(group_id)d','%(device_id)d', '%(added)s', '%(modified)s') RETURNING id;"

    #insert device to the group then the database
    SQL_INSERT_GROUP = "INSERT INTO apc_groups(name, description, config_id, date_added, date_modified) " \
                       "VALUES('{0}','{1}', '{2}', '{3}', '{4}') RETURNING id;"

    # =============================
    #insert vlan config values to the database
    SQL_INSERT_VLAN_CONFIG = "INSERT INTO apc_vlan(name, ip, subnet, number, interface, date_added, date_modified) " \
                             "VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')"

    # =============================
    # update queries
    # =============================
    #update device group
    SQL_UPDATE_DEVICE_CONFIG = "UPDATE apc_config " \
                               "SET %(key)s = '%(value)s', date_modified='%(modified)s' " \
                               "WHERE id IN (" \
                               "SELECT ac.id FROM apc_config AS ac " \
                               "INNER JOIN apc_device AS ad ON ad.config_id = ac.id " \
                               "WHERE ad.id=%(id)d);"


    #update config
    SQL_UPDATE_CONFIG = "UPDATE apc_config " \
                        "SET %(key)s = '%(value)s', date_modified='%(modified)s'" \
                        "WHERE id=%(id)d"
    # =============================
    #update group
    SQL_UPDATE_GROUP = "UPDATE apc_groups " \
                       "SET name='%(name)s', description='%(description)s', " \
                       "config_id=%(config_id)d, date_modified='%(modified)s'" \
                       "WHERE id=%(id)d"
    # =============================
    #update device
    SQL_UPDATE_DEVICE = "UPDATE apc_device " \
                        "SET name='%(name)s', ip='%(ip)s',description='%(description)s', config_id=%(config_id)d, " \
                        "username='%(username)s', password='%(password)s', date_modified='%(modified)s'" \
                        "WHERE id=%(id)d"

    SQL_UPDATE_GROUP_CONFIG = "UPDATE apc_config SET %(key)s = '%(value)s' WHERE id IN " \
                              "(" \
                              "SELECT ac.id FROM apc_config AS ac " \
                              "INNER JOIN apc_device AS ad ON ad.config_id = ac.id " \
                              "INNER JOIN apc_device_group AS adg ON ad.id = adg.device_id " \
                              "INNER JOIN apc_groups AS ag ON ag.id = adg.group_id " \
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
    SQL_REMOVE_DEVICE_FROM_GROUP = "DELETE FROM apc_device_group WHERE device_id = %(device)d AND group_id = %(group)d;"