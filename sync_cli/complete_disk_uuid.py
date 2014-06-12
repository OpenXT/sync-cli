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
    parser = subparsers.add_parser("complete-disk-uuid",
                                   help="complete disk uuid")

    parser.add_argument("disk",
                        metavar="PARTIAL_DISK_UUID",
                        help="partial disk uuid to be completed")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config, required=False)
    if connection is None:
        return

    cursor = connection.cursor()

    disk_uuids = cursor.callfunc("sync_admin.complete_disk_uuid",
                                 cx_Oracle.CURSOR,
                                 keywordParameters={
                                     "partial_disk_uuid": args.disk})
    
    output.print_cursor(disk_uuids, ["disk_uuid"], output.QUIET)
