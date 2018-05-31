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

import collections
import os
import textwrap

import json
from rally.common.plugin import info

import xrally_docs_tools
from xrally_docs_tools import mdutils
from xrally_docs_tools import r2m


ROOT_DIR = os.path.join(xrally_docs_tools.DOCS_DIR, "plugins")


class PackagePage(object):
    """Base class for package pages."""
    NAME = None

    def __init__(self, package):
        self.package = package
        self._ntitle = self.package["title"].lower().replace("-", "_")
        self._root_path = os.path.join(ROOT_DIR, "%s" % self._ntitle)
        if not os.path.exists(self._root_path):
            os.makedirs(self._root_path)
        if self.NAME is not None:
            self._path = os.path.join(self._root_path, self.NAME)

    def _make(self):
        return ""

    def save(self):
        with open(self._path, "w") as f:
            f.write(self._make())
        return self._path.replace("%s/" % xrally_docs_tools.DOCS_DIR, "")


class OverviewPage(PackagePage):
    """Shows the overview page for a package.

    Includes such information like latest release, repository url,
    description, etc.
    """
    NAME = "overview.md"

    def _make(self):
        page = ["# %s" % self.package["title"],
                "__Relevant release__: %s" % self.package["versions"][1],
                "__Repository__: <%s>" % self.package["repository"]]
        for key in ("License", "Author", "Author-email"):
            if key in self.package["pkg_info"]:
                page.append(
                    "__%s__: %s" % (key, self.package["pkg_info"][key]))
        if self.package["pkg_info"]["Description"]:
            description = info.trim(self.package["pkg_info"]["Description"])
            if not description.startswith("#"):
                # rst
                description = r2m.convert(description)
            page.extend(description.split("\n\n")[1:])
        elif self.package["pkg_info"]["Summary"]:
            # we do not need to add summary in case of existance of long
            # description. otherwise it will produce duplication
            page.append(self.package["pkg_info"]["Summary"])

        return "\n\n".join(page)


class DevOverviewPage(PackagePage):
    """Shows the overview page for a package which had not been released yet"""
    NAME = "overview.md"

    def _make(self):
        page = [
            "# %s" % self.package["title"],
            "__Repository__: <%s>" % self.package["repository"],
            "!!! note",
            "    This package is under active development and has not "
            "been released yet.",
            "    Follow the repository on GitHub to do not miss any updates."
        ]
        if "description" in self.package:
            page.append("## Description")
            page.append(self.package["description"])

        return "\n\n".join(page)


class ChangeLogPage(PackagePage):
    """Shows changelog for the package."""

    NAME = "changelog.md"

    def _make(self):
        if self.package["changelog_file"].endswith(".md"):
            return self.package["changelog"]
        else:
            return r2m.convert(self.package["changelog"])


class ConfigOptionsReference(PackagePage):
    """Shows expected config options for the package."""
    NAME = "options.md"

    @staticmethod
    def _group_sort_key(group_item):
        """DEFAULT group should always be in the top"""
        group_name, _group_cfg = group_item
        if group_name == "DEFAULT":
            return 0, group_name
        else:
            return 1, group_name

    def _make(self):
        page = ["# Available configuration options"]
        groups = sorted(self.package["options"].items(),
                        key=self._group_sort_key)
        for group_name, options in groups:
            if self.package["name"] == "rally" and group_name == "openstack":
                # it will be removed soon. no need to even display
                continue

            page.append("## [%s]" % group_name)

            options = sorted(options, key=lambda o: o["name"])
            for option in options:
                section = []

                # help message
                help = textwrap.TextWrapper().fill(option["help"])

                section.append(
                    "# %s" % "\n# ".join(help.split("\n")))

                # type
                section.append("# (%s)" % option["type"])

                for deprecation in option["deprecated_opts"]:
                    dgroup = deprecation["group"] or group_name
                    dname = deprecation["name"] or option["name"]
                    section.append(
                        "# Deprecated group/name - %s/%s" %
                        (dgroup, dname))

                # option itself
                if not option["default"] and option["type"] == "boolean value":
                    default = False
                elif option["default"] and option["type"] == "string value":
                    default = "'%s'" % option["default"]
                else:
                    default = option["default"] or "<None>"
                section.append("#%s = %s" % (option["name"], default))

                page.append("```\n%s\n```" % "\n".join(section))

        return "\n\n".join(page)


class PluginsReferencesPage(PackagePage):
    """Shows available plugins for the package."""

    NAME = "plugins.md"

    _CATEGORIES = {
        "Common": ["OS Client", "Exporters"],
        "Environment Component": ["Platform"],
        "Task Component": ["Chart", "Context", "Hook Action", "Hook Trigger",
                           "Resource Type", "Task Exporter", "SLA", "Scenario",
                           "Scenario Runner", "Trigger", "Validator"],
        "Verification Component": ["Verifier Context", "Verification Reporter",
                                   "Verifier Manager"]
    }

    # NOTE(andreykurilin): several bases do not have docstings at all, so it is
    # redundant to display them
    _IGNORED_BASES = ["Resource Type", "OS Client"]

    def _group_plugins(self):
        """Group plugins by plugin bases."""
        grouped_by_bases = dict(
            (name, {"description": descr, "plugins": [], "name": name}) 
            for name, descr in self.package["plugins_bases"].items())

        plugins = self.package["plugins"].values()
        if self.package["name"] == "rally":
            # ignore in-tree openstack plugins
            plugins = [p for p in plugins if p["platform"] != "openstack"]

        for p in plugins:
            base = p.get("base", "Common")
            if base in self._IGNORED_BASES:
                continue
            
            grouped_by_bases[base]["plugins"].append(p)

        grouped_by_categories = {}
        for pbase in grouped_by_bases.values():
            if not pbase["plugins"]:
                continue
            category_of_base = "Common"
            for cname, cbases in self._CATEGORIES.items():
                if pbase["name"] in cbases:
                    category_of_base = cname

            grouped_by_categories.setdefault(category_of_base, []).append(
                pbase)

        return grouped_by_categories

    @staticmethod
    def _make_arg_items(items, ref_prefix, title="Parameters"):
        definition = mdutils.DefinitionsList(
            title=title,
            prefix=ref_prefix,
            term_label="Argument")
        for item in items:
            iname = item.get("name", "") or item.pop("type")
            if "type" in item:
                iname += " (%s)" % item["type"]
            definition.add_term(iname, item["doc"])
        return definition.to_md()

    _schema_key_order = ["$schema",
                         "type",
                         "description",
                         "properties",
                         "patternProperties",
                         "minProperties",
                         "maxProperties",
                         "additionalProperties",
                         "required",
                         "enum",
                         "items",
                         "oneOf",
                         "anyOf",
                         "minItems",
                         "maxItems",
                         "uniqueItems",
                         "minimum",
                         "maximum",
                         "exclusiveMinimum",
                         "definitions",
                         "$ref"]

    def _process_json_schema(self, raw_schema):
        # let's sort elements of jsonschema
        if isinstance(raw_schema, list):
            new_schema = []
            for elem in raw_schema:
                new_schema.append(self._process_json_schema(elem))
        elif isinstance(raw_schema, dict):
            schema = collections.OrderedDict()
            missed = list(set(raw_schema) - set(self._schema_key_order))
            for key in self._schema_key_order + missed:
                if key in raw_schema:
                    if key in ("properties", "patternProperties",
                               "definitions"):
                        items = collections.OrderedDict()
                        for p, p_schema in sorted(raw_schema[key].items()):
                            items[p] = self._process_json_schema(p_schema)
                        schema[key] = items
                    elif key == "items":
                        schema[key] = self._process_json_schema(
                            raw_schema[key])
                    elif key in ("oneOf", "anyOf"):
                        items = []
                        for item in raw_schema[key]:
                            items.append(self._process_json_schema(item))
                        schema[key] = items
                    else:
                        schema[key] = raw_schema[key]

            return schema
        else:
            return raw_schema

    def _make_plugin_section(self, plugin):
        page = ["#### %s [%s]" % (plugin["name"], plugin["base"])]
        if plugin["title"]:
            title = plugin["title"]
            if not title.endswith("."):
                title += "."
            page.append(title)
        if plugin["description"]:
            page.append(r2m.convert(plugin["description"]))

        if plugin["platform"]:
            page.append("__Platform__: %s" % plugin["platform"])

        if plugin["introduced_in"]:
            page.append(
                "__Introduced in__: %s" % plugin["introduced_in"])

        if "removed_in" in plugin:
            page.append(
                "__Removed in__: %s" % plugin["removed_in"])

        ref_prefix = "%s-%s-" % (plugin["base"], plugin["name"])

        if plugin["parameters"]:
            page.append(self._make_arg_items(plugin["parameters"], ref_prefix))

        if plugin["returns"]:
            page.append("__Returns__:  \n%s" % plugin["returns"])

        if plugin["schema"]:
            schema = self._process_json_schema(plugin["schema"])
            schema = json.dumps(schema, indent=4).split("\n")
            schema = "\n        ".join(schema)
            title = ("The input of this plugin should be valid to the "
                     "following JSONSchema")
            page.append(
                "??? note \"%s\"\n"
                "        :::json\n"
                "        %s" % (title, schema))

        if "required_platforms" in plugin:
            page.append("__Requires platform(s)__:")
            for p in plugin["required_platforms"]:
                platform_name = p.pop("platform")
                page.append("* %s with the next options: %s" % (
                    platform_name, p))

        filename = plugin["module"].replace(".", "/").replace("-", "_")
        ref = ("%s/blob/master/%s.py" % (self.package["repository"], filename))
        page.append("__Module__: [%s](%s)" % (plugin["module"], ref))
        return "\n\n".join(page)

    def _make(self):
        if self.package["name"] == "rally":
            title = "# In-tree plugins."
        else:
            title = "# Plugins for %s" % self.package["title"]
        page = [title,
                "Processed releases: %s %s - %s" % (
                    self.package["name"],
                    self.package["versions"][0],
                    self.package["versions"][1])]

        for category, plugins_bases in sorted(self._group_plugins().items()):
            page.append("## %s" % category)
            plugins_bases = sorted(plugins_bases, key=lambda b: b["name"])
            for plugins_base in plugins_bases:
                page.append("### %s" % plugins_base["name"])
                if plugins_base["description"]:
                    page.append(r2m.convert(plugins_base["description"]))

                plugins = sorted(plugins_base["plugins"],
                                 key=lambda p: p["name"])
                for plugin in plugins:
                    page.append(self._make_plugin_section(plugin))
                    page.append("<hr />")

        return "\n\n".join(page)
