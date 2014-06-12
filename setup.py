#!/usr/bin/python
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

import os
import sys
from distutils.core import setup

# Generate bash completion script.
# TODO: This duplicates code from generate-completion script.
if os.path.isdir("sync_cli_completion"):
    try:
        import sync_db
    except ImportError:
        # Useful when running from source tree.
        sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,
                                     "sync-database"))
        import sync_db

    import sync_cli.main
    import sync_cli.add_disk
    import sync_cli_completion.main

    if not os.path.exists("generated"):
        os.mkdir("generated")

    parser = sync_cli.main.create_parser()
    with open("generated/sync-admin", "w") as cf:
        cf.write(sync_cli_completion.main.format_script(
                     parser,
                     sync_cli.add_disk.DISK_TYPES))

setup_cfg = {
    "name": "sync-admin",
    "version": os.environ.get("VERSION"),
    "description": "XenClient Synchronizer XT administration tool",
    "packages": ["sync_cli"],
    "scripts": ["sync-admin"],
    "data_files":  [("/etc/bash_completion.d", ["generated/sync-admin"])],
}

setup(**setup_cfg)
