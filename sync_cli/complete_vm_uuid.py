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
    parser = subparsers.add_parser("complete-vm-uuid",
                                   help="complete VM uuid")

    parser.add_argument("vm",
                        metavar="PARTIAL_VM_UUID",
                        help="partial VM uuid to be completed")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config, required=False)
    if connection is None:
        return

    cursor = connection.cursor()

    vm_uuids = cursor.callfunc("sync_admin.complete_vm_uuid",
                               cx_Oracle.CURSOR,
                               keywordParameters={
                                   "partial_vm_uuid": args.vm})
    
    output.print_cursor(vm_uuids, ["vm_uuid"], output.QUIET)
