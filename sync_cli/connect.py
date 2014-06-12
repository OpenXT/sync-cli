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

import cx_Oracle

import configuration

class Error(Exception):
    pass

def connect(args, config, required=True):
    login = _get_database_login(args, config, required)

    if login is not None:
        try:
            return cx_Oracle.connect(login)
        except cx_Oracle.InterfaceError as error:
            raise Error("Failed to connect to database: {0}.\n"
                        "Check that ORACLE_HOME is set "
                        "correctly.".format(error))
    else:
        return None

def _get_database_login(args, config, required):
    if args.database is not None:
        login = args.database
    else:
        login = configuration.get_optional_value(config, "database", "login")

    if login is None and required:
        raise Error("Database login must be specified either with the -d "
                    "argument or in the configuration file.")

    return login
