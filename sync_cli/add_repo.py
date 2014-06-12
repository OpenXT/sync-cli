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
import tarfile

import arguments
import connect
import get_file
import os
import output

# TODO: Improve help text.

_METADATA_FILE = os.path.join("packages.main", "XC-REPOSITORY")

class Error(Exception):
    pass

def add_subparser(subparsers):
    description = """Add a new repository."""

    parser = subparsers.add_parser("add-repo",
                                   help="add new repository",
                                   description=description)

    arguments.add_output_args(parser, field="repo_uuid")

    parser.add_argument("file_path",
                        metavar="FILE_PATH",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="path to file")

    parser.add_argument("--release",
                        metavar="RELEASE",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="assume release is RELEASE rather than extract "
                             "it from file")

    parser.add_argument("--build",
                        metavar="BUILD",
                        action=arguments.StoreSingleNonEmptyValue,
                        help="assume build is BUILD rather than extract it "
                             "from file")

    parser.add_argument("--hash",
                        metavar="FILE_HASH",
                        action=arguments.StoreSingleValue,
                        help="assume SHA-256 checksum of file is FILE_HASH "
                             "rather than compute it")

    parser.set_defaults(func=_run)

def _run(args, config):
    file_path = os.path.abspath(args.file_path)
    release, build = args.release, args.build

    if args.hash:
        file_size = get_file.get_file_size(file_path)
        file_hash = args.hash
    else:
        file_size, file_hash = get_file.get_file_size_and_hash(file_path)

    if None in [release, build]:
        (extracted_release,
         extracted_build) = _extract_repo_release_and_build(file_path)

        if release is None:
            release = extracted_release
        if build is None:
            build = extracted_build

    connection = connect.connect(args, config)
    cursor = connection.cursor()

    repo_uuid = cursor.callfunc("sync_admin.add_repo",
                                cx_Oracle.STRING,
                                keywordParameters={
                                    "release": release,
                                    "build": build,
                                    "file_path": file_path,
                                    "file_size": file_size,
                                    "file_hash": file_hash})

    output.print_value(repo_uuid, "repo_uuid", args.output)

def _extract_repo_release_and_build(file_path):
    metadata = _extract_repo_metadata(file_path)

    try:
        return metadata["release"], metadata["build"]
    except KeyError as error:
        raise Error("Invalid repository '{0}'. Metadata file '{1}' in tar "
                    "archive is missing '{2}' item.".format(file_path,
                                                            _METADATA_FILE,
                                                            error.args[0]))

def _extract_repo_metadata(file_path):
    try:
        tar = tarfile.open(file_path, "r")
        try:
            metadata_file = _open_tar_member(tar, _METADATA_FILE)
            try:
                return _read_metadata_file(metadata_file)
            finally:
                metadata_file.close()
        finally:
            tar.close()
    except IOError as error:
        raise Error("Failed to read '{0}': {1}.".format(file_path,
                                                        error.strerror))
    except tarfile.TarError as error:
        raise Error("Invalid repository '{0}'. Not a valid tar archive: "
                    "{1}.".format(file_path,
                                  error))

def _open_tar_member(tar, member_path):
    try:
        return tar.extractfile(member_path)
    except KeyError:
        raise Error("Invalid repository '{0}'. Metadata file '{1}' not found "
                    "in tar archive.".format(tar.name,
                                             member_path))

def _read_metadata_file(metadata_file):
    metadata = {}

    for line in metadata_file.read().splitlines():
        if line:
            fields = line.split(":", 2)
            if len(fields) == 2:
                metadata[fields[0]] = fields[1]

    return metadata
