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

import arguments
import connect
import get_file
import output

def add_subparser(subparsers):
    description = """Show the encryption key for a disk."""

    parser = subparsers.add_parser("show-disk-key",
                                   help="show encryption key for disk",
                                   description=description)

    arguments.add_output_args(parser, field="encryption_key")

    parser.add_argument("disk",
                        metavar="DISK_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="disk uuid")

    parser.add_argument("-f", "--file",
                        metavar="KEY_FILE",
                        action=arguments.StoreSingleValue,
                        help="write raw disk encryption key to file")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    encryption_key = cursor.callfunc("sync_admin.get_disk_key",
                                    cx_Oracle.STRING,
                                    keywordParameters={
                                        "disk_uuid": args.disk})

    if args.file is not None:
        get_file.write_encryption_key_to_file(encryption_key, args.file)
    else:
        output.print_value(encryption_key, "encryption_key", args.output)
