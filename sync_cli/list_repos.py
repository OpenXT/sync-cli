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
    description = """List repositories."""

    parser = subparsers.add_parser("list-repos",
                                   help="list repositories",
                                   description=description)

    arguments.add_output_args(parser, field="repo_uuid")
    _add_filter_args(parser)

    parser.set_defaults(func=_run)

def _add_filter_args(parser):
    # TODO: This work arounds an argparse bug which breaks mutual exclusivity.
    #filter_group = parser.add_argument_group("filter arguments")
    #group = filter_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-r", "--release",
                       metavar="RELEASE",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by release")

    group.add_argument("-b", "--build",
                       metavar="BUILD",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by build")

    group.add_argument("-p", "--path",
                       metavar="FILE_PATH",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by file path")

    group.add_argument("--hash",
                       metavar="FILE_HASH",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="filter by file hash")

    group.add_argument("--unused",
                       action="store_true",
                       help="list repositories not associated with any device")

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    repos = cursor.callfunc("sync_admin.list_repos",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "release": args.release,
                                 "build": args.build,
                                 "file_path": args.path,
                                 "file_hash": args.hash,
                                 "unused": args.unused})

    if args.output == output.QUIET:
        fields = ["repo_uuid"]
    else:
        fields = None

    output.print_cursor(repos, fields, args.output)
