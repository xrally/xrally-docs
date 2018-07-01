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

from email import message_from_string
import json
import re
import sys

import pkg_resources
from setuptools import find_packages

from rally.common.plugin import info
from rally.common.plugin import plugin
from rally.common import validation
from rally import plugins as rplugins


def _parse_class_name(cls):
    name = ""
    for word in re.split(r"([A-Z][a-z]*)", cls.__name__):
        if word:
            if len(word) > 1 and name:
                name += " "
            name += word
    return name


def find_plugins(dist):
    """Find all plugins for the distribution."""
    plugins = []
    bases = {}
    packages = find_packages(exclude=["tests", "tests.*"],
                             where=dist.location)
    for p in plugin.Plugin.get_all():
        if (p.__module__.split(".", 1)[0] not in packages
                # do not save info about in-tree openstack plugins
                or p.__module__.startswith("rally.plugins.openstack")
                # another place of openstack plugins...
                or p.__module__.startswith("rally.task.validation")):
            continue
        p_info = p.get_info()
        p_info["module"] = p.__module__
        base = p._get_base()
        if base != plugin.Plugin:
            b_name = _parse_class_name(base)
            if b_name not in bases:
                bases[b_name] = info.trim(base.__doc__)
            p_info["base"] = b_name
        if issubclass(p, validation.ValidatablePluginMixin):
            validators = p._meta_get("validators", default=[])
            platforms = [kwargs for name, args, kwargs in validators
                         if name == "required_platform"]
            if platforms:
                p_info["required_platforms"] = platforms
        plugins.append(p_info)

    plugins = dict(("%s@%s" % (p["name"], p["platform"]), p)
                   for p in plugins)
    return plugins, bases


def _get_opts_from_method(module_name, function_name="list_opts"):
    import importlib

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return {}
    list_func = getattr(module, function_name, None)
    if list_func is None:
        return {}
    opts = list_func()
    if isinstance(opts, dict):
        opts = opts.items()
    return opts


def process_cfg(dist):
    """Grep configuration options for the distribution."""

    # get the path to options
    cfg_ep = dist.get_entry_info("rally_plugins", "options")
    if cfg_ep is None:
        if dist.project_name != "rally":
            return {}
        from rally.common import opts

        opts = dict(opts.list_opts())
        # remove this hardcode as soon as we get rid off these libraries
        for module in ("oslo_db.options", "oslo_log._options"):
            for group, options in _get_opts_from_method(module):
                group = group or "DEFAULT"
                opts.setdefault(group, []).extend(options)
        opts = opts.items()
    else:
        module_name = cfg_ep.module_name
        function_name = cfg_ep.attrs[0] if cfg_ep.attrs else None

        opts = _get_opts_from_method(module_name, function_name)

    result = {}
    for group, options in opts:
        result[group] = []
        for option in options:
            result[group].append({
                "name": option.name,
                "help": option.help,
                "type": option.type.type_name,
                "default": option.default,
                "deprecated_opts": [{"group": opt.group, "name": opt.name}
                                    for opt in option.deprecated_opts]
            })

    return result


@rplugins.ensure_plugins_are_loaded
def main():
    if len(sys.argv) != 2:
        print("{}")
        return 0

    result = {}
    dist = pkg_resources.get_distribution(sys.argv[1])

    # Step #1: collect information about all installed plugins and filter
    #   them by __module__ to get rid off default plugins.
    result["plugins"] = find_plugins(dist)

    # Step #2: collect available configuration options
    result["options"] = process_cfg(dist)

    # TODO(andreykurilin): import path and iterate over all options

    # Step #3: collect basic information about package
    pkg_info = dist.get_metadata("PKG-INFO")
    result["pkg_info"] = dict(message_from_string(pkg_info).items())

    print(json.dumps(result))


if __name__ == "__main__":
    main()
