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
    description = """List disks."""

    parser = subparsers.add_parser("list-disks",
                                   help="list disks",
                                   description=description)

    arguments.add_output_args(parser, field="disk_uuid")
    _add_filter_args(parser)

    parser.set_defaults(func=_run)

def _add_filter_args(parser):
    # TODO: This work arounds an argparse bug which breaks mutual exclusivity.
    #filter_group = parser.add_argument_group("filter arguments")
    #group = filter_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-n", "--name",
                       metavar="DISK_NAME",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by disk name")

    group.add_argument("-t", "--type",
                       metavar="DISK_TYPE",
                       action=arguments.StoreSingleNonEmptyValue,
                       choices=["vhd", "iso"],
                       help="filter by disk type ('iso' or 'vhd')")

    group.add_argument("-p", "--path",
                       metavar="FILE_PATH",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by file path")

    group.add_argument("--hash",
                       metavar="FILE_HASH",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by file hash")

    group.add_argument("-v", "--vm",
                       metavar="VM_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list disks for VM")

    group.add_argument("-i", "--vm-instance",
                       metavar="VM_INSTANCE_UUID",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="list disks for VM instance")

    group.add_argument("--unused",
                       action="store_true",
                       help="list disks not associated with any VM")

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    if args.type is not None:
        disk_type = args.type[0]
    else:
        disk_type = None

    disks = cursor.callfunc("sync_admin.list_disks",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "disk_name": args.name,
                                 "disk_type": disk_type,
                                 "file_path": args.path,
                                 "file_hash": args.hash,
                                 "vm_uuid": args.vm,
                                 "vm_instance_uuid": args.vm_instance,
                                 "unused": args.unused})

    if args.output == output.QUIET:
        fields = ["disk_uuid"]
    else:
        fields = None

    output.print_cursor(disks, fields, args.output)
