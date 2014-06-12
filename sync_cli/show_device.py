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
import output

def add_subparser(subparsers):
    description = """Show information about a device."""

    parser = subparsers.add_parser("show-device",
                                   help="show device",
                                   description=description)

    arguments.add_output_args(parser)

    parser.add_argument("device",
                        metavar="DEVICE_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="device uuid")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    device = cursor.callfunc("sync_admin.get_device",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "device_uuid": args.device})

    if args.output == output.QUIET:
        fields = ["device_uuid"]
    else:
        fields = None

    output.print_cursor(device, fields, args.output, single_row=True)
