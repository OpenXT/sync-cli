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
    description = """List VM instances."""

    parser = subparsers.add_parser("list-vm-instances",
                                   help="list VM instances",
                                   description=description)

    arguments.add_output_args(parser, field="vm_instance_uuid")
    _add_filter_args(parser)

    parser.add_argument("--removed",
                        action="store_true",
                        help="list VM instances which have been removed")

    parser.set_defaults(func=_run)

def _add_filter_args(parser):
    # TODO: This works around an argparse bug which breaks mutual exclusivity.
    #filter_group = parser.add_argument_group("filter arguments")
    #group = filter_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-n", "--name",
                       metavar="VM_INSTANCE_NAME",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by VM instance name")

    group.add_argument("--device",
                       metavar="DEVICE_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list VM instances for device")

    group.add_argument("-v", "--vm",
                       metavar="VM_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list instances of VM")

    group.add_argument("--disk",
                       metavar="DISK_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list VM instances using disk")

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    vm_instances = cursor.callfunc("sync_admin.list_vm_instances",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "vm_instance_name": args.name,
                                 "device_uuid": args.device,
                                 "vm_uuid": args.vm,
                                 "disk_uuid": args.disk,
                                 "removed": args.removed})

    if args.output == output.QUIET:
        fields = ["vm_instance_uuid"]
    else:
        fields = None

    output.print_cursor(vm_instances, fields, args.output)
