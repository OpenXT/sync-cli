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

# TODO: Improve help text about repository.

def add_subparser(subparsers):
    description = """Add a new device."""

    epilog = """Configuration items should be specified in DAEMON:KEY:VALUE
                format, either as a series of --config arguments, or using the
                --config-file argument with a file containing one configuration
                item per line."""

    parser = subparsers.add_parser("add-device",
                                   help="add new device",
                                   description=description,
                                   epilog=epilog)

    arguments.add_output_args(parser, field="device_uuid")
    _add_config_args(parser)

    parser.add_argument("-r", "--repo",
                        metavar="REPO_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="repository uuid")

    parser.add_argument("name",
                        metavar="DEVICE_NAME",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="device name")

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
        device_config = get_file.read_config_from_file(args.config_file)
    else:
        device_config = args.config

    connection = connect.connect(args, config)
    cursor = connection.cursor()

    device_uuid = cursor.callfunc("sync_admin.add_device",
                                  cx_Oracle.STRING,
                                  keywordParameters={
                                      "device_name": args.name,
                                      "repo_uuid": args.repo,
                                      "config": device_config})

    output.print_value(device_uuid, "device_uuid", args.output)
