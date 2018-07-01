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

import json
import os
import shutil

import xrally_docs_tools
from xrally_docs_tools.plugins_ref import pages
from xrally_docs_tools import utils


_WORK_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         "plugins_ref")
_AGENT = os.path.join(_WORK_DIR, "agent.py")


class Package(object):

    def __init__(self, info, tmp_dir, mkdocs_section):
        """Init package helper

        :param info: package info
        :param tmp_dir: a path to temporary dir to clone data to
        :param mkdocs_section: MKDocs plugins section
        """
        self._info = info
        self._tmp_dir = tmp_dir
        self._mkdocs_section = mkdocs_section
        self._load()
        self._changed_data = {}

    @property
    def name(self):
        """Package name"""
        return self._info["name"]

    @property
    def is_changed(self):
        """Whether any data is changed or not"""
        return bool(self._changed_data)

    @property
    def _dump_file(self):
        """A path to file with all the discovered information about package."""
        return os.path.join(
            xrally_docs_tools.SOURCE_DATA_DIR,
            "%s.json" % self.name.replace("-", "_"))

    def _load(self):
        """Load saved data."""
        if os.path.exists(self._dump_file):
            with open(self._dump_file) as f:
                try:
                    _dump_data = json.loads(f.read())
                except ValueError:
                    return
            # check if something is changed
            for key, value in self._info.items():
                if key not in _dump_data or value != _dump_data[key]:
                    self._changed_data[key] = value
            self._info = _dump_data
        else:
            self._info["plugins"] = {}
            self._info["plugins_bases"] = {}
            # everything is changed
            self._changed_data = self._info

    def _retrieve_data(self):
        """Retrieve new data."""
        print("Cloning the source code.")

        repo_dir = utils.generate_random_path(self._tmp_dir)
        utils.sp_call(["git", "clone", self._info["repository"], repo_dir])

        print("Getting all available tags.")
        tags = utils.sp_call(["git", "tag"], cwd=repo_dir).decode()
        tags = utils.Tag.parse_list(tags)
        print("\ttags: %s" % ", ".join(map(str, tags)))

        # filtering
        start_tag, end_tag = self._changed_data["versions"]
        start_tag = utils.Tag.parse(start_tag)
        end_tag = utils.Tag.parse(end_tag)

        tags = [tag for tag in tags
                if start_tag <= tag <= end_tag]
        if self._info["versions"] != self._changed_data["versions"]:
            # see which tags were already processed and ignore them
            _old_start_tag, old_end_tag = self._info["versions"]
            old_end_tag = utils.Tag.parse(old_end_tag)

            tags = [tag for tag in tags if tag > old_end_tag]

            # update info
            self._info["versions"] = self._changed_data["versions"]

        print("The next tags will be processed: %s." % ", ".join(
            map(str, tags)))

        print("Initializing virtual environment.")
        utils.sp_call(["virtualenv", ".venv"], cwd=repo_dir)

        env = os.environ.copy()
        # activate virtual environment
        env["VIRTUAL_ENV"] = os.path.join(repo_dir, ".venv")
        env["PATH"] = "%s:%s" % (
            os.path.join(repo_dir, ".venv", "bin"), env["PATH"])

        for tag in tags:
            print("Checkout to %s tag." % tag)
            utils.sp_call(["git", "checkout", "%s" % tag], cwd=repo_dir)
            utils.sp_call(["pip", "install", "-U", "-e", "./"],
                          cwd=repo_dir, env=env)
            if self.name == "rally-openstack" and tag == utils.Tag(1, 0, 0):
                # rally-openstack 1.0.0 was a first attempt to deliver rally
                #   plugins as separate package. It showed a bunch of issues
                #   which were fixed in further releases. Unfortunately, after
                #   releasing Rally 1.0.0, the first rally-openstack
                #   release doesn't work.
                #   Let's apply this hack and to still be able to discover info
                #   from first release.
                utils.sp_call(["pip", "install", "rally==0.12.1"],
                              cwd=repo_dir, env=env)

            print("Collecting data...")
            tag_data = utils.sp_call(["python", _AGENT, self.name],
                                     env=env, merge_stdout=False)
            if tag_data:
                tag_data = json.loads(tag_data)
                if tag == end_tag:
                    # use the latest data
                    self._info["pkg_info"] = tag_data["pkg_info"]
                    self._info["options"] = tag_data["options"]

                tag_plugins, tag_bases = tag_data["plugins"]
                for name, plugin in tag_plugins.items():
                    introduced_in = self._info["plugins"][name]["introduced_in"]
                    if name not in self._info["plugins"]:
                        if tag != start_tag:
                            introduced_in = tag.to_str()
                    self._info["plugins"][name] = plugin
                    self._info["plugins"][name]["introduced_in"] = introduced_in
                deleted = set(self._info["plugins"]) - set(tag_plugins)
                for p in deleted:
                    self._info["plugins"][p]["removed_in"] = tag.to_str()
                self._info["plugins_bases"].update(tag_bases)

        if "changelog_file" in self._info:
            changelog_file = os.path.join(
                repo_dir, self._info["changelog_file"])

            if os.path.exists(changelog_file):
                with open(changelog_file) as f:
                    self._info["changelog"] = f.read()

    def _dump_info(self):
        """Save data to the file."""
        if self.is_changed:
            dump_results = json.dumps(self._info, indent=4)
            with open(self._dump_file, "w") as f:
                f.write(dump_results)

    def _generate_pages(self):
        if self.name == "rally":
            # for root package no need to show package overview and etc
            generated_pages = [
                {"Plugins": pages.PluginsReferencesPage(self._info).save()},
                {"Config Options": pages.ConfigOptionsReference(
                    self._info).save()}
            ]
        elif "versions" not in self._info:
            generated_pages = pages.DevOverviewPage(self._info).save()
        else:
            generated_pages = [
                {"Overview": pages.OverviewPage(self._info).save()},
                {"Plugins": pages.PluginsReferencesPage(self._info).save()}
            ]
            if self._info["options"]:
                generated_pages.append({
                    "Config Options":
                        pages.ConfigOptionsReference(self._info).save()})
            if self._info["changelog"]:
                generated_pages.append({"ChangeLog": pages.ChangeLogPage(
                    self._info).save()})

        self._mkdocs_section.append({self._info["title"]: generated_pages})

    def process(self):
        print("Start processing %s." % self.name)

        if not self.is_changed:
            print("Nothing had changed. No new data to retrieve...\n\n")
        elif ("versions" not in self._info
              and "versions" not in self._changed_data):
            print("Package is under active development, but had not been "
                  "released yet...\n\n")
        else:
            self._retrieve_data()

        self._dump_info()
        self._generate_pages()

        print("Done.\n\n")


def main():
    print("WARNING: This tool may require internet access to retrieve "
          "information about packages and plugins.")
    with open(xrally_docs_tools.PLUGINS_FILE) as f:
        packages = json.loads(f.read())

    mkdocs_cfg = utils.get_mkdocs_cfg()

    print("Removing existing doc pages.")
    if os.path.exists(pages.ROOT_DIR):
        shutil.rmtree(pages.ROOT_DIR)
    plugins_section = []
    old_plugins_section = [p for p in mkdocs_cfg["pages"] if "Plugins" in p]
    old_plugins_section[0]["Plugins"] = plugins_section

    tmp_dir = utils.generate_random_path()
    os.mkdir(tmp_dir)

    packages = sorted(packages,
                      # put the root package to the top
                      key=lambda p: (p["name"] != "rally", p["title"]))

    for package in packages:
        p = Package(package, tmp_dir=tmp_dir, mkdocs_section=plugins_section)
        p.process()

    utils.update_mkdocs_cfg(mkdocs_cfg)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
