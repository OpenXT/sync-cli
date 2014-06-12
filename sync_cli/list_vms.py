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
    description = """List VMs."""

    parser = subparsers.add_parser("list-vms",
                                   help="list VMs",
                                   description=description)

    arguments.add_output_args(parser, field="vm_uuid")
    _add_filter_args(parser)

    parser.set_defaults(func=_run)

def _add_filter_args(parser):
    # TODO: This work arounds an argparse bug which breaks mutual exclusivity.
    #filter_group = parser.add_argument_group("filter arguments")
    #group = filter_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-n", "--name",
                       metavar="VM_NAME",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by VM name")

    group.add_argument("--device",
                       metavar="DEVICE_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list VMs associated with device")

    group.add_argument("--disk",
                       metavar="DISK_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list VMs using disk")

    group.add_argument("--unused",
                       action="store_true",
                       help="list VMs with no instances")

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    vms = cursor.callfunc("sync_admin.list_vms",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "vm_name": args.name,
                                 "device_uuid": args.device,
                                 "disk_uuid": args.disk,
                                 "unused": args.unused})

    if args.output == output.QUIET:
        fields = ["vm_uuid"]
    else:
        fields = None

    output.print_cursor(vms, fields, args.output)
