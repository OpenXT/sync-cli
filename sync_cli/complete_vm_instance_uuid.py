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

import connect
import output

def add_subparser(subparsers):
    parser = subparsers.add_parser("complete-vm-instance-uuid",
                                   help="complete VM instance uuid")

    parser.add_argument("vm_instance",
                        metavar="PARTIAL_VM_INSTANCE_UUID",
                        help="partial VM instance uuid to be completed")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--all",
                       action="store_true",
                       help="include removed VM instances")

    group.add_argument("--removed",
                       action="store_true",
                       help="only removed VM instances")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config, required=False)
    if connection is None:
        return

    cursor = connection.cursor()

    vm_instance_uuids = (
        cursor.callfunc("sync_admin.complete_vm_instance_uuid",
                        cx_Oracle.CURSOR,
                        keywordParameters={
                            "partial_vm_instance_uuid": args.vm_instance,
                            "include_unremoved": not args.removed,
                            "include_removed": args.all or args.removed}))
    
    output.print_cursor(vm_instance_uuids, ["vm_instance_uuid"], output.QUIET)
