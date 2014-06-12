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

import arguments
import connect

# TODO: Should this command remove the file as well?

def add_subparser(subparsers):
    description = """Remove a disk."""

    parser = subparsers.add_parser("remove-disk",
                                   help="remove disk",
                                   description=description)

    arguments.add_output_args(parser, suppress=True)

    parser.add_argument("disk",
                        metavar="DISK_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="disk uuid")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    cursor.callproc("sync_admin.remove_disk",
                    keywordParameters={
                        "disk_uuid": args.disk})
