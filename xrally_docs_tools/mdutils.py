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

import xml.etree.ElementTree as ET

from rally.common import utils as rally_utils


def _escape_cdata(text, encoding=None):
    """Do not escape anything."""
    return text.encode(encoding, "xmlcharrefreplace")


# NOTE(andreykurilin): This class is made private to keep interface of
#   inheritors simple. For example, DefinitionsList should not expose 'add_row'
#   method, since it has own 'add_term' method with custom logic.
class _Table(object):
    """Create a table via html tags.

    # NOTE(andreykurilin): I did not find any possible options from
        https://www.mkdocs.org/user-guide/writing-your-docs/#tables
        which supports multi-line cells. That is why raw html tags are used.
    """

    def __init__(self, title=None, headers=None, nowrap_columns=None):
        """Init table.

        :param title: An optional Title for the table
        :param headers: An optional list of headers for the table.
            If specified, each row should have the same number of cells as
            this list.
        :param nowrap_columns: whether add "nowrap" style to the columns or
            not. Boolean value is accepted of a list of boolean values. In
            second case the index in the list is equal to the index of the
            column.
        """
        self._title = title
        self._headers = headers
        self._rows = []
        self._nowrap = nowrap_columns or []

    def _add_row(self, *cells):
        """Add a row to the table.

        Each cell should be a string with text or a dict. As for dict the
        following keys are allowed:

        * elements - a list of custom xml.etree.Element to add to the cell
        * text - a text to add to the cell
        """
        if self._headers and len(cells) != len(self._headers):
            raise ValueError("The number of table cells is bigger then "
                             "specified headers.")
        for cell in cells:
            if isinstance(cell, dict):
                if set(cell) - {"elements", "text"}:
                    raise ValueError("The cell '%s' contains redundant keys. "
                                     "'elements' and 'text' are only allowed "
                                     "keys." % cell)
                cell.setdefault("text", "")
                cell.setdefault("elements", [])
        self._rows.append(cells)

    def get_string(self):
        document = ET.Element("table")

        if self._title:
            title = ET.SubElement(document, "caption")
            title.text = self._title
        if self._headers:
            thead = ET.SubElement(document, "thead")
            tr = ET.SubElement(thead, "tr")
            for header in self._headers:
                th = ET.SubElement(tr, "th")
                th.text = header

        tbody = ET.SubElement(document, "tbody")
        for row in self._rows:
            tr = ET.SubElement(tbody, "tr")
            for i, cell in enumerate(row):
                if self._nowrap is True or (
                        i < len(self._nowrap) and self._nowrap[i]):
                    td = ET.SubElement(tr, "td", style="white-space: nowrap")
                else:
                    td = ET.SubElement(tr, "td")
                if isinstance(cell, dict):
                    if cell["elements"]:
                        for elem in cell["elements"]:
                            td.append(elem)
                    if cell["text"]:
                        td.text = cell["text"]
                else:
                    td.text = cell

        rally_utils.prettify_xml(document)

        # NOTE(andreykurilin): we do not want to escape chars, so we can inject
        #   custom things.
        original_escape_cdata = ET._escape_cdata
        ET._escape_cdata = _escape_cdata

        document = ET.tostring(
            document,
            encoding="utf-8",
            # use 'html' method to force adding closing tags
            method="html").decode("utf-8")
        ET._escape_cdata = original_escape_cdata
        return document


class Table(_Table):
    def add_row(self, *cells):
        return self._add_row(*cells)


class DefinitionsList(_Table):
    """Create a definitions list with anchors for each term."""

    def __init__(self, title=None, prefix=None,
                 term_label=None, description_label=None,
                 no_wrap_term=True, no_wrap_description=False):
        """Init definitions list.

        :param title: Optional title of the list
        :param prefix: Optional prefix for anchors
        :param term_label: A label for term column. Defaults to "Term"
        :param description_label: A label for description column. Defaults to
            "Description"
        """
        headers = [
            term_label if term_label else "Term",
            description_label if description_label else "Description"
        ]
        super(DefinitionsList, self).__init__(
            title=title, headers=headers,
            nowrap_columns=[no_wrap_term, no_wrap_description])
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
            d_elems = []
            for d in definition:
                d_elems.append(ET.Element("span"))
                d_elems[-1].text = d
                d_elems.append(ET.Element("br"))
            definition = {"elements": d_elems}

        anchor = ET.Element("a", name=ref)
        anchor.tail = term.replace("<", "&lt;").replace(">", "&gt;").replace(
            "\n", "<br />")
        ref_tag = ET.Element("a", href="#%s" % ref)
        ref_tag.text = " [ref]"

        self._add_row({"elements": [anchor, ref_tag]}, definition)

    def to_md(self):
        return self.get_string()
