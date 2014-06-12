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

import json

NORMAL = 0
QUIET  = 1
JSON   = 2

class Error(Exception):
    pass

def print_cursor(cursor, fields, output, single_row=False):
    field_nums = {}
    all_fields = []

    for i, column_desc in enumerate(cursor.description):
        field_name = column_desc[0].lower()
        field_nums[field_name] = i
        all_fields.append(field_name)

    if fields is None:
        fields = all_fields

    rows = cursor.fetchall()
    if single_row and len(rows) != 1:
        raise Error("Database cursor returned {0} rows. Expected 1 "
                    "row.".format(len(rows)))

    if output == NORMAL:
        field_name_len = max(len(x) for x in fields)

        for i, row in enumerate(rows):
            if i > 0 and len(fields) > 1:
                print

            for field_name in fields:
                label = (field_name + ": ").ljust(field_name_len + 2)
                value = row[field_nums[field_name]]
                print label + _to_str(value)
    elif output == QUIET:
        for row in rows:
            print ":".join(row[field_nums[field_name]]
                           for field_name in fields)
    elif output == JSON:
        data = []

        for row in rows:
            node = {}
            for field_name in fields:
                node[field_name] = row[field_nums[field_name]]
            data.append(node)

        print _to_json(data[0] if single_row else data)
    else:
        assert False

def print_value(value, field_name, output):
    if output == NORMAL:
        print field_name + ": " + _to_str(value)
    elif output == QUIET:
        print _to_str(value)
    elif output == JSON:
        print _to_json(value)
    else:
        assert False

def _to_str(value):
    if value is not None:
        return str(value)
    else:
        return ""

def _to_json(data):
    return json.dumps(data, indent=4)
