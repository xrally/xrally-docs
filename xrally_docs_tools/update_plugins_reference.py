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
import shutil
import sys

import requests

import xrally_docs_tools
from xrally_docs_tools.plugins_ref import pages
from xrally_docs_tools import utils


_ROOT_TMP_DIR = None
_WORK_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         "plugins_ref")
_AGENT = os.path.join(_WORK_DIR, "agent.py")
RESULTS_FILE = os.path.join(xrally_docs_tools.SOURCE_DATA_DIR, "plugins.json")


def process_package(package, results):
    print("Start processing %s." % package["name"])
    if package["name"] not in results:
        # this package is new for us.
        results[package["name"]] = copy.deepcopy(package)
        results[package["name"]]["plugins"] = {}
        results[package["name"]]["plugins_bases"] = {}
        processed_versions = None
    else:
        processed_versions = results[package["name"]]["versions"]

    p_data = results[package["name"]]

    if processed_versions and processed_versions == package["versions"]:
        # nothing had changed. skipping
        print("Nothing had changed. Skipping...\n\n")
        return

    print("Cloning the source code.")
    repo_dir = utils.generate_random_path(_ROOT_TMP_DIR)
    utils.sp_call(["git", "clone", p_data["repository"], repo_dir])

    print("Getting all available tags.")
    tags = utils.sp_call(["git", "tag"], cwd=repo_dir).decode()
    tags = utils.Tag.parse_list(tags)
    print("\ttags: %s" % ", ".join(map(str, tags)))

    # filtering
    start_tag, end_tag = p_data["versions"]
    start_tag = utils.Tag.parse(start_tag)
    end_tag = utils.Tag.parse(end_tag)

    tags = [tag for tag in tags
            if start_tag <= tag <= end_tag]
    if processed_versions:
        # ignore processed tags
        _old_start_tag, old_end_tag = processed_versions
        old_end_tag = utils.Tag.parse(old_end_tag)

        tags = [tag for tag in tags if tag > old_end_tag]

    print("The next tags will be processed: %s." % ", ".join(map(str, tags)))

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

        print("Collecting data...")
        tag_data = utils.sp_call(
            ["python", _AGENT, package["name"]], env=env,
            merge_stdout=False)
        if tag_data:
            tag_data = json.loads(tag_data)
            if tag == end_tag:
                # use the latest data
                p_data["pkg_info"] = tag_data["pkg_info"]
                p_data["options"] = tag_data["options"]

            tag_plugins, tag_bases = tag_data["plugins"]
            for name, plugin in tag_plugins.items():
                introduced_in = None
                if name not in p_data["plugins"]:
                    if tag != start_tag:
                        introduced_in = tag.to_str()
                else:
                    introduced_in = p_data["plugins"][name]["introduced_in"]
                p_data["plugins"][name] = plugin
                p_data["plugins"][name]["introduced_in"] = introduced_in
            deleted = set(p_data["plugins"]) - set(tag_plugins)
            for p in deleted:
                p_data["plugins"][p]["removed_in"] = tag.to_str()
            p_data["plugins_bases"].update(tag_bases)

    if "changelog_file" in p_data:
        changelog_file = os.path.join(repo_dir, p_data["changelog_file"])
        if os.path.exists(changelog_file):
            with open(changelog_file) as f:
                p_data["changelog"] = f.read()

    print("Done.\n\n")
    return True


def generate_pages(data):
    print("Removing existing pages.")
    if os.path.exists(pages.ROOT_DIR):
        shutil.rmtree(pages.ROOT_DIR)

    cfg = utils.get_mkdocs_cfg()

    plugins_section = [p for p in cfg["pages"] if "Plugins" in p]
    if plugins_section:
        plugins_section[0]["Plugins"] = []
        plugins_section = plugins_section[0]["Plugins"]
    else:
        plugins_section = {"Plugins": []}
        cfg["pages"].append(plugins_section)
        plugins_section = plugins_section["Plugins"]

    print("Regenerating updated ones.")

    root_package = data.pop("rally")
    plugins_section.append(
        {"In-tree": [
            {"Plugins": pages.PluginsReferencesPage(root_package).save()},
            {"Config Options": pages.ConfigOptionsReference(root_package).save()}
        ]})
    for package in sorted(data.values(), key=lambda p: p["title"]):
        res = [
            {"Overview": pages.OverviewPage(package).save()},
            {"Plugins": pages.PluginsReferencesPage(package).save()}
        ]
        if package["changelog"]:
            res.append({"ChangeLog": pages.ChangeLogPage(package).save()})
        if package["options"]:
            res.append({
                "Config Options":
                    pages.ConfigOptionsReference(package).save()})

        plugins_section.append({package["title"]: res})

    utils.update_mkdocs_cfg(cfg)


def main():
    with open(xrally_docs_tools.PLUGINS_FILE) as f:
        packages = json.loads(f.read())

    with open(RESULTS_FILE) as f:
        try:
            results = json.loads(f.read())
        except ValueError:
            results = {}
    if len(sys.argv) == 1:
        print("WARNING: This tool requires internet access. Checking...")
        resp = requests.get("https://github.com")
        if resp.status_code != 200:
            return 1

        global _ROOT_TMP_DIR
        _ROOT_TMP_DIR = utils.generate_random_path()
        os.mkdir(_ROOT_TMP_DIR)

        changed = False
        for package in packages:
            res = process_package(package, results)
            if res:
                changed = True

        if os.path.exists(_ROOT_TMP_DIR):
            shutil.rmtree(_ROOT_TMP_DIR)

        results = json.dumps(results, indent=4)
        if changed:
            with open(RESULTS_FILE, "w") as f:
                f.write(results)

    generate_pages(results)


if __name__ == "__main__":
    main()
