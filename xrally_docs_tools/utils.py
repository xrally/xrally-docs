# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import inspect
import os
import subprocess
import tempfile
import uuid

import yaml

import xrally_docs_tools


def generate_random_path(root_dir=None):
    """Generates a vacant name for a file or dir at the specified place.

    :param root_dir: Name of a directory to generate path in. If None (default
        behaviour), temporary directory (i.e /tmp in linux) will be used.
    """
    root_dir = root_dir or tempfile.gettempdir()
    path = None
    while path is None:
        candidate = os.path.join(root_dir, str(uuid.uuid4()))
        if not os.path.exists(candidate):
            path = candidate
    return path


class Tag(object):
    """A helper class for representing rally versions"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return self.x, self.y, self.z

    def to_str(self):
        return "%s" % self

    def __str__(self):
        return "%s.%s.%s" % self.to_tuple()

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()

    def __gt__(self, other):
        return self.to_tuple() > other.to_tuple()

    def __ge__(self, other):
        return self.to_tuple() >= other.to_tuple()

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def __ne__(self, other):
        return self.to_tuple() != other.to_tuple()

    @classmethod
    def parse(cls, stag):
        """Parse a string with a tag."""
        try:
            version = tuple(int(i) for i in stag.split("."))
            if len(version) != 3:
                # wrong format.ignoring
                return None
            return cls(*version)
        except ValueError:
            # it is not a valid version. maybe it is just a pointer for some
            # stuff like oef of a branch
            return None

    @classmethod
    def parse_list(cls, stags):
        """Parse a list with string-like tags."""
        tags = []
        for tag in stags.split("\n"):
            if not tag:
                continue
            version = cls.parse(tag)
            if version is None:
                continue
            tags.append(version)
        return sorted(tags)


def sp_call(cmd, env=None, cwd=None, merge_stdout=True):
    """Call subprocess.check_output with hiding stdout and stderr."""
    try:
        stderr = subprocess.STDOUT if merge_stdout else None
        return subprocess.check_output(cmd, env=env, cwd=cwd,
                                       stderr=stderr)
    except subprocess.CalledProcessError as e:
        print("Output: %s" % e.output)


def get_defaults(func):
    """Return a map of argument:default_value for specified function."""
    spec = inspect.getargspec(func)
    if spec.defaults:
        return dict(zip(spec.args[-len(spec.defaults):], spec.defaults))
    return {}


def get_mkdocs_cfg():
    with open(xrally_docs_tools.MKDOCS_CFG) as f:
        return yaml.safe_load(f)


def update_mkdocs_cfg(cfg):
    print("Updating MKDocs configuration.")
    with open(xrally_docs_tools.MKDOCS_CFG, "w") as f:
        f.write(yaml.safe_dump(cfg))
