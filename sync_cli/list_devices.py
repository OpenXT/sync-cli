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

import cx_Oracle

import arguments
import connect
import output

def add_subparser(subparsers):
    description = """List devices."""

    parser = subparsers.add_parser("list-devices",
                                   help="list devices",
                                   description=description)

    arguments.add_output_args(parser, field="device_uuid")
    _add_filter_args(parser)

    parser.set_defaults(func=_run)

def _add_filter_args(parser):
    # TODO: This works an around argparse bug which breaks mutual exclusivity.
    #filter_group = parser.add_argument_group("filter arguments")
    #group = filter_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-n", "--name",
                       metavar="DEVICE_NAME",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by device name")

    group.add_argument("-r", "--repo",
                       metavar="REPO_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list devices associated with repository")

    group.add_argument("--no-repo",
                       action="store_true",
                       help="list devices not associated with any repository")

    group.add_argument("-v", "--vm",
                       metavar="VM_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list devices with instances of VM")

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    devices = cursor.callfunc("sync_admin.list_devices",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "device_name": args.name,
                                 "repo_uuid": args.repo,
                                 "no_repo": args.no_repo,
                                 "vm_uuid": args.vm})

    if args.output == output.QUIET:
        fields = ["device_uuid"]
    else:
        fields = None

    output.print_cursor(devices, fields, args.output)
