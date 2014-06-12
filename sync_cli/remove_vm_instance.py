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

def add_subparser(subparsers):
    description = """Remove a VM instance from a device. Information about the
                     VM instance is retained, but can be permanently removed
                     with the purge-vm-instance command."""

    epilog = """By default, the device will wait until the VM instance is no
                longer running before removing it. With the --hard argument,
                the device will force the VM instance to shut down and remove
                it."""
    
    parser = subparsers.add_parser("remove-vm-instance",
                                   help="remove VM instance",
                                   description=description,
                                   epilog=epilog)

    arguments.add_output_args(parser, suppress=True)

    parser.add_argument("--hard",
                        action="store_true",
                        help="don't wait until VM instance is shut down")

    parser.add_argument("vm_instance",
                        metavar="VM_INSTANCE_UUID",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="VM instance uuid")

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    cursor = connection.cursor()

    cursor.callproc("sync_admin.remove_vm_instance",
                    keywordParameters={
                        "vm_instance_uuid": args.vm_instance,
                        "hard_removal": args.hard})
