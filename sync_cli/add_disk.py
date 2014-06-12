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
import os.path
import output

DISK_TYPES = ["iso", "vhd"]

class Error(Exception):
    pass

def add_subparser(subparsers):
    description = """Add a new disk."""

    parser = subparsers.add_parser("add-disk",
                                   help="add new disk",
                                   description=description)

    arguments.add_output_args(parser, field="disk_uuid")
    _add_key_args(parser)

    parser.add_argument("name",
                        metavar="DISK_NAME",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="disk name")

    parser.add_argument("file_path",
                        metavar="FILE_PATH",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="path to file")

    parser.add_argument("-r", "--read-only",
                        action="store_true",
                        help="read-only")

    parser.add_argument("-s", "--shared",
                        action="store_true",
                        help="share disk between VMs") # TODO: improve help

    parser.add_argument("--hash",
                        metavar="FILE_HASH",
                        action=arguments.StoreSingleValue,
                        help="assume SHA-256 checksum of file is FILE_HASH "
                             "rather than compute it")

    parser.add_argument("-t", "--type",
                        metavar="DISK_TYPE",
                        action=arguments.StoreSingleValue,
                        choices=DISK_TYPES,
                        help="disk type ('iso' or 'vhd'); if not specified, "
                             "deduce from file name")

    parser.set_defaults(func=_run)

def _add_key_args(parser):
    # TODO: This works around an argparse bug which breaks mutual exclusivity.
    #config_group = parser.add_argument_group("encryption key arguments")
    #group = config_group.add_mutually_exclusive_group()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-k", "--key",
                       metavar="ENCRYPTION_KEY",
                       action=arguments.StoreSingleValue,
                       help="disk encryption key as hexadecimal string")

    group.add_argument("-f", "--key-file",
                        metavar="KEY_FILE",
                        action=arguments.StoreSingleValue,
                        help="read raw disk encryption key from file")

def _run(args, config):
    file_path = os.path.abspath(args.file_path)

    if args.type is not None:
        disk_type = args.type[0]
        read_only = args.read_only
    elif args.file_path.endswith(".vhd"):
        disk_type = "v"
        read_only = args.read_only
    elif args.file_path.endswith(".iso"):
        disk_type = "i"
        read_only = True
    else:
        raise Error("Disk type must be specified.")

    if args.hash:
        file_size = get_file.get_file_size(file_path)
        file_hash = args.hash
    else:
        file_size, file_hash = get_file.get_file_size_and_hash(file_path)

    if args.key is not None:
        assert args.key_file is None
        encryption_key = args.key
    elif args.key_file is not None:
        encryption_key = get_file.read_encryption_key_from_file(args.key_file)
    else:
        encryption_key = None

    connection = connect.connect(args, config)
    cursor = connection.cursor()

    disk_uuid = cursor.callfunc("sync_admin.add_disk",
                                cx_Oracle.STRING,
                                keywordParameters={
                                    "disk_name": args.name,
                                    "disk_type": disk_type,
                                    "file_path": file_path,
                                    "file_size": file_size,
                                    "file_hash": file_hash,
                                    "encryption_key": encryption_key,
                                    "shared": args.shared,
                                    "read_only": read_only})

    output.print_value(disk_uuid, "disk_uuid", args.output)
