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

import cx_Oracle
import sys

import sync_db.error

import arguments
import connect
import get_file
import output

_PROGRESS_MESSAGE = "Verifying file {0}/{1}..."
_DISK, _REPO = range(2)
_FILE_TYPE_NAME = {_DISK: "disk", _REPO: "repository"}

class Error(Exception):
    pass

def add_subparser(subparsers):
    description = """Verify all disk files and repository files. For each file,
                     check that it exists and has the correct size and hash."""

    parser = subparsers.add_parser("verify-files",
                                   help="verify all disk files and repository "
                                        "files",
                                   description=description)

    parser.add_argument("-s", "--short",
                        action="store_true",
                        help="short verification: skip file hash check")

    arguments.add_output_args(parser, suppress=True)

    parser.set_defaults(func=_run)

def _run(args, config):
    connection = connect.connect(args, config)
    disks, repos = _get_all_files(connection)

    files = [(_DISK, x) for x in disks] + [(_REPO, x) for x in repos]
    num_files = len(files)
    num_errors = 0
    i = 0

    for file_type, file_ in files:
        i += 1
        _show_progress(i, num_files, args.output)

        try:
            _verify_file(connection, file_type, file_, args.short)
        except get_file.Error as error:
            num_errors += 1
            _clear_progress(num_files, args.output)
            sys.stderr.write("{0}\n\n".format(error))

    _clear_progress(num_files, args.output)

    if num_errors > 0:
        raise Error("Found {0} {1} during file verification.".format(
                        num_errors,
                        "error" if num_errors == 1 else "errors"))

    if args.output == output.NORMAL:
        print "File verification succeeded."

def _get_all_files(connection):
    cursor = connection.cursor()
    disks = connection.cursor()
    repos = connection.cursor()

    cursor.callproc("sync_admin.list_all_files",
                     keywordParameters={
                         "disks": disks,
                         "repos": repos})

    return ([disk for disk in disks], [repo for repo in repos])

def _verify_file(connection, file_type, file_, skip_hash):
    file_uuid, file_path, file_size, file_hash = file_

    try:
        get_file.verify_file(file_path,
                             file_size,
                             None if skip_hash else file_hash,
                             "{0} uuid '{1}'".format(
                                 _FILE_TYPE_NAME[file_type], file_uuid))
    except get_file.Error:
        # File is missing or invalid. Check if this disk or repository has been
        # removed from the database since the original query. If so, this is
        # not an error.
        if file_type == _DISK:
            if _disk_exists(connection, file_uuid):
                raise
        else:
            if _repo_exists(connection, file_uuid):
                raise

def _disk_exists(connection, disk_uuid):
    cursor = connection.cursor()

    try:
        with sync_db.error.convert():
            cursor.callfunc("sync_admin.get_disk",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "disk_uuid": disk_uuid})
    except sync_db.error.SyncError as error:
        if error.code == sync_db.error.DISK_NOT_FOUND:
            return False
        raise

    return True

def _repo_exists(connection, repo_uuid):
    cursor = connection.cursor()

    try:
        with sync_db.error.convert():
            cursor.callfunc("sync_admin.get_repo",
                             cx_Oracle.CURSOR,
                             keywordParameters={
                                 "repo_uuid": repo_uuid})
    except sync_db.error.SyncError as error:
        if error.code == sync_db.error.REPO_NOT_FOUND:
            return False
        raise

    return True

def _show_progress(current, num_files, output_mode):
    if output_mode == output.NORMAL:
        sys.stderr.write(_PROGRESS_MESSAGE.format(current, num_files) + "\r")

def _clear_progress(num_files, output_mode):
    if output_mode == output.NORMAL:
        message_len = len(_PROGRESS_MESSAGE.format(num_files, num_files))
        sys.stderr.write(" " * message_len + "\r")
