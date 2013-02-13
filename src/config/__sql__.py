__author__ = 'fatih'
class SQL():
    """
        This class includes all using database commands such as insert, remove, select etc.
        Only need to do is you will write your sql command and format it into running command by given values
    """

    #insert commands
    SQL_INSERT_CONFIG = "INSERT INTO apc_config(name, description, ip, radius_config_id, ssid, vlan_id, channel, channel_freq, date_added, date_modified) "\
                        "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}') RETURNING id;"
                        #(config_name, description, ip, radius_config_id, ssid, vlan_id, channel, channel_freq, date_added, date_modified)

    SQL_INSERT_DEVICE = "INSERT INTO apc_device(name, ip, config_id, username, password, date_added, date_modified) "\
                        "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}') RETURNING id;"
                        #(nick, ip, config_id, username, password, date_added, date_modified)

    SQL_INSERT_GROUP = "INSERT INTO apc_groups(name, config_id) VALUES('{0}','{1}') RETURNING id;" #insert group to the database

    SQL_INSERT_VLAN_CONFIG = "INSERT INTO apc_vlan(name, ip, subnet, number, interface) " \
                             "VALUES('{0}','{1}','{2}','{3}','{4}')" #insert vlan config values to the database

    #remove commands
    SQL_REMOVE_CONFIG = "DELETE FROM apc_config WHERE name = '{0}';"
    SQL_REMOVE_DEVICE = "DELETE FROM apc_device WHERE name = '{0}' AND id = {1};"
    SQL_REMOVE_GROUP = "DELETE FROM apc_groups WHERE name = '{0}' AND id = {1};"
    SQL_REMOVE_VLAN = "DELETE FROM apc_vlan WHERE name = '{0}' AND id = {1};"
    SQL_REMOVE_DEVICE_FROM_GROUP = "DELETE FROM apc_device_group WHERE device_id = {0} AND group_id = {1};"


    #select queries
    #select device records
    SQL_SELECT_DEVICE = "SELECT * FROM apc_device d WHERE d.name IS NOT NULL AND d.id = {0};"
    SQL_SELECT_DEVICE_CONFIG = "SELECT * FROM apc_device d LEFT JOIN apc_config c ON d.config_id = c.id WHERE d.id = {0};"
    SQL_SELECT_DEVICE_ALL = "SELECT * FROM apc_device AS d WHERE d.name IS NOT NULL ORDER BY DATE(date_added) ASC;"

    #select config records
    SQL_SELECT_CONFIG = "SELECT * FROM apc_config c WHERE c.name IS NOT NULL ORDER BY date_added ASC;"
    SQL_SELECT_CONFIG_DETAIL = "SELECT * FROM apc_config AS c WHERE c.name IS NOT NULL AND c.name IS '{0}';"

    SQL_SELECT_GROUP_DETAIL = "SELECT * FROM apc_groups g WHERE g.name IS NOT NULL AND g.id = {0};"
    SQL_SELECT_GROUP_ALL = "SELECT * FROM apc_groups d WHERE d.name IS NOT NULL ORDER BY date_added ASC;"
    SQL_SELECT_GROUP_DEVICE = "SELECT * FROM apc_device d LEFT JOIN apc_group g ON d.config_id = g.id WHERE d.id = {0};"

    SQL_SELECT_VLAN = "SELECT * FROM apc_vlan v WHERE v.id IS NOT NULL ORDER BY date_added ASC;"
    SQL_SELECT_VLAN_DETAIL = "SELECT * FROM apc_config AS c WHERE c.name IS NOT NULL AND c.name IS '{0}';"
