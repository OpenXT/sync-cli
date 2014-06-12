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

import hashlib
import os

class Error(Exception):
    pass

class ReadError(Error):
    def __init__(self, message, strerror):
        self.args = message,
        self.strerror = strerror

class WriteError(Error):
    def __init__(self, message, strerror):
        self.args = message,
        self.strerror = strerror

def get_file_size(file_path):
    try:
        # Open (rather than stat) the file to make sure it can be read.
        with open(file_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            return f.tell()
    except IOError as error:
        raise ReadError("Failed to read '{0}': {1}.".format(file_path,
                                                            error.strerror),
                        strerror=error.strerror)

def get_file_size_and_hash(file_path):
    hash = hashlib.sha256()
    size = 0

    try:
        with open(file_path, "rb") as f:
            while True:
                data = f.read(1048576)
                if data == "":
                    break
                hash.update(data)
                size += len(data)
    except IOError as error:
        raise ReadError("Failed to read '{0}': {1}.".format(file_path,
                                                            error.strerror),
                        strerror=error.strerror)

    return size, hash.hexdigest()

def read_config_from_file(file_path):
    lines = []

    try:
        with open(file_path, "r") as f:
            for line in f.readlines():
                if not line.isspace() and not line.startswith("#"):
                    lines.append(line.rstrip(os.linesep))
    except IOError as error:
        raise ReadError("Failed to read '{0}': {1}.".format(file_path,
                                                            error.strerror),
                        strerror=error.strerror)
    return lines

def read_encryption_key_from_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read().encode("hex")
    except IOError as error:
        raise ReadError("Failed to read '{0}': {1}.".format(file_path,
                                                            error.strerror),
                        strerror=error.strerror)

def verify_file(file_path, file_size, file_hash, desc):
    try:
        if file_hash is not None:
            actual_size, actual_hash = get_file_size_and_hash(file_path)
        else:
            actual_size = get_file_size(file_path)
            actual_hash = None
    except ReadError as error:
        raise Error("Failed to read {0}:\n"
                    "    file path:     {1}\n"
                    "    error:         {2}".format(desc,
                                                    file_path,
                                                    error.strerror))

    errors = []
    lines = ["    file path:     {0}".format(file_path)]

    if actual_size != file_size:
        errors.append("size")
        lines.append("    expected size: {0}".format(file_size))
        lines.append("    actual size:   {0}".format(actual_size))

    if file_hash is not None and actual_hash != file_hash:
        errors.append("hash")
        lines.append("    expected hash: {0}".format(file_hash))
        lines.append("    actual hash:   {0}".format(actual_hash))

    if errors:
        raise Error("Incorrect {0} for {1}:\n".format(" and ".join(errors),
                                                      desc) +
                    "\n".join(lines))

def write_encryption_key_to_file(key, file_path):
    if key is None:
        raise Error("No encryption key set.")

    try:
        with open(file_path, "wb") as f:
            f.write(key.decode("hex"))
    except IOError as error:
        raise WriteError("Failed to write to '{0}': "
                         "{1}.".format(file_path,
                                       error.strerror),
                         strerror=error.strerror)
