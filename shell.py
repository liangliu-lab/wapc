# coding=utf-8

"""
@mainpage Labris Wirelss Access Point Controller v1.1.0

<h1>DESCRIPTION</h1>

This software has been created to manage wireless acess point controllers with
no brand dependency.

Version 1.0 includes only CLI(Command Line Interface) to manage devices via
Linux-familiar commands such as rm, ls, etc..

Please see commands and options list below.

<h1>FEATURES</h1>
<ul>
<li>Add new devices into the inventory</li>
<li>Create groups with given devices</li>
<li>Manage device configurations, add, update and delete</li>
<li>Manage device SSID, Channel, Associations, Maxclients</li>
<li>Roaming</li>
<li>Group management</li>
<li>Service oriented architecture to communicate devices over Telnet</li>
<li>Configure device commands over wapc-config.json</li>
<</ul>

<h1>COMMAND & OPTIONS</h1>
Use methods below to add, remove, update and list device(s), group(s) or
config(s) with commands:

<h2>Commands:</h2>
<h3>Usage: $ add [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-I],[--ip] Use this params when adding some new variables which needs
an ip such as device, config, etc.</li>
<li>[-n],[--name] To set a name to related type variable</li>
<li>[-b],[--brand] To set device brand to relate with its model and/or 
firmware</li>
<li>[-m],[--model] To set device model to relate with its config file</li>
<li>[-F],[--firmware] To set device firmware to relate with its config file</li>
<li>[-R],[--relation] To set device relation one of MASTER of SLAVE</li>
<li>[-D],[--description] To set a description to related type variable</li>
<li>[-u],[--username] Provide a username which will be used to connect
device</li>
<li>[-p],[--password] Provide a password which will be used to connect and
configure device</li>
</ul>
<h3>Usage: $ edit [OPTIONS]</h3>
Edit details of given type of device with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-o],[--option] Provide option must be one of related type database 
fields</li>
<li>[-P],[--param] Provide parameter to be update value</li>
</ul>
<h3>Usage: $ group [OPTIONS]</h3>
Group given devices
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-g],[--group] Define the group where given device will be added into</li>
<li>[-i],[--id] Define id of device, group, vlan, config</li>
</ul>
<h3>Usage: $ set [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of "ssid, vlan, channel,
frequency, maxclients, ip, cpu, memory, permanent, conf, firmware, model,
serial, clients"</li>
</ul>
These will be used to gather related commands from config file you provided
<h3>Usage: $ unset [OPTIONS]</h3>
Unset option, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of</li>
</ul>
"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf,
firmware, model, serial, clients"
These will be used to gather related commands from config file you provided
<h3>Usage: $ ls [OPTIONS]</h3>
List details of given type
<ul>
<li>[-t],[--type] List device, group, vlan, config</li>
<li>[-g],[--group] List device, vlan or config from given group</li>
<li>[-i],[--id] Define id of group</li>
</ul>
<h3>Usage: $ sh [OPTIONS]</h3>
Show details of given type
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of</li>
</ul>
"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf,
<h3>Usage: $ rm [OPTIONS]</h3>
Show details of given type
<ul>
<li>[-t],[--type] Define type device, group, vlan, config and also it can be
used such asgiven type is from to remove a device from a group</li>
<li>[-g],[--group] Define the group where given device will be remove from</li>
<li>[-i],[--id] Define id of device, group, vlan, config</li>
</ul>
<h3>Usage: $ self [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-I],[--ip] Use this params when adding some new variables which needs an
ip such as device, config, etc.</li>
<li>[-n],[--name] To set a name to related type variable</li>
<li>[-D],[--description] To set a description to related type variable</li>
<li>[-u],[--username] Provide a username which will be used to connect
device</li>
</ul>

<h2>Options:</h2>
<ul>
<li>-i,--id Provide ID address to determine the variable with
usage id</li>
<li>-I,--ip Provide IP address for the newly added device with
usage to connect</li>
<li>-n,--name Provide name for the newly added device with usage name</li>
<li>-u,--username Provide username for the newly added device with
usage username</li>
<li>-p,--password Provide password for given username of the newly
added device with usage password</li>
<li>-P,--param Provide a parameter to be set to the given option</li>
<li>-g,--group Add device to the group with usage group</li>
<li>-c,--config Add new configuration and map it to the given group or 
device</li>
<li>-s,--subnet Define subnet for VLAN will be configured with usage 
255.255.255.0</li>
<li>-d,--device Provide device id to add provided device to the group</li>
<li>-D,--description Provide a short description for group or device
with usage</li>
<li>-r,--radius Provide Radius id to configure radius authentication for 
group or device with usage radius_id</li>
<li>-S,--ssid Provide SSID for group or device with usage ssid</li>
<li>-V,--vlan Provide VLAN id to determine VLAN for group or device with 
usage vlan_id</li>
<li>-H,--channel Provide channel to configure for group or device with 
usage channel</li>
<li>-t,--type Provide type of group/device/config/vlan from database with 
usage group/device/config/vlan others will cause error(s)</li>
<li>-o,--option Provide type of group/device/config/vlan from database with 
usage group/device/config/vlan</li>
</ul>

<h1>REQUIREMENTS</h1>
<h4>Databases</h4>
<ul>
<li>PostgreSQL 9.x</li>
<li>CouchDB 1.2.x <br />
Please see details http://pythonhosted.org/CouchDB/getting-started.html</li>
</ul>
<h4>Libraries</h4>
<h5>For Perl script</h5>
<ul>
<li>Readonly</li>
<li>Try::Tiny</li>
<li>Net::Telnet</li>
<li>Net::Appliance::Session</li>
<li>JSON</li>
<li>Data::Dumper</li>
</ul>
<h5>For WAPC</h5>
<ul>
<li>ArgParse 1.x</li>
<li>json</li>
</li>

<h1>LICENSE</h1>
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

@package controller
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

<h1>CHANGELOG</h1>
<h5>v1.1.0</h5>
<ul>
<li>Requirements been added to main documentation.</li>
<li>Set commands bug fixed.</li>
<li>Group methods been made to work properly.</li>
<li>ORM structured database methods have been implemented.</li>
<li>CouchDB driver has been implemented.</li>
<li>Refactored regarding Pylint needs.</li>
</ul>

<h5>v1.0.0</h5>
<ul>
<li>SRS base requirements have been implemented.</li>
<li>Documentation has been generated.</li>
</ul>
"""
from src.cli.ConsoleInterface import ConsoleInterface
from src.language.Language import Language

__author__ = 'fatih'


def __main__():
    try:
        print Language.MSG_APP_WELCOME
        print Language.MSG_APP_CMD_INIT
        ConsoleInterface().cmdloop_with_keyboard_interrupt()
    except BaseException as exception:
        print exception.message
    finally:
        ConsoleInterface().cmdloop_with_keyboard_interrupt()


if __name__ == "__main__":
    __main__()