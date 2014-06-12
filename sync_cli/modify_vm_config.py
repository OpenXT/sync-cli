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

import arguments
import connect
import get_file

def add_subparser(subparsers):
    description = """Modify the configuration for a VM."""

    epilog = """Configuration items should be specified in DAEMON:KEY:VALUE
                format, either as a series of --config arguments, or using the
                --config-file argument with a file containing one configuration
                item per line. Leaving VALUE empty removes the configuration
                item."""

    parser = subparsers.add_parser("modify-vm-config",
                                   help="modify VM configuration",
                                   description=description,
                                   epilog=epilog)

    arguments.add_output_args(parser, suppress=True)
    _add_config_args(parser)

    parser.add_argument("vm",
                        metavar="VM_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="VM uuid")

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

    # TODO: This works around an argparse bug which breaks mutual exclusivity.
    #config_group.add_argument("-r", "--replace",
    parser.add_argument("-r", "--replace",
                        action="store_true",
                        help="remove all existing configuration first")

def _run(args, config):
    if args.config_file is not None:
        assert not args.config
        vm_config = get_file.read_config_from_file(args.config_file)
    else:
        vm_config = args.config

    connection = connect.connect(args, config)
    cursor = connection.cursor()

    cursor.callproc("sync_admin.modify_vm_config",
                    keywordParameters={
                        "vm_uuid": args.vm,
                        "config": vm_config,
                        "replace": args.replace})
