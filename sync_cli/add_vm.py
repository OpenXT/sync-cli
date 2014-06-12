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
import get_file
import output

def add_subparser(subparsers):
    description = """Add a new VM."""

    epilog = """Configuration items should be specified in DAEMON:KEY:VALUE
                format, either as a series of --config arguments, or using the
                --config-file argument with a file containing one configuration
                item per line."""

    parser = subparsers.add_parser("add-vm",
                                   help="add new VM",
                                   description=description,
                                   epilog=epilog)

    arguments.add_output_args(parser, field="vm_uuid")
    _add_config_args(parser)

    parser.add_argument("-d", "--disk",
                        metavar="DISK_UUID",
                        action=arguments.AppendNonEmptyValue,
                        default=[],
                        help="disk uuid (can be specified multiple times)")

    parser.add_argument("name",
                        metavar="VM_NAME",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="VM name")

    parser.set_defaults(func=_run)

def _add_config_args(parser):
    # TODO: This works around an argparse bug which breaks mutual exclusivity.
    #config_group = parser.add_argument_group("configuration arguments")
    #group = config_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-c", "--config",
                       metavar="CONFIG",
                       action=arguments.AppendNonEmptyValue,
                       default=[],
                       help="configuration item (can be specified multiple "
                            "times)")

    group.add_argument("-f", "--config-file",
                       metavar="CONFIG_FILE",
                       action=arguments.StoreSingleNonEmptyValue,
                       help="read configuration items from file")

def _run(args, config):
    if args.config_file is not None:
        assert not args.config
        vm_config = get_file.read_config_from_file(args.config_file)
    else:
        vm_config = args.config

    connection = connect.connect(args, config)
    cursor = connection.cursor()

    vm_uuid = cursor.callfunc("sync_admin.add_vm",
                              cx_Oracle.STRING,
                              keywordParameters={
                                  "vm_name": args.name,
                                  "disk_uuids": args.disk,
                                  "config": vm_config})

    output.print_value(vm_uuid, "vm_uuid", args.output)
