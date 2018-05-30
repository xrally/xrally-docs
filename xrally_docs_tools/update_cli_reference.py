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

import copy
import json
import os
import sys

from rally.common import version
from rally.cli import cliutils
from rally.cli import main as rally_cli_main

import xrally_docs_tools
from xrally_docs_tools import mdutils
from xrally_docs_tools import utils


CLI_SOURCE = os.path.join(xrally_docs_tools.SOURCE_DATA_DIR, "cli.json")
CLI_OUTPUT = os.path.join(xrally_docs_tools.DOCS_DIR, "ref", "cli.md")


class Parser(object):
    """A simplified interface of argparse.ArgumentParser"""
    def __init__(self):
        self.parsers = {}
        self.subparser = None
        self.defaults = {}
        self.arguments = []

    def add_parser(self, name, help=None, description=None,
                   formatter_class=None):
        parser = Parser()
        self.parsers[name] = {"description": description,
                              "help": help,
                              "fclass": formatter_class,
                              "parser": parser}
        return parser

    def set_defaults(self, command_object=None, action_fn=None,
                     action_kwargs=None):
        if command_object:
            self.defaults["command_object"] = command_object
        if action_fn:
            self.defaults["action_fn"] = action_fn
        if action_kwargs:
            self.defaults["action_kwargs"] = action_kwargs

    def add_subparsers(self, dest):
        # NOTE(andreykurilin): there is only one expected call
        if self.subparser:
            raise ValueError("Can't add one more subparser.")
        self.subparser = Parser()
        return self.subparser

    def add_argument(self, *args, **kwargs):
        if "action_args" in args:
            return
        self.arguments.append((args, kwargs))


def discover_cli():
    categories = []

    parser = Parser()

    raw_categories = copy.copy(rally_cli_main.categories)
    cliutils._add_command_parsers(raw_categories, parser)

    for cg in sorted(raw_categories.keys()):
        if cg == "deployment":
            # oops. let's skip it
            continue
        cparser = parser.parsers[cg]["parser"]
        # NOTE(andreykurilin): we are re-using `_add_command_parsers`
        #   method from `rally.cli.cliutils`, but, since it was designed
        #   to print help message, generated description for categories
        #   contains specification for all sub-commands. We don't need
        #   information about sub-commands at this point, so let's skip
        #   "generated description" and take it directly from category
        #   class.
        description = cparser.defaults["command_object"].__doc__

        commands = []

        for command in sorted(cparser.subparser.parsers.keys()):
            subparser = cparser.subparser.parsers[command]

            arguments = []
            defaults = utils.get_defaults(
                subparser["parser"].defaults["action_fn"])
            for args, kwargs in subparser["parser"].arguments:
                # for future changes...
                # :param args: a single command argument which can represented
                #    by several names(for example, --uuid and --task-id) in cli
                # :type args: tuple
                # :param kwargs: description of argument. Have next format:
                #   {"dest": "action_kwarg_<name of keyword argument in code>",
                #    "help": "just a description of argument"
                #    "metavar": "[optional] metavar of argument."
                #               "Example: argument '--file'; metavar 'path' ",
                #    "type": "[optional] class object of argument's type",
                #    "required": "[optional] boolean value"}
                # :type kwargs: dict

                argument = {
                    "dest": kwargs.get("dest").replace("action_kwarg_", ""),
                    "args": args,
                    "metavar": kwargs.get("metavar"),
                    "description": kwargs.get("help", ""),

                }
                action = kwargs.get("action")
                if not action:
                    arg_type = kwargs.get("type")
                    if arg_type:
                        argument["type"] = arg_type.__name__

                    skip_default = argument["dest"] in ("deployment",
                                                        "env",
                                                        "task_id",
                                                        "verification")
                    if not skip_default and argument["dest"] in defaults:
                        argument["defaults"] = defaults[argument["dest"]]

                arguments.append(argument)
            commands.append({
                "name": "rally %s %s" % (cg, command),
                "command": command,
                "description": subparser["description"],
                "arguments": arguments
            })

        categories.append({
            "name": cg,
            "description": description,
            "commands": commands})
    data = {"categories": categories, "rally": version.version_string()}
    with open(CLI_SOURCE, "w") as f:
        f.write(json.dumps(data, indent=4))
    return data


def generate_page(categories):
    page = ["# Command Line Interface Reference"]
    for category in sorted(categories, key=lambda c: c["name"]):
        page.append("## Category \"%s\"" % category["name"])
        page.append(category["description"])
        for command in sorted(category["commands"], key=lambda c: c["name"]):
            page.append("### %s" % (command["name"]))
            page.append(command["description"])
            definition = mdutils.DefinitionsList(
                prefix="%s_%s_" % (category["name"], command["command"]),
                term_label="Argument",
                no_wrap_term=True)
            for argument in command["arguments"]:
                description = [argument["description"]]

                if "type" in argument or "defaults" in argument:
                    # add empty line to split description from meta data
                    description.append("\n")

                if "type" in argument:
                    description.append("<i>Type</i>: %s" % argument["type"])
                if "defaults" in argument and argument["defaults"]:
                    description.append(
                        "<i>Defaults</i>: %s" % argument["defaults"])

                args = argument["args"]
                if argument["metavar"]:
                    args = ["%s %s" % (arg, argument["metavar"])
                            for arg in args]
                definition.add_term(",\n".join(args), description)
            if command["arguments"]:
                page.append(definition.to_md())

    with open(CLI_OUTPUT, "w") as f:
        f.write("\n\n".join(page))


def main():
    if len(sys.argv) == 1:
        with open(xrally_docs_tools.PLUGINS_FILE) as f:
            plugins = json.loads(f.read())
        requested_version = utils.Tag.parse(
            [p["versions"][1] for p in plugins
             if p["name"] == "rally"][0])
        actual_version = utils.Tag.parse(version.version_string())
        if requested_version != actual_version:
            print("Requested Rally version (%s) from plugins.json is not "
                  "equal to the release which you have installed (%s)."
                  "Try to recreate virtual environment with "
                  "`tox -r -e update_cli`." % (requested_version,
                                               actual_version))
            return 1
        collected_data = discover_cli()
    else:
        if os.path.exists(CLI_SOURCE):
            with open(CLI_SOURCE) as f:
                collected_data = json.loads(f.read())
        else:
            collected_data = discover_cli()

    generate_page(collected_data["categories"])


if __name__ == "__main__":
    main()
