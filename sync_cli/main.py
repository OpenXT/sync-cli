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

import argparse
import ConfigParser
import os
import sys

import sync_db.error

import add_device
import add_disk
import add_repo
import add_vm
import add_vm_instance
import arguments
import complete_device_uuid
import complete_disk_uuid
import complete_repo_uuid
import complete_vm_instance_uuid
import complete_vm_uuid
import configuration
import connect
import get_file
import list_devices
import list_disks
import list_repos
import list_vm_instances
import list_vms
import lock_vm_instance
import modify_device_config
import modify_device_repo
import modify_vm_config
import modify_vm_instance_name
import output
import purge_vm_instance
import readd_vm_instance
import remove_device
import remove_disk
import remove_repo
import remove_vm
import remove_vm_instance
import reset_device_secret
import show_device
import show_device_config
import show_device_secret
import show_disk
import show_disk_key
import show_licensing
import show_repo
import show_report
import show_vm
import show_vm_config
import show_vm_instance
import unlock_vm_instance
import verify_database
import verify_files

# TODO: improve help text
# TODO: ideally make these show same help text:
#           sync-admin
#           sync-admin -h
#           sync-admin help
#       and these:
#           sync-admin add-device
#           sync-admin -h add-device
#           sync-admin add-device -h
#           sync-admin help add-device
# TODO: help text lists commands in no particular order
# TODO: missing "]" in help text for commands with two groups of mutually
#       exclusive arguments, e.g. list-disks - see
#       http://bugs.python.org/issue9355
# TODO: describe configuration file
# TODO: don't include complete-* commands in help text; but still allow, e.g.
#           sync-admin complete-device-uuid -h

def run():
    try:
        with sync_db.error.convert():
            _run_command()
    except ConfigParser.Error as error:
        sys.stderr.write("Error in configuration file: {0}\n".format(error))
        sys.exit(1)
    except sync_db.error.SyncError as error:
        sys.stderr.write("Error: {0}\n".format(error))
        sys.exit(1)
    except sync_db.error.Error as error:
        sys.stderr.write("Database error: {0}\n".format(error))
        sys.exit(1)
    except (add_disk.Error, add_repo.Error, connect.Error, get_file.Error,
            output.Error, verify_database.Error, verify_files.Error) as error:
        sys.stderr.write("Error: {0}\n".format(error))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write("Aborted.\n")
        sys.exit(1)

def _run_command():
    parser = create_parser()
    args = parser.parse_args()

    config = configuration.read_config()

    args.func(args, config)

def create_parser():
    epilog = """For more information about a command, run
                '{0} COMMAND -h'.""".format(os.path.basename(sys.argv[0]))

    parser = argparse.ArgumentParser(epilog=epilog)

    parser.add_argument("-d", "--database",
                        metavar="DATABASE",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="database login (user/pass@host)")

    subparsers = parser.add_subparsers(title="commands",
                                       metavar="COMMAND")

    for module in [add_device,
                   add_disk,
                   add_repo,
                   add_vm,
                   add_vm_instance,
                   complete_device_uuid,
                   complete_disk_uuid,
                   complete_repo_uuid,
                   complete_vm_instance_uuid,
                   complete_vm_uuid,
                   list_devices,
                   list_disks,
                   list_repos,
                   list_vm_instances,
                   list_vms,
                   lock_vm_instance,
                   modify_device_config,
                   modify_device_repo,
                   modify_vm_config,
                   modify_vm_instance_name,
                   purge_vm_instance,
                   readd_vm_instance,
                   remove_device,
                   remove_disk,
                   remove_repo,
                   remove_vm,
                   remove_vm_instance,
                   reset_device_secret,
                   show_device,
                   show_device_config,
                   show_device_secret,
                   show_disk,
                   show_disk_key,
                   show_licensing,
                   show_repo,
                   show_report,
                   show_vm,
                   show_vm_config,
                   show_vm_instance,
                   unlock_vm_instance,
                   verify_database,
                   verify_files]:
        module.add_subparser(subparsers)

    return parser
