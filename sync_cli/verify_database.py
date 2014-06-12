#
# Copyright (c) 2013 Citrix Systems, Inc.
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

import sys

import arguments
import connect
import output

class Error(Exception):
    pass

def add_subparser(subparsers):
    description = """Verify the integrity of the database."""

    parser = subparsers.add_parser("verify-database",
                                   help="verify database",
                                   description=description)

    arguments.add_output_args(parser, suppress=True)

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    _verify_database(connection)

    if args.output == output.NORMAL:
        print "Database verification succeeded."

def _verify_database(connection):
    cursor = connection.cursor()

    cursor.callproc("sync_admin.verify_database",
                     keywordParameters={})
