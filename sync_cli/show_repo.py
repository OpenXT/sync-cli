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
    description = """Show information about a repository."""

    parser = subparsers.add_parser("show-repo",
                                   help="show repository",
                                   description=description)

    arguments.add_output_args(parser)

    parser.add_argument("repo",
                        metavar="REPO_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="repo uuid")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    repo = cursor.callfunc("sync_admin.get_repo",
                            cx_Oracle.CURSOR,
                            keywordParameters={
                                "repo_uuid": args.repo})

    if args.output == output.QUIET:
        fields = ["repo_uuid"]
    else:
        fields = None

    output.print_cursor(repo, fields, args.output, single_row=True)
