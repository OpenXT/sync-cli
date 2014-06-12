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
    description = """Add a new VM instance to a device."""

    parser = subparsers.add_parser("add-vm-instance",
                                   help="add new VM instance",
                                   description=description)

    arguments.add_output_args(parser, field="vm_instance_uuid")

    parser.add_argument("device",
                        metavar="DEVICE_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="device uuid")

    parser.add_argument("vm",
                        metavar="VM_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="VM uuid")

    parser.add_argument("name",
                        metavar="VM_INSTANCE_NAME",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="VM instance name")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    vm_instance_uuid = cursor.callfunc("sync_admin.add_vm_instance",
                                       cx_Oracle.STRING,
                                       keywordParameters={
                                           "device_uuid": args.device,
                                           "vm_uuid": args.vm,
                                           "vm_instance_name": args.name})

    output.print_value(vm_instance_uuid, "vm_instance_uuid", args.output)
