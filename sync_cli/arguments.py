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
import output

class StoreSingleValue(argparse.Action):
    """Equivalent to argparse's "store" action but raises an exception if the
    argument is specified more than once.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            raise argparse.ArgumentError(self, "specified more than once")
        setattr(namespace, self.dest, values)

class StoreSingleNonEmptyValue(argparse.Action):
    """Equivalent to argparse's "store" action but raises an exception if the
    argument is specified more than once or the argument value is empty.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            raise argparse.ArgumentError(self, "specified more than once")
        if values == "":
            raise argparse.ArgumentError(self, "empty value not allowed")
        setattr(namespace, self.dest, values)

class AppendNonEmptyValue(argparse.Action):
    """Equivalent to argparse's "append" action but raises an exception if the
    argument value is empty.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if values == "":
            raise argparse.ArgumentError(self, "empty value not allowed")

        items = getattr(namespace, self.dest, [])[:]
        items.append(values)
        setattr(namespace, self.dest, items)

def add_output_args(parser, field=None, suppress=False):
    if suppress:
        quiet_help = argparse.SUPPRESS
        json_help = argparse.SUPPRESS
    else:
        quiet_help = "quiet output"
        if field is not None:
            quiet_help += ": only print " + field
        json_help = "json output"

    # TODO: argparse bug breaks mutual exclusivity here.
    output_group = parser.add_argument_group("output arguments")
    group = output_group.add_mutually_exclusive_group()

    group.add_argument("-j", "--json",
                       action="store_const",
                       const=output.JSON,
                       dest="output",
                       default=output.NORMAL,
                       help=json_help)

    group.add_argument("-q", "--quiet",
                       action="store_const",
                       const=output.QUIET,
                       dest="output",
                       default=output.NORMAL,
                       help=quiet_help)
