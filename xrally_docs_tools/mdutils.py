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


class DefinitionsList(object):
    """Create a definitions list with anchors for each term."""
    def __init__(self, title=None, description=None, prefix=None):
        """Init definitions list.

        :param title: Optional title of the list
        :param description: Optional description of the lest
        :param prefix: Optional prefix for anchors
        """
        self._content = []
        if title:
            self._content.append("**%s**:" % title)
        if description:
            self._content.append(description)
        if prefix and not prefix.endswith("_"):
            prefix += "_"
        self.prefix = prefix or ""

    def add_term(self, term, definition):
        """Add a term to a definition list.

        :param term: term name
        :param definition: term definition. Can be a string or a list of
            strings.
        """
        # make the correct reference without restricted chars
        ref = self.prefix + term.replace("<", "").replace(">", "")
        ref = ref.replace(".", "").replace(",", "").replace("*", "")
        ref = ref.replace("-", "").replace("_", "-").replace(" ", "-")

        # process definition
        if isinstance(definition, list):
            definition = "  \n\n  ".join(definition)

        self._content.append(
            "<a name=%(ref)s></a>\n\n"
            "* *%(term)s* [[ref]](#%(ref)s)  \n  "
            "%(definition)s" % {
                "ref": ref,
                "term": term.replace("<", "&lt;").replace(">", "&gt;"),
                "definition": "\n  ".join(definition.split("\n"))})

    def to_md(self):
        return "\n\n".join(self._content)
