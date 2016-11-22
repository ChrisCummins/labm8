# Copyright (C) 2015, 2016 Chris Cummins.
#
# Labm8 is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Labm8 is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with labm8.  If not, see <http://www.gnu.org/licenses/>.
#
"""
JSON parser which supports comments.
"""
import json
import re

import labm8
from labm8 import fs


def loads(text, **kwargs):
    """
    Deserialize `text` (a `str` or `unicode` instance containing a JSON
    document with Python or JavaScript like comments) to a Python object.

    Taken from `commentjson <https://github.com/vaidik/commentjson>`_, written
    by `Vaidik Kapoor <https://github.com/vaidik>`_.

    Copyright (c) 2014 Vaidik Kapoor, MIT license.

    Arguments:
        text (str): serialized JSON string with or without comments.
        **kwargs (optional): all the arguments that
            `json.loads <http://docs.python.org/2/library/json.html#json.loads>`_
            accepts.

    Returns:
        `dict` or `list`: Decoded JSON.
    """
    regex = r'\s*(#|\/{2}).*$'
    regex_inline = r'(:?(?:\s)*([A-Za-z\d\.{}]*)|((?<=\").*\"),?)(?:\s)*(((#|(\/{2})).*)|)$'
    lines = text.split('\n')

    for index, line in enumerate(lines):
        if re.search(regex, line):
            if re.search(r'^' + regex, line, re.IGNORECASE):
                lines[index] = ""
            elif re.search(regex_inline, line):
                lines[index] = re.sub(regex_inline, r'\1', line)

    return json.loads('\n'.join(lines), **kwargs)


def loadf(*components):
    """
    Load a JSON data blob.

    Arguments:
        *components (str[]): Path to file.

    Returns:
        `dict` or `list`: JSON data.

    Raises:
        fs.File404: If path does not exist.
    """
    with open(fs.must_exist(*components)) as infile:
        return loads(infile.read())