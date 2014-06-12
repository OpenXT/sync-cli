#
# Copyright (c) 2012 Citrix Systems, Inc.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import ConfigParser
import os

_CONFIG_FILE_ENV_VAR = "SYNC_ADMIN_CONF"
_DEFAULT_CONFIG_FILE = "~/.sync-admin.conf"

def read_config():
    config = ConfigParser.RawConfigParser()
    config_file = os.environ.get(_CONFIG_FILE_ENV_VAR, _DEFAULT_CONFIG_FILE)
    config.read(os.path.expanduser(config_file))

    return config

def get_optional_value(config, section, option):
    try:
        return config.get(section, option)
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        return None
